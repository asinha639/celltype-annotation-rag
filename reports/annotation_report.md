# Cell Type Annotation Report

| Cluster | Predicted Cell Type | Confidence |
|---|---|---|
| 0 | B cell | 0.95 |
| 1 | cytotoxic T cell | 0.90 |
| 2 | classical monocyte | 0.90 |
| 3 | unknown | 0.00 |
| 4 | unknown | 0.00 |
| 5 | unknown | 0.00 |
| 6 | unknown | 0.00 |
| 7 | unknown | 0.00 |
| 8 | unknown | 0.00 |
| 9 | unknown | 0.00 |

## Cluster 0

**Predicted cell type:** B cell
**Confidence:** 0.95

### Reasoning
Strong markers for B cell (MS4A1, CD79A) with no conflicting markers.

### Marker evidence
- MS4A1: Strong marker for B cell.
- CD79A: Strong marker for B cell.
- CD74: Possible marker for B cell or other immune cells.
- HLA-DRA: Possible marker for immune cells.
- CD37: Possible marker for B cell or other immune cells.

### Alternative cell types
- None

## Cluster 1

**Predicted cell type:** cytotoxic T cell
**Confidence:** 0.90

### Reasoning
Presence of NKG7, GNLY, PRF1, CTSW, and TRAC in the marker gene list strongly suggests cytotoxic T cell.

### Marker evidence
- NKG7: Strong marker for cytotoxic T cell and NK cell.
- GNLY: Strong marker for cytotoxic T cell and NK cell.
- PRF1: Strong marker for cytotoxic T cell.
- CTSW: Strong marker for cytotoxic T cell.
- TRAC: Strong marker for cytotoxic T cell.

### Alternative cell types
- NK cell

## Cluster 2

**Predicted cell type:** classical monocyte
**Confidence:** 0.90

### Reasoning
LYZ, FCN1, CTSS, S100A8, and S100A9 are strong markers for classical monocytes, but no strong neutrophil markers are present.

### Marker evidence
- LYZ: strong marker for classical monocytes
- S100A8: strong marker for classical monocytes
- S100A9: strong marker for classical monocytes
- FCN1: strong marker for classical monocytes
- CTSS: strong marker for classical monocytes

### Alternative cell types
- neutrophil

## Cluster 3

**Predicted cell type:** unknown
**Confidence:** 0.00

### Reasoning
Annotation failed for this cluster.

### Marker evidence
- None

### Alternative cell types
- None

### Warning
LLM annotation failed after retries: Reasoning mentions genes not in input markers: CTSW, GNLY, NKG7, PRF1, TRAC

## Cluster 4

**Predicted cell type:** unknown
**Confidence:** 0.00

### Reasoning
Annotation failed for this cluster.

### Marker evidence
- None

### Alternative cell types
- None

### Warning
LLM annotation failed after retries: Reasoning mentions genes not in input markers: CTSW, GNLY, NKG7, PRF1, TRAC

## Cluster 5

**Predicted cell type:** unknown
**Confidence:** 0.00

### Reasoning
Annotation failed for this cluster.

### Marker evidence
- None

### Alternative cell types
- None

### Warning
LLM annotation failed after retries: Reasoning mentions genes not in input markers: CD79A, MS4A1

## Cluster 6

**Predicted cell type:** unknown
**Confidence:** 0.00

### Reasoning
Annotation failed for this cluster.

### Marker evidence
- None

### Alternative cell types
- None

### Warning
LLM annotation failed after retries: Reasoning mentions genes not in input markers: CD79A, MS4A1

## Cluster 7

**Predicted cell type:** unknown
**Confidence:** 0.00

### Reasoning
Annotation failed for this cluster.

### Marker evidence
- None

### Alternative cell types
- None

### Warning
LLM annotation failed after retries: 402 Client Error: Payment Required for url: https://router.huggingface.co/v1/chat/completions

## Cluster 8

**Predicted cell type:** unknown
**Confidence:** 0.00

### Reasoning
Annotation failed for this cluster.

### Marker evidence
- None

### Alternative cell types
- None

### Warning
LLM annotation failed after retries: 402 Client Error: Payment Required for url: https://router.huggingface.co/v1/chat/completions

## Cluster 9

**Predicted cell type:** unknown
**Confidence:** 0.00

### Reasoning
Annotation failed for this cluster.

### Marker evidence
- None

### Alternative cell types
- None

### Warning
LLM annotation failed after retries: 402 Client Error: Payment Required for url: https://router.huggingface.co/v1/chat/completions
