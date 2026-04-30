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
- CD74: Monocyte marker, but no strong neutrophil markers present
- HLA-DRA: Present in various immune cells, no strong marker for any cell type
- CD37: Present in various immune cells, no strong marker for any cell type

### Alternative cell types
- None

## Cluster 1

**Predicted cell type:** cytotoxic T cell
**Confidence:** 0.90

### Reasoning
Marker genes NKG7, GNLY, PRF1, CTSW, and TRAC are characteristic of cytotoxic T cells, with NK cell as an alternative possibility.

### Marker evidence
- NKG7: Marker of cytotoxic T cells and NK cells
- GNLY: Marker of cytotoxic T cells and NK cells
- PRF1: Marker of cytotoxic T cells
- CTSW: Marker of cytotoxic T cells
- TRAC: Marker of cytotoxic T cells

### Alternative cell types
- NK cell

## Cluster 2

**Predicted cell type:** classical monocyte
**Confidence:** 0.90

### Reasoning
The presence of LYZ, FCN1, CTSS, S100A8, and S100A9 in the marker genes suggests a classical monocyte identity, but the absence of strong neutrophil markers means we do not call neutrophil.

### Marker evidence
- LYZ: strongly supports classical monocyte
- S100A8: supports classical monocyte
- S100A9: supports classical monocyte
- FCN1: supports classical monocyte
- CTSS: supports classical monocyte

### Alternative cell types
- neutrophil
