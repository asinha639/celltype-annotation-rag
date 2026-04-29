#!/usr/bin/env python3
import json
from pathlib import Path

from pypdf import PdfReader


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


def main() -> None:
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
        chunk_payload = {
            "source_pdf": pdf_path.name,
            "chunks": [
                {"chunk_id": idx, "text": chunk}
                for idx, chunk in enumerate(chunk_texts)
            ],
        }

        chunk_output_path = chunks_output_dir / f"{pdf_path.stem}_chunks.json"
        chunk_output_path.write_text(
            json.dumps(chunk_payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"Saved chunks: data/paper_chunks/{chunk_output_path.name}")


if __name__ == "__main__":
    main()
