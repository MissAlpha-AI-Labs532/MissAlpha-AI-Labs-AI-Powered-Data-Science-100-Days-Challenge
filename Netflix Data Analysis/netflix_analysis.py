"""
IMDb / Netflix-style Content Analysis
Run: python netflix_analysis.py --input "imdb(1).csv" --output-dir "project_output"
Requires: pandas, numpy, matplotlib, seaborn
"""
import argparse, ast
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

LIST_COLS = ["genre", "country", "language", "cast", "director", "composer", "writer"]

def parse_list(value):
    if pd.isna(value): return []
    try:
        parsed = ast.literal_eval(str(value))
        if isinstance(parsed, list): return [str(v).strip() for v in parsed if str(v).strip()]
        return [str(parsed).strip()]
    except Exception:
        return [str(value).strip()] if str(value).strip() else []

def classify_kind(value):
    kind = str(value).lower()
    if "movie" in kind: return "Movie"
    if "tv" in kind or "episode" in kind: return "TV Show"
    if kind in ("", "nan", "none"): return "Unknown"
    return "Other"

def main(input_file, output_dir):
    out = Path(output_dir); (out/"data").mkdir(parents=True, exist_ok=True); (out/"outputs").mkdir(exist_ok=True)
    df = pd.read_csv(input_file)
    df = df.drop(columns=["Unnamed: 0"], errors="ignore")
    for col in LIST_COLS:
        df[col+"_list"] = df[col].apply(parse_list)
        df[col+"_primary"] = df[col+"_list"].apply(lambda x: x[0] if x else None)
    for col in ["year", "rating", "vote", "runtime"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["content_type"] = df["kind"].apply(classify_kind)
    df["decade"] = (df["year"] // 10 * 10).astype("Int64")
    df.to_csv(out/"data"/"imdb_cleaned.csv", index=False)

    for col in ["genre", "country"]:
        t = df[["title","year","kind","content_type","rating","vote","runtime",col+"_list"]].explode(col+"_list")
        t = t.rename(columns={col+"_list": col})
        t = t[t[col].notna() & (t[col].astype(str).str.strip() != "")]
        t.to_csv(out/"data"/(col+"_analysis.csv"), index=False)

    genre = pd.read_csv(out/"data"/"genre_analysis.csv")
    country = pd.read_csv(out/"data"/"country_analysis.csv")
    df.groupby("content_type").size().rename("record_count").reset_index().to_csv(out/"outputs"/"content_type_summary.csv", index=False)
    df.dropna(subset=["year"]).groupby(["year","content_type"]).size().rename("record_count").reset_index().to_csv(out/"outputs"/"release_year_trends.csv", index=False)
    genre.groupby("genre").size().rename("title_genre_records").reset_index().sort_values("title_genre_records", ascending=False).to_csv(out/"outputs"/"genre_summary.csv", index=False)
    country.groupby("country").size().rename("title_country_records").reset_index().sort_values("title_country_records", ascending=False).to_csv(out/"outputs"/"country_summary.csv", index=False)
    pd.DataFrame([{
        "total_records":len(df), "movies":int((df.content_type=="Movie").sum()),
        "tv_shows":int((df.content_type=="TV Show").sum()),
        "other_or_unknown":int(df.content_type.isin(["Other","Unknown"]).sum()),
        "average_rating":round(df.rating.mean(),2), "missing_year":int(df.year.isna().sum())
    }]).to_csv(out/"outputs"/"kpi_summary.csv", index=False)

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(8,5)); df.content_type.value_counts().plot(kind="bar", ax=ax)
    ax.set(title="Content Records by Type", xlabel="Content type", ylabel="Records"); fig.tight_layout()
    fig.savefig(out/"outputs"/"content_type.png", dpi=160); plt.close(fig)
    trend = df.dropna(subset=["year"]).groupby(["year","content_type"]).size().reset_index(name="records")
    fig, ax = plt.subplots(figsize=(11,5))
    for typ, group in trend.groupby("content_type"): ax.plot(group.year, group.records, label=typ)
    ax.set(title="Release-Year Distribution", xlabel="Release year", ylabel="Records"); ax.legend()
    fig.tight_layout(); fig.savefig(out/"outputs"/"release_trends.png", dpi=160); plt.close(fig)
    print("Analysis complete. Tableau-ready files are in:", out)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", default="project_output")
    args = parser.parse_args()
    main(args.input, args.output_dir)
