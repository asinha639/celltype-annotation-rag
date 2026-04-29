#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

from fastapi import FastAPI

app = FastAPI()


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
    return {
        "success": success,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "report_path": "reports/annotation_report.md",
    }
