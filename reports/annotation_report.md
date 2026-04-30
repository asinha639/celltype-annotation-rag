# Cell Type Annotation Report

| Cluster | Predicted Cell Type | Confidence |
|---|---|---|
| 0 | B cell | 0.95 |
| 1 | cytotoxic T cell | 0.90 |
| 2 | classical monocyte | 0.95 |
| 3 | naive/central memory T cell | 0.80 |
| 4 | non-classical monocyte | 0.80 |
| 5 | unknown | 0.00 |
| 6 | unknown | 0.00 |
| 7 | unknown | 0.00 |
| 8 | unknown | 0.00 |
| 9 | unknown | 0.00 |

## Cluster 0

**Predicted cell type:** B cell
**Confidence:** 0.95

### Reasoning
Markers MS4A1 and CD79A strongly support B cell.

### Marker evidence
- MS4A1: Strongly supports B cell.
- CD79A: Strongly supports B cell.
- CD74: Not specific to B cell, but present in B cells.
- HLA-DRA: Not specific to B cell, but present in B cells.
- CD37: Not specific to B cell, but present in B cells.

### Alternative cell types
- None

## Cluster 1

**Predicted cell type:** cytotoxic T cell
**Confidence:** 0.90

### Reasoning
NKG7, GNLY, PRF1, CTSW, and TRAC are markers for cytotoxic T cells and NK cells. Since NKG7, GNLY, PRF1, CTSW, and TRAC are present, cytotoxic T cell is preferred over NK cell.

### Marker evidence
- NKG7: marker for cytotoxic T cells and NK cells
- GNLY: marker for cytotoxic T cells and NK cells
- PRF1: marker for cytotoxic T cells and NK cells
- CTSW: marker for cytotoxic T cells and NK cells
- TRAC: marker for cytotoxic T cells and NK cells

### Alternative cell types
- NK cell

## Cluster 2

**Predicted cell type:** classical monocyte
**Confidence:** 0.95

### Reasoning
N/A

### Marker evidence
- LYZ: Strongly supports neutrophil or monocyte
- S100A8: Supports neutrophil or monocyte
- S100A9: Supports neutrophil or monocyte
- FCN1: Supports neutrophil or monocyte
- CTSS: Supports neutrophil or monocyte

### Alternative cell types
- None

## Cluster 3

**Predicted cell type:** naive/central memory T cell
**Confidence:** 0.80

### Reasoning
N/A

### Marker evidence
- CD3D: T cell marker
- CD3E: T cell marker
- IL7R: T cell marker
- CCR7: T cell marker
- LTB: T cell marker

### Alternative cell types
- CD4 T cell

### Warning
No clear cell type supported by marker genes

## Cluster 4

**Predicted cell type:** non-classical monocyte
**Confidence:** 0.80

### Reasoning
No clear markers for a specific cell type

### Marker evidence
- FCGR3A: Strongly suggests a myeloid cell type
- MS4A7: May be associated with B cells or other immune cells
- LST1: May be associated with B cells or other immune cells
- AIF1: May be associated with monocytes or other myeloid cells
- TYROBP: May be associated with monocytes or other myeloid cells

### Alternative cell types
- NK cell

### Warning
Uncertain cell type assignment

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
LLM annotation failed after retries: 402 Client Error: Payment Required for url: https://router.huggingface.co/v1/chat/completions

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
LLM annotation failed after retries: 402 Client Error: Payment Required for url: https://router.huggingface.co/v1/chat/completions

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
