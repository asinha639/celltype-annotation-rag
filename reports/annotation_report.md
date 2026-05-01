# Cell Type Annotation Report

| Cluster | Predicted Cell Type | Confidence |
|---|---|---|
| 0 | naive/central memory T cell | 0.90 |
| 1 | cytotoxic T cell | 0.50 |
| 2 | exhausted T cell | 0.90 |
| 3 | unknown | 0.00 |
| 4 | unknown | 0.00 |
| 5 | unknown | 0.00 |
| 6 | classical monocyte | 0.50 |
| 7 | proliferating cells | 0.50 |
| 8 | endothelial cell | 0.95 |
| 9 | proliferating cells | 0.85 |

## Cluster 0

**Predicted cell type:** naive/central memory T cell
**Confidence:** 0.90

### Reasoning
N/A

### Marker evidence
- CD3D: 
- CD3E: 
- TRAC: 
- IL7R: 
- CCR7: 

### Alternative cell types
- CD4 T cell

### Literature context used
- None

## Cluster 1

**Predicted cell type:** cytotoxic T cell
**Confidence:** 0.50

### Reasoning
NKG7, GNLY, and PRF1 are strong markers for cytotoxic T cells and NK cells. TRAC is also a marker for cytotoxic T cells.

### Marker evidence
- CD8A: strong marker for cytotoxic T cells
- CD8B: strong marker for cytotoxic T cells
- NKG7: strong marker for cytotoxic T cells and NK cells
- GNLY: strong marker for cytotoxic T cells and NK cells
- GZMH: marker for cytotoxic T cells

### Alternative cell types
- NK cell

### Literature context used
- Source: 1-s2.0-S0888754325000102-main.pdf
  Score: 0.5158
  Snippet: ls, and monocytes, which can influence the results of 
cell clustering and identification [39,40].
Moreover, scRNA-seq in population-based cohorts is limited by both 
technical and logistical challenges, including low throughput and high 
cost. Therefore, the advancement of single-cell sequencing te

### Warning
Reasoning contains genes not in input. Reasoning references canonical markers not present in input.

## Cluster 2

**Predicted cell type:** exhausted T cell
**Confidence:** 0.90

### Reasoning
N/A

### Marker evidence
- CXCL13: chemokine, supports immune cell
- PDCD1: immune checkpoint, supports immune cell
- HAVCR2: immune checkpoint, supports immune cell
- LAG3: immune checkpoint, supports immune cell
- TOX: T cell transcription factor, supports T cell

### Alternative cell types
- T follicular helper cell

### Literature context used
- None

## Cluster 3

**Predicted cell type:** unknown
**Confidence:** 0.00

### Reasoning
N/A

### Marker evidence
- FOXP3: Treg marker
- IL2RA: Treg marker
- CTLA4: Treg marker
- TIGIT: Treg marker
- CD4: T cell marker

### Alternative cell types
- None

### Literature context used
- None

### Warning
Insufficient marker evidence Low confidence prediction. Model could not confidently assign a cell type.

## Cluster 4

**Predicted cell type:** unknown
**Confidence:** 0.00

### Reasoning
No strong markers present

### Marker evidence
- FXYD6: No clear association with any cell type
- LSAMP: No clear association with any cell type
- MEG3: No clear association with any cell type
- NCAM1: No clear association with any cell type
- SOX11: No clear association with any cell type

### Alternative cell types
- None

### Literature context used
- Source: Systematic comparison of single-cell and single-nucleus RNA-sequencing methods.pdf
  Score: 0.5380
  Snippet: uenced 
together and assigned one cell barcode, can be detected when cell 
barcodes have a substantial fraction of reads from both species. We 
profiled frozen human PBMCs because (1) they are a heterogeneous 
mixture of cells, particularly with respect to their amount of RNA 
per cell, yet they do

### Warning
No clear markers for any cell type Low confidence prediction. Model could not confidently assign a cell type.

## Cluster 5

**Predicted cell type:** unknown
**Confidence:** 0.00

### Reasoning
N/A

### Marker evidence
- CD68: marker for monocytes
- SOX2: marker for stem cells
- AIF1: marker for monocytes
- CSF1R: marker for monocytes
- TYROBP: marker for monocytes

### Alternative cell types
- None

### Literature context used
- None

### Warning
Insufficient marker evidence Low confidence prediction. Model could not confidently assign a cell type.

## Cluster 6

**Predicted cell type:** classical monocyte
**Confidence:** 0.50

### Reasoning
LYZ, CD163, and C1QA are strong markers for monocytes. LYZ, FCN1, CTSS, S100A8, and S100A9 also support classical monocyte over neutrophil.

### Marker evidence
- CD68: monocyte marker
- LYZ: strong marker for classical monocyte
- CD163: strong marker for monocytes
- C1QA: strong marker for monocytes
- C1QB: monocyte marker

### Alternative cell types
- neutrophil

### Literature context used
- None

### Warning
Reasoning contains genes not in input. Reasoning references canonical markers not present in input.

## Cluster 7

**Predicted cell type:** proliferating cells
**Confidence:** 0.50

### Reasoning
The presence of MKI67 and TOP2A in the marker genes suggests proliferating cells.

### Marker evidence
- GFAP: astrocyte marker, supports neural lineage
- SOX2: neural progenitor marker, supports neural lineage
- EGFR: epithelial marker, supports epithelial cells
- NES: neural marker, supports neural lineage
- TOP2A: proliferating cell marker, supports proliferating cells

### Alternative cell types
- None

### Literature context used
- Source: Systematic comparison of single-cell and single-nucleus RNA-sequencing methods.pdf
  Score: 0.5359
  Snippet: uenced 
together and assigned one cell barcode, can be detected when cell 
barcodes have a substantial fraction of reads from both species. We 
profiled frozen human PBMCs because (1) they are a heterogeneous 
mixture of cells, particularly with respect to their amount of RNA 
per cell, yet they do

### Warning
Reasoning contains genes not in input. Reasoning references canonical markers not present in input.

## Cluster 8

**Predicted cell type:** endothelial cell
**Confidence:** 0.95

### Reasoning
PECAM1, VWF, KDR, ENG, CDH5 are endothelial cell markers.

### Marker evidence
- PECAM1: endothelial cell marker
- VWF: endothelial cell marker
- KDR: endothelial cell marker
- ENG: endothelial cell marker
- CDH5: endothelial cell marker

### Alternative cell types
- None

### Literature context used
- Source: 1-s2.0-S0888754325000102-main.pdf
  Score: 0.5126
  Snippet: ls, and monocytes, which can influence the results of 
cell clustering and identification [39,40].
Moreover, scRNA-seq in population-based cohorts is limited by both 
technical and logistical challenges, including low throughput and high 
cost. Therefore, the advancement of single-cell sequencing te

## Cluster 9

**Predicted cell type:** proliferating cells
**Confidence:** 0.85

### Reasoning
MKI67, TOP2A, STMN1, PCNA, and TYMS are markers of proliferating cells.

### Marker evidence
- MKI67: marker of proliferating cells
- TOP2A: marker of proliferating cells
- STMN1: marker of proliferating cells
- PCNA: marker of proliferating cells
- TYMS: marker of proliferating cells

### Alternative cell types
- None

### Literature context used
- Source: Systematic comparison of single-cell and single-nucleus RNA-sequencing methods.pdf
  Score: 0.5517
  Snippet: uenced 
together and assigned one cell barcode, can be detected when cell 
barcodes have a substantial fraction of reads from both species. We 
profiled frozen human PBMCs because (1) they are a heterogeneous 
mixture of cells, particularly with respect to their amount of RNA 
per cell, yet they do

### Warning
Cell cycle markers indicate proliferation; parent lineage may require additional markers.
