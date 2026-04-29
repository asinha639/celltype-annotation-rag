import json
import os
from pathlib import Path

import requests
from retrieve_context import retrieve_context_points

HF_URL = "https://router.huggingface.co/v1/chat/completions"
MODEL_NAME = os.getenv("HF_MODEL", "meta-llama/Llama-3.1-8B-Instruct")
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


def build_messages(cluster_id: str, genes: list[str], literature_context: str) -> list[dict]:
    genes_text = ", ".join(genes)
    prompt_input = {
        "cluster": cluster_id,
        "top_marker_genes": genes_text,
        "literature_context": literature_context,
    }
    system_prompt = (
        "You are a single-cell RNA-seq annotation assistant.\n"
        "Use both sources for reasoning:\n"
        "1) top marker genes for the cluster\n"
        "2) literature_context snippets from retrieved papers\n"
        "Be conservative: literature supports reasoning, but final cell-type decisions must be driven by marker genes.\n"
        "marker_evidence must ONLY include genes from the input marker list for this cluster. "
        "Do not add genes from literature_context into marker_evidence.\n"
        "Do not mention genes from other clusters."
    )

    user_prompt = (
        "Return only valid JSON with keys exactly:\n"
        "cluster\n"
        "predicted_cell_type\n"
        "confidence\n"
        "reasoning\n"
        "alternative_cell_types\n\n"
        "warning\n"
        "marker_evidence\n\n"
        "Input:\n"
        f"{json.dumps(prompt_input, ensure_ascii=False)}\n\n"
        "Rules:\n"
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

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def call_hf_chat(token: str, messages: list[dict], temperature: float = 0.2) -> str:
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "max_tokens": 400,
        "temperature": temperature,
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


def validate_annotation(annotation: dict, input_genes: list[str]) -> dict:
    warnings: list[str] = []
    existing_warning = annotation.get("warning", "")
    if isinstance(existing_warning, str) and existing_warning.strip():
        warnings.append(existing_warning.strip())

    confidence_value = annotation.get("confidence", 0.0)
    try:
        confidence = float(confidence_value)
    except (TypeError, ValueError):
        confidence = 0.0
        annotation["confidence"] = confidence

    if confidence < 0.5:
        warnings.append("Low confidence prediction.")

    marker_evidence = annotation.get("marker_evidence")
    if not isinstance(marker_evidence, dict):
        marker_evidence = {}
        annotation["marker_evidence"] = marker_evidence

    # Extra safety check: keep only evidence genes present in the input list.
    allowed_genes = {gene.strip() for gene in input_genes if gene.strip()}
    filtered_evidence = {}
    for gene_name, evidence_text in marker_evidence.items():
        if gene_name in allowed_genes:
            filtered_evidence[gene_name] = evidence_text
    annotation["marker_evidence"] = filtered_evidence

    if not filtered_evidence:
        warnings.append("No marker evidence provided.")

    predicted_cell_type = str(annotation.get("predicted_cell_type", "")).strip().lower()
    if predicted_cell_type == "unknown":
        warnings.append("Model could not confidently assign a cell type.")

    # Preserve order while removing duplicates.
    unique_warnings = list(dict.fromkeys(warnings))
    annotation["warning"] = " ".join(unique_warnings)

    return annotation


def calibrate_confidence(annotation: dict, input_genes: list[str]) -> float:
    confidence_value = annotation.get("confidence", 0.0)
    try:
        confidence = float(confidence_value)
    except (TypeError, ValueError):
        confidence = 0.0

    marker_evidence = annotation.get("marker_evidence", {})
    if isinstance(marker_evidence, dict) and len(marker_evidence) >= 4:
        confidence += 0.1

    reasoning = str(annotation.get("reasoning", ""))
    reasoning_lower = reasoning.lower()
    mentioned_markers = 0
    for gene in input_genes:
        gene_clean = gene.strip()
        if gene_clean and gene_clean.lower() in reasoning_lower:
            mentioned_markers += 1
    if mentioned_markers >= 2:
        confidence += 0.1

    warning = str(annotation.get("warning", "")).strip()
    if warning:
        confidence -= 0.1

    alternatives = annotation.get("alternative_cell_types", [])
    if isinstance(alternatives, list) and alternatives:
        confidence -= 0.05

    return max(0.0, min(1.0, confidence))


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

        last_exception: Exception | None = None
        query_text = " ".join(genes)
        try:
            retrieved = retrieve_context_points(query_text, token, limit=5)
        except Exception as exc:
            print(f"Literature retrieval failed for cluster {cluster_id}: {exc}")
            retrieved = []

        literature_texts = [item.get("text", "").strip() for item in retrieved if item.get("text")]
        literature_context = "\n\n".join(literature_texts[:5])
        messages = build_messages(cluster_id, genes, literature_context)

        for attempt in range(1, 4):
            try:
                temperature = 0.1 + (0.1 * attempt)  # 0.2, 0.3, 0.4
                raw_output = call_hf_chat(token, messages, temperature=temperature)
                parsed_output = parse_model_json(raw_output, cluster_id, genes)
                parsed_output = validate_annotation(parsed_output, genes)
                parsed_output["confidence"] = calibrate_confidence(parsed_output, genes)

                if not parsed_output.get("marker_evidence"):
                    raise ValueError("marker_evidence is empty")

                annotations.append(parsed_output)
                last_exception = None
                break
            except (requests.RequestException, ValueError, KeyError, IndexError) as exc:
                last_exception = exc
                if attempt < 3:
                    print(f"Retrying cluster {cluster_id} (attempt {attempt + 1})...")

        if last_exception is not None:
            annotations.append(
                {
                    "cluster": cluster_id,
                    "predicted_cell_type": "unknown",
                    "confidence": 0.0,
                    "reasoning": "Annotation failed for this cluster.",
                    "alternative_cell_types": [],
                    "warning": "Model call or JSON parsing failed; output is a fallback.",
                    "marker_evidence": {},
                    "error": str(last_exception),
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

    print(f"Using model: {MODEL_NAME}")

    clusters = load_clusters(INPUT_PATH)
    annotations = annotate_clusters(clusters, token)
    save_annotations(OUTPUT_PATH, annotations)

    print(f"Saved {len(annotations)} cluster annotations to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
