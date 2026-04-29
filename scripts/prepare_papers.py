#!/usr/bin/env python3
from pathlib import Path

from pypdf import PdfReader


def main() -> None:
    papers_dir = Path("papers")
    output_dir = Path("data/paper_texts")
    pdf_files = sorted(papers_dir.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in papers/")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    for pdf_path in pdf_files:
        print(f"Extracting: {pdf_path.name}")

        reader = PdfReader(pdf_path)
        text_parts = []
        for page in reader.pages:
            text_parts.append(page.extract_text() or "")

        output_path = output_dir / f"{pdf_path.stem}.txt"
        output_path.write_text("\n".join(text_parts), encoding="utf-8")
        print(f"Saved: data/paper_texts/{output_path.name}")


if __name__ == "__main__":
    main()
