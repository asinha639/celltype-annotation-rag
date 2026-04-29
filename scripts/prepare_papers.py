#!/usr/bin/env python3
import json
import os
from pathlib import Path

from pypdf import PdfReader
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


def main() -> None:
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
        chunks = []
        for idx, chunk in enumerate(chunk_texts):
            print(f"Embedding chunk {idx}")
            embedding = get_embedding(chunk, hf_token)
            chunks.append(
                {
                    "chunk_id": idx,
                    "text": chunk,
                    "embedding": embedding,
                }
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
