#!/usr/bin/env python3
import json
from pathlib import Path

INPUT_PATH = Path("data/annotations.json")
OUTPUT_PATH = Path("reports/evaluation_summary.md")


def to_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_PATH}")

    with INPUT_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    annotations = data.get("annotations", [])
    if not isinstance(annotations, list):
        annotations = []

    total_clusters = len(annotations)
    high_conf = 0
    med_conf = 0
    low_conf = 0
    unknown_count = 0
    clusters_with_warnings: list[str] = []
    manual_review_clusters: list[str] = []

    for ann in annotations:
        cluster = str(ann.get("cluster", "unknown"))
        predicted = str(ann.get("predicted_cell_type", "unknown")).strip().lower()
        confidence = to_float(ann.get("confidence", 0.0))
        warning = str(ann.get("warning", "")).strip()

        if confidence >= 0.85:
            high_conf += 1
        elif confidence >= 0.60:
            med_conf += 1
        else:
            low_conf += 1

        if predicted == "unknown":
            unknown_count += 1

        if warning:
            clusters_with_warnings.append(cluster)

        needs_manual_review = (
            confidence < 0.80 or predicted == "unknown" or bool(warning)
        )
        if needs_manual_review:
            manual_review_clusters.append(cluster)

    lines: list[str] = []
    lines.append("# Annotation Evaluation Summary")
    lines.append("")
    lines.append(f"- Total number of clusters: {total_clusters}")
    lines.append(f"- High-confidence annotations (>= 0.85): {high_conf}")
    lines.append(f"- Medium-confidence annotations (0.60 to < 0.85): {med_conf}")
    lines.append(f"- Low-confidence annotations (< 0.60): {low_conf}")
    lines.append(f"- Unknown annotations: {unknown_count}")
    lines.append("")

    lines.append("## Clusters with Warnings")
    if clusters_with_warnings:
        for cluster in clusters_with_warnings:
            lines.append(f"- Cluster {cluster}")
    else:
        lines.append("- None")
    lines.append("")

    lines.append("## Clusters Needing Manual Review")
    if manual_review_clusters:
        for cluster in manual_review_clusters:
            lines.append(f"- Cluster {cluster}")
    else:
        lines.append("- None")
    lines.append("")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print("Wrote evaluation summary to reports/evaluation_summary.md")


if __name__ == "__main__":
    main()
