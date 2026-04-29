#!/usr/bin/env python3
from pathlib import Path


def main() -> None:
    papers_dir = Path("papers")
    pdf_files = sorted(papers_dir.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in papers/")
        return

    for pdf_path in pdf_files:
        print(pdf_path.name)


if __name__ == "__main__":
    main()
