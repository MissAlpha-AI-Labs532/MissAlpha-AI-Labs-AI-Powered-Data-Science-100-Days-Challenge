"""Streamlit dashboard for UPI fraud analysis."""
import json
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT/"data"/"processed"/"upi_cleaned.csv"
MODEL = ROOT/"models"/"xgboost_pipeline.joblib"
METRICS = ROOT/"reports"/"model_metrics.json"

st.set_page_config(page_title="UPI Fraud Detection", page_icon="🔐", layout="wide")
st.title("🔐 AI-Based UPI Fraud Detection & Risk Prediction")
st.caption("Decision-support prototype. A high score is an alert for review, not proof of fraud.")

if not DATA.exists():
    st.warning("Cleaned data not found. Run: python src/prepare_data.py")
    st.stop()
df = pd.read_csv(DATA)
if "fraud_flag" not in df:
    st.error("fraud_flag column is required for labelled dataset analysis.")
    st.stop()

st.sidebar.header("Transaction filters")
types = sorted(df["transaction_type"].astype(str).unique()) if "transaction_type" in df else []
selected = st.sidebar.multiselect("Transaction type", types, default=types)
view = df[df["transaction_type"].astype(str).isin(selected)] if types else df.copy()
c1,c2,c3,c4 = st.columns(4)
c1.metric("Transactions", f"{len(view):,}")
c2.metric("Fraud cases", f"{int(view.fraud_flag.sum()):,}")
c3.metric("Fraud rate", f"{view.fraud_flag.mean()*100:.2f}%")
c4.metric("Average amount", f"₹{view.amount_inr.mean():,.2f}")
st.subheader("Transaction insights")
left,right = st.columns(2)
with left:
    st.write("Fraud label distribution")
    st.bar_chart(view["fraud_flag"].value_counts().sort_index())
with right:
    st.write("Average amount by fraud label")
    st.bar_chart(view.groupby("fraud_flag")["amount_inr"].mean())
if "transaction_type" in view:
    st.write("Transactions by payment type and fraud label")
    st.bar_chart(view.groupby(["transaction_type","fraud_flag"]).size().unstack(fill_value=0))
st.subheader("Model evaluation")
if METRICS.exists():
    metrics = json.loads(METRICS.read_text())
    rows=[]
    for model, vals in metrics.items():
        rows.append({"Model":model, **{k:vals.get(k) for k in ["accuracy","precision","recall","f1_score","roc_auc"]}})
    st.dataframe(pd.DataFrame(rows), use_container_width=True)
else:
    st.info("Train models to display evaluation metrics: python src/train_model.py")

st.subheader("Transaction risk scoring")
if MODEL.exists():
    bundle = joblib.load(MODEL)
    features = bundle["features"]
    model, pre = bundle["model"], bundle["preprocessor"]
    sample = view[features].copy()
    sample["fraud_probability"] = model.predict_proba(pre.transform(sample))[:,1]
    # Isolation Forest anomaly score is shown separately where model is available.
    iso_path = ROOT/"models"/"isolation_forest_pipeline.joblib"
    if iso_path.exists():
        ib = joblib.load(iso_path)
        anomaly = (ib["model"].predict(ib["preprocessor"].transform(view[ib["features"]])) == -1).astype(int)
    else:
        anomaly = np.zeros(len(sample), dtype=int)
    sample["anomaly_flag"] = anomaly
    sample["risk_score"] = (100*(0.75*sample["fraud_probability"]+0.25*sample["anomaly_flag"])).clip(0,100).round(1)
    sample["risk_category"] = pd.cut(sample.risk_score, [-1,29,59,79,100],
        labels=["Low","Medium","High","Critical"])
    st.dataframe(sample.sort_values("risk_score",ascending=False).head(500), use_container_width=True)
    st.download_button("Download scored transactions", sample.to_csv(index=False), "upi_risk_scores.csv", "text/csv")
else:
    st.warning("Model files not found. Run the training command first.")

st.caption("Educational prototype only. Do not connect to live payment rails or automatically block payments based solely on this model.")
