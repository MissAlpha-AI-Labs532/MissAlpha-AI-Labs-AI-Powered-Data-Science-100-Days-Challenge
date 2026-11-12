from pathlib import Path
from collections import Counter
import re
import pandas as pd

ROOT = Path(__file__).resolve().parent
REPORT_DIR = ROOT / "reports"
STOPWORDS = {
    "the","and","for","with","this","that","was","are","is","it","my","to","of",
    "in","on","a","an","i","have","has","had","but","so","very","not","your",
    "me","we","they","their","our","be","been","from","after","than","as","at",
    "too","does","do","did","will","would","can","could","should","just","yet"
}

def extract_keywords(text):
    words = re.findall(r"\b[a-z]{3,}\b", str(text).lower())
    return [w for w in words if w not in STOPWORDS]

def analyze_topics(input_file=None):
    input_file = Path(input_file) if input_file else REPORT_DIR / "sentiment_report.csv"
    if not input_file.exists():
        from sentiment_analyzer import run_analysis
        run_analysis()
    df = pd.read_csv(input_file)
    if "cleaned_review" not in df.columns:
        from data_processor import clean_text
        df["cleaned_review"] = df["customer_review"].map(clean_text)
    df["keywords"] = df["cleaned_review"].fillna("").map(extract_keywords)
    groups = [
        ("All", df),
        ("Positive", df[df["sentiment"] == "Positive"]),
        ("Negative", df[df["sentiment"] == "Negative"])
    ]
    print("TOP KEYWORDS")
    for label, subset in groups:
        counts = Counter(word for row in subset["keywords"] for word in row)
        print(f"\n{label}: {counts.most_common(12)}")
    if "topic" in df.columns:
        print("\nTOPIC COUNTS BY SENTIMENT")
        print(pd.crosstab(df["topic"], df["sentiment"]).to_string())
    return df

if __name__ == "__main__":
    analyze_topics()
