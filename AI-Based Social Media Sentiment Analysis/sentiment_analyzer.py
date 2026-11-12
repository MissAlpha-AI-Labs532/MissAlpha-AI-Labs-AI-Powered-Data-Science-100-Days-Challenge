from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
except ImportError:
    VADER_AVAILABLE = False

    class SentimentIntensityAnalyzer:
        # Offline smoke-test fallback only. Install requirements.txt for VADER.
        POSITIVE = {"excellent", "great", "amazing", "happy", "helpful", "good",
                    "smooth", "love", "impressed", "reliable", "worth", "polite"}
        NEGATIVE = {"disappointing", "delayed", "poor", "crashing", "frustrating",
                    "rude", "ignored", "damaged", "slow", "worse", "issue", "complaint"}

        def polarity_scores(self, text):
            words = [w.strip(".,!?;:") for w in str(text).lower().split()]
            pos = sum(w in self.POSITIVE for w in words)
            neg = sum(w in self.NEGATIVE for w in words)
            total = max(len(words), 1)
            compound = (pos - neg) / max(pos + neg, 1)
            compound = max(-1.0, min(1.0, compound))
            return {
                "pos": pos / total,
                "neg": neg / total,
                "neu": max(0.0, 1.0 - (pos + neg) / total),
                "compound": compound if pos != neg else 0.0
            }

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    scores = analyzer.polarity_scores(str(text))
    compound = float(scores["compound"])
    if compound >= 0.05:
        label = "Positive"
    elif compound <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"
    return {
        "positive_score": scores["pos"],
        "negative_score": scores["neg"],
        "neutral_score": scores["neu"],
        "sentiment_score": compound,
        "sentiment": label,
    }

def run_analysis(input_file=None, output_file=None):
    from data_processor import process_data
    input_file = Path(input_file) if input_file else DATA_DIR / "customer_reviews.csv"
    output_file = Path(output_file) if output_file else REPORT_DIR / "sentiment_report.csv"
    df = process_data(input_file)
    results = pd.DataFrame(
        df["customer_review"].map(analyze_sentiment).tolist(),
        index=df.index
    )
    result = pd.concat([df, results], axis=1)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_file, index=False, date_format="%Y-%m-%d")
    return result

if __name__ == "__main__":
    result = run_analysis()
    engine = "VADER" if VADER_AVAILABLE else "offline fallback (install requirements.txt for VADER)"
    print(f"Sentiment analysis completed using {engine}.")
    print(result["sentiment"].value_counts().to_string())
    print(f"Saved: {REPORT_DIR / 'sentiment_report.csv'}")
