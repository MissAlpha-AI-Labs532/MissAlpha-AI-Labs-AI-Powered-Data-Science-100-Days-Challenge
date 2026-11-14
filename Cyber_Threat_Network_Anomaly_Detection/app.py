"""Streamlit dashboard for controlled, offline network-flow analysis."""
from pathlib import Path
import json
import joblib
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from src_preprocess import make_features

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "network_traffic_synthetic.csv"
MODEL_PATH = ROOT / "models"
st.set_page_config(page_title="AI Cyber Threat Monitor", page_icon="🛡️", layout="wide")
st.title("🛡️ AI-Based Cyber Threat & Network Anomaly Detection")
st.caption("Offline demonstration using flow-level data. This is not a live packet sniffer or production IDS.")

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

@st.cache_resource
def load_models():
    rf=joblib.load(MODEL_PATH/"random_forest.joblib")
    iso=joblib.load(MODEL_PATH/"isolation_forest.joblib")
    cols=joblib.load(MODEL_PATH/"feature_columns.joblib")
    return rf,iso,cols

try:
    df=load_data()
    rf,iso,feature_cols=load_models()
except Exception as e:
    st.error("Dataset or trained models are missing. Run: python train_model.py")
    st.exception(e)
    st.stop()

X=make_features(df,feature_cols)
df["predicted_threat"]=rf.predict(X).astype(int)
df["threat_probability"]=rf.predict_proba(X)[:,1]
df["anomaly_score"]=iso.decision_function(X)
df["is_anomaly"]=iso.predict(X)==-1
df["security_alert"]=df["predicted_threat"].eq(1) | df["is_anomaly"]

with st.sidebar:
    st.header("Filters")
    protocol=st.multiselect("Protocol",sorted(df.protocol.unique()),default=sorted(df.protocol.unique()))
    threat_filter=st.multiselect("Actual label (demo data)",["Normal","Malicious"],default=["Normal","Malicious"])
    min_prob=st.slider("Minimum threat probability",0.0,1.0,0.0,0.05)
    st.caption("For testing and education only. Do not use synthetic labels as operational ground truth.")

view=df[df.protocol.isin(protocol) & df.label.isin(threat_filter) & (df.threat_probability>=min_prob)].copy()
c1,c2,c3,c4=st.columns(4)
c1.metric("Flows analyzed",f"{len(view):,}")
c2.metric("ML threat predictions",f"{int(view.predicted_threat.sum()):,}")
c3.metric("Anomalies",f"{int(view.is_anomaly.sum()):,}")
c4.metric("Security alerts",f"{int(view.security_alert.sum()):,}")

tab1,tab2,tab3,tab4=st.tabs(["Overview","Alerts & flows","Network graph","Model evaluation"])
with tab1:
    left,right=st.columns(2)
    with left:
        st.subheader("Traffic label distribution")
        st.bar_chart(view.label.value_counts())
    with right:
        st.subheader("Protocol distribution")
        st.bar_chart(view.protocol.value_counts())
    st.subheader("Connection rate vs transferred bytes")
    st.scatter_chart(view,x="connection_rate",y="bytes_transferred",color="label")
    st.info("Anomaly detection uses Isolation Forest; supervised classification uses Random Forest.")
with tab2:
    alerts=view[view.security_alert].sort_values("threat_probability",ascending=False)
    st.subheader(f"Potential security alerts ({len(alerts):,})")
    st.dataframe(alerts[["flow_id","source_ip","destination_ip","destination_port","protocol","login_attempts","failed_logins","connection_rate","predicted_threat","threat_probability","is_anomaly","threat_type"]],use_container_width=True)
    st.download_button("Download filtered alerts CSV",alerts.to_csv(index=False).encode("utf-8"),"security_alerts.csv","text/csv")
with tab3:
    st.subheader("Communication graph")
    limit=st.slider("Maximum flows to plot",50,500,150,50)
    graph_data=view.sort_values("threat_probability",ascending=False).head(limit)
    G=nx.from_pandas_edgelist(graph_data,source="source_ip",target="destination_ip",edge_attr=["threat_probability","security_alert"],create_using=nx.DiGraph())
    if G.number_of_nodes():
        fig,ax=plt.subplots(figsize=(11,7))
        pos=nx.spring_layout(G,seed=42,k=0.5)
        colors=["tomato" if any(graph_data.loc[(graph_data.source_ip==node)|(graph_data.destination_ip==node),"security_alert"]) else "skyblue" for node in G.nodes()]
        nx.draw_networkx(G,pos,ax=ax,node_size=350,node_color=colors,font_size=6,arrows=True,with_labels=True,edge_color="gray",alpha=.8)
        ax.set_title("Red nodes participate in at least one flagged flow")
        ax.axis("off"); st.pyplot(fig)
    else: st.warning("No network edges for selected filters.")
with tab4:
    metrics_path=MODEL_PATH/"metrics.json"
    if metrics_path.exists():
        m=json.loads(metrics_path.read_text())
        a,b,c,d=st.columns(4)
        a.metric("Accuracy",f"{m['accuracy']:.3f}")
        b.metric("Precision",f"{m['precision']:.3f}")
        c.metric("Recall",f"{m['recall']:.3f}")
        d.metric("F1-score",f"{m['f1_score']:.3f}")
        cm=pd.DataFrame(m["confusion_matrix"],index=["Actual Normal","Actual Malicious"],columns=["Predicted Normal","Predicted Malicious"])
        st.subheader("Confusion matrix")
        st.dataframe(cm,use_container_width=True)
        st.caption("Metrics are from a held-out split of this synthetic dataset; performance on real networks will differ.")
    else: st.warning("Run train_model.py to generate evaluation metrics.")
st.divider()
st.caption("Responsible use: analyze only networks and data you own or are explicitly authorized to monitor.")
