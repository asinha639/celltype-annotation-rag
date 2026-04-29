#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


def read_report_markdown(project_root: Path) -> str:
    report_path = project_root / "reports" / "annotation_report.md"
    if not report_path.exists():
        return ""
    return report_path.read_text(encoding="utf-8")


@app.post("/run-pipeline")
def run_pipeline() -> dict:
    project_root = Path(__file__).resolve().parent.parent

    result = subprocess.run(
        [sys.executable, "scripts/run_pipeline.py"],
        cwd=project_root,
        capture_output=True,
        text=True,
    )

    success = result.returncode == 0
    report_markdown = read_report_markdown(project_root)
    return {
        "success": success,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "report_path": "reports/annotation_report.md",
        "report_markdown": report_markdown,
    }


@app.post("/upload-markers")
async def upload_markers(file: UploadFile = File(...)) -> dict:
    project_root = Path(__file__).resolve().parent.parent
    data_dir = project_root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    input_path = data_dir / "uploaded_markers.csv"
    file_bytes = await file.read()
    input_path.write_bytes(file_bytes)

    result = subprocess.run(
        [sys.executable, "scripts/run_pipeline.py", "--input", "data/uploaded_markers.csv"],
        cwd=project_root,
        capture_output=True,
        text=True,
    )

    success = result.returncode == 0
    report_markdown = read_report_markdown(project_root)
    return {
        "success": success,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "input_path": "data/uploaded_markers.csv",
        "report_path": "reports/annotation_report.md",
        "report_markdown": report_markdown,
    }
