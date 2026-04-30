# Cell Type Annotation Report

| Cluster | Predicted Cell Type | Confidence |
|---|---|---|
| 0 | naive/central memory T cell | 0.80 |
| 1 | cytotoxic T cell | 0.50 |
| 2 | unknown | 0.00 |
| 3 | unknown | 0.00 |
| 4 | unknown | 0.00 |
| 5 | unknown | 0.00 |
| 6 | monocyte | 0.90 |
| 7 | proliferating cells | 0.50 |
| 8 | endothelial cell | 0.95 |
| 9 | proliferating cells | 0.85 |

## Cluster 0

**Predicted cell type:** naive/central memory T cell
**Confidence:** 0.80

### Reasoning
N/A

### Marker evidence
- CD3D: T cell marker
- CD3E: T cell marker
- TRAC: T cell marker
- IL7R: T cell marker
- CCR7: T cell marker

### Alternative cell types
- CD4 T cell

### Literature context used
- None

### Warning
No clear cell type supported by markers

## Cluster 1

**Predicted cell type:** cytotoxic T cell
**Confidence:** 0.50

### Reasoning
NKG7, GNLY, and PRF1 are strong markers for cytotoxic T cells, while TRAC is also present.

### Marker evidence
- CD8A: strong marker for cytotoxic T cells
- CD8B: strong marker for cytotoxic T cells
- NKG7: strong marker for cytotoxic T cells
- GNLY: strong marker for cytotoxic T cells
- GZMH: strong marker for cytotoxic T cells

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

**Predicted cell type:** unknown
**Confidence:** 0.00

### Reasoning
N/A

### Marker evidence
- CXCL13: chemokine involved in lymphoid organ development
- PDCD1: co-inhibitory receptor on T cells
- HAVCR2: receptor on T cells and NK cells
- LAG3: co-inhibitory receptor on T cells
- TOX: transcription factor involved in T cell development

### Alternative cell types
- None

### Literature context used
- None

### Warning
Insufficient marker evidence Low confidence prediction. Model could not confidently assign a cell type.

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
No strong markers for a specific cell type

### Marker evidence
- FXYD6: No clear association with a specific cell type
- LSAMP: No clear association with a specific cell type
- MEG3: No clear association with a specific cell type
- NCAM1: No clear association with a specific cell type
- SOX11: No clear association with a specific cell type

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
Insufficient marker evidence Low confidence prediction. Model could not confidently assign a cell type.

## Cluster 5

**Predicted cell type:** unknown
**Confidence:** 0.00

### Reasoning
N/A

### Marker evidence
- CD68: marker for monocytes/macrophages
- SOX2: marker for stem cells and progenitor cells
- AIF1: marker for macrophages
- CSF1R: marker for monocytes/macrophages
- TYROBP: marker for monocytes/macrophages

### Alternative cell types
- None

### Literature context used
- None

### Warning
No clear cell type supported by markers Low confidence prediction. Model could not confidently assign a cell type.

## Cluster 6

**Predicted cell type:** monocyte
**Confidence:** 0.90

### Reasoning
LYZ, CD163, and C1QA are strong markers for monocytes.

### Marker evidence
- CD68: marker for monocytes
- LYZ: strong marker for monocytes
- CD163: strong marker for monocytes
- C1QA: marker for monocytes
- C1QB: marker for monocytes

### Alternative cell types
- neutrophil

### Literature context used
- None

## Cluster 7

**Predicted cell type:** proliferating cells
**Confidence:** 0.50

### Reasoning
The presence of MKI67 and TOP2A in the marker genes suggests proliferating cells.

### Marker evidence
- GFAP: marker for neural cells, but not strongly supported here
- SOX2: marker for neural cells, but not strongly supported here
- EGFR: marker for epithelial cells, but not strongly supported here
- NES: marker for neural cells, but not strongly supported here
- TOP2A: strong marker for proliferating cells

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
PECAM1 and VWF are strong markers for endothelial cells.

### Marker evidence
- PECAM1: strong marker for endothelial cells
- VWF: strong marker for endothelial cells
- KDR: marker for endothelial cells
- ENG: marker for endothelial cells
- CDH5: marker for endothelial cells

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
MKI67 and TOP2A are markers of proliferating cells.

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
