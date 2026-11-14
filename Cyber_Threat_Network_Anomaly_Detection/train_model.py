"""Train Random Forest threat classifier and Isolation Forest anomaly detector."""
from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from src_preprocess import make_features

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "network_traffic_synthetic.csv"
MODEL_DIR = ROOT / "models"
MODEL_DIR.mkdir(exist_ok=True)

def main():
    df = pd.read_csv(DATA)
    y = (df["label"] == "Malicious").astype(int)
    X = make_features(df)
    feature_columns = X.columns.tolist()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    rf = RandomForestClassifier(n_estimators=250, max_depth=16, min_samples_leaf=2,
                                class_weight="balanced", random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    pred = rf.predict(X_test)
    metrics = {
        "accuracy": float(accuracy_score(y_test, pred)),
        "precision": float(precision_score(y_test, pred, zero_division=0)),
        "recall": float(recall_score(y_test, pred, zero_division=0)),
        "f1_score": float(f1_score(y_test, pred, zero_division=0)),
        "confusion_matrix": confusion_matrix(y_test, pred).tolist(),
        "classification_report": classification_report(y_test, pred, target_names=["Normal","Malicious"], zero_division=0, output_dict=True)
    }
    # Fit unsupervised detector on training traffic; contamination is a configurable estimate.
    iso = IsolationForest(n_estimators=200, contamination=0.10, random_state=42)
    iso.fit(X_train)
    joblib.dump(rf, MODEL_DIR / "random_forest.joblib")
    joblib.dump(iso, MODEL_DIR / "isolation_forest.joblib")
    joblib.dump(feature_columns, MODEL_DIR / "feature_columns.joblib")
    (MODEL_DIR / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print("Training complete.")
    print(json.dumps({k:v for k,v in metrics.items() if k!="classification_report"}, indent=2))

if __name__ == "__main__":
    main()
