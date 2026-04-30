#!/usr/bin/env python3
"""
Parse marker genes CSV and write cluster-wise JSON for LLM annotation.

Input columns expected:
- cluster
- gene
- avg_log2FC
- p_val_adj
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


REQUIRED_COLUMNS = {"cluster", "gene", "avg_log2FC", "p_val_adj"}
COLUMN_ALIASES = {
    "cluster": ["cluster", "seurat_clusters", "leiden", "cluster_id"],
    "gene": ["gene", "genes", "marker", "marker_gene"],
    "avg_log2FC": ["avg_log2fc", "avg_logfc", "log2fc", "logfc"],
    "p_val_adj": ["p_val_adj", "p_adj", "padj", "adjusted_p_value", "q_value"],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Group top marker genes by cluster and export JSON."
    )
    parser.add_argument(
        "--input",
        default="data/example_markers.csv",
        help="Path to input marker CSV file.",
    )
    parser.add_argument(
        "--output",
        default="data/cluster_markers.json",
        help="Path to output JSON file.",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=5,
        help="Number of top genes to keep per cluster (default: 5).",
    )
    return parser.parse_args()


def normalize_column_name(name: str) -> str:
    return name.strip().replace("\ufeff", "").lower()


def build_column_mapping(fieldnames: list[str]) -> dict[str, str]:
    normalized_to_original = {}
    for name in fieldnames:
        normalized_to_original[normalize_column_name(name)] = name

    mapping: dict[str, str] = {}
    for canonical, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in normalized_to_original:
                mapping[canonical] = normalized_to_original[alias]
                break
    return mapping


def ensure_columns(fieldnames: list[str] | None, column_mapping: dict[str, str]) -> None:
    if not fieldnames:
        raise ValueError("CSV appears empty or is missing a header row.")

    missing = REQUIRED_COLUMNS - set(column_mapping.keys())
    if missing:
        found = [normalize_column_name(col) for col in fieldnames]
        raise ValueError(
            "CSV is missing required columns.\n"
            f"Required canonical columns: {', '.join(sorted(REQUIRED_COLUMNS))}\n"
            f"Found columns: {', '.join(found)}"
        )


def to_float_or_default(
    value: str, column: str, row_number: int, default: float
) -> tuple[float, bool]:
    raw = (value or "").strip()
    if not raw:
        print(
            f"Warning: missing {column} on row {row_number}; using default {default}."
        )
        return default, True
    try:
        return float(raw), False
    except ValueError:
        print(
            f"Warning: invalid {column} on row {row_number} ('{value}'); using default {default}."
        )
        return default, True


def load_markers(csv_path: Path) -> list[dict]:
    rows: list[dict] = []
    skipped_rows = 0
    repaired_values = 0

    with csv_path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        raw_fieldnames = reader.fieldnames or []
        column_mapping = build_column_mapping(raw_fieldnames)
        ensure_columns(raw_fieldnames, column_mapping)

        for idx, row in enumerate(reader, start=2):  # Header is row 1.
            cluster = (row.get(column_mapping["cluster"]) or "").strip()
            gene = (row.get(column_mapping["gene"]) or "").strip()
            if not cluster or not gene:
                skipped_rows += 1
                continue

            avg_log2fc, repaired_avg = to_float_or_default(
                row.get(column_mapping["avg_log2FC"], ""),
                "avg_log2FC",
                idx,
                0.0,
            )
            p_val_adj, repaired_padj = to_float_or_default(
                row.get(column_mapping["p_val_adj"], ""),
                "p_val_adj",
                idx,
                1.0,
            )
            repaired_values += int(repaired_avg) + int(repaired_padj)

            rows.append(
                {
                    "cluster": cluster,
                    "gene": gene,
                    "avg_log2FC": avg_log2fc,
                    "p_val_adj": p_val_adj,
                }
            )

    print(f"Rows loaded: {len(rows)}")
    print(f"Rows skipped: {skipped_rows}")
    print(f"Numeric values repaired: {repaired_values}")
    return rows


def group_top_markers(rows: list[dict], top_n: int) -> dict:
    by_cluster: dict[str, list[dict]] = defaultdict(list)
    for item in rows:
        by_cluster[item["cluster"]].append(item)

    output = {
        "clusters": []
    }

    for cluster_name in sorted(by_cluster.keys()):
        sorted_genes = sorted(
            by_cluster[cluster_name],
            key=lambda x: (-x["avg_log2FC"], x["p_val_adj"]),
        )
        top_genes = sorted_genes[:top_n]

        output["clusters"].append(
            {
                "cluster": cluster_name,
                "top_markers": [
                    {
                        "gene": gene_entry["gene"],
                        "avg_log2FC": gene_entry["avg_log2FC"],
                        "p_val_adj": gene_entry["p_val_adj"],
                    }
                    for gene_entry in top_genes
                ],
            }
        )

    return output


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    if args.top_n <= 0:
        raise ValueError("--top-n must be greater than 0.")

    if not input_path.exists():
        raise FileNotFoundError(f"Input CSV not found: {input_path}")

    rows = load_markers(input_path)
    grouped = group_top_markers(rows, args.top_n)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(grouped, handle, indent=2)

    print(f"Wrote {len(grouped['clusters'])} clusters to {output_path}")


if __name__ == "__main__":
    main()
