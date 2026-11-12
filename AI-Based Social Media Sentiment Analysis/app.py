from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "reports" / "sentiment_report.csv"

st.set_page_config(page_title="AI Social Media Sentiment Analysis", page_icon="📊", layout="wide")
st.title("AI-Based Social Media Sentiment Analysis")
st.caption("Customer feedback, sentiment trends, keyword and brand perception dashboard")
st.info("Dataset notice: the included 500 reviews are synthetic demonstration data, not real customer feedback.")

if not DATA_FILE.exists():
    st.warning("Sentiment report not found. Run `python sentiment_analyzer.py` in the project terminal, then refresh this page.")
    st.stop()

@st.cache_data
def load_data(path, modified):
    return pd.read_csv(path)

df = load_data(str(DATA_FILE), DATA_FILE.stat().st_mtime)
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["sentiment_score"] = pd.to_numeric(df["sentiment_score"], errors="coerce")

st.sidebar.header("Dashboard Filters")
platforms = sorted(df["platform"].dropna().unique().tolist())
chosen_platforms = st.sidebar.multiselect("Platform", platforms, default=platforms)
sentiments = ["Positive", "Negative", "Neutral"]
chosen_sentiments = st.sidebar.multiselect("Sentiment", sentiments, default=sentiments)

min_date = df["date"].min().date()
max_date = df["date"].max().date()
date_range = st.sidebar.date_input("Date range", value=(min_date, max_date),
                                   min_value=min_date, max_value=max_date)

filtered = df[df["platform"].isin(chosen_platforms) &
              df["sentiment"].isin(chosen_sentiments)].copy()
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    filtered = filtered[filtered["date"].dt.date.between(date_range[0], date_range[1])]
elif isinstance(date_range, (tuple, list)) and len(date_range) == 1:
    filtered = filtered[filtered["date"].dt.date == date_range[0]]

total = len(filtered)
if total == 0:
    st.warning("No reviews match the selected filters. Change the filters to see results.")
    st.stop()

counts = filtered["sentiment"].value_counts()
positive = int(counts.get("Positive", 0))
negative = int(counts.get("Negative", 0))
neutral = int(counts.get("Neutral", 0))

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total reviews", total)
k2.metric("Positive", f"{positive / total * 100:.1f}%")
k3.metric("Negative", f"{negative / total * 100:.1f}%")
k4.metric("Neutral", f"{neutral / total * 100:.1f}%")
k5.metric("Average rating", f"{filtered['rating'].mean():.2f}/5")

left, right = st.columns(2)
with left:
    st.subheader("Sentiment distribution")
    dist = counts.reindex(sentiments, fill_value=0).rename_axis("Sentiment").reset_index(name="Reviews")
    st.plotly_chart(px.pie(dist, names="Sentiment", values="Reviews", hole=0.4), use_container_width=True)
with right:
    st.subheader("Platform-wise sentiment")
    platform_data = filtered.groupby(["platform", "sentiment"]).size().reset_index(name="Reviews")
    st.plotly_chart(px.bar(platform_data, x="platform", y="Reviews", color="sentiment", barmode="group"),
                    use_container_width=True)

st.subheader("Sentiment trend over time")
daily = (filtered.dropna(subset=["date"])
         .groupby([filtered["date"].dt.date, "sentiment"]).size()
         .reset_index(name="Reviews"))
daily.columns = ["Date", "Sentiment", "Reviews"]
st.plotly_chart(px.line(daily, x="Date", y="Reviews", color="Sentiment", markers=True),
                use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Top keywords")
    from topic_analyzer import extract_keywords
    from collections import Counter
    words = Counter(word for review in filtered["customer_review"] for word in extract_keywords(review))
    keyword_df = pd.DataFrame(words.most_common(15), columns=["Keyword", "Count"])
    if not keyword_df.empty:
        st.plotly_chart(px.bar(keyword_df.sort_values("Count"), x="Count", y="Keyword", orientation="h"),
                        use_container_width=True)
    else:
        st.caption("No keywords found.")
with right:
    st.subheader("Trending topics")
    if "topic" in filtered.columns:
        topic_df = filtered.groupby(["topic", "sentiment"]).size().reset_index(name="Reviews")
        st.plotly_chart(px.bar(topic_df, x="topic", y="Reviews", color="sentiment", barmode="group"),
                        use_container_width=True)

st.subheader("Brand perception")
brand_score = filtered["sentiment_score"].mean() * 100
st.metric("Average compound sentiment score", f"{brand_score:.2f} / 100")
st.caption("Model-derived indicator; it is not a definitive measure of brand reputation.")

st.subheader("Customer feedback")
columns = ["date", "platform", "customer_review", "rating", "sentiment", "sentiment_score"]
st.dataframe(filtered[columns].sort_values("date", ascending=False), use_container_width=True, hide_index=True)
st.download_button("Download filtered reviews", filtered.to_csv(index=False).encode("utf-8"),
                   "filtered_sentiment_reviews.csv", "text/csv")
