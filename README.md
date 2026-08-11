# financial-market-analytics-platform
![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![XGBoost](https://img.shields.io/badge/XGBoost-ML-orange)
![Next.js](https://img.shields.io/badge/Next.js-Frontend-black)
![License](https://img.shields.io/badge/License-MIT-yellow)


An end-to-end financial data science platform that automates market data collection, feature engineering, machine learning, and interactive visualization.

---

## Table of Contents

- Overview
- Dashboard
- Features
- System Architecture
- Tech Stack
- Project Structure
- Machine Learning Pipeline
- API
- Installation
- Running the Project
- Documentation
- Future Improvements

---

## Overview

The Financial Market Analytics Platform is an end-to-end data science project designed to demonstrate the complete machine learning lifecycle using historical stock market data.

The platform automatically collects market data, stores it in a PostgreSQL database, engineers technical indicators, trains machine learning models to classify future market movements into Buy, Hold, and Sell signals, and exposes predictions through a FastAPI backend. A modern Next.js dashboard provides interactive candlestick charts, technical indicators, and analytics for exploring the results.

Rather than focusing solely on building a prediction model, this project showcases the integration of data engineering, machine learning, backend development, database management, and frontend visualization into a single production-style application.

---

## Dashboard

The interactive dashboard provides:

- Candlestick charts
- Moving averages and technical indicators
- BUY/HOLD/SELL predictions
- Model confidence scores
- Historical market analytics
---

## Key Features

* Automated ETL pipeline for historical stock market data
* PostgreSQL database for reliable data storage
* Feature engineering with 30+ technical indicators
* Machine learning using XGBoost and Random Forest classifiers
* Walk-forward validation for time-series evaluation
* Model registry for version management
* FastAPI REST API for analytics and prediction services
* Interactive Next.js dashboard with candlestick charts
* Modular architecture separating data, ML, backend, and frontend components

---

## Tech Stack

| Category | Technologies |
|----------|--------------|
| Programming | Python, TypeScript |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn, XGBoost |
| Backend | FastAPI |
| Frontend | Next.js, React |
| Database | PostgreSQL |
| Visualization | Lightweight Charts, Matplotlib |
| Scheduling | APScheduler |
| Version Control | Git, GitHub |

---

## Documentation

- [System Architecture](backend/docs/system-architecture.md)

---

## Project Structure

```text
financial_platform_portfolio/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── ml/
│   │   ├── services/
│   │   └── main.py
│   ├── docs/
│   │   └── system-architecture.md
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   ├── components/
│   └── package.json
│
├── .gitignore
└── README.md
```
---

## Machine Learning Pipeline

The machine learning workflow is designed for time-series financial data and includes:

1. **Data Collection**
   Historical market data is collected through the ETL pipeline and stored in PostgreSQL.

2. **Feature Engineering**
   Technical indicators, moving averages, momentum, volatility, lagged returns, and candlestick features are generated from historical price data.

3. **Target Creation**
   Future returns are used to classify market movement into three classes:
   - BUY
   - HOLD
   - SELL

4. **Model Training**
   XGBoost and Random Forest classifiers are trained using engineered features.

5. **Time-Series Validation**
   Walk-forward validation is used to evaluate model performance while preserving the chronological order of financial data.

6. **Model Registry**
   Trained models and their metadata are versioned through the model registry.

7. **Prediction**
   The selected model generates market signals and probability estimates through the FastAPI prediction service.

8. **Visualization**
   Predictions, confidence scores, technical indicators, and historical prices are displayed through the Next.js dashboard.

---

## API

The FastAPI backend provides REST endpoints for market data, analytics, ETL operations, and machine learning predictions.

### REST Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API health/root endpoint |
| `/stocks` | GET | Retrieve available stock symbols |
| `/etl/{symbol}` | GET | Trigger or access ETL processing for a stock symbol |
| `/analytics/ohlc/{symbol}` | GET | Retrieve historical OHLC data and analytics |
| `/predict/{symbol}` | GET | Generate a machine learning prediction for a stock |
| `/predict/history/{symbol}` | GET | Retrieve prediction history |

| Endpoint | Type | Description |
|----------|------|-------------|
| `/ws/market` | WebSocket | Stream market data updates |
