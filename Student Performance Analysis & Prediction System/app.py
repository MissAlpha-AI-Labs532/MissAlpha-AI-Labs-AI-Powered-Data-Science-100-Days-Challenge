from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "student_data.csv"
OUT = ROOT / "outputs"
st.set_page_config(page_title="Student Performance Analytics", page_icon="📊", layout="wide")
st.title("📊 Student Performance Analysis & Prediction")
st.caption("MissAlpha™ AI Labs | Student Support & Data Analytics Project")

@st.cache_data
def load_data():
    try:
        d = pd.read_csv(DATA)
        if d.shape[1] == 1:
            d = pd.read_csv(DATA, sep=";")
    except Exception:
        d = pd.read_csv(DATA, sep=";")
    return d

df = load_data()
target = "G3" if "G3" in df.columns else df.columns[-1]
a, b, c, d = st.columns(4)
a.metric("Student records", f"{len(df):,}")
b.metric("Dataset columns", len(df.columns))
c.metric("Missing cells", int(df.isna().sum().sum()))
d.metric("Duplicate rows", int(df.duplicated().sum()))

tab1, tab2, tab3, tab4 = st.tabs(["Dataset", "Exploration", "Model results", "Try a prediction"])
with tab1:
    st.subheader("Dataset preview")
    st.dataframe(df.head(20), use_container_width=True)
    st.subheader("Column types")
    st.dataframe(df.dtypes.astype(str).rename("Data type"), use_container_width=True)
    st.subheader("Missing values")
    st.dataframe(df.isna().sum().rename("Missing values"), use_container_width=True)

with tab2:
    st.subheader("Descriptive statistics")
    st.dataframe(df.describe(include="all").transpose(), use_container_width=True)
    numeric = df.select_dtypes(include=np.number)
    if target in numeric.columns:
        st.subheader(f"{target} distribution")
        st.bar_chart(numeric[target].value_counts().sort_index())
    if "studytime" in df.columns and target in df.columns:
        st.subheader("Average final grade by study-time category")
        st.bar_chart(df.groupby("studytime")[target].mean())
    if "absences" in df.columns and target in df.columns:
        st.subheader("Absences and final grade")
        st.scatter_chart(df, x="absences", y=target)

with tab3:
    result_file = OUT / "model_comparison.csv"
    if result_file.exists():
        st.subheader("Held-out test-set comparison")
        st.dataframe(pd.read_csv(result_file), use_container_width=True)
        st.caption("MAE and RMSE are error measures (lower is better); R² is goodness of fit. Results vary with the dataset and split.")
    else:
        st.info("Run `python analysis.py` in the project terminal to train models and generate evaluation results.")

with tab4:
    model_file = OUT / "student_performance_model.joblib"
    if not model_file.exists():
        st.info("Train the model first: run `python analysis.py` in the project terminal.")
    else:
        bundle = joblib.load(model_file)
        pipe, features = bundle["pipeline"], bundle["features"]
        st.write(f"Selected model: **{bundle['model_name']}**")
        st.caption("Enter values for the available non-grade features. Categorical fields use text values from the dataset.")
        row = {}
        cols = st.columns(2)
        for i, feature in enumerate(features):
            series = df[feature]
            with cols[i % 2]:
                if pd.api.types.is_numeric_dtype(series):
                    default = float(series.median()) if series.notna().any() else 0.0
                    row[feature] = st.number_input(feature, value=default)
                else:
                    options = sorted(series.dropna().astype(str).unique().tolist())
                    row[feature] = st.selectbox(feature, options) if options else ""
        if st.button("Predict estimated final grade", type="primary"):
            input_df = pd.DataFrame([row], columns=features)
            prediction = float(pipe.predict(input_df)[0])
            st.success(f"Estimated {target}: {prediction:.2f}")
            st.warning("This is an educational model estimate, not a definitive judgement about a student.")
