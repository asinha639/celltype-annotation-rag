#!/usr/bin/env python3
import json
from pathlib import Path

INPUT_PATH = Path("data/annotations.json")
OUTPUT_PATH = Path("reports/annotation_report.md")


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

    lines: list[str] = []
    lines.append("# Cell Type Annotation Report")
    lines.append("")
    lines.append("| Cluster | Predicted Cell Type | Confidence |")
    lines.append("|---|---|---|")

    for ann in annotations:
        cluster = str(ann.get("cluster", "unknown"))
        predicted = str(ann.get("predicted_cell_type", "unknown"))
        confidence = to_float(ann.get("confidence", 0.0))
        lines.append(f"| {cluster} | {predicted} | {confidence:.2f} |")

    lines.append("")

    for ann in annotations:
        cluster = str(ann.get("cluster", "unknown"))
        predicted = str(ann.get("predicted_cell_type", "unknown"))
        confidence = to_float(ann.get("confidence", 0.0))
        reasoning = str(ann.get("reasoning", "")).strip() or "N/A"
        warning = str(ann.get("warning", "")).strip()

        marker_evidence = ann.get("marker_evidence", {})
        if not isinstance(marker_evidence, dict):
            marker_evidence = {}

        alternatives = ann.get("alternative_cell_types", [])
        if not isinstance(alternatives, list):
            alternatives = []

        lines.append(f"## Cluster {cluster}")
        lines.append("")
        lines.append(f"**Predicted cell type:** {predicted}")
        lines.append(f"**Confidence:** {confidence:.2f}")
        lines.append("")
        lines.append("### Reasoning")
        lines.append(reasoning)
        lines.append("")
        lines.append("### Marker evidence")
        if marker_evidence:
            for gene, evidence in marker_evidence.items():
                lines.append(f"- {gene}: {str(evidence)}")
        else:
            lines.append("- None")
        lines.append("")
        lines.append("### Alternative cell types")
        if alternatives:
            for alt in alternatives:
                lines.append(f"- {str(alt)}")
        else:
            lines.append("- None")
        lines.append("")

        if warning:
            lines.append("### Warning")
            lines.append(warning)
            lines.append("")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print("Wrote report to reports/annotation_report.md")


if __name__ == "__main__":
    main()
