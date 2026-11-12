# Student Performance Analysis & Prediction System
**MissAlpha™ AI Labs | Day 1 onward project**

## Project contents
- `data/student_data.csv` — supplied dataset
- `Student_Performance_Analysis.ipynb` — guided end-to-end notebook
- `analysis.py` — reusable command-line analysis and model training
- `app.py` — interactive Streamlit dashboard
- `requirements.txt` — dependencies
- `outputs/` — generated charts, summaries and model files
- `screenshots/` — save your own environment and execution screenshots here

## Dataset detected
- Rows: 395
- Columns: 33
- Target candidate: `G3`
- Columns: school, sex, age, address, famsize, Pstatus, Medu, Fedu, Mjob, Fjob, reason, guardian, traveltime, studytime, failures, schoolsup, famsup, paid, activities, nursery, higher, internet, romantic, famrel, freetime, goout, Dalc, Walc, health, absences, G1, G2, G3

## 1. Setup (Windows PowerShell)
Open this project folder in VS Code, then run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run this once in the current terminal:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 2. Run the notebook
```powershell
jupyter notebook
```
Open `Student_Performance_Analysis.ipynb` and run cells from top to bottom.

## 3. Run the analysis script
```powershell
python analysis.py
```
It creates dataset summaries, charts, model evaluation results and a saved model under `outputs/`.

## 4. Run the Streamlit dashboard
```powershell
streamlit run app.py
```
The dashboard opens in your browser. Use the sidebar to explore the data and make a sample prediction.

## Project workflow
1. Load and validate the CSV.
2. Explore dimensions, columns, data types, missing values and duplicates.
3. Review descriptive statistics and grade distributions.
4. Explore relationships between study time, absences, prior grades and final grade.
5. Train/test split and compare baseline Linear Regression and Random Forest models.
6. Evaluate with MAE, RMSE and R².
7. Use the Streamlit dashboard to inspect the data and try predictions.

## Important modelling note
This dataset contains earlier grades (`G1`, `G2`) as well as final grade (`G3`) when those columns exist. The default model excludes `G1` and `G2` to demonstrate an early-warning scenario using non-grade factors. This avoids using earlier assessment results as predictors. If your use case allows them, you can deliberately include them, but explain that choice and the timing of prediction. Predictions are educational estimates, not decisions about students.

## Submission checklist
- [ ] Python and VS Code/Jupyter installed
- [ ] Virtual environment activated
- [ ] `pip install -r requirements.txt` completed
- [ ] Notebook executed successfully
- [ ] `python analysis.py` completed
- [ ] `streamlit run app.py` opened successfully
- [ ] Screenshots saved in `screenshots/`
- [ ] Be ready to explain each step and the model's limitations

## Dataset columns
- `school`
- `sex`
- `age`
- `address`
- `famsize`
- `Pstatus`
- `Medu`
- `Fedu`
- `Mjob`
- `Fjob`
- `reason`
- `guardian`
- `traveltime`
- `studytime`
- `failures`
- `schoolsup`
- `famsup`
- `paid`
- `activities`
- `nursery`
- `higher`
- `internet`
- `romantic`
- `famrel`
- `freetime`
- `goout`
- `Dalc`
- `Walc`
- `health`
- `absences`
- `G1`
- `G2`
- `G3`
