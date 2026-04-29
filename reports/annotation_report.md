# Cell Type Annotation Report

| Cluster | Predicted Cell Type | Confidence |
|---|---|---|
| 0 | B cell | 0.95 |
| 1 | cytotoxic T cell | 0.90 |
| 2 | classical monocyte | 0.85 |

## Cluster 0

**Predicted cell type:** B cell
**Confidence:** 0.95

### Reasoning
Strong markers for B cell (MS4A1, CD79A) with no conflicting markers.

### Marker evidence
- MS4A1: Strong marker for B cell
- CD79A: Strong marker for B cell
- CD74: Monocyte marker, but not strong enough to override B cell markers
- HLA-DRA: Present in various immune cells, not specific enough to determine cell type
- CD37: Present in various immune cells, not specific enough to determine cell type

### Alternative cell types
- None

## Cluster 1

**Predicted cell type:** cytotoxic T cell
**Confidence:** 0.90

### Reasoning
NKG7, GNLY, PRF1, CTSW, and TRAC are characteristic of cytotoxic T cells.

### Marker evidence
- NKG7: strong marker for cytotoxic T cells and NK cells
- GNLY: strong marker for cytotoxic T cells and NK cells
- PRF1: strong marker for cytotoxic T cells and NK cells
- CTSW: strong marker for cytotoxic T cells and NK cells
- TRAC: strong marker for cytotoxic T cells and NK cells

### Alternative cell types
- NK cell

## Cluster 2

**Predicted cell type:** classical monocyte
**Confidence:** 0.85

### Reasoning
The cluster contains LYZ, FCN1, CTSS, S100A8, and S100A9, which are strong markers for classical monocytes. This is consistent with the literature context, which shows the expression levels of these genes in monocytes.

### Marker evidence
- LYZ: Strong marker for classical monocytes
- S100A8: Strong marker for classical monocytes
- S100A9: Strong marker for classical monocytes
- FCN1: Strong marker for classical monocytes
- CTSS: Strong marker for classical monocytes

### Alternative cell types
- neutrophil

### Warning
Some genes are not typically associated with classical monocytes, but the strong presence of LYZ, FCN1, CTSS, S100A8, and S100A9 suggests a classical monocyte identity.
