# Cell-Type Annotation RAG Starter

A beginner-friendly project for annotating cell clusters from marker-gene CSV input using a Python pipeline.

## Stack

- Python
- Hugging Face Inference API
- Requests

## Model

This project uses the Hugging Face Inference API with:

- `meta-llama/Llama-3.1-8B-Instruct`

## Current Status

- The pipeline is currently Python-based.
- It does **not** depend on n8n yet.
- n8n is planned as a future workflow orchestration layer.

## Project Structure

- `scripts/parse_markers.py`
- `scripts/annotate_clusters.py`
- `data/example_markers.csv`
- `data/cluster_markers.json` (generated)
- `data/annotations.json` (generated)

## Prerequisites

1. Python 3.10+
2. A Hugging Face token with Inference API access

## Setup (PowerShell)

```powershell
$env:HF_TOKEN="your_hf_token_here"
```

## Current Pipeline

`marker CSV` -> `parse_markers.py` -> `cluster_markers.json` -> `annotate_clusters.py` -> `annotations.json`

## Run (PowerShell)

1. Parse markers:

```powershell
python scripts/parse_markers.py
```

Optional:

```powershell
python scripts/parse_markers.py --input data/example_markers.csv --output data/cluster_markers.json --top-n 5
```

2. Annotate clusters:

```powershell
python scripts/annotate_clusters.py
```

## Future Architecture

- Qdrant (vector DB)
- n8n (automation/workflow orchestration)
- Web app interface
