### 🎓 Student Performance Predictor – Math Score Prediction System
A machine learning web application that predicts a student's math score based on their
background and other test scores. This project demonstrates an end-to-end ML pipeline —
data ingestion, preprocessing, model training, a Flask web app, Docker packaging, and a
CI/CD pipeline to Azure.

### 🎯 Quick Links
Overview

- Features

- Installation

- Quick Start

- Web App Features

- Implementation Details

Model Architecture

Dataset Information

Example Outputs

Known Bugs

Deployment (Azure)

Troubleshooting

📌 Overview
This is a regression project: given a student's gender, race/ethnicity, parental
education level, lunch type, whether they completed a test-prep course, and their
reading and writing scores, it predicts their math score.

The system combines:

A scikit-learn/XGBoost/CatBoost training pipeline

A Flask web application

A Dockerized deployment

GitHub Actions CI/CD to Azure Web App

🚀 What's Actually Working
✅ End-to-end pipeline: ingestion → transformation → training → saved model
✅ Flask web form for entering student details and getting a prediction
✅ Docker image builds and runs
✅ A pre-trained model (`model.pkl`) and preprocessor (`preprocessor.pkl`) are already checked into the repo, so predictions work out of the box
✅ GitHub Actions workflow for Azure deployment (needs your own credentials — see below)

📁 Project Structure
```
Student-Performance-Azure-deployment/
├── app.py                          # Flask web application
├── src/
│   ├── components/
│   │   ├── data_ingestion.py       # reads the raw CSV, splits into train/test
│   │   ├── data_transformation.py  # builds the preprocessing pipeline
│   │   └── model_trainer.py        # trains and compares several regression models
│   ├── pipeline/
│   │   └── predict_pipeline.py     # loads the saved model + preprocessor, predicts
│   ├── utils.py                    # save/load objects, model evaluation
│   ├── logger.py
│   └── exception.py
├── templates/                      # home.html has the prediction form
├── notebook/                       # original EDA + model training notebooks, raw CSV
├── artifacts/                      # train.csv, test.csv, model.pkl, preprocessor.pkl
├── Dockerfile
├── requirements.txt
├── setup.py
└── .github/workflows/main_studentperformancecheck.yml
```

✨ Features
🧠 Model Training Features
Trains and compares 7 regression models: Linear Regression, Random Forest, Decision
Tree, Gradient Boosting, XGBoost, CatBoost, AdaBoost

Small hyperparameter grid search per model

Keeps whichever model scores highest on R² against the test set — no hardcoded winner

Numerical features (reading_score, writing_score) get scaled; categorical features
(gender, race/ethnicity, parental education, lunch, test prep) get one-hot encoded

🌐 Web Application Features
📝 User Inputs
Gender

Race/Ethnicity (group A–E)

Parental level of education

Lunch type (standard / free-or-reduced)

Test preparation course (none / completed)

Reading score

Writing score

⚙️ How It Predicts
Loads the saved model and preprocessor from `artifacts/`

Transforms the input the same way training data was transformed

Runs the model, returns a single predicted math score

📊 Output
One number: predicted math score (0–100), rendered back on the same page

🛠 Installation
**Prerequisites**
- Python 3.8+ (see Known Bugs — the Dockerfile currently uses 3.7, which is EOL)
- pip

**Setup**
```bash
git clone <your-repo-url>
cd Student-Performance-Azure-deployment

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

▶️ Quick Start
**Run locally**
```bash
python app.py
```
Open `http://localhost:80/predictdata` (port 80 usually needs admin/sudo rights locally
— change it in `app.py` to something like 5000 if that's a problem).

**Run with Docker**
```bash
docker build -t student-performance .
docker run -p 80:80 student-performance
```

**Retrain the model**
```bash
python src/components/data_ingestion.py
```
This re-runs the whole pipeline and overwrites `artifacts/model.pkl`. Read the bug list
below first — retraining currently breaks prediction unless you fix a filename typo.

🧠 Model Architecture
**Step 1: Data Ingestion**
Reads the raw CSV, does an 80/20 train/test split, saves both to `artifacts/`.

**Step 2: Data Transformation**
- Numerical pipeline: median imputation → standard scaling (`reading_score`, `writing_score`)
- Categorical pipeline: most-frequent imputation → one-hot encoding → scaling (gender, race/ethnicity, parental education, lunch, test prep)

**Step 3: Model Training**
Trains all 7 models above with grid search, evaluates each on R², saves the best one to
`model.pkl`.

**Step 4: Prediction**
`predict_pipeline.py` loads the saved model + preprocessor and runs inference on new
input.

📊 Dataset Information
`notebook/data/stud.csv`

| Column | Meaning |
|---|---|
| gender | male / female |
| race_ethnicity | group A–E (anonymized) |
| parental_level_of_education | e.g. "bachelor's degree", "some college" |
| lunch | standard / free-or-reduced |
| test_preparation_course | none / completed |
| math_score | 0–100 — this is the prediction target |
| reading_score | 0–100 |
| writing_score | 0–100 |

The model does not see `math_score` at prediction time — obviously, since that's what
it's predicting.

🌍 Example Output
**User Input:**
- Gender: female
- Race/Ethnicity: group B
- Parental education: bachelor's degree
- Lunch: standard
- Test prep: none
- Reading score: 72
- Writing score: 74

**Predicted math score:** somewhere in the low-to-mid 70s, based on the training data's
patterns (I'm not going to fabricate a specific number here — I haven't run the actual
saved model against this input, so any exact figure I gave you would be made up. Run it
yourself to get the real prediction.)

🐞 Known Bugs — fix these before relying on this
1. **Reading and writing scores are swapped in `app.py`.**
   ```python
   reading_score=float(request.form.get('writing_score')),
   writing_score=float(request.form.get('reading_score')))
   ```
   Whatever the user types into "writing score" gets used as "reading score" and vice
   versa. Wrong predictions, silently.

2. **Retraining breaks prediction because of a filename typo.**
   `data_transformation.py` saves the preprocessor as `artifacts/proprocessor.pkl`
   (missing the 'e'), but `predict_pipeline.py` loads `artifacts/preprocessor.pkl`
   (correct spelling). Retrain, and the app keeps using the *old* preprocessor already
   sitting in `artifacts/` — or crashes if that file's ever removed.

3. **`data_ingestion.py` uses a Windows-only file path.**
   ```python
   df = pd.read_csv('notebook\data\stud.csv')
   ```
   Backslashes aren't path separators on Linux/Mac or inside the Docker container. This
   line only works on Windows.

4. **Dockerfile uses `python:3.7-slim-buster`** — both Python 3.7 and Debian Buster are
   end-of-life and unpatched. Move to `python:3.11-slim-bookworm` or newer.

5. **`requirements.txt` has no pinned versions** — fine today, will eventually break as
   pandas/scikit-learn/xgboost/catboost move on.

6. **No input validation on the web form** — an empty field or bad input throws an
   unhandled exception instead of a friendly error.

☁️ Deployment (Azure)
`.github/workflows/main_studentperformancecheck.yml` builds the Docker image, pushes it
to Azure Container Registry, and deploys to Azure Web App on every push to `main`.

**This will not work for you as-is.** It's hardcoded to the original author's own
resources: registry `testdockerkrish.azurecr.io`, web app `studentperformancecheck`, and
GitHub Secrets specific to that account. To use it:

1. Create your own Azure Container Registry and Azure Web App (for containers).
2. Add your own registry credentials and publish profile as GitHub Actions secrets.
3. Edit the `.yml` file to point at your registry, image name, and web app name.

🔧 System Requirements
| Requirement | Minimum | Recommended |
|---|---|---|
| RAM | 2 GB | 4+ GB |
| Disk | 500 MB | 1 GB |
| Python | 3.8 | 3.11 |

🛠 Troubleshooting
**`ModuleNotFoundError`**
```bash
pip install -r requirements.txt
```

**Predictions look wrong / reading and writing seem flipped**
That's a real bug, not a config issue — see Known Bugs #1 above.

**Retrained model gives errors or ignores retraining**
See Known Bugs #2 — check the preprocessor filename mismatch first.

**`FileNotFoundError` on `notebook/data/stud.csv` when running on Linux/Docker**
See Known Bugs #3 — the path uses Windows-style backslashes.

✅ What's Actually Solid Here
✔️ The pipeline structure itself (ingestion → transformation → training → prediction) is
a reasonable, standard layout
✔️ Model selection genuinely compares multiple algorithms instead of hardcoding one
✔️ Docker + CI/CD scaffolding exists and just needs your own credentials swapped in

None of the six bugs above are hard to fix — they're the kind of thing you'd catch in a
five-minute code review. But they're real, and it's better to know before you deploy this
than after.
