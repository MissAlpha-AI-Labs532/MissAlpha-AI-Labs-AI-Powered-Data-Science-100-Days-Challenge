"""Generate exploratory data analysis charts and summary without seaborn-specific defaults."""
import pandas as pd
import matplotlib.pyplot as plt
from config import PROCESSED_DIR, REPORT_DIR

def save_bar(series, title, xlabel, ylabel, path, rotation=0):
    fig, ax = plt.subplots(figsize=(8, 4))
    series.plot(kind="bar", ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", labelrotation=rotation)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)

def main():
    path = PROCESSED_DIR / "upi_cleaned.csv"
    if not path.exists():
        raise FileNotFoundError(f"{path} not found. Run python src/prepare_data.py first.")
    df = pd.read_csv(path)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    df.describe(include="all").transpose().to_csv(REPORT_DIR / "eda_summary.csv")

    fraud_counts = df["fraud_flag"].value_counts().sort_index()
    save_bar(fraud_counts, "Genuine vs Fraud Transactions",
             "Fraud flag (0=Genuine, 1=Fraud)", "Transaction count",
             REPORT_DIR / "fraud_distribution.png")

    fig, ax = plt.subplots(figsize=(8, 4))
    df.boxplot(column="amount_inr", by="fraud_flag", showfliers=False, ax=ax)
    ax.set_title("Transaction Amount by Fraud Label")
    ax.set_xlabel("Fraud flag (0=Genuine, 1=Fraud)")
    ax.set_ylabel("Amount (INR)")
    fig.suptitle("")
    fig.tight_layout()
    fig.savefig(REPORT_DIR / "amount_by_fraud.png", dpi=150)
    plt.close(fig)

    if "transaction_type" in df:
        cross = pd.crosstab(df["transaction_type"], df["fraud_flag"])
        save_bar(cross, "Transactions by Type and Fraud Label",
                 "Transaction type", "Transaction count",
                 REPORT_DIR / "fraud_by_type.png", rotation=25)

    if "hour_of_day" in df:
        hourly = df.groupby("hour_of_day")["fraud_flag"].agg(["count", "sum"])
        hourly.columns = ["total_transactions", "fraud_transactions"]
        hourly.to_csv(REPORT_DIR / "hourly_fraud_summary.csv")
        save_bar(hourly["fraud_transactions"], "Fraud Transactions by Hour",
                 "Hour of day", "Fraud transactions",
                 REPORT_DIR / "fraud_by_hour.png")

    print("EDA outputs saved in reports/")
if __name__ == "__main__":
    main()
