# Financial Market Analytics Platform — Backend

The backend service for the Financial Market Analytics Platform.

Built with **Python, FastAPI, PostgreSQL, SQLAlchemy, Pandas, Scikit-learn, XGBoost, and APScheduler**, the backend provides market-data ingestion, feature engineering, machine-learning training and evaluation, model management, and REST APIs for the frontend dashboard.

---

# Overview

The backend is responsible for:

- Collecting historical market data
- Storing OHLCV data in PostgreSQL
- Generating technical indicators and predictive features
- Training machine-learning classification models
- Evaluating models using time-series validation
- Managing model versions through a model registry
- Generating BUY, HOLD, and SELL predictions
- Storing prediction history
- Providing REST APIs to the Next.js frontend
- Scheduling automated market-data and model workflows

The backend follows a modular architecture separating:

- API Layer
- Service Layer
- Database Layer
- Machine Learning Layer
- Application Layer

---

# Architecture

```text
                    Market Data Source
                           |
                           v
                    ETL / Data Service
                           |
                           v
                    PostgreSQL Database
                           |
                           v
                  Feature Engineering
                           |
                           v
                    ML Training
                           |
                           v
                Walk-Forward Validation
                           |
                           v
                    Model Registry
                           |
                           v
                   Prediction Engine
                           |
                           v
                    FastAPI REST API
                           |
                           v
                    Next.js Dashboard
```

---

# Backend Layers

## 1. API Layer

Located in:

```text
backend/app/api/
```

The API layer exposes the backend functionality through FastAPI REST endpoints.

### `stocks.py`

Provides the list of market symbols currently available in the database.

```text
GET /stocks
```

### `analytics.py`

Provides historical OHLC data and calculated technical indicators.

```text
GET /analytics/ohlc/{symbol}
```

### `predictions.py`

Generates machine-learning predictions and retrieves prediction history.

```text
GET /predict/{symbol}
GET /predict/history/{symbol}
```

### `etl.py`

Provides an endpoint for triggering market-data ingestion.

```text
GET /etl/{symbol}
```

---

# 2. Service Layer

Located in:

```text
backend/app/services/
```

The service layer contains application-level services responsible for external data ingestion and scheduled workflows.

### Market Data Ingestion

The platform uses Yahoo Finance as the primary market-data source.

The ingestion workflow:

```text
Yahoo Finance
      |
      v
Download Market Data
      |
      v
Clean / Validate
      |
      v
Check Existing Records
      |
      v
Insert New Data
      |
      v
PostgreSQL
```

### Main Services

- `yfinance_service.py` — retrieves and processes Yahoo Finance data
- `market_data_ingestion.py` — handles market-data ingestion logic
- `scheduler_service.py` — schedules recurring platform tasks

---

# 3. Database Layer

Located in:

```text
backend/app/database/
backend/app/models/
```

The database layer manages communication between the application and PostgreSQL.

### Database Components

- PostgreSQL database
- SQLAlchemy ORM
- Database connection management
- Stock price model
- Prediction history model

### Main Database Models

#### `StockPrice`

Stores historical OHLCV market data.

```text
symbol
date
open
high
low
close
volume
```

#### `PredictionHistory`

Stores generated machine-learning predictions.

```text
symbol
model_name
model_version
prediction_class
signal
probability
confidence
confidence_level
current_price
prediction_date
```

---

# 4. Machine Learning Layer

Located in:

```text
backend/app/ml/
```

The machine-learning layer manages the complete model lifecycle.

```text
Historical Market Data
          |
          v
      Data Loader
          |
          v
  Feature Engineering
          |
          v
     Training Data
          |
          v
    Model Training
          |
          v
Walk-Forward Validation
          |
          v
    Model Registry
          |
          v
 Prediction Engine
          |
          v
     FastAPI API
```

---

## Data Loading

Located in:

```text
backend/app/ml/data_loader.py
```

Loads historical market data from PostgreSQL and prepares it for feature engineering and model training.

---

## Feature Engineering

Located in:

```text
backend/app/ml/feature_engineering.py
```

Creates technical and statistical features used by the machine-learning models.

Features include:

### Moving Averages

- MA7
- MA20
- MA50
- MA100
- MA200

### Exponential Moving Averages

- EMA12
- EMA26

### Momentum

- Daily return
- 5-day return
- 10-day return
- 20-day return
- Momentum features

### Technical Indicators

- RSI
- MACD
- Bollinger Bands

### Market Behavior

- Volatility
- Volume change
- Candle features

The goal is to transform raw OHLCV data into a structured feature set suitable for machine learning.

---

# 5. Machine Learning Algorithms

Located in:

```text
backend/app/ml/algorithms/
```

The platform currently implements two classification algorithms:

### Random Forest

```text
RandomForestClassifier
```

### XGBoost

```text
XGBClassifier
```

Both models are used to predict the future direction of a security.

---

# Prediction Target

The model predicts market direction over a **5-day prediction horizon**.

Classification labels:

```text
0 = SELL
1 = HOLD
2 = BUY
```

The prediction target is based on the future price return relative to predefined thresholds.

The model therefore attempts to classify whether the future market movement is:

```text
Bearish → SELL
Neutral  → HOLD
Bullish  → BUY
```

---

# 6. Model Training

Located in:

```text
backend/app/ml/train.py
backend/app/ml/core/
```

The training pipeline:

1. Loads historical market data
2. Creates technical features
3. Creates classification targets
4. Validates the feature dataset
5. Trains Random Forest and XGBoost models
6. Evaluates model performance
7. Stores trained model artifacts
8. Registers model metadata
9. Makes the models available to the prediction engine

---

# 7. Model Evaluation

Located in:

```text
backend/app/ml/evaluation/
```

The platform uses **walk-forward validation** because financial market data is time-dependent.

Traditional random train/test splitting can introduce future information into the training process.

Instead, the platform uses an expanding training window:

```text
Fold 1

TRAIN TRAIN TRAIN | TEST
                  ↑
               future


Fold 2

TRAIN TRAIN TRAIN TRAIN | TEST
                        ↑
                     future


Fold 3

TRAIN TRAIN TRAIN TRAIN TRAIN | TEST
                              ↑
                           future
```

No random shuffling is used.

This better reflects how a financial prediction model would operate in production.

---

# Evaluation Metrics

The platform evaluates classification performance using:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC

### Accuracy

Measures the percentage of predictions that are correct.

### Precision

Measures how often predicted classes are correct.

### Recall

Measures how many actual observations of a class are correctly identified.

### F1 Score

Balances precision and recall.

### ROC-AUC

Measures the model's ability to distinguish between classes based on predicted probabilities.

---

# 8. Model Registry

Located in:

```text
backend/app/ml/registry/
```

The model registry manages trained model versions and their metadata.

Registry information includes:

- Symbol
- Model type
- Model version
- Model path
- Performance metrics
- Feature list
- Feature importance
- Creation timestamp

Example:

```text
AAPL
 |
 +-- Random Forest
 |      |
 |      +-- Version
 |      +-- Metrics
 |      +-- Features
 |
 +-- XGBoost
        |
        +-- Version
        +-- Metrics
        +-- Features
```

The registry allows the prediction engine to select the best registered model for a given symbol.

---

# Model Selection

The current model-selection strategy prioritizes:

1. Highest F1 score
2. Highest accuracy
3. Newest model version

Conceptually:

```text
Registered Models
       |
       v
Compare F1
       |
       v
Compare Accuracy
       |
       v
Compare Version
       |
       v
Best Model
```

This separates model training from model serving and provides a reproducible way to select production models.

---

# 9. Prediction Engine

Located in:

```text
backend/app/ml/predictor.py
```

The prediction engine:

1. Loads the best registered model
2. Loads the latest market data
3. Applies feature engineering
4. Selects the required model features
5. Generates a prediction
6. Calculates class probabilities
7. Maps the prediction to BUY/HOLD/SELL
8. Calculates prediction confidence
9. Returns the prediction to the API
10. Stores the result in prediction history

---

# Prediction Confidence

The platform calculates a confidence score using:

```text
Confidence =
    70% × highest class probability
    +
    30% × probability margin
```

Where the probability margin represents the difference between the highest and second-highest class probabilities.

Confidence levels are categorized as:

```text
HIGH
MEDIUM
LOW
```

This provides additional context around the model's prediction rather than returning only the predicted class.

---

# 10. Application Layer

The main FastAPI application is located in:

```text
backend/app/main.py
```

The application layer:

- Creates the FastAPI application
- Registers API routers
- Configures CORS
- Starts the scheduler
- Shuts down scheduled services gracefully
- Provides the application health-check endpoint

Application entry point:

```text
app.main:app
```

---

# Technology Stack

| Layer | Technology |
|---|---|
| Programming Language | Python |
| API Framework | FastAPI |
| ASGI Server | Uvicorn |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Gradient Boosting | XGBoost |
| Market Data | Yahoo Finance / yfinance |
| Scheduling | APScheduler |
| API Documentation | OpenAPI / Swagger |
| Frontend Consumer | Next.js |

---

# Project Structure

```text
backend/
│
├── app/
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── analytics.py
│   │   ├── etl.py
│   │   ├── predictions.py
│   │   └── stocks.py
│   │
│   ├── core/
│   │   └── schema.py
│   │
│   ├── database/
│   │   ├── base.py
│   │   └── connection.py
│   │
│   ├── ml/
│   │   ├── algorithms/
│   │   │   ├── random_forest_model.py
│   │   │   └── xgboost_model.py
│   │   │
│   │   ├── core/
│   │   │   ├── base_model.py
│   │   │   ├── model_factory.py
│   │   │   └── trainer.py
│   │   │
│   │   ├── evaluation/
│   │   │   ├── check_target.py
│   │   │   └── walk_forward.py
│   │   │
│   │   ├── registry/
│   │   │   └── model_registry.py
│   │   │
│   │   ├── data_loader.py
│   │   ├── evaluate.py
│   │   ├── feature_engineering.py
│   │   ├── feature_validator.py
│   │   ├── predictor.py
│   │   ├── train.py
│   │   └── utils.py
│   │
│   ├── models/
│   │   ├── prediction_history.py
│   │   └── stock_price.py
│   │
│   ├── schemas/
│   │   ├── analytics.py
│   │   ├── prediction.py
│   │   └── stock.py
│   │
│   ├── services/
│   │   ├── market_data_ingestion.py
│   │   ├── scheduler_service.py
│   │   └── yfinance_service.py
│   │
│   └── main.py
│
├── requirements.txt
└── README.md
```

---

# API Endpoints

## Health Check

```http
GET /
```

Returns the application status and version.

Example:

```json
{
  "status": "ok",
  "application": "Financial Intelligence Platform",
  "version": "0.1.0"
}
```

---

## Available Stocks

```http
GET /stocks
```

Returns the symbols currently available in PostgreSQL.

Example:

```json
{
  "stocks": [
    "AAPL",
    "AMD",
    "AMZN"
  ]
}
```

---

## Historical Analytics

```http
GET /analytics/ohlc/{symbol}
```

Returns historical market data and calculated technical indicators.

Example:

```text
GET /analytics/ohlc/AAPL
```

The response includes:

- Symbol
- Historical dates
- OHLCV data
- Technical indicators
- Engineered features

---

## Generate Prediction

```http
GET /predict/{symbol}
```

Generates a machine-learning prediction for a symbol.

Example:

```text
GET /predict/AAPL
```

The response includes information such as:

```json
{
  "symbol": "AAPL",
  "signal": "BUY",
  "probability": 0.72,
  "confidence": 68.5,
  "confidence_level": "MEDIUM",
  "model_used": "xgboost"
}
```

---

## Prediction History

```http
GET /predict/history/{symbol}
```

Returns previously generated predictions stored in PostgreSQL.

Example:

```text
GET /predict/history/AAPL
```

Optional parameter:

```text
?limit=10
```

---

## ETL

```http
GET /etl/{symbol}
```

Triggers market-data ingestion for the requested symbol.

Example:

```text
GET /etl/AAPL
```

---

# Running Locally

From the project root, activate the virtual environment:

```bash
source portfolio_venv/bin/activate
```

Move into the backend directory:

```bash
cd backend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The backend runs at:

```text
http://localhost:8000
```

---

# API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

These interfaces allow developers to inspect and test the available REST endpoints.

---

# Database

The backend uses PostgreSQL for persistent storage.

The database stores:

- Historical market prices
- OHLCV data
- Prediction history

SQLAlchemy provides the ORM layer between Python and PostgreSQL.

Conceptually:

```text
FastAPI
   |
   v
SQLAlchemy
   |
   v
PostgreSQL
```

---

# Scheduled Processing

The backend uses APScheduler to automate recurring platform tasks.

The scheduler supports workflows such as:

```text
Scheduled Job
      |
      v
Market Data Ingestion
      |
      v
PostgreSQL Update
```

Scheduled processing reduces the need for manual data updates and supports continuous operation of the platform.

---

# Error Handling

The API uses FastAPI's HTTP exception handling to return appropriate HTTP responses.

Examples include:

```text
200 OK
404 Not Found
500 Internal Server Error
```

Prediction and data-processing errors are captured and returned through the API rather than silently failing.

---

# Production Considerations

The backend architecture is designed to separate:

```text
Data Ingestion
      |
      v
Data Storage
      |
      v
Feature Engineering
      |
      v
Model Training
      |
      v
Model Registry
      |
      v
Model Serving
      |
      v
REST API
```

This separation makes individual components easier to test, maintain, replace, and scale.

---

# Limitations

The current platform has several limitations:

- Market direction is difficult to predict consistently.
- Historical performance does not guarantee future performance.
- The current models rely primarily on price, volume, and technical indicators.
- External factors such as news, macroeconomic events, and market sentiment are not fully modeled.
- Model performance can vary significantly across securities and market regimes.
- The platform is intended for analytics and educational purposes rather than financial advice.

---

# Future Improvements

Planned enhancements include:

- Real-time market streaming
- Additional financial datasets
- News and sentiment analysis
- Advanced feature selection
- Improved model-selection strategies
- Deep learning models such as LSTM
- Portfolio optimization
- Model monitoring and drift detection
- Cloud deployment using AWS
- Automated CI/CD
- Expanded automated testing
- Production-grade authentication and authorization

---

# Summary

The backend provides the core data engineering, machine-learning, and API infrastructure for the Financial Market Analytics Platform.

It combines:

```text
Python
+
PostgreSQL
+
FastAPI
+
ETL
+
Feature Engineering
+
Machine Learning
+
Walk-Forward Validation
+
Model Registry
+
REST APIs
```

to create an end-to-end financial analytics and machine-learning platform.
