#!/usr/bin/env python3
import streamlit as st
import requests


API_URL = "http://localhost:8000/upload-markers"


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

    with st.container(border=True):
        st.subheader("Upload Marker CSV")
        st.write("Expected CSV columns: `cluster`, `gene`, `avg_log2FC`, `p_val_adj`")
        uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is None:
        return

    if st.button("Run Annotation Pipeline"):
        with st.spinner("Running pipeline..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
            try:
                response = requests.post(API_URL, files=files, timeout=300)
                response.raise_for_status()
                result = response.json()
            except requests.RequestException as exc:
                st.error(f"Request failed: {exc}")
                return

        success = bool(result.get("success", False))
        report_markdown = result.get("report_markdown", "")
        evaluation_markdown = result.get("evaluation_markdown", "")
        report_path = result.get("report_path", "reports/annotation_report.md")
        error_message = str(result.get("error_message", "")).strip()
        stderr_text = str(result.get("stderr", "")).strip()

        left_col, right_col = st.columns([1, 1], gap="large")

        with left_col:
            with st.container(border=True):
                if success:
                    st.success("Pipeline completed successfully.")
                else:
                    st.error("Pipeline failed.")
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
                            data=report_markdown,
                            file_name="annotation_report.md",
                            mime="text/markdown",
                        )
                    if evaluation_markdown:
                        st.download_button(
                            label="Download Evaluation Summary",
                            data=evaluation_markdown,
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
                            str(result.get("input_path", "N/A")),
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
            st.info("Report outputs are not shown because the pipeline failed.")


if __name__ == "__main__":
    main()
