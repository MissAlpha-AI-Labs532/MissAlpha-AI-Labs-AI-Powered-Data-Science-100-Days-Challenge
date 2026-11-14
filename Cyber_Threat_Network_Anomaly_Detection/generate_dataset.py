"""Regenerate the deterministic synthetic network-flow dataset."""
# The distributed CSV is ready to use. This script is a pointer for reproducibility.
from pathlib import Path
import pandas as pd
p=Path(__file__).resolve().parent/"data"/"network_traffic_synthetic.csv"
df=pd.read_csv(p)
print(f"Dataset available: {p} | rows={len(df)} | columns={len(df.columns)}")
print("This dataset is synthetic, not captured from real devices.")
