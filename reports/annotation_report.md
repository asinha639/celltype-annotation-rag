# Cell Type Annotation Report

| Cluster | Predicted Cell Type | Confidence |
|---|---|---|
| 0 | naive/central memory T cell | 0.80 |
| 1 | cytotoxic T cell | 0.85 |
| 2 | unknown | 0.00 |
| 3 | regulatory T cell | 0.95 |
| 4 | unknown | 0.00 |
| 5 | monocyte | 0.85 |
| 6 | monocyte | 0.90 |
| 7 | proliferating cells | 0.85 |
| 8 | endothelial cell | 0.95 |
| 9 | proliferating cells | 0.85 |

## Cluster 0

**Predicted cell type:** naive/central memory T cell
**Confidence:** 0.80

### Reasoning
NKG7, GNLY, PRF1, CTSW, and TRAC are present in the marker genes, which prefer cytotoxic T cell over other options.

### Marker evidence
- CD3D: strongly supports cytotoxic T cell
- CD3E: supports cytotoxic T cell
- TRAC: supports cytotoxic T cell
- IL7R: supports T cell
- CCR7: supports T cell

### Alternative cell types
- CD4 T cell

### Warning
Reasoning references canonical markers not present in input.

## Cluster 1

**Predicted cell type:** cytotoxic T cell
**Confidence:** 0.85

### Reasoning
NKG7, GNLY, PRF1, CTSW, and TRAC are strong markers for cytotoxic T cells and NK cells. Since NKG7 and GNLY are present, NK cell is considered an alternative.

### Marker evidence
- CD8A: marker for cytotoxic T cells
- CD8B: marker for cytotoxic T cells
- NKG7: strong marker for cytotoxic T cells and NK cells
- GNLY: strong marker for cytotoxic T cells and NK cells
- GZMH: marker for cytotoxic T cells

### Alternative cell types
- NK cell

### Warning
Reasoning references canonical markers not present in input.

## Cluster 2

**Predicted cell type:** unknown
**Confidence:** 0.00

### Reasoning
No clear markers for a specific cell type

### Marker evidence
- CXCL13: marker for activated B cells and follicular helper T cells
- PDCD1: marker for regulatory T cells
- HAVCR2: marker for regulatory T cells
- LAG3: marker for regulatory T cells
- TOX: marker for regulatory T cells

### Alternative cell types
- None

### Warning
No clear markers for a specific cell type Low confidence prediction. Model could not confidently assign a cell type.

## Cluster 3

**Predicted cell type:** regulatory T cell
**Confidence:** 0.95

### Reasoning
FOXP3, IL2RA, CTLA4, and TIGIT are strong markers for regulatory T cells.

### Marker evidence
- FOXP3: strong marker for regulatory T cells
- IL2RA: strong marker for regulatory T cells
- CTLA4: strong marker for regulatory T cells
- TIGIT: strong marker for regulatory T cells
- CD4: marker for T cells, but not specific to regulatory T cells

### Alternative cell types
- None

## Cluster 4

**Predicted cell type:** unknown
**Confidence:** 0.00

### Reasoning
N/A

### Marker evidence
- FXYD6: no clear cell type supported
- LSAMP: no clear cell type supported
- MEG3: no clear cell type supported
- NCAM1: no clear cell type supported
- SOX11: no clear cell type supported

### Alternative cell types
- None

### Warning
No clear cell type supported by marker genes. Low confidence prediction. Model could not confidently assign a cell type.

## Cluster 5

**Predicted cell type:** monocyte
**Confidence:** 0.85

### Reasoning
The presence of CD68 and CSF1R in the marker genes supports a monocyte cell type. The absence of strong neutrophil markers such as FCGR3B, CSF3R, CXCR2, S100A8, S100A9, LCN2, or MPO also supports this classification.

### Marker evidence
- CD68: strongly supports monocyte cell type
- SOX2: not a strong indicator of any cell type
- AIF1: not a strong indicator of any cell type
- CSF1R: strongly supports monocyte cell type
- TYROBP: not a strong indicator of any cell type

### Alternative cell types
- neutrophil

### Warning
Reasoning references canonical markers not present in input.

## Cluster 6

**Predicted cell type:** monocyte
**Confidence:** 0.90

### Reasoning
LYZ, CD163, and C1QA are strong markers for monocytes.

### Marker evidence
- CD68: strong monocyte marker
- LYZ: strong monocyte marker
- CD163: strong monocyte marker
- C1QA: strong monocyte marker
- C1QB: monocyte marker

### Alternative cell types
- neutrophil

## Cluster 7

**Predicted cell type:** proliferating cells
**Confidence:** 0.85

### Reasoning
The presence of TOP2A and MKI67 in the marker genes suggests proliferating cells.

### Marker evidence
- GFAP: neural progenitor marker
- SOX2: neural progenitor marker
- EGFR: epithelial marker
- NES: neural progenitor marker
- TOP2A: proliferating cell marker

### Alternative cell types
- None

### Warning
Reasoning references canonical markers not present in input.

## Cluster 8

**Predicted cell type:** endothelial cell
**Confidence:** 0.95

### Reasoning
PECAM1, VWF, KDR, ENG, CDH5 are endothelial markers

### Marker evidence
- PECAM1: endothelial marker
- VWF: endothelial marker
- KDR: endothelial marker
- ENG: endothelial marker
- CDH5: endothelial marker

### Alternative cell types
- None

## Cluster 9

**Predicted cell type:** proliferating cells
**Confidence:** 0.85

### Reasoning
MKI67, TOP2A, STMN1, PCNA, TYMS are markers of proliferating cells.

### Marker evidence
- MKI67: marker of proliferating cells
- TOP2A: marker of proliferating cells
- STMN1: marker of proliferating cells
- PCNA: marker of proliferating cells
- TYMS: marker of proliferating cells

### Alternative cell types
- None

### Warning
Cell cycle markers indicate proliferation; parent lineage may require additional markers.
