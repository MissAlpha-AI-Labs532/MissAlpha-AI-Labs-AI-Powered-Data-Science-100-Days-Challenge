"""Load and prepare traffic data for model training and dashboard analysis."""
from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).parent / "data" / "traffic_data.csv"

def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp", "location", "vehicle_count", "road_capacity"])
    df = df.drop_duplicates()
    df["vehicle_count"] = pd.to_numeric(df["vehicle_count"], errors="coerce")
    df["road_capacity"] = pd.to_numeric(df["road_capacity"], errors="coerce")
    df = df.dropna(subset=["vehicle_count", "road_capacity"])
    df = df[(df["vehicle_count"] >= 0) & (df["road_capacity"] > 0)]
    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.dayofweek
    df["month"] = df["timestamp"].dt.month
    df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)
    df["date"] = df["timestamp"].dt.date.astype(str)
    df["congestion_ratio"] = df["vehicle_count"] / df["road_capacity"]
    return df.reset_index(drop=True)

if __name__ == "__main__":
    data = load_data()
    print(f"Rows after cleaning: {len(data):,}")
    print(data.head())
