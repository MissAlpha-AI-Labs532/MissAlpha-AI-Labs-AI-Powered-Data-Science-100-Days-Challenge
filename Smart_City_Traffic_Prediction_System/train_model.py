"""Train and evaluate a deployable congestion classification pipeline."""
from pathlib import Path
import json
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from src_preprocess import load_data

ROOT = Path(__file__).parent
MODEL_DIR = ROOT / "models"
MODEL_DIR.mkdir(exist_ok=True)

def main():
    df = load_data()
    features = ["hour", "day_of_week", "month", "is_weekend",
                "location", "weather", "road_capacity", "special_event"]
    target = "congestion_level"
    X, y = df[features], df[target]
    categorical = ["location", "weather"]
    numeric = [c for c in features if c not in categorical]
    prep = ColumnTransformer([
        ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical),
        ("numeric", StandardScaler(), numeric)
    ])
    model = Pipeline([
        ("preprocess", prep),
        ("classifier", RandomForestClassifier(
            n_estimators=250, max_depth=14, min_samples_leaf=2,
            class_weight="balanced", random_state=42, n_jobs=-1
        ))
    ])
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    metrics = {
        "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
        "classification_report": classification_report(
            y_test, predictions, output_dict=True, zero_division=0
        ),
        "confusion_matrix": confusion_matrix(
            y_test, predictions, labels=["Low", "Medium", "High"]
        ).tolist(),
        "labels": ["Low", "Medium", "High"],
        "test_rows": int(len(X_test)),
        "features": features,
        "note": "Performance is measured on a synthetic demonstration dataset."
    }
    joblib.dump(model, MODEL_DIR / "traffic_congestion_model.joblib")
    with open(MODEL_DIR / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    print("Model saved to models/traffic_congestion_model.joblib")
    print(f"Test accuracy: {metrics['accuracy']:.3f}")
    print(classification_report(y_test, predictions, zero_division=0))

if __name__ == "__main__":
    main()
