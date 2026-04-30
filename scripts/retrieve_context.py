#!/usr/bin/env python3
import argparse
import os
import re

import requests
from qdrant_client import QdrantClient


def get_embedding(text: str, hf_token: str) -> list[float]:
    api_url = (
        "https://router.huggingface.co/hf-inference/models/"
        "sentence-transformers/all-MiniLM-L6-v2/pipeline/feature-extraction"
    )
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {"inputs": text}

    response = requests.post(api_url, headers=headers, json=payload, timeout=60)
    if not response.ok:
        raise RuntimeError(
            f"Hugging Face request failed ({response.status_code}): {response.text}"
        )
    result = response.json()

    if not isinstance(result, list) or not result:
        raise ValueError(f"Unexpected embedding response format: {type(result)}")

    if all(isinstance(x, (int, float)) for x in result):
        return [float(x) for x in result]

    if all(isinstance(x, list) and x for x in result):
        if not all(len(x) == len(result[0]) for x in result):
            raise ValueError("Token embeddings have inconsistent dimensions.")
        token_count = len(result)
        dim = len(result[0])
        averaged = []
        for i in range(dim):
            averaged.append(sum(float(token[i]) for token in result) / token_count)
        return averaged

    raise ValueError(f"Unexpected embedding response format: {type(result)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Retrieve relevant paper chunks from Qdrant.")
    parser.add_argument(
        "--query",
        type=str,
        default="cell type annotation marker genes single-cell RNA sequencing",
        help="Search query text.",
    )
    return parser.parse_args()


def expand_biological_query(query: str) -> str:
    tokens = query.split()
    upper_tokens = [t for t in tokens if t.isupper() and any(c.isalpha() for c in t)]
    if upper_tokens:
        genes = " ".join(upper_tokens)
        return (
            f"single cell RNA-seq marker genes {genes} "
            "cell type annotation identity"
        )
    return f"single cell RNA-seq marker genes {query} cell type annotation identity"


def filter_retrieved_chunks(chunks: list[dict]) -> list[dict]:
    noise_keywords = [
        "references",
        "doi",
        "copyright",
        "et al",
        "supplementary",
        "available online",
        "article info",
        "contents lists available",
        "fig.",
        "figure",
    ]
    bio_keywords = ["t cell", "marker", "expression", "subset", "cd", "gene"]

    filtered_with_priority = []
    for chunk in chunks:
        text = str(chunk.get("text", ""))
        text_lower = text.lower()
        if len(text.strip()) < 200:
            continue
        if any(keyword in text_lower for keyword in noise_keywords):
            continue

        # Remove chunks that look like dense reference lists:
        # repeated numbered bullets (e.g., 1. 2. 3.) or many citation-like tokens.
        numbered_refs = re.findall(r"\b\d+\.", text)
        citation_like = re.findall(r"\[\d+\]|\(\d{4}\)|\b\d{1,3},\d{1,3}\b", text)
        long_number_runs = re.findall(r"\d{4,}", text)
        if len(numbered_refs) >= 5:
            continue
        if len(citation_like) >= 4:
            continue
        if len(long_number_runs) > 3:
            continue

        priority_score = sum(1 for kw in bio_keywords if kw in text_lower)
        filtered_with_priority.append((priority_score, chunk))

    filtered_with_priority.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in filtered_with_priority]


def retrieve_context_points(query: str, hf_token: str, limit: int = 5) -> list[dict]:
    expanded_query = expand_biological_query(query)
    query_embedding = get_embedding(expanded_query, hf_token)

    client = QdrantClient(url="http://localhost:6333")
    results = client.query_points(
        collection_name="paper_chunks",
        query=query_embedding,
        limit=limit,
    )

    output = []
    for point in results.points:
        payload = point.payload or {}
        output.append(
            {
                "score": point.score,
                "source_pdf": payload.get("source_pdf", "unknown"),
                "text": payload.get("text", ""),
            }
        )
    filtered = filter_retrieved_chunks(output)
    return filtered[:3]


def main() -> None:
    args = parse_args()

    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise RuntimeError("HF_TOKEN environment variable is not set.")

    query = args.query
    expanded_query = expand_biological_query(query)
    print(f"Expanded query: {expanded_query}")
    results = retrieve_context_points(query, hf_token, limit=5)

    for item in results:
        print("---")
        print(f"Score: {item['score']}")
        print(f"Source: {item['source_pdf']}")
        print(f"Text: {item['text']}")
        print("---")


if __name__ == "__main__":
    main()
