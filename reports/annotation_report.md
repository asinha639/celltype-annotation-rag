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
Strongly prefer B cell due to presence of MS4A1 and CD79A.

### Marker evidence
- MS4A1: Strongly supports B cell identity.
- CD79A: Strongly supports B cell identity.
- CD74: Not specific to B cells, but present.
- HLA-DRA: Not specific to B cells, but present.
- CD37: Not specific to B cells, but present.

### Alternative cell types
- None

## Cluster 1

**Predicted cell type:** cytotoxic T cell
**Confidence:** 0.90

### Reasoning
Marker genes NKG7, GNLY, PRF1, CTSW, and TRAC are strongly associated with cytotoxic T cells.

### Marker evidence
- NKG7: Strongly associated with cytotoxic T cells.
- GNLY: Strongly associated with cytotoxic T cells.
- PRF1: Strongly associated with cytotoxic T cells.
- CTSW: Strongly associated with cytotoxic T cells.
- TRAC: Strongly associated with cytotoxic T cells.

### Alternative cell types
- NK cell

## Cluster 2

**Predicted cell type:** classical monocyte
**Confidence:** 0.90

### Reasoning
The presence of LYZ, FCN1, CTSS, S100A8, and S100A9 in the marker genes suggests classical monocyte. However, the absence of strong neutrophil markers means we do not overcall neutrophils.

### Marker evidence
- LYZ: strongly supports classical monocyte
- FCN1: supports classical monocyte
- CTSS: supports classical monocyte
- S100A8: supports classical monocyte
- S100A9: supports classical monocyte

### Alternative cell types
- neutrophil
