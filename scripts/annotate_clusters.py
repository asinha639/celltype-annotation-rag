import json
import os
from pathlib import Path

import requests

HF_URL = "https://router.huggingface.co/v1/chat/completions"
MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct"
INPUT_PATH = Path("data/cluster_markers.json")
OUTPUT_PATH = Path("data/annotations.json")


def load_clusters(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    clusters = data.get("clusters")
    if not isinstance(clusters, list):
        raise ValueError("Invalid input JSON: expected a 'clusters' list")

    return clusters


def build_messages(cluster_id: str, genes: list[str]) -> list[dict]:
    genes_text = ", ".join(genes)
    prompt = (
        "You are a single-cell RNA-seq annotation assistant. "
        f"Cluster: {cluster_id}. "
        f"Top marker genes: {genes_text}.\n\n"
        "Return only valid JSON with keys exactly:\n"
        "cluster\n"
        "predicted_cell_type\n"
        "confidence\n"
        "reasoning\n"
        "alternative_cell_types\n\n"
        "warning\n"
        "marker_evidence\n\n"
        "Rules:\n"
        "- for this cluster, only discuss the marker genes provided above\n"
        "- do not mention genes from other clusters\n"
        "- be conservative in cell type calling\n"
        "- do not overcall neutrophils unless markers include FCGR3B, CSF3R, CXCR2, S100A8, S100A9, LCN2, or MPO\n"
        "- if markers include LYZ, FCN1, CTSS, S100A8, and S100A9, prefer classical monocyte over neutrophil unless strong neutrophil markers are present\n"
        "- confidence should be a number between 0 and 1\n"
        "- alternative_cell_types should be a JSON array of strings\n"
        "- warning should be a short string about uncertainty or caution (or empty string if none)\n"
        "- marker_evidence should be a JSON object with keys that are marker genes and values that briefly explain support/conflict\n"
        "- marker_evidence must only include genes from the input marker list for this cluster\n"
        "- no markdown, no extra text"
    )

    return [{"role": "user", "content": prompt}]


def call_hf_chat(token: str, messages: list[dict]) -> str:
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "max_tokens": 400,
        "temperature": 0.2,
    }

    response = requests.post(
        HF_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )

    response.raise_for_status()
    response_json = response.json()

    return response_json["choices"][0]["message"]["content"]


def parse_model_json(raw_text: str, cluster_id: str, input_genes: list[str]) -> dict:
    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError:
        # Basic recovery for cases where the model wraps JSON in extra text.
        start = raw_text.find("{")
        end = raw_text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("Model response is not valid JSON")
        parsed = json.loads(raw_text[start : end + 1])

    required_keys = {
        "cluster",
        "predicted_cell_type",
        "confidence",
        "reasoning",
        "alternative_cell_types",
        "warning",
        "marker_evidence",
    }
    missing = required_keys - set(parsed.keys())
    if missing:
        raise ValueError(f"Missing keys in model JSON: {sorted(missing)}")

    parsed["cluster"] = str(cluster_id)

    if not isinstance(parsed.get("alternative_cell_types"), list):
        parsed["alternative_cell_types"] = []
    if not isinstance(parsed.get("warning"), str):
        parsed["warning"] = ""
    if not isinstance(parsed.get("marker_evidence"), dict):
        parsed["marker_evidence"] = {}
    else:
        # Keep evidence limited to the marker genes provided for this cluster.
        allowed_genes = {gene.strip() for gene in input_genes if gene.strip()}
        filtered_evidence = {}
        for gene_name, evidence_text in parsed["marker_evidence"].items():
            if gene_name in allowed_genes:
                filtered_evidence[gene_name] = evidence_text
        parsed["marker_evidence"] = filtered_evidence

    return parsed


def annotate_clusters(clusters: list[dict], token: str) -> list[dict]:
    annotations = []

    for cluster_obj in clusters:
        cluster_id = str(cluster_obj.get("cluster", "unknown"))
        markers = cluster_obj.get("top_markers", [])
        genes = [m.get("gene", "") for m in markers if m.get("gene")]

        if not genes:
            annotations.append(
                {
                    "cluster": cluster_id,
                    "predicted_cell_type": "unknown",
                    "confidence": 0.0,
                    "reasoning": "No marker genes found for this cluster.",
                    "alternative_cell_types": [],
                    "warning": "No marker genes were provided; prediction is unreliable.",
                    "marker_evidence": {},
                    "error": "No marker genes in input.",
                }
            )
            continue

        try:
            messages = build_messages(cluster_id, genes)
            raw_output = call_hf_chat(token, messages)
            parsed_output = parse_model_json(raw_output, cluster_id, genes)
            annotations.append(parsed_output)
        except (requests.RequestException, ValueError, KeyError, IndexError) as exc:
            annotations.append(
                {
                    "cluster": cluster_id,
                    "predicted_cell_type": "unknown",
                    "confidence": 0.0,
                    "reasoning": "Annotation failed for this cluster.",
                    "alternative_cell_types": [],
                    "warning": "Model call or JSON parsing failed; output is a fallback.",
                    "marker_evidence": {},
                    "error": str(exc),
                }
            )

    return annotations


def save_annotations(path: Path, annotations: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump({"annotations": annotations}, f, indent=2)


def main() -> None:
    token = os.getenv("HF_TOKEN")
    if not token:
        raise ValueError("HF_TOKEN is not set")

    clusters = load_clusters(INPUT_PATH)
    annotations = annotate_clusters(clusters, token)
    save_annotations(OUTPUT_PATH, annotations)

    print(f"Saved {len(annotations)} cluster annotations to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
