"""Train Isolation Forest and XGBoost; save models and evaluation metrics."""
import json
import numpy as np
import pandas as pd
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             confusion_matrix, classification_report, roc_auc_score)
from config import PROCESSED_DIR, MODEL_DIR, REPORT_DIR, TARGET

NUMERIC = ["amount_inr", "hour_of_day", "day_of_week", "is_night", "amount_vs_median", "prior_sender_txn_count"]
CATEGORICAL = ["transaction_type", "transaction_status", "sender_state", "sender_bank",
               "receiver_bank", "device_type", "network_type", "upi_app"]

def main():
    df = pd.read_csv(PROCESSED_DIR/"upi_cleaned.csv")
    features = [c for c in NUMERIC + CATEGORICAL if c in df.columns]
    X, y = df[features], df[TARGET].astype(int)
    if y.nunique() < 2:
        raise ValueError("Training requires both genuine (0) and fraud (1) examples.")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y)
    num_cols = [c for c in NUMERIC if c in features]
    cat_cols = [c for c in CATEGORICAL if c in features]
    pre = ColumnTransformer([
        ("num", Pipeline([("imputer", SimpleImputer(strategy="median")),
                          ("scale", StandardScaler())]), num_cols),
        ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                          ("onehot", OneHotEncoder(handle_unknown="ignore"))]), cat_cols)
    ])
    Xtr = pre.fit_transform(X_train)
    Xte = pre.transform(X_test)
    iso = IsolationForest(n_estimators=200, contamination="auto", random_state=42)
    iso.fit(Xtr)
    iso_pred = (iso.predict(Xte) == -1).astype(int)
    try:
        from xgboost import XGBClassifier
        ratio = max(1.0, (y_train == 0).sum() / max((y_train == 1).sum(), 1))
        clf = XGBClassifier(n_estimators=300, max_depth=5, learning_rate=0.05,
            subsample=0.85, colsample_bytree=0.85, objective="binary:logistic",
            eval_metric="logloss", scale_pos_weight=ratio, random_state=42,
            n_jobs=4)
        clf.fit(Xtr, y_train)
    except ImportError as e:
        raise ImportError("Install XGBoost using: pip install xgboost") from e
    prob = clf.predict_proba(Xte)[:,1]
    pred = (prob >= 0.5).astype(int)
    def metrics(actual, predicted, probabilities=None):
        result = {
            "accuracy": float(accuracy_score(actual, predicted)),
            "precision": float(precision_score(actual, predicted, zero_division=0)),
            "recall": float(recall_score(actual, predicted, zero_division=0)),
            "f1_score": float(f1_score(actual, predicted, zero_division=0)),
            "confusion_matrix": confusion_matrix(actual, predicted).tolist(),
            "classification_report": classification_report(actual, predicted, zero_division=0, output_dict=True)
        }
        if probabilities is not None and len(np.unique(actual)) == 2:
            result["roc_auc"] = float(roc_auc_score(actual, probabilities))
        return result
    results = {"isolation_forest": metrics(y_test, iso_pred),
               "xgboost": metrics(y_test, pred, prob)}
    MODEL_DIR.mkdir(exist_ok=True); REPORT_DIR.mkdir(exist_ok=True)
    joblib.dump({"preprocessor": pre, "model": clf, "features": features}, MODEL_DIR/"xgboost_pipeline.joblib")
    joblib.dump({"preprocessor": pre, "model": iso, "features": features}, MODEL_DIR/"isolation_forest_pipeline.joblib")
    with open(REPORT_DIR/"model_metrics.json","w") as f: json.dump(results, f, indent=2)
    test_out = X_test.copy()
    test_out["actual_fraud"] = y_test.values
    test_out["xgboost_probability"] = prob
    test_out["xgboost_prediction"] = pred
    test_out["isolation_forest_prediction"] = iso_pred
    test_out["risk_score"] = np.clip(100*(0.75*prob + 0.25*iso_pred),0,100).round(1)
    test_out.to_csv(REPORT_DIR/"test_predictions.csv", index=False)
    print(json.dumps({k:{m:v for m,v in val.items() if m!="classification_report"} for k,val in results.items()}, indent=2))
    print("Models and reports saved.")

if __name__ == "__main__":
    main()
