# AI-Assisted Cell Type Annotation for scRNA-seq

This project is a local Python pipeline for annotating single-cell RNA-seq clusters using marker genes, LLM reasoning, and retrieval-augmented context from research papers.

## Features

- Marker-based cluster annotation
- LLM reasoning with Llama 3.1 via Hugging Face
- RAG over scientific PDF chunks
- Parallel embedding generation for paper chunks
- Qdrant vector database integration

## Pipeline Overview

`marker CSV -> parsing -> cluster JSON -> embeddings -> Qdrant -> retrieval -> LLM -> annotations`

## Project Structure

- `data/` - inputs and generated outputs (`cluster_markers.json`, `annotations.json`, chunk files)
- `scripts/` - pipeline scripts (`parse_markers.py`, `prepare_papers.py`, `retrieve_context.py`, `annotate_clusters.py`)
- `papers/` - research PDFs for RAG ingestion
- `docker-compose.yml` - local services (Qdrant)
- `requirements.txt` - Python dependencies

## Setup

1. Set your Hugging Face token:
   - PowerShell: `$env:HF_TOKEN="your_token_here"`
2. Start local infrastructure:
   - `docker compose up -d`
3. Install Python dependencies:
   - `pip install -r requirements.txt`

## Quick Start (Full Pipeline)

1. Set Hugging Face token (PowerShell):
   - `$env:HF_TOKEN="your_token_here"`
2. Run full pipeline:
   - `python scripts/run_pipeline.py`
3. Outputs:
   - `data/annotations.json` -> structured annotations
   - `reports/annotation_report.md` -> human-readable report
4. (Optional) Prepare papers for RAG:
   - `python scripts/prepare_papers.py --workers 12 --upload-qdrant`

## Usage

- Run main annotation pipeline:
  - `python scripts/parse_markers.py`
  - `python scripts/annotate_clusters.py`
- Prepare papers and build chunk embeddings:
  - `python scripts/prepare_papers.py --workers 12 --upload-qdrant`
- Retrieve context for a query:
  - `python scripts/retrieve_context.py --query "PBMC monocyte marker genes LYZ FCN1 S100A8 S100A9"`

## Current Status

- Working local prototype
- Supports RAG-based annotation with paper chunk retrieval from Qdrant

## Future Work

- n8n integration for orchestration
- Web app for interactive annotation review
- Multiple LLM comparison and benchmarking
- Improved biological knowledge base and retrieval quality
