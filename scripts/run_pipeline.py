#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from annotate_clusters import annotate_clusters, save_annotations
from generate_report import main as generate_report_main
from parse_markers import group_top_markers, load_markers


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the full annotation pipeline.")
    parser.add_argument(
        "--input",
        default="data/example_markers.csv",
        help="Path to input marker CSV file (default: data/example_markers.csv).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    token = os.getenv("HF_TOKEN")
    if not token:
        raise ValueError("HF_TOKEN is not set")

    input_csv = Path(args.input)
    cluster_json_path = Path("data/cluster_markers.json")
    annotations_path = Path("data/annotations.json")

    print("Parsing markers...")
    rows = load_markers(input_csv)
    grouped = group_top_markers(rows, top_n=5)

    cluster_json_path.parent.mkdir(parents=True, exist_ok=True)
    with cluster_json_path.open("w", encoding="utf-8") as handle:
        json.dump(grouped, handle, indent=2)

    with cluster_json_path.open("r", encoding="utf-8") as handle:
        clusters = json.load(handle).get("clusters", [])

    print("Annotating clusters...")
    annotations = annotate_clusters(clusters, token)
    save_annotations(annotations_path, annotations)
    generate_report_main()
    print("Report generation complete: reports/annotation_report.md")

    print("Pipeline complete.")


if __name__ == "__main__":
    main()
