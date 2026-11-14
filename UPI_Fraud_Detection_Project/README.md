# AI-Based UPI Fraud Detection & Risk Prediction System

## Overview
A learning-oriented end-to-end fraud analytics project using Python, Pandas, Scikit-learn Isolation Forest, XGBoost and Streamlit. It cleans transaction data, explores patterns, trains two models, evaluates them and displays transaction-level risk indicators.

> **Dataset honesty:** The included `data/upi_transactions_demo.csv` is a generated demonstration dataset, not real UPI banking data. Replace it with a properly licensed dataset before reporting final results. Public UPI datasets may also contain synthetic records or synthetic fraud labels. Do not describe them as verified real-world fraud.

## Dataset
Recommended starting point: [UPI Transactions 2024 on Kaggle](https://www.kaggle.com/datasets/skullagos5246/upi-transactions-2024-dataset). Review the dataset card, licence and columns before use. Another benchmark is [PaySim](https://www.kaggle.com/datasets/ealaxi/paysim1), which is synthetic mobile-money data and is not UPI.

Put your CSV in `data/raw/` and run:
```bash
python src/prepare_data.py --input data/raw/your_dataset.csv
```
The input must contain a transaction amount column and a binary fraud label. If names differ, add their mapping in `src/prepare_data.py` under `ALIASES`.

## Installation (Windows CMD / Git Bash)
```bash
python -m venv .venv
# Windows CMD:
.venv\Scripts\activate
# Git Bash:
source .venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the project
```bash
python src/prepare_data.py
python src/eda.py
python src/train_model.py
streamlit run app.py
```
Open the local URL shown by Streamlit (normally http://localhost:8501).

## Models
- **Isolation Forest:** unsupervised anomaly detection; identifies observations unlike the learned normal pattern. It does not learn the fraud label.
- **XGBoost:** supervised binary classifier trained on labelled examples.
- **Risk score:** prototype blend of XGBoost probability (75%) and Isolation Forest anomaly flag (25%). Thresholds are configurable and should be calibrated on validation data and business costs.

## Evaluation
The training script reports accuracy, precision, recall, F1-score, ROC-AUC (when available), confusion matrices and a classification report. With highly imbalanced fraud data, do not rely on accuracy alone; examine recall, precision-recall trade-offs and false-positive burden.

## Project structure
```text
UPI_Fraud_Detection_Project/
├── app.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── upi_transactions_demo.csv
├── models/
├── reports/
├── sql/upi_analysis.sql
├── src/
│   ├── config.py
│   ├── prepare_data.py
│   ├── eda.py
│   └── train_model.py
├── requirements.txt
└── README.md
```

## Limitations and responsible use
- A model trained on synthetic or proxy data is not validated for real UPI fraud.
- Prevent target leakage: exclude post-transaction outcomes, investigation results and fields unavailable at decision time.
- Use time-based validation where possible; random splits can overstate performance when transactions from the same users appear in both sets.
- Protect personal and financial information. Never upload customer identifiers, account numbers, phone numbers, UPI IDs or raw private banking records to a public repository.
- This prototype is for education and analyst decision support, not autonomous payment blocking.
