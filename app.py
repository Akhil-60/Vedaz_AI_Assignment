import subprocess
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Vedaz AI Dashboard",
    page_icon="🔮",
    layout="wide"
)

st.title("🔮 Vedaz AI Dashboard")
st.write("AI Astrologer Dataset Toolkit")

st.divider()

col1, col2, col3 = st.columns(3)

# ====================================================
# Checker
# ====================================================

with col1:

    st.subheader("📁 Chat Checker")

    if st.button("Run Checker"):

        with st.spinner("Running Checker..."):

            result = subprocess.run(
                ["python", "scripts/checker.py"],
                capture_output=True,
                text=True
            )

        st.success("Checker Completed")

        st.text(result.stdout)

# ====================================================
# Generator
# ====================================================

with col2:

    st.subheader("🤖 Chat Generator")

    if st.button("Generate Chats"):

        with st.spinner("Generating Chats..."):

            result = subprocess.run(
                ["python", "scripts/generator.py"],
                capture_output=True,
                text=True
            )

        st.success("Generation Completed")

        st.text(result.stdout)

# ====================================================
# Evaluator
# ====================================================

with col3:

    st.subheader("📊 Evaluator")

    if st.button("Run Evaluation"):

        with st.spinner("Evaluating..."):

            result = subprocess.run(
                ["python", "scripts/evaluator.py"],
                capture_output=True,
                text=True
            )

        st.success("Evaluation Completed")

        st.text(result.stdout)

st.divider()

st.header("📂 Generated Files")

# ====================================================
# Report
# ====================================================

report = Path("outputs/report.txt")

if report.exists():

    st.subheader("Checker Report")

    st.code(report.read_text(encoding="utf-8"))

# ====================================================
# CSV
# ====================================================

csv_file = Path("outputs/evaluation.csv")

if csv_file.exists():

    st.subheader("Evaluation Results")

    df = pd.read_csv(csv_file)

    st.dataframe(df, width="stretch")

st.divider()

st.success("Vedaz Assignment Dashboard Ready ✅")