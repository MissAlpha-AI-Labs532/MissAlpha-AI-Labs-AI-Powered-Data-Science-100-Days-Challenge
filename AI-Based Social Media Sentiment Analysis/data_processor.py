from pathlib import Path
import re
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"

def clean_text(value):
    if pd.isna(value):
        return ""
    text = str(value).lower()
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"@[A-Za-z0-9_]+", " ", text)
    text = re.sub(r"#[A-Za-z0-9_]+", " ", text)
    text = re.sub(r"[^a-z0-9\s']", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def process_data(input_file=None, output_file=None):
    input_file = Path(input_file) if input_file else DATA_DIR / "customer_reviews.csv"
    output_file = Path(output_file) if output_file else DATA_DIR / "customer_reviews.csv"
    if not input_file.exists():
        raise FileNotFoundError(f"Dataset not found: {input_file}")
    df = pd.read_csv(input_file)
    required = {"review_id", "date", "platform", "rating", "customer_review"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")
    df = df.drop_duplicates(subset=["review_id"], keep="first").copy()
    df["customer_review"] = df["customer_review"].fillna("").astype(str)
    df["cleaned_review"] = df["customer_review"].map(clean_text)
    df = df[df["cleaned_review"].ne("")].copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df = df.dropna(subset=["date", "rating"])
    df = df[df["rating"].between(1, 5)].copy()
    if df.empty:
        raise ValueError("No valid reviews remain after cleaning.")
    # Keep the original raw dataset intact; return cleaned rows for analysis.
    return df

if __name__ == "__main__":
    cleaned = process_data()
    output = DATA_DIR / "processed_reviews_temp.csv"
    cleaned.to_csv(output, index=False, date_format="%Y-%m-%d")
    print(f"Cleaning completed: {len(cleaned)} valid reviews.")
    print(f"Intermediate cleaned data saved to {output.name}")
