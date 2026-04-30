# Cell Type Annotation Report

| Cluster | Predicted Cell Type | Confidence |
|---|---|---|
| 0 | B cell | 0.95 |
| 1 | cytotoxic T cell | 0.90 |
| 2 | classical monocyte | 0.85 |
| 3 | naive/central memory T cell | 0.80 |
| 4 | non-classical monocyte | 0.80 |
| 5 | platelet | 0.85 |
| 6 | proliferating cells | 0.85 |
| 7 | epithelial cell | 0.95 |
| 8 | endothelial cell | 0.95 |
| 9 | smooth muscle cell | 0.85 |

## Cluster 0

**Predicted cell type:** B cell
**Confidence:** 0.95

### Reasoning
Markers MS4A1 and CD79A strongly support B cell

### Marker evidence
- MS4A1: strongly supports B cell
- CD79A: strongly supports B cell
- CD74: no strong evidence for or against B cell
- HLA-DRA: no strong evidence for or against B cell
- CD37: no strong evidence for or against B cell

### Alternative cell types
- None

## Cluster 1

**Predicted cell type:** cytotoxic T cell
**Confidence:** 0.90

### Reasoning
NKG7, GNLY, PRF1, CTSW, and TRAC are strong markers for cytotoxic T cells and NK cells. Given the presence of these markers, we prefer cytotoxic T cell with NK cell as an alternative.

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
Insufficient marker evidence to make a confident prediction.

### Marker evidence
- LYZ: Supports classical monocyte or neutrophil.
- S100A8: Supports classical monocyte or neutrophil.
- S100A9: Supports classical monocyte or neutrophil.
- FCN1: Supports classical monocyte or neutrophil.
- CTSS: Supports classical monocyte or neutrophil.

### Alternative cell types
- None

### Warning
No clear cell type supported by marker genes.

## Cluster 3

**Predicted cell type:** naive/central memory T cell
**Confidence:** 0.80

### Reasoning
NKG7, GNLY, PRF1, CTSW, and TRAC are present in the marker genes, which prefer cytotoxic T cell over other options.

### Marker evidence
- CD3D: strongly supports cytotoxic T cell
- CD3E: strongly supports cytotoxic T cell
- IL7R: not specific to cytotoxic T cell, but present in marker genes
- CCR7: not specific to cytotoxic T cell, but present in marker genes
- LTB: not specific to cytotoxic T cell, but present in marker genes

### Alternative cell types
- CD4 T cell

### Warning
Reasoning references canonical markers not present in input.

## Cluster 4

**Predicted cell type:** non-classical monocyte
**Confidence:** 0.80

### Reasoning
N/A

### Marker evidence
- FCGR3A: Strongly supports neutrophil or monocyte
- MS4A7: Supports B cell or monocyte
- AIF1: Supports monocyte
- TYROBP: Supports monocyte

### Alternative cell types
- NK cell

### Warning
No clear cell type supported by marker genes.

## Cluster 5

**Predicted cell type:** platelet
**Confidence:** 0.85

### Reasoning
Insufficient evidence to determine cell type.

### Marker evidence
- PPBP: Supports platelet, but not strongly present.
- PF4: Supports platelet, but not strongly present.
- NRGN: No clear association with any cell type.
- GP9: Supports platelet, but not strongly present.
- ITGA2B: No clear association with any cell type.

### Alternative cell types
- None

### Warning
Strong platelet markers detected.

## Cluster 6

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

## Cluster 7

**Predicted cell type:** epithelial cell
**Confidence:** 0.95

### Reasoning
KRT18, KRT8, and EPCAM are strongly associated with epithelial cells.

### Marker evidence
- KRT18: strongly associated with epithelial cells
- KRT8: strongly associated with epithelial cells
- EPCAM: strongly associated with epithelial cells
- KRT19: associated with epithelial cells
- CLDN4: associated with epithelial cells

### Alternative cell types
- None

## Cluster 8

**Predicted cell type:** endothelial cell
**Confidence:** 0.95

### Reasoning
PECAM1 and VWF are strongly associated with endothelial cells.

### Marker evidence
- PECAM1: strongly associated with endothelial cells
- VWF: strongly associated with endothelial cells
- KDR: also expressed in endothelial cells
- ENG: also expressed in endothelial cells
- CDH5: also expressed in endothelial cells

### Alternative cell types
- None

## Cluster 9

**Predicted cell type:** smooth muscle cell
**Confidence:** 0.85

### Reasoning
The presence of ACTA2 and VWF in the marker genes supports endothelial cell identity.

### Marker evidence
- ACTA2: endothelial cell marker
- TAGLN: smooth muscle cell marker, but also present in endothelial cells
- MYH11: smooth muscle cell marker, but also present in endothelial cells
- CNN1: smooth muscle cell marker, but also present in endothelial cells
- DES: smooth muscle cell marker, but also present in endothelial cells

### Alternative cell types
- pericyte

### Warning
Reasoning references canonical markers not present in input.
