# 🌱 Temporal AI Framework for Soil Micro-Nutrient Stress Detection and Fertilizer Optimization

Welcome to the **Temporal AI Framework** – a research-driven project designed to analyze soil nutrient levels, detect micro-nutrient stress, and recommend optimized fertilizer usage based on temporal data. This repository powers a web application that allows users to interact with models predicting soil nutrition needs and fertilizer suggestions.

---

## 📌 Project Overview

Agriculture neuroscience leverages data to make smarter decisions. This framework:

1. Ingests time-series soil nutrient readings.
2. Detects micro-nutrient deficiencies or stresses affecting crop health.
3. Generates fertilizer recommendations tailored to the soil's current state.
4. Offers a simple Flask web interface for users to input data and view results.


## 🔍 Features

- **Data-driven insights** from CSV datasets (`Soil Nutrients.csv`, `Fertilizer Prediction.csv`)
- **Machine learning models** stored in `models/` for prediction tasks
- **Encoders** for preprocessing categorical inputs in `encoders/`
- **Flask web app** (`app.py`) with templates for home, nutrition, fertilizer, history, login/register
- **Notebook explorations** (`.ipynb`) for experimentation


## ⚙️ Getting Started

### Prerequisites

- Python 3.8 or later
- `pip` package manager

### Installation

```bash
# clone repository
git clone <repo-url> "soil nutrition and fertilizer recommendation"
cd "soil nutrition and fertilizer recommendation"

# create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate   # Windows

# install dependencies
pip install -r requirements.txt
```

### Running the App

```bash
# make sure you're in the project root
python app.py
```

Visit `http://localhost:5000` in your browser. You can register/login, view nutrition and fertilizer pages, and check prediction history.


## 🗂️ Repository Structure

```
├── app.py                     # Flask application entry point
├── requirements.txt           # Python dependencies
├── README.md                  # This documentation
├── Fertilizer Prediction.csv  # Model training data
├── Soil Nutrients.csv         # Soil data for ML
├── *.ipynb                    # Jupyter notebooks for analysis
├── encoders/                  # preprocessing objects (label encoders, scalers)
├── models/                    # trained ML models (pickle files)
└── templates/                 # HTML templates for Flask
    ├── base.html
    ├── home.html
    ├── nutrition.html
    ├── fertilizer.html
    ├── history.html
    ├── login.html
    └── register.html
```


## 📁 Data Sets

- **Soil Nutrients.csv** – contains time series nutrient measurements per sample.
- **Fertilizer Prediction.csv** – used to train models mapping soil properties to fertilizer recommendations.

Feel free to explore or replace with your own data.


## 🤖 Model Training / Notebooks

Model development was done in the Jupyter notebooks included in the repo (`*.ipynb`). They walk through data cleaning, feature engineering, training, and evaluation. Use them as a starting point to retrain or improve the models.


## 🧪 Testing & Development

This project currently does not include formal unit tests. If you extend the code, consider adding tests with `pytest`.


## 📬 Feedback & Contributions

Contributions are welcome! Open an issue or submit a pull request. For questions, reach me at <rawatpranav4730@gmail.com> .


---

Thanks for visiting 🌾 – happy farming with AI!