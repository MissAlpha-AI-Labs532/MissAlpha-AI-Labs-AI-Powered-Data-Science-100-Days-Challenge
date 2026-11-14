"""Feature preparation shared by training and dashboard."""
import pandas as pd

TARGET = "label"
CATEGORICAL = ["protocol", "service"]
DROP = ["flow_id", "source_ip", "destination_ip", "threat_type", TARGET]

def make_features(frame, feature_columns=None):
    """Convert raw network-flow rows into numeric model features."""
    x = frame.drop(columns=[c for c in DROP if c in frame.columns], errors="ignore").copy()
    x = pd.get_dummies(x, columns=[c for c in CATEGORICAL if c in x.columns], dtype=int)
    x = x.replace([float("inf"), float("-inf")], 0).fillna(0)
    if feature_columns is not None:
        x = x.reindex(columns=feature_columns, fill_value=0)
    return x
