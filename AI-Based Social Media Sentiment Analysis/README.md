# AI-Based Social Media Sentiment Analysis

## Project structure
```text
AI-Social-Media-Sentiment-Analysis/
├── app.py
├── sentiment_analyzer.py
├── data_processor.py
├── topic_analyzer.py
├── requirements.txt
├── README.md
├── data/
│   └── customer_reviews.csv
├── reports/
│   └── sentiment_report.csv
└── screenshots/
    ├── dashboard.png
    └── sentiment_analysis.png
```

## Dataset notice
The included 500 customer reviews are synthetic demonstration records created for development and testing. They are not real customer feedback.

## Setup (Windows / VS Code)
Open the project folder in VS Code, then run:
```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the project
Run sentiment analysis (this also performs data cleaning):
```powershell
python sentiment_analyzer.py
```
Run keyword and topic analysis:
```powershell
python topic_analyzer.py
```
Launch the interactive dashboard:
```powershell
streamlit run app.py
```
Open the local URL shown in the terminal, normally http://localhost:8501.

## Modules
- `data_processor.py`: validates required columns, removes duplicate IDs and empty comments, validates dates and ratings, and normalizes text.
- `sentiment_analyzer.py`: classifies each review as Positive, Negative, or Neutral and saves scores to `reports/sentiment_report.csv`.
- `topic_analyzer.py`: extracts frequent words and summarizes supplied topic labels by sentiment.
- `app.py`: interactive Streamlit dashboard with filters, Plotly charts, customer feedback and CSV export.

## Power BI / Tableau
Import `reports/sentiment_report.csv` into Power BI or Tableau. Suggested fields: date, platform, sentiment, sentiment_score, rating, topic and customer_review.

## Methodology and limitations
VADER is a lexicon/rule-based English sentiment model. It can struggle with sarcasm, mixed opinions, contextual meaning, slang and multilingual feedback. Validate predictions against human-labelled examples before business use. The `topic` field in this demonstration dataset is supplied synthetic metadata; topic analysis groups those labels and does not claim to infer topics from text.
