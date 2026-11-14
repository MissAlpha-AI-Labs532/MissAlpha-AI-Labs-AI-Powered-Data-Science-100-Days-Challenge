# AI-Based Cyber Threat & Network Anomaly Detection System

A runnable, offline educational project that analyzes network-flow records, flags unusual activity with Isolation Forest, classifies potential malicious flows with Random Forest, and visualizes communication patterns with NetworkX in Streamlit.

## Important dataset note
`data/network_traffic_synthetic.csv` contains **6,000 synthetic records generated for this project**. It is safe for demonstrations and reproducible testing, but it is not real packet capture data and must not be represented as a public real-world dataset. For research validation, download a public dataset such as:
- **CIC-IDS2017 (Canadian Institute for Cybersecurity):** https://www.unb.ca/cic/datasets/ids-2017.html
- **UNSW-NB15 (UNSW Canberra):** https://research.unsw.edu.au/projects/unsw-nb15-dataset

These datasets have their own schemas and usage terms. Map their fields to this project's feature schema before training; do not simply rename unrelated columns.

## Features
- Data inspection, cleaning, derived network-flow features and EDA-ready CSV.
- Random Forest binary classification (`Normal` / `Malicious`).
- Isolation Forest unsupervised anomaly detection.
- Flow-level security alerts and downloadable CSV.
- NetworkX directed communication graph.
- Accuracy, precision, recall, F1-score and confusion matrix.
- Interactive Streamlit dashboard with filters.

## Project structure
```text
Cyber_Threat_Network_Anomaly_Detection/
├── app.py
├── train_model.py
├── src_preprocess.py
├── generate_dataset.py
├── requirements.txt
├── README.md
├── data/
│   └── network_traffic_synthetic.csv
├── models/                 # generated after training
└── reports/
    └── EDA_summary.txt
```

## Run in Visual Studio Code (Windows)
1. Extract the ZIP and open this folder in VS Code.
2. Open Terminal → New Terminal.
3. Create and activate a virtual environment:
   ```bash
   py -3.11 -m venv .venv
   .venv\Scripts\activate
   ```
4. Upgrade pip and install dependencies:
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. Train both models:
   ```bash
   python train_model.py
   ```
6. Launch dashboard:
   ```bash
   streamlit run app.py
   ```
7. Open the local URL printed by Streamlit (usually `http://localhost:8501`).

## Git Bash alternative
```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python train_model.py
streamlit run app.py
```

## Dataset fields
| Field | Meaning |
|---|---|
| source_ip / destination_ip | Simulated communicating endpoints |
| source_port / destination_port | TCP/UDP port values |
| protocol / service | Network protocol and service category |
| duration_sec | Flow duration |
| packet_count / bytes_transferred | Volume indicators |
| login_attempts / failed_logins | Simulated authentication behaviour |
| connection_rate | Connections per time unit (simulated) |
| bytes_per_packet | Derived transfer feature |
| label | Ground-truth demo label: Normal or Malicious |
| threat_type | Demo subtype (Brute Force, Port Scan, DoS-like, Suspicious Transfer) |

## How the system works
1. `src_preprocess.py` removes identifiers/labels from model input, one-hot encodes protocol/service, and aligns columns.
2. `train_model.py` uses a stratified train/test split. Random Forest learns labelled traffic patterns. Isolation Forest learns a baseline from the training feature vectors.
3. `app.py` scores flows. A row is shown as an alert if Random Forest predicts malicious **or** Isolation Forest flags it as anomalous.
4. NetworkX draws source-to-destination communication edges. Nodes participating in flagged flows are highlighted.

## Evaluation and limitations
- Evaluation is performed on a held-out 25% test split of synthetic data.
- Synthetic data can make metrics look better than real-world results due to simplified patterns and generated labels.
- Isolation Forest contamination is set to 10% as a configurable starting estimate, not a measured real-world prevalence.
- IP addresses are excluded from model features to reduce memorization; they are retained for graph display.
- This is an offline batch demo, not a live IDS, packet sniffer, firewall, SIEM, or incident-response tool.
- Validate on a properly licensed public dataset and in an authorized controlled lab before drawing security conclusions.

## Safe-use note
Only inspect networks and logs you own or are explicitly authorized to monitor. Alerts are leads for investigation, not proof of compromise.
