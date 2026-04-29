#!/usr/bin/env python3
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

from pypdf import PdfReader
from qdrant_client import QdrantClient
from qdrant_client.http import models
import requests


def chunk_text(text: str, chunk_size: int = 1200, chunk_overlap: int = 200) -> list[str]:
    if not text:
        return []

    chunks = []
    step = chunk_size - chunk_overlap
    start = 0

    while start < len(text):
        chunk = text[start : start + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
        start += step

    return chunks


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
    parser = argparse.ArgumentParser(description="Prepare paper chunks and embeddings.")
    parser.add_argument(
        "--workers",
        type=int,
        default=12,
        help="Number of worker threads for embedding generation (default: 12).",
    )
    parser.add_argument(
        "--upload-qdrant",
        action="store_true",
        help="Upload chunk embeddings to Qdrant.",
    )
    return parser.parse_args()


def embed_chunk(chunk_id: int, text: str, hf_token: str) -> tuple[int, list[float]]:
    print(f"Embedding chunk {chunk_id}")
    try:
        embedding = get_embedding(text, hf_token)
    except Exception as exc:
        raise RuntimeError(f"Failed to embed chunk_id {chunk_id}: {exc}") from exc
    return chunk_id, embedding


def ensure_qdrant_collection(
    client: QdrantClient, collection_name: str, vector_size: int
) -> None:
    collections = client.get_collections().collections
    existing_names = {collection.name for collection in collections}
    if collection_name in existing_names:
        return

    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=vector_size,
            distance=models.Distance.COSINE,
        ),
    )


def upload_chunks_to_qdrant(
    client: QdrantClient,
    collection_name: str,
    source_pdf: str,
    chunks: list[dict],
) -> None:
    points = []
    for chunk in chunks:
        point_id = str(uuid5(NAMESPACE_URL, f"{source_pdf}:{chunk['chunk_id']}"))
        points.append(
            models.PointStruct(
                id=point_id,
                vector=chunk["embedding"],
                payload={
                    "source_pdf": source_pdf,
                    "chunk_id": chunk["chunk_id"],
                    "text": chunk["text"],
                },
            )
        )

    if points:
        client.upsert(collection_name=collection_name, points=points)


def main() -> None:
    args = parse_args()
    workers = args.workers
    upload_qdrant = args.upload_qdrant
    if workers < 1:
        raise ValueError("--workers must be at least 1.")

    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise RuntimeError("HF_TOKEN environment variable is not set.")

    papers_dir = Path("papers")
    text_output_dir = Path("data/paper_texts")
    chunks_output_dir = Path("data/paper_chunks")
    pdf_files = sorted(papers_dir.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in papers/")
        return

    qdrant_client = None
    qdrant_collection_name = "paper_chunks"
    qdrant_collection_ready = False
    if upload_qdrant:
        qdrant_client = QdrantClient(url="http://localhost:6333")

    text_output_dir.mkdir(parents=True, exist_ok=True)
    chunks_output_dir.mkdir(parents=True, exist_ok=True)

    for pdf_path in pdf_files:
        print(f"Extracting: {pdf_path.name}")

        reader = PdfReader(pdf_path)
        text_parts = []
        for page in reader.pages:
            text_parts.append(page.extract_text() or "")

        full_text = "\n".join(text_parts)
        text_output_path = text_output_dir / f"{pdf_path.stem}.txt"
        text_output_path.write_text(full_text, encoding="utf-8")
        print(f"Saved: data/paper_texts/{text_output_path.name}")

        chunk_texts = chunk_text(full_text, chunk_size=1200, chunk_overlap=200)
        print(f"Embedding chunks with {workers} workers...")

        chunk_embeddings: list[list[float] | None] = [None] * len(chunk_texts)
        with ThreadPoolExecutor(max_workers=workers) as executor:
            future_to_chunk_id = {
                executor.submit(embed_chunk, idx, chunk, hf_token): idx
                for idx, chunk in enumerate(chunk_texts)
            }
            for future in as_completed(future_to_chunk_id):
                chunk_id, embedding = future.result()
                chunk_embeddings[chunk_id] = embedding

        chunks = []
        for idx, chunk in enumerate(chunk_texts):
            embedding = chunk_embeddings[idx]
            if embedding is None:
                raise RuntimeError(f"Missing embedding for chunk_id {idx}.")
            chunks.append({"chunk_id": idx, "text": chunk, "embedding": embedding})

        if upload_qdrant and chunks and qdrant_client is not None:
            if not qdrant_collection_ready:
                vector_size = len(chunks[0]["embedding"])
                ensure_qdrant_collection(
                    client=qdrant_client,
                    collection_name=qdrant_collection_name,
                    vector_size=vector_size,
                )
                qdrant_collection_ready = True

            upload_chunks_to_qdrant(
                client=qdrant_client,
                collection_name=qdrant_collection_name,
                source_pdf=pdf_path.name,
                chunks=chunks,
            )

        chunk_payload = {"source_pdf": pdf_path.name, "chunks": chunks}

        chunk_output_path = chunks_output_dir / f"{pdf_path.stem}_chunks.json"
        chunk_output_path.write_text(
            json.dumps(chunk_payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"Saved chunks: data/paper_chunks/{chunk_output_path.name}")


if __name__ == "__main__":
    main()
