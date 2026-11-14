"""Streamlit dashboard for traffic exploration and future congestion prediction."""
from pathlib import Path
import json
import joblib
import pandas as pd
import plotly.express as px
import streamlit as st
from src_preprocess import load_data

ROOT = Path(__file__).parent
MODEL_PATH = ROOT / "models" / "traffic_congestion_model.joblib"
METRICS_PATH = ROOT / "models" / "metrics.json"

st.set_page_config(page_title="Smart City Traffic Intelligence", page_icon="🚦", layout="wide")
st.title("🚦 Smart City Traffic Prediction System")
st.caption("Explore traffic patterns and estimate congestion for a selected location and time.")

@st.cache_data
def get_data():
    return load_data()

@st.cache_resource
def get_model():
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)

df = get_data()
model = get_model()

with st.sidebar:
    st.header("Dashboard filters")
    locations = sorted(df["location"].unique())
    selected_locations = st.multiselect("Locations", locations, default=locations)
    date_min, date_max = df["timestamp"].min().date(), df["timestamp"].max().date()
    date_range = st.date_input("Date range", value=(date_min, date_max),
                               min_value=date_min, max_value=date_max)
    levels = st.multiselect("Congestion level", ["Low", "Medium", "High"],
                            default=["Low", "Medium", "High"])

if len(date_range) == 2:
    filtered = df[
        df["location"].isin(selected_locations) &
        (df["timestamp"].dt.date >= date_range[0]) &
        (df["timestamp"].dt.date <= date_range[1]) &
        df["congestion_level"].isin(levels)
    ]
else:
    filtered = df[df["location"].isin(selected_locations) & df["congestion_level"].isin(levels)]

if filtered.empty:
    st.warning("No records match these filters. Select a wider date range or more locations.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Traffic records", f"{len(filtered):,}")
c2.metric("Average vehicles", f"{filtered['vehicle_count'].mean():.0f}")
c3.metric("High congestion records", f"{(filtered['congestion_level']=='High').sum():,}")
c4.metric("Locations covered", filtered["location"].nunique())

st.subheader("Traffic pattern exploration")
left, right = st.columns(2)
hourly = filtered.groupby("hour", as_index=False)["vehicle_count"].mean()
left.plotly_chart(px.line(hourly, x="hour", y="vehicle_count", markers=True,
                          title="Average vehicle count by hour",
                          labels={"hour":"Hour of day","vehicle_count":"Average vehicles"}),
                  use_container_width=True)
by_location = filtered.groupby("location", as_index=False)["vehicle_count"].mean().sort_values("vehicle_count", ascending=False)
right.plotly_chart(px.bar(by_location, x="location", y="vehicle_count",
                          title="Average traffic by location",
                          labels={"location":"Location","vehicle_count":"Average vehicles"}),
                  use_container_width=True)

st.subheader("Congestion distribution and time patterns")
left, right = st.columns(2)
dist = filtered["congestion_level"].value_counts().reindex(["Low","Medium","High"], fill_value=0).rename_axis("level").reset_index(name="records")
left.plotly_chart(px.pie(dist, names="level", values="records", title="Congestion level distribution",
                         hole=0.35), use_container_width=True)
heat = filtered.pivot_table(index="location", columns="hour", values="vehicle_count", aggfunc="mean")
right.plotly_chart(px.imshow(heat, aspect="auto", color_continuous_scale="YlOrRd",
                             labels=dict(x="Hour", y="Location", color="Avg vehicles"),
                             title="Location vs hour traffic heatmap"),
                  use_container_width=True)

st.subheader("Peak traffic insights")
peak_hour = int(hourly.loc[hourly["vehicle_count"].idxmax(), "hour"])
busiest_location = str(by_location.iloc[0]["location"])
st.write(f"- **Busiest hour in the selected data:** {peak_hour:02d}:00.")
st.write(f"- **Highest average traffic location:** {busiest_location}.")
high_share = (filtered["congestion_level"].eq("High").mean() * 100)
st.write(f"- **High congestion share:** {high_share:.1f}% of filtered records.")

st.divider()
st.subheader("Predict congestion for a selected future scenario")
st.write("Choose the expected conditions. The model predicts a congestion category without requiring a future vehicle count.")
if model is None:
    st.error("Model file not found. Run `python train_model.py` first.")
else:
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        pred_location = st.selectbox("Location", sorted(df["location"].unique()), key="pred_loc")
        pred_hour = st.slider("Hour", 0, 23, 8)
    with p2:
        pred_day = st.selectbox("Day of week", ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
        pred_month = st.selectbox("Month", list(range(1,13)), index=10)
    with p3:
        pred_weather = st.selectbox("Weather", ["Clear","Cloudy","Rain","Heavy Rain"])
        pred_event = st.selectbox("Special event?", ["No","Yes"])
    with p4:
        pred_capacity = int(df.loc[df["location"] == pred_location, "road_capacity"].median())
        st.metric("Road capacity (reference)", pred_capacity)
    day_num = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"].index(pred_day)
    scenario = pd.DataFrame([{
        "hour": pred_hour, "day_of_week": day_num, "month": pred_month,
        "is_weekend": int(day_num >= 5), "location": pred_location,
        "weather": pred_weather, "road_capacity": pred_capacity,
        "special_event": int(pred_event == "Yes")
    }])
    if st.button("Predict congestion", type="primary"):
        prediction = model.predict(scenario)[0]
        probabilities = model.predict_proba(scenario)[0]
        classes = model.classes_
        confidence = float(probabilities[list(classes).index(prediction)]) * 100
        st.success(f"Predicted congestion: **{prediction}**")
        st.metric("Model confidence for predicted class", f"{confidence:.1f}%")
        prob_df = pd.DataFrame({"Congestion": classes, "Probability": probabilities})
        st.plotly_chart(px.bar(prob_df, x="Congestion", y="Probability",
                               title="Prediction probabilities", range_y=[0,1]),
                        use_container_width=True)

with st.expander("Model evaluation"):
    if METRICS_PATH.exists():
        metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
        st.metric("Hold-out test accuracy", f"{metrics['accuracy']*100:.1f}%")
        st.caption(metrics.get("note", ""))
        report = pd.DataFrame(metrics["classification_report"]).T
        st.dataframe(report, use_container_width=True)
        st.write("Confusion matrix (rows = actual; columns = predicted; order Low, Medium, High):")
        st.dataframe(pd.DataFrame(metrics["confusion_matrix"],
                                  index=metrics["labels"], columns=metrics["labels"]))
    else:
        st.info("Run train_model.py to generate evaluation metrics.")

with st.expander("Filtered data preview"):
    st.dataframe(filtered[["timestamp","location","vehicle_count","road_capacity","weather","special_event","congestion_level"]],
                 use_container_width=True)
    st.download_button("Download filtered CSV", filtered.to_csv(index=False).encode("utf-8"),
                       file_name="filtered_traffic_data.csv", mime="text/csv")
