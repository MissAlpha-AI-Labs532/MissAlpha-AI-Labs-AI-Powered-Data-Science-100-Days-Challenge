"""Clean and standardize the supplied UPI-style transaction CSV."""
import argparse
from pathlib import Path
import pandas as pd
from config import ROOT, DATA_PATH, PROCESSED_DIR

ALIASES = {
    "amount": "amount_inr", "amount_inr": "amount_inr", "amount_(inr)": "amount_inr",
    "transaction_amount": "amount_inr", "transaction_amount_inr": "amount_inr",
    "fraud": "fraud_flag", "is_fraud": "fraud_flag", "isfraud": "fraud_flag",
    "fraudulent": "fraud_flag", "is_fraudulent": "fraud_flag", "fraud_status": "fraud_flag",
    "transaction_timestamp": "timestamp", "date_time": "timestamp",
    "transaction_date": "timestamp", "transaction_datetime": "timestamp",
    "payment_method": "transaction_type", "payment_type": "transaction_type",
    "state": "sender_state", "bank": "sender_bank", "device": "device_type",
    "app": "upi_app", "status": "transaction_status"
}

def clean_data(input_path):
    df = pd.read_csv(input_path)
    df.columns = [str(c).strip().lower().replace("-", "_").replace(" ", "_") for c in df.columns]
    df = df.rename(columns={c: ALIASES.get(c, c) for c in df.columns})
    required = ["amount_inr", "fraud_flag"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}. Map your dataset columns in ALIASES.")
    if "transaction_id" not in df:
        df["transaction_id"] = [f"TXN{i:07d}" for i in range(1, len(df)+1)]
    if "timestamp" not in df:
        df["timestamp"] = pd.NaT
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["amount_inr"] = pd.to_numeric(
        df["amount_inr"].astype(str).str.replace(r"[^0-9.\\-]", "", regex=True),
        errors="coerce"
    )
    label_map = {"fraud": 1, "fraudulent": 1, "yes": 1, "true": 1, "genuine": 0,
                 "legitimate": 0, "not_fraud": 0, "no": 0, "false": 0}
    raw_labels = df["fraud_flag"].astype(str).str.strip().str.lower()
    mapped_labels = raw_labels.map(label_map)
    numeric_labels = pd.to_numeric(df["fraud_flag"], errors="coerce")
    df["fraud_flag"] = numeric_labels.fillna(mapped_labels)
    df = df.drop_duplicates(subset=["transaction_id"])
    df = df.dropna(subset=["amount_inr", "fraud_flag"])
    df = df[df["amount_inr"] >= 0]
    df["fraud_flag"] = df["fraud_flag"].astype(int)
    df = df[df["fraud_flag"].isin([0, 1])]
    # Derive historical transaction frequency if an account identifier is supplied.
    # The identifier itself is not retained as a model feature or exported column.
    sender_id_col = next((c for c in ["sender_id", "sender_account_hash",
                        "sender_vpa_hash", "sender_account_id", "payer_id"] if c in df.columns), None)
    if sender_id_col:
        df["prior_sender_txn_count"] = df.groupby(sender_id_col, dropna=False).cumcount()
        df = df.drop(columns=[sender_id_col])
    else:
        df["prior_sender_txn_count"] = 0

    for col in ["transaction_type","transaction_status","sender_state","sender_bank",
                "receiver_bank","device_type","network_type","upi_app"]:
        if col not in df:
            df[col] = "Unknown"
        df[col] = df[col].fillna("Unknown").astype(str).str.strip()
    df["hour_of_day"] = df["timestamp"].dt.hour.fillna(0).astype(int)
    df["day_of_week"] = df["timestamp"].dt.dayofweek.fillna(0).astype(int)
    df["is_night"] = df["hour_of_day"].between(0, 5).astype(int)
    # Derive transaction-level signals only from fields available at prediction time.
    median = df["amount_inr"].median()
    df["amount_vs_median"] = df["amount_inr"] / max(float(median), 1.0)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out = PROCESSED_DIR / "upi_cleaned.csv"
    df.to_csv(out, index=False)
    print(f"Saved {len(df):,} cleaned rows to {out}")
    print("Fraud distribution:")
    print(df["fraud_flag"].value_counts(dropna=False))
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DATA_PATH), help="Input CSV path")
    args = parser.parse_args()
    clean_data(Path(args.input))
