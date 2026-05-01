import json
import os
from pathlib import Path
import re

import requests
from retrieve_context import filter_retrieved_chunks, retrieve_context_points

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
        "Marker genes are the primary evidence.\n"
        "You MUST base your prediction ONLY on the provided marker genes.\n"
        "Literature context is supporting background only, not the main decision signal.\n"
        "Be conservative: literature supports reasoning, but final cell-type decisions must be driven by marker genes.\n"
        "Never let literature_context override the marker genes provided for the cluster.\n"
        "Do NOT infer cell types based on general biological knowledge if marker genes do not support it.\n"
        "Do NOT default to common immune cell types unless markers strongly support them.\n"
        "If markers do not clearly support a known immune cell type, return a more general label such as "
        "'proliferating cells', 'epithelial cells', or 'endothelial cells'.\n"
        "If uncertain, return 'unknown' instead of guessing.\n"
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
        "- if markers include MS4A1 and CD79A, strongly prefer B cell\n"
        "- if markers include NKG7, GNLY, PRF1, CTSW, and TRAC, prefer cytotoxic T cell with NK cell as alternative\n"
        "- do not overcall neutrophils unless markers include FCGR3B, CSF3R, CXCR2, S100A8, S100A9, LCN2, or MPO\n"
        "- if markers include LYZ, FCN1, CTSS, S100A8, and S100A9, prefer classical monocyte over neutrophil unless strong neutrophil markers are present\n"
        "- do NOT call neutrophil unless strong neutrophil markers are present, such as FCGR3B, CSF3R, CXCR2, LCN2, MPO, ELANE, AZU1, or S100A12\n"
        "- NKG7, GNLY, PRF1, CTSW, and TRAC are NOT neutrophil markers\n"
        "- MS4A1 and CD79A are NOT monocyte markers\n"
        "- confidence should be a number between 0 and 1\n"
        "- alternative_cell_types should be a JSON array of strings\n"
        "- warning should be a short string about uncertainty or caution (or empty string if none)\n"
        "- marker_evidence should be a JSON object with keys that are marker genes and values that briefly explain support/conflict\n"
        "- marker_evidence must only include genes from the input marker list for this cluster\n"
        "- the reasoning must ONLY mention marker genes provided for the current cluster\n"
        "- never mention genes from other clusters\n"
        "- if you mention a gene not in the input marker list, the output is invalid\n"
        "- You MUST base your prediction ONLY on the provided marker genes\n"
        "- Do NOT default to common immune cell types unless markers strongly support them\n"
        "- Do NOT infer cell types from general biological knowledge when input markers do not support it\n"
        "- If markers do not clearly support a known immune cell type, use a general label such as "
        "'proliferating cells', 'epithelial cells', or 'endothelial cells'\n"
        "- If uncertain, return 'unknown' instead of guessing\n"
        "- Examples:\n"
        "  Markers: PPBP, PF4, GP9 -> platelet\n"
        "  Markers: MKI67, TOP2A -> proliferating cells\n"
        "  Markers: EPCAM, KRT8 -> epithelial cells\n"
        "  Markers: PECAM1, VWF -> endothelial cells\n"
        "- Return ONLY valid JSON. No extra text. No explanation outside JSON.\n"
        "- Do not wrap JSON in markdown.\n"
        "- Do not include explanatory text before or after JSON.\n"
        "- Use double quotes for all JSON keys and string values.\n"
        "- Do not use trailing commas.\n"
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
        "max_tokens": 700,
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
    cleaned_text = raw_text.strip()
    if cleaned_text.startswith("```"):
        cleaned_text = re.sub(r"^```(?:json)?\s*", "", cleaned_text, flags=re.IGNORECASE)
        cleaned_text = re.sub(r"\s*```$", "", cleaned_text)

    try:
        parsed = json.loads(cleaned_text)
    except json.JSONDecodeError:
        # Strict recovery for cases where model adds extra text around JSON.
        start = cleaned_text.find("{")
        end = cleaned_text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("Model response is not valid JSON")
        json_block = cleaned_text[start : end + 1]
        try:
            parsed = json.loads(json_block)
        except json.JSONDecodeError as exc:
            raise ValueError("Model response is not valid JSON") from exc

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
    rule_applied = False
    original_predicted = str(annotation.get("predicted_cell_type", "")).strip()
    original_predicted_lower = original_predicted.lower()
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

    reasoning = str(annotation.get("reasoning", ""))
    allowed_genes_upper = {gene.strip().upper() for gene in input_genes if gene.strip()}
    ignored_tokens = {"RNA", "SCRNA", "PBMC", "DNA", "JSON", "LLM"}
    gene_like_tokens = set(re.findall(r"\b[A-Z0-9-]{3,15}\b", reasoning))
    external_reasoning_genes = []
    for token in gene_like_tokens:
        if token in ignored_tokens:
            continue
        if token not in allowed_genes_upper:
            external_reasoning_genes.append(token)
    if external_reasoning_genes:
        warnings.append("Reasoning contains genes not in input.")
        warnings.append("Reasoning references canonical markers not present in input.")

    input_gene_set = {gene.strip().upper() for gene in input_genes if gene.strip()}

    def current_confidence() -> float:
        try:
            return float(annotation.get("confidence", 0.0))
        except (TypeError, ValueError):
            return 0.0

    def set_min_confidence(min_value: float) -> None:
        annotation["confidence"] = max(current_confidence(), min_value)

    if len(external_reasoning_genes) >= 3:
        annotation["confidence"] = min(current_confidence(), 0.5)

    # Hard rule: B cell
    if {"MS4A1", "CD79A"}.issubset(input_gene_set):
        annotation["predicted_cell_type"] = "B cell"
        set_min_confidence(0.90)
        rule_applied = True

    # Hard rule: cytotoxic T cell signature
    cytotoxic_t_markers = {"NKG7", "GNLY", "PRF1", "CTSW", "TRAC"}
    if cytotoxic_t_markers.issubset(input_gene_set):
        annotation["predicted_cell_type"] = "cytotoxic T cell"
        set_min_confidence(0.85)
        annotation["alternative_cell_types"] = ["NK cell"]
        rule_applied = True

    # Hard rule: classical monocyte when canonical monocyte markers are present,
    # unless strong neutrophil markers are also present in the input list.
    monocyte_signature = {"LYZ", "FCN1", "CTSS", "S100A8", "S100A9"}
    strong_neutrophil_markers = {
        "FCGR3B",
        "CSF3R",
        "CXCR2",
        "LCN2",
        "MPO",
        "ELANE",
        "AZU1",
        "S100A12",
    }
    has_monocyte_signature = monocyte_signature.issubset(input_gene_set)
    has_strong_neutrophil_markers = bool(input_gene_set & strong_neutrophil_markers)
    if has_monocyte_signature and not has_strong_neutrophil_markers:
        annotation["predicted_cell_type"] = "classical monocyte"
        set_min_confidence(0.85)
        rule_applied = True

    platelet_markers = {"PPBP", "PF4", "GP9", "ITGA2B", "NRGN"}
    if input_gene_set & platelet_markers:
        annotation["predicted_cell_type"] = "platelet"
        set_min_confidence(0.90)
        rule_applied = True
        existing_warning_text = str(annotation.get("warning", ""))
        warning_lower = existing_warning_text.lower()
        if "b cell" in warning_lower or "t cell" in warning_lower:
            annotation["warning"] = ""
        warnings.append("Strong platelet markers detected.")

    proliferating_markers = {"MKI67", "TOP2A", "STMN1", "PCNA", "TYMS"}
    if len(input_gene_set & proliferating_markers) >= 3:
        annotation["predicted_cell_type"] = "proliferating cells"
        set_min_confidence(0.85)
        rule_applied = True
        annotation["alternative_cell_types"] = []
        annotation["warning"] = (
            "Cell cycle markers indicate proliferation; parent lineage may require additional markers."
        )

    epithelial_markers = {"EPCAM", "KRT8", "KRT18", "KRT19", "CLDN4"}
    if len(input_gene_set & epithelial_markers) >= 2:
        annotation["predicted_cell_type"] = "epithelial cell"
        set_min_confidence(0.90)
        rule_applied = True
        annotation["alternative_cell_types"] = []

    endothelial_markers = {"PECAM1", "VWF", "KDR", "ENG", "CDH5"}
    if len(input_gene_set & endothelial_markers) >= 2:
        annotation["predicted_cell_type"] = "endothelial cell"
        set_min_confidence(0.90)
        rule_applied = True
        annotation["alternative_cell_types"] = []

    smooth_muscle_markers = {"ACTA2", "TAGLN", "MYH11", "CNN1", "DES"}
    if len(input_gene_set & smooth_muscle_markers) >= 3:
        annotation["predicted_cell_type"] = "smooth muscle cell"
        set_min_confidence(0.90)
        rule_applied = True
        annotation["alternative_cell_types"] = ["pericyte"]

    t_cell_core = {"CD3D", "CD3E"}
    t_cell_support = {"IL7R", "CCR7", "LTB"}
    cytotoxic_markers = {"NKG7", "GNLY", "PRF1"}
    has_t_cell_core = t_cell_core.issubset(input_gene_set)
    has_t_cell_support = bool(input_gene_set & t_cell_support)
    has_cytotoxic_signature = bool(input_gene_set & cytotoxic_markers)
    if has_t_cell_core and has_t_cell_support and not has_cytotoxic_signature:
        annotation["predicted_cell_type"] = "naive/central memory T cell"
        set_min_confidence(0.85)
        rule_applied = True
        annotation["alternative_cell_types"] = ["CD4 T cell"]

    nonclassical_monocyte_markers = {"FCGR3A", "MS4A7", "LST1", "AIF1", "TYROBP"}
    if nonclassical_monocyte_markers.issubset(input_gene_set):
        annotation["predicted_cell_type"] = "non-classical monocyte"
        set_min_confidence(0.85)
        rule_applied = True
        annotation["alternative_cell_types"] = ["NK cell"]

    exhausted_t_markers = {"PDCD1", "LAG3", "TOX", "HAVCR2", "CXCL13"}
    if len(input_gene_set & exhausted_t_markers) >= 3:
        annotation["predicted_cell_type"] = "exhausted T cell"
        set_min_confidence(0.85)
        rule_applied = True
        annotation["alternative_cell_types"] = ["T follicular helper cell"]

    predicted_cell_type = str(annotation.get("predicted_cell_type", "")).strip().lower()
    if predicted_cell_type == "unknown":
        warnings.append("Model could not confidently assign a cell type.")

    updated_warning = annotation.get("warning", "")
    if isinstance(updated_warning, str) and updated_warning.strip():
        warnings.append(updated_warning.strip())

    final_confidence_value = annotation.get("confidence", 0.0)
    try:
        final_confidence = float(final_confidence_value)
    except (TypeError, ValueError):
        final_confidence = 0.0

    current_predicted = str(annotation.get("predicted_cell_type", "")).strip()
    current_predicted_lower = current_predicted.lower()
    known_immune_terms = ("t cell", "b cell", "monocyte")
    original_is_known_immune = any(term in original_predicted_lower for term in known_immune_terms)
    if (
        original_is_known_immune
        and current_predicted_lower == "unknown"
        and final_confidence >= 0.3
    ):
        annotation["predicted_cell_type"] = original_predicted

    if final_confidence >= 0.8:
        warnings = [w for w in warnings if "low confidence" not in w.lower()]

    if predicted_cell_type != "unknown":
        warnings = [
            w
            for w in warnings
            if "model could not confidently assign a cell type" not in w.lower()
        ]

    if rule_applied:
        filtered_warnings = []
        for warning_text in warnings:
            warning_lower = warning_text.lower()
            if "no clear markers" in warning_lower:
                continue
            if "low confidence prediction" in warning_lower:
                continue
            if "model could not confidently assign a cell type" in warning_lower:
                continue
            if "insufficient marker evidence" in warning_lower:
                continue
            filtered_warnings.append(warning_text)
        warnings = filtered_warnings

    # Preserve order while removing duplicates.
    normalized_warnings = []
    for w in warnings:
        clean = " ".join(str(w).split()).strip()
        if clean:
            normalized_warnings.append(clean)
    unique_warnings = list(dict.fromkeys(normalized_warnings))
    annotation["warning"] = " ".join(unique_warnings) if unique_warnings else ""

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
    warning_lower = warning.lower()
    if warning:
        confidence -= 0.1

    alternatives = annotation.get("alternative_cell_types", [])
    if isinstance(alternatives, list) and alternatives:
        confidence -= 0.05

    confidence = min(confidence, 0.95)

    if isinstance(alternatives, list) and alternatives:
        confidence = min(confidence, 0.90)

    if warning:
        confidence = min(confidence, 0.85)

    if "reasoning contains genes not in input." in warning_lower:
        confidence = min(confidence, 0.5)

    if not isinstance(marker_evidence, dict) or len(marker_evidence) < 3:
        confidence = min(confidence, 0.75)

    return max(0.0, confidence)


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
                    "literature_sources": [],
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

        filtered_retrieved = filter_retrieved_chunks(retrieved)
        literature_sources = []
        for item in filtered_retrieved[:5]:
            source_pdf = str(item.get("source_pdf", "unknown"))
            score_raw = item.get("score", 0.0)
            try:
                score = float(score_raw)
            except (TypeError, ValueError):
                score = 0.0
            snippet = str(item.get("text", "")).strip()[:300]
            literature_sources.append(
                {
                    "source_pdf": source_pdf,
                    "score": score,
                    "text": snippet,
                }
            )
        literature_texts = [
            item.get("text", "").strip() for item in filtered_retrieved if item.get("text")
        ]
        literature_context = "\n\n".join(literature_texts[:3])
        messages = build_messages(cluster_id, genes, literature_context)

        for attempt in range(1, 4):
            raw_output = ""
            try:
                temperature = 0.1 + (0.1 * attempt)  # 0.2, 0.3, 0.4
                raw_output = call_hf_chat(token, messages, temperature=temperature)
                parsed_output = parse_model_json(raw_output, cluster_id, genes)
                parsed_output = validate_annotation(parsed_output, genes)
                parsed_output["confidence"] = calibrate_confidence(parsed_output, genes)
                parsed_output["literature_sources"] = literature_sources

                if not parsed_output.get("marker_evidence"):
                    raise ValueError("marker_evidence is empty")

                annotations.append(parsed_output)
                last_exception = None
                break
            except (requests.RequestException, ValueError, KeyError, IndexError) as exc:
                last_exception = exc
                print(
                    f"Cluster {cluster_id} attempt {attempt} failed: "
                    f"{type(exc).__name__}: {exc}"
                )
                if raw_output:
                    print(raw_output[:1000])
                if attempt < 3:
                    if isinstance(exc, ValueError) and "JSON" in str(exc).upper():
                        print(
                            f"Invalid JSON response for cluster {cluster_id} on attempt {attempt}"
                        )
                        print((raw_output or "<no response>")[:500])
                    print(f"Retrying cluster {cluster_id} (attempt {attempt + 1})...")

        if last_exception is not None:
            annotations.append(
                {
                    "cluster": cluster_id,
                    "predicted_cell_type": "unknown",
                    "confidence": 0.0,
                    "reasoning": "Annotation failed for this cluster.",
                    "alternative_cell_types": [],
                    "warning": (
                        "LLM annotation failed after retries: "
                        f"{str(last_exception)}"
                    ),
                    "marker_evidence": {},
                    "literature_sources": literature_sources,
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
