#!/usr/bin/env python3
import argparse
import os

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
        return f"marker genes {genes} cell type identity monocyte function biology"
    return f"{query} cell type identity function biology marker genes"


def main() -> None:
    args = parse_args()

    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise RuntimeError("HF_TOKEN environment variable is not set.")

    query = args.query
    expanded_query = expand_biological_query(query)
    print(f"Expanded query: {expanded_query}")
    query_embedding = get_embedding(expanded_query, hf_token)

    client = QdrantClient(url="http://localhost:6333")
    results = client.query_points(
        collection_name="paper_chunks",
        query=query_embedding,
        limit=5,
    )

    for point in results.points:
        payload = point.payload or {}
        source_pdf = payload.get("source_pdf", "unknown")
        text = payload.get("text", "")
        print("---")
        print(f"Score: {point.score}")
        print(f"Source: {source_pdf}")
        print(f"Text: {text}")
        print("---")


if __name__ == "__main__":
    main()
