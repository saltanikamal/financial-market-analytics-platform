# Financial Market Analytics Platform — Backend

The backend service for the Financial Market Analytics Platform.

Built with **FastAPI**, **PostgreSQL**, and **Python**, the backend provides data ingestion, feature engineering, machine learning pipelines, and REST APIs for financial market analytics.

---

# Overview

The backend is responsible for:

- Collecting historical market data
- Storing financial data in PostgreSQL
- Generating technical indicators
- Training machine learning models
- Managing model versions
- Providing prediction and analytics APIs

The backend follows a modular architecture separating:

- Data Engineering
- Machine Learning
- API Services
- Database Operations

---

# Architecture

```text
Market Data Source
        |
        v
ETL Pipeline
        |
        v
PostgreSQL Database
        |
        v
Feature Engineering
        |
        v
Machine Learning Models
        |
        v
FastAPI REST API
        |
        v
Next.js Dashboard
```

---

# Tech Stack

| Component | Technology |
|---|---|
| Programming | Python |
| API Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn, XGBoost |
| Scheduling | APScheduler |
| Server | Uvicorn |

---

# Project Structure

```text
backend/
│
├── app/
│   │
│   ├── api/
│   │   ├── stocks.py
│   │   ├── analytics.py
│   │   └── predictions.py
│   │
│   ├── ml/
│   │   ├── train.py
│   │   ├── feature_engineering.py
│   │   ├── data_loader.py
│   │   └── registry/
│   │
│   ├── services/
│   │
│   ├── database/
│   │
│   └── main.py
│
├── tests/
├── scripts/
├── requirements.txt
└── README.md
```

---

# Data Pipeline

The ETL pipeline:

1. Downloads historical stock market data
2. Cleans and validates data
3. Stores OHLCV data in PostgreSQL
4. Updates new market records automatically

Supported market data:

- Open
- High
- Low
- Close
- Volume

---

# Feature Engineering

The machine learning pipeline creates technical indicators including:

- Moving averages:
  - MA7
  - MA20
  - MA50
  - MA100
  - MA200

- Returns:
  - Daily return
  - 5-day return
  - 10-day return
  - 20-day return

- Momentum indicators

- Volatility measures

- RSI

- MACD

- Bollinger Bands

---

# Machine Learning Pipeline

The prediction task:

**Predict future market direction over a 5-day horizon**

Classification labels:

```text
0 = SELL
1 = HOLD
2 = BUY
```

Models implemented:

- XGBoost Classifier
- Random Forest Classifier

Model workflow:

```text
Historical Data
        |
        v
Feature Engineering
        |
        v
Training Dataset
        |
        v
Model Training
        |
        v
Validation
        |
        v
Model Registry
        |
        v
Prediction API
```

---

# Model Validation

Time-series validation uses:

- Walk-forward validation
- Accuracy
- Precision
- Recall
- F1 score
- ROC-AUC

Walk-forward validation avoids using future market information during training.

---

# Model Registry

The backend maintains model versions containing:

- Model type
- Training timestamp
- Performance metrics
- Feature information

This enables reproducible model deployment.

---

# API Endpoints

## Health Check

```
GET /
```

## Stock Analytics

```
GET /analytics/ohlc/{symbol}
```

Returns:

- Historical prices
- Technical indicators
- Market features

Example:

```
/analytics/ohlc/AAPL
```

---

## Predictions

```
GET /predict/{symbol}
```

Returns:

- Predicted signal
- Confidence score
- Model information

Example:

```
/predict/AAPL
```

---

# Running Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start backend:

```bash
uvicorn app.main:app --reload
```

Backend runs at:

```
http://localhost:8000
```

API documentation:

```
http://localhost:8000/docs
```

---

# Future Improvements

Planned enhancements:

- Real-time market streaming
- Additional financial datasets
- Sentiment analysis integration
- Portfolio optimization
- Cloud deployment using AWS
- Advanced deep learning models
