from pathlib import Path
import json
import warnings
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "student_data.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def load_data(path=DATA_PATH):
    try:
        data = pd.read_csv(path)
        if data.shape[1] == 1:
            data = pd.read_csv(path, sep=";")
    except Exception:
        data = pd.read_csv(path, sep=";")
    return data

def main():
    df = load_data()
    print("\\n=== DATASET OVERVIEW ===")
    print("Shape:", df.shape)
    print("\\nFirst 10 rows:\\n", df.head(10).to_string(index=False))
    print("\\nData types:\\n", df.dtypes.to_string())
    print("\\nMissing values:\\n", df.isna().sum().to_string())
    print("\\nDuplicate rows:", int(df.duplicated().sum()))
    print("\\nDescriptive statistics:\\n", df.describe(include="all").transpose().to_string())

    (OUT / "dataset_info.txt").write_text(
        f"Rows: {df.shape[0]}\\nColumns: {df.shape[1]}\\n"
        f"Missing values:\\n{df.isna().sum().to_string()}\\n"
        f"Duplicate rows: {df.duplicated().sum()}\\n\\n"
        f"Data types:\\n{df.dtypes.to_string()}\\n\\n"
        f"Summary:\\n{df.describe(include='all').transpose().to_string()}",
        encoding="utf-8"
    )
    df.describe(include="all").transpose().to_csv(OUT / "descriptive_statistics.csv")
    df.isna().sum().rename("missing_count").to_csv(OUT / "missing_values.csv")

    target = "G3" if "G3" in df.columns else df.columns[-1]
    if not pd.api.types.is_numeric_dtype(df[target]):
        df[target] = pd.to_numeric(df[target], errors="coerce")
    model_df = df.dropna(subset=[target]).copy()

    # Visualisations
    numeric = model_df.select_dtypes(include=np.number)
    if target in numeric.columns:
        plt.figure(figsize=(8, 5))
        sns.histplot(model_df[target], bins=15, kde=True)
        plt.title(f"Distribution of {target}")
        plt.xlabel(target); plt.tight_layout()
        plt.savefig(OUT / "target_distribution.png", dpi=150); plt.close()

    if len(numeric.columns) > 1:
        plt.figure(figsize=(11, 8))
        sns.heatmap(numeric.corr(), cmap="coolwarm", center=0, annot=False)
        plt.title("Numerical Feature Correlation")
        plt.tight_layout(); plt.savefig(OUT / "correlation_heatmap.png", dpi=150); plt.close()

    if "studytime" in model_df.columns and target in model_df.columns:
        plt.figure(figsize=(8, 5))
        sns.boxplot(data=model_df, x="studytime", y=target)
        plt.title(f"{target} by Study Time")
        plt.tight_layout(); plt.savefig(OUT / "grade_by_studytime.png", dpi=150); plt.close()

    if "absences" in model_df.columns and target in model_df.columns:
        plt.figure(figsize=(8, 5))
        sns.scatterplot(data=model_df, x="absences", y=target, alpha=.7)
        plt.title(f"{target} vs Absences")
        plt.tight_layout(); plt.savefig(OUT / "grade_vs_absences.png", dpi=150); plt.close()

    # Exclude grade columns for early-warning prediction
    excluded = {target}
    if target == "G3":
        excluded.update(c for c in ["G1", "G2"] if c in model_df.columns)
    X = model_df.drop(columns=list(excluded), errors="ignore")
    y = model_df[target]
    if X.shape[1] == 0 or len(model_df) < 10:
        print("\\nNot enough usable features/records to train a model.")
        return

    num_cols = X.select_dtypes(include=np.number).columns.tolist()
    cat_cols = X.select_dtypes(exclude=np.number).columns.tolist()
    numeric_pipe = Pipeline([("imputer", SimpleImputer(strategy="median")),
                              ("scaler", StandardScaler())])
    categorical_pipe = Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                                 ("onehot", OneHotEncoder(handle_unknown="ignore"))])
    prep = ColumnTransformer([("num", numeric_pipe, num_cols),
                              ("cat", categorical_pipe, cat_cols)])
    models = {
        "Baseline (mean)": DummyRegressor(strategy="mean"),
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=300, random_state=42,
                                                min_samples_leaf=2)
    }
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    results = []
    fitted = {}
    for name, estimator in models.items():
        pipe = Pipeline([("preprocessor", prep), ("model", estimator)])
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        results.append({
            "Model": name,
            "MAE": mean_absolute_error(y_test, pred),
            "RMSE": np.sqrt(mean_squared_error(y_test, pred)),
            "R2": r2_score(y_test, pred)
        })
        fitted[name] = pipe

    result_df = pd.DataFrame(results).sort_values("MAE")
    print("\\n=== MODEL EVALUATION (held-out test set) ===\\n", result_df.to_string(index=False))
    result_df.to_csv(OUT / "model_comparison.csv", index=False)
    best_name = result_df.iloc[0]["Model"]
    joblib.dump({"pipeline": fitted[best_name], "features": X.columns.tolist(),
                 "target": target, "model_name": best_name},
                OUT / "student_performance_model.joblib")
    print(f"\\nSaved best model: {best_name}")
    print("Outputs saved to:", OUT)

if __name__ == "__main__":
    main()
