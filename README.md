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

Optional model selection:

```powershell
$env:HF_MODEL="meta-llama/Llama-3.1-70B-Instruct"
```

If `HF_MODEL` is not set, the default is `meta-llama/Llama-3.1-8B-Instruct`.

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

## RAG Preparation

The `papers/` folder will later store uploaded research PDFs.

`scripts/prepare_papers.py` is the first step toward PDF ingestion and currently scans `papers/` for PDF files.

## Future Architecture

- Qdrant (vector DB)
- n8n (automation/workflow orchestration)
- Web app interface

## Future Model Comparison

The current prototype uses the Hugging Face Inference API with `meta-llama/Llama-3.1-8B-Instruct`.

Future versions will support multiple LLM backends/models. The goal is to compare annotation quality across models for different datasets and cell types.

Candidate future models may include:

- `meta-llama/Llama-3.1-8B-Instruct`
- `meta-llama/Llama-3.1-70B-Instruct`
- `Qwen/Qwen2.5-7B-Instruct-1M`
- `Mistral-Nemo-Instruct-2407` (or another Mistral instruct model available through Hugging Face)

Model choice should eventually be configurable instead of hard-coded.

## Evaluation Plan

We will eventually compare multiple Hugging Face models on the same marker inputs.

Outputs will be compared by:

- predicted cell type
- confidence
- warning frequency
- marker evidence quality
- agreement with expert/known labels

This evaluation will support future manuscript figures and tables.
