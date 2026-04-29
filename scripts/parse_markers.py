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


def ensure_columns(fieldnames: list[str] | None) -> None:
    if not fieldnames:
        raise ValueError("CSV appears empty or is missing a header row.")

    missing = REQUIRED_COLUMNS - set(fieldnames)
    if missing:
        raise ValueError(
            f"CSV is missing required columns: {', '.join(sorted(missing))}"
        )


def to_float(value: str, column: str, row_number: int) -> float:
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(
            f"Invalid numeric value in column '{column}' on row {row_number}: {value}"
        ) from exc


def load_markers(csv_path: Path) -> list[dict]:
    rows: list[dict] = []
    with csv_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        ensure_columns(reader.fieldnames)

        for idx, row in enumerate(reader, start=2):  # Header is row 1.
            rows.append(
                {
                    "cluster": row["cluster"].strip(),
                    "gene": row["gene"].strip(),
                    "avg_log2FC": to_float(row["avg_log2FC"], "avg_log2FC", idx),
                    "p_val_adj": to_float(row["p_val_adj"], "p_val_adj", idx),
                }
            )
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
