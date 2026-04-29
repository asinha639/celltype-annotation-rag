# Cell Type Annotation Report

| Cluster | Predicted Cell Type | Confidence |
|---|---|---|
| 0 | B cell | 0.95 |
| 1 | cytotoxic T cell | 0.90 |
| 2 | classical monocyte | 0.90 |

## Cluster 0

**Predicted cell type:** B cell
**Confidence:** 0.95

### Reasoning
Strong markers for B cell (MS4A1, CD79A) with no conflicting markers.

### Marker evidence
- MS4A1: Strong marker for B cell
- CD79A: Strong marker for B cell
- CD74: Common marker in various immune cells
- HLA-DRA: Common marker in various immune cells
- CD37: Common marker in various immune cells

### Alternative cell types
- None

## Cluster 1

**Predicted cell type:** cytotoxic T cell
**Confidence:** 0.90

### Reasoning
Based on the presence of NKG7, GNLY, PRF1, CTSW, and TRAC, this cluster is likely cytotoxic T cells.

### Marker evidence
- NKG7: Strongly supports cytotoxic T cell or NK cell
- GNLY: Supports cytotoxic T cell or NK cell
- PRF1: Supports cytotoxic T cell or NK cell
- CTSW: Supports cytotoxic T cell or NK cell
- TRAC: Supports cytotoxic T cell or NK cell

### Alternative cell types
- NK cell

## Cluster 2

**Predicted cell type:** classical monocyte
**Confidence:** 0.90

### Reasoning
The cluster is annotated as classical monocyte due to the presence of LYZ, FCN1, CTSS, S100A8, and S100A9, which are strong markers for this cell type.

### Marker evidence
- LYZ: strong marker for classical monocyte
- FCN1: strong marker for classical monocyte
- CTSS: strong marker for classical monocyte
- S100A8: strong marker for classical monocyte
- S100A9: strong marker for classical monocyte

### Alternative cell types
- neutrophil
