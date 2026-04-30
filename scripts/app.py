#!/usr/bin/env python3
import streamlit as st
import requests


API_URL = "http://localhost:8000/upload-markers"
PAPERS_API_URL = "http://localhost:8000/upload-papers"


def main() -> None:
    st.set_page_config(
        page_title="Cell Type Annotation",
        page_icon="🧬",
        layout="wide",
    )

    st.markdown(
        """
        <style>
        .block-container {
            max-width: 1100px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 1rem 1.25rem;
            margin-bottom: 1rem;
        }
        .stButton > button {
            border-radius: 10px;
            padding: 0.5rem 1rem;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("🧬 Cell Type Annotation Assistant")
    st.caption("Upload marker genes and generate AI-assisted cluster annotations.")

    st.sidebar.header("About")
    st.sidebar.write(
        "This app uploads marker-gene CSV data, runs the annotation pipeline, and returns "
        "a structured annotation report generated with AI + literature context."
    )
    st.sidebar.write(f"Backend URL: `{API_URL}`")

    if "has_run" not in st.session_state:
        st.session_state.has_run = False
    if "success" not in st.session_state:
        st.session_state.success = False
    if "annotation_report" not in st.session_state:
        st.session_state.annotation_report = ""
    if "evaluation_summary" not in st.session_state:
        st.session_state.evaluation_summary = ""
    if "run_summary" not in st.session_state:
        st.session_state.run_summary = {}
    if "paper_ingestion" not in st.session_state:
        st.session_state.paper_ingestion = {}

    with st.container(border=True):
        st.subheader("Upload Marker CSV")
        st.write("Expected CSV columns: `cluster`, `gene`, `avg_log2FC`, `p_val_adj`")
        uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
        st.subheader("Upload Research PDFs (optional)")
        uploaded_pdfs = st.file_uploader(
            "Add one or more PDF files",
            type=["pdf"],
            accept_multiple_files=True,
            key="pdf_uploader",
        )
        st.info("PDF upload UI ready; ingestion endpoint coming next.")

    if uploaded_file is None:
        return

    if st.button("Run Annotation Pipeline"):
        with st.spinner("Running pipeline..."):
            st.session_state.paper_ingestion = {}

            if uploaded_pdfs:
                paper_files = [
                    ("files", (pdf.name, pdf.getvalue(), "application/pdf"))
                    for pdf in uploaded_pdfs
                ]
                try:
                    papers_response = requests.post(
                        PAPERS_API_URL, files=paper_files, timeout=600
                    )
                    papers_response.raise_for_status()
                    papers_result = papers_response.json()
                    st.session_state.paper_ingestion = {
                        "success": bool(papers_result.get("success", False)),
                        "message": str(papers_result.get("message", "")),
                        "stderr": str(papers_result.get("stderr", "")),
                        "saved_files": papers_result.get("saved_files", []),
                    }
                except requests.RequestException as exc:
                    st.session_state.paper_ingestion = {
                        "success": False,
                        "message": f"Paper ingestion request failed: {exc}",
                        "stderr": "",
                        "saved_files": [],
                    }

            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
            try:
                response = requests.post(API_URL, files=files, timeout=300)
                response.raise_for_status()
                result = response.json()
            except requests.RequestException as exc:
                st.error(f"Request failed: {exc}")
                return

        report_markdown = result.get("report_markdown", "")
        evaluation_markdown = result.get("evaluation_markdown", "")
        report_path = result.get("report_path", "reports/annotation_report.md")
        success = bool(result.get("success", False))

        st.session_state.has_run = True
        st.session_state.success = success
        st.session_state.run_summary = {
            "success": success,
            "input_path": str(result.get("input_path", "N/A")),
            "report_path": str(report_path),
            "error_message": str(result.get("error_message", "")).strip(),
            "stderr": str(result.get("stderr", "")).strip(),
        }
        if success:
            st.session_state.annotation_report = report_markdown
            st.session_state.evaluation_summary = evaluation_markdown

    if not st.session_state.has_run:
        return

    success = bool(st.session_state.run_summary.get("success", False))
    report_markdown = st.session_state.annotation_report
    evaluation_markdown = st.session_state.evaluation_summary
    report_path = str(st.session_state.run_summary.get("report_path", "reports/annotation_report.md"))
    error_message = str(st.session_state.run_summary.get("error_message", "")).strip()
    stderr_text = str(st.session_state.run_summary.get("stderr", "")).strip()

    left_col, right_col = st.columns([1, 1], gap="large")

    with left_col:
        with st.container(border=True):
            paper_ingestion = st.session_state.paper_ingestion
            if paper_ingestion:
                if paper_ingestion.get("success", False):
                    st.success(
                        paper_ingestion.get("message", "Paper ingestion completed successfully.")
                    )
                else:
                    st.error(
                        paper_ingestion.get("message", "Paper ingestion failed.")
                    )
                saved_files = paper_ingestion.get("saved_files", [])
                if saved_files:
                    st.write("Uploaded PDFs: " + ", ".join(saved_files))

            if success:
                st.success("Pipeline completed successfully.")
            else:
                st.error("Pipeline failed.")
                stderr_lower = stderr_text.lower()
                if "402 client error" in stderr_lower or "payment required" in stderr_lower:
                    st.warning(
                        "Hugging Face quota/payment limit reached. Some clusters could not be annotated."
                    )
                if error_message:
                    st.write(error_message)
                if stderr_text:
                    with st.expander("Error details"):
                        st.code(stderr_text)
            st.write(f"Report path: `{report_path}`")

            if success:
                if report_markdown:
                    st.download_button(
                        label="Download Annotation Report",
                        data=st.session_state.annotation_report,
                        file_name="annotation_report.md",
                        mime="text/markdown",
                    )
                if evaluation_markdown:
                    st.download_button(
                        label="Download Evaluation Summary",
                        data=st.session_state.evaluation_summary,
                        file_name="evaluation_summary.md",
                        mime="text/markdown",
                    )

    with right_col:
        with st.container(border=True):
            st.subheader("Run Summary")
            st.table(
                {
                    "Field": ["success", "input_path", "report_path"],
                    "Value": [
                        str(success),
                        str(st.session_state.run_summary.get("input_path", "N/A")),
                        str(report_path),
                    ],
                }
            )

    st.divider()
    if success:
        tab_report, tab_eval = st.tabs(["Annotation Report", "Evaluation Summary"])
        with tab_report:
            if report_markdown:
                st.markdown(report_markdown)
            else:
                st.info("No annotation report content returned.")
        with tab_eval:
            if evaluation_markdown:
                st.markdown(evaluation_markdown)
            else:
                st.info("No evaluation summary content returned.")
    else:
        if st.session_state.annotation_report or st.session_state.evaluation_summary:
            st.info("Showing outputs from previous successful run.")
            tab_report, tab_eval = st.tabs(["Annotation Report", "Evaluation Summary"])
            with tab_report:
                if st.session_state.annotation_report:
                    st.markdown(st.session_state.annotation_report)
                else:
                    st.info("No annotation report from previous successful run.")
            with tab_eval:
                if st.session_state.evaluation_summary:
                    st.markdown(st.session_state.evaluation_summary)
                else:
                    st.info("No evaluation summary from previous successful run.")
        else:
            st.info("Report outputs are not shown because the pipeline failed.")


if __name__ == "__main__":
    main()
