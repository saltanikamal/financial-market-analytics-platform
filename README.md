# Financial Market Analytics Platform

An end-to-end financial data science platform that combines data engineering, time-series feature engineering, machine learning, REST APIs, PostgreSQL, and interactive financial visualization into a production-style application.

The platform collects historical market data, stores and processes it through an automated ETL pipeline, generates technical and statistical features, trains machine-learning models to classify future market movement, and exposes the results through a FastAPI backend and interactive Next.js dashboard.

Portfolio project: This system is designed to demonstrate an end-to-end Data Science workflow. ML predictions are experimental and should not be interpreted as financial advice or as a standalone basis for investment decisions.

⸻

Table of Contents

* ## Project Overview
* ## Dashboard
* ## Key Features
* ## System Architecture
* ## Tech Stack

| Category | Technologies |
|---|---|
| Programming | Python, TypeScript |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn, XGBoost |
| Backend | FastAPI, SQLAlchemy |
| Database | PostgreSQL |
| Frontend | Next.js, React |
| Financial Visualization | Lightweight Charts |
| Statistical Visualization | Matplotlib |
| Scheduling | APScheduler |
| Data Source | yfinance |
| API Communication | REST, WebSocket |
| Version Control | Git, GitHub |

---

## Data Pipeline
* ## Machine Learning Pipeline
* ## Model Evaluation
* ## API
* ## Project Structure
* ## Installation
* ## Running the Project
* ## Documentation
* ## Limitations
* ## Future Improvements

⸻

## Project Overview

Financial market data is time-dependent, noisy, and highly sensitive to changes in market conditions. A machine-learning model that performs well on historical data may fail when applied to future or unseen market periods.

This project was built to explore that problem through a complete data science pipeline.

The platform:

1. Collects historical stock-market data.
2. Stores market data in PostgreSQL.
3. Performs data validation and preprocessing.
4. Generates technical and statistical features.
5. Creates future-return-based BUY/HOLD/SELL targets.
6. Trains machine-learning classification models.
7. Evaluates models using chronological walk-forward validation.
8. Registers trained models and their metadata.
9. Serves predictions through a FastAPI API.
10. Visualizes market data and model outputs through a Next.js dashboard.

The project therefore goes beyond a standalone notebook or prediction model and demonstrates how a data science model can be integrated into a complete application.

⸻

## Dashboard

The Next.js dashboard provides an interactive interface for exploring historical market behavior and model outputs.

Dashboard Capabilities

* Interactive candlestick charts
* Historical OHLC price data
* Moving-average overlays
* Technical indicators
* BUY / HOLD / SELL market signals
* Machine-learning predictions
* Prediction probabilities
* Model confidence information
* Historical market analytics
* Real-time market-data WebSocket infrastructure

Dashboard Preview

Screenshots will be added after the final dashboard visual polish.

⸻

## Key Features

Data Engineering

* Automated market-data ingestion
* ETL pipeline using historical stock-market data
* PostgreSQL persistence
* Duplicate detection
* Data validation
* Scheduled data updates
* Support for multiple market symbols

Feature Engineering

The platform generates financial and statistical features including:

* Moving averages
* Exponential moving averages
* RSI
* MACD
* Bollinger Bands
* Momentum
* Daily returns
* Lagged returns
* Rolling volatility
* Volume changes
* Trend strength
* Candlestick features

Machine Learning

* XGBoost classification
* Random Forest classification
* Multiclass BUY / HOLD / SELL prediction
* Probability estimates
* Model registry
* Model versioning
* Walk-forward time-series validation

Backend

* FastAPI REST API
* WebSocket market-data infrastructure
* SQLAlchemy database integration
* Scheduled ETL and model operations
* Modular backend architecture

Frontend

* Next.js
* React
* Interactive financial charts
* Lightweight Charts
* Market analytics dashboard

⸻

## System Architecture

The platform is organized as an end-to-end data engineering, machine-learning, backend, and frontend system.

### Production Data and Application Flow

```mermaid
flowchart LR
    A[Yahoo Finance] --> B[ETL Pipeline]
    B --> C[PostgreSQL]
    C --> D[Feature Engineering]
    D --> E[ML Training]
    E --> F[Model Registry]
    F --> G[FastAPI Backend]
    G --> H[Next.js Dashboard]
    G --> I[WebSocket Market Stream]
    H --> J[Interactive Charts]
    H --> K[Market Signals]
    H --> L[ML Predictions]
```

## Tech Stack

| Category | Technologies |
|---|---|
| Programming | Python, TypeScript |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn, XGBoost |
| Backend | FastAPI, SQLAlchemy |
| Database | PostgreSQL |
| Frontend | Next.js, React |
| Financial Visualization | Lightweight Charts |
| Statistical Visualization | Matplotlib |
| Scheduling | APScheduler |
| Data Source | yfinance |
| API Communication | REST, WebSocket |
| Version Control | Git, GitHub |

---

## Data Pipeline

## Data Pipeline

The data pipeline follows an automated ETL workflow.

1. Extract

Historical market data is collected for supported stock symbols.

Current dashboard/watchlist symbols include:

AAPL
MSFT
NVDA
SPY

2. Transform

Raw market data is processed and transformed into a structured dataset containing:

* Open
* High
* Low
* Close
* Volume
* Returns
* Technical indicators
* Rolling statistics
* Lagged features
* Candlestick features

3. Load

Processed market data is stored in PostgreSQL.

The database provides persistent storage that can be queried by both the analytics and machine-learning components.

4. Scheduling

APScheduler is used to automate recurring data and model-related tasks.

⸻

## Machine Learning Pipeline

The machine-learning workflow is specifically designed for chronological financial data.

1. Historical Data

Market data is retrieved from PostgreSQL rather than repeatedly training directly from an external source.

2. Feature Engineering

Technical and statistical features are generated from historical observations.

Examples include:

MA7
MA20
MA50
MA100
MA200
EMA12
EMA26
RSI
MACD
Bollinger Bands
Momentum
Volatility
Lagged Returns
Volume Change
Candlestick Features

3. Target Creation

The model predicts future market movement over a defined prediction horizon.

Future returns are converted into three classes:

SELL
HOLD
BUY

The classification thresholds are based on future returns rather than simply predicting whether the next closing price is higher or lower.

4. Model Training

The platform currently supports:

* XGBoost
* Random Forest

5. Walk-Forward Validation

Traditional random train/test splitting is inappropriate for time-series financial data because it can allow information from the future to influence the training process.

The platform therefore uses walk-forward validation.

Conceptually:

Fold 1:
TRAIN ──────────────► TEST
Fold 2:
TRAIN ─────────────────────► TEST
Fold 3:
TRAIN ───────────────────────────► TEST
Fold 4:
TRAIN ─────────────────────────────────► TEST

Each training set contains only information available before its corresponding test period.

This provides a more realistic evaluation of how the model may behave on future data.

6. Model Registry

Trained models are versioned and stored with metadata such as:

* Model type
* Symbol
* Training timestamp
* Feature information
* Evaluation metrics
* Model version

The registry allows the prediction service to select an appropriate trained model.

7. Prediction

The prediction service generates:

* BUY / HOLD / SELL signal
* Class probabilities
* Confidence information
* Model metadata

These results are exposed through the FastAPI backend.

⸻

## Model Evaluation

Because financial prediction is a difficult and noisy problem, model evaluation is an important part of this project.

The walk-forward validation process produced results in the following range during development:

Metric	Result
Accuracy	~0.26–0.33
Precision	~0.17–0.32
Recall	~0.26–0.33
F1 Score	~0.13–0.29
ROC-AUC	~0.50

These results indicate that the current model does not demonstrate strong predictive power and should not be treated as a profitable trading strategy.

This is an intentional part of the project.

The objective is not to claim that machine learning can reliably predict financial markets. Instead, the project demonstrates how to:

* Build a financial ML pipeline
* Avoid inappropriate random splitting
* Apply time-series validation
* Track model versions
* Expose predictions through an API
* Evaluate model limitations honestly

⸻

## API

The FastAPI backend provides services for market data, analytics, ETL operations, and machine-learning predictions.

REST Endpoints

Endpoint	Method	Description
/	GET	API health/root endpoint
/stocks	GET	Retrieve available stock symbols
/etl/{symbol}	GET	Trigger/access ETL processing
/analytics/ohlc/{symbol}	GET	Retrieve historical OHLC data and analytics
/predict/{symbol}	GET	Generate a machine-learning prediction
/predict/history/{symbol}	GET	Retrieve prediction history

WebSocket

Endpoint	Type	Description
/ws/market	WebSocket	Stream market-data updates

⸻

## Project Structure

financial-market-analytics-platform/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── ml/
│   │   │   ├── models/
│   │   │   ├── registry/
│   │   │   ├── data_loader.py
│   │   │   ├── feature_engineering.py
│   │   │   ├── feature_validator.py
│   │   │   └── train.py
│   │   ├── services/
│   │   ├── ws/
│   │   └── main.py
│   │
│   ├── docs/
│   │   └── system-architecture.md
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── package.json
│   └── ...
│
├── docs/
│
├── .gitignore
├── README.md
└── ...

⸻

## Installation

1. Clone the Repository

git clone https://github.com/saltanikamal/financial-market-analytics-platform.git
cd financial-market-analytics-platform

2. Create the Python Environment

python3 -m venv portfolio_venv
source portfolio_venv/bin/activate

3. Install Backend Dependencies

cd backend
pip install -r requirements.txt

4. Configure PostgreSQL

Create a PostgreSQL database and configure the required database connection variables in the backend environment configuration.

Example:

DATABASE_URL=postgresql://username:password@localhost:5432/stockdb

5. Install Frontend Dependencies

From the project root:

cd frontend
npm install

⸻

## Running the Project

Start PostgreSQL

Ensure PostgreSQL is running and the configured database is available.

Start the FastAPI Backend

From the backend directory:

uvicorn app.main:app --reload

The API will be available at:

http://127.0.0.1:8000

FastAPI interactive documentation:

http://127.0.0.1:8000/docs

Start the Next.js Frontend

From the frontend directory:

npm run dev

The dashboard will be available at:

http://localhost:3000

⸻

## Documentation

Additional technical documentation:

- Backend documentation
- System architecture
- Frontend documentation — coming next
- Architecture diagram — coming next
- Dashboard screenshots — coming next
⸻

## Limitations

Financial markets are highly complex, noisy, and non-stationary.

The current system has several limitations:

* Model predictive performance is currently weak.
* Historical performance does not guarantee future performance.
* The model does not incorporate all macroeconomic, fundamental, or geopolitical information.
* Confidence scores represent model probabilities and should not be interpreted as certainty.
* The current system is not a fully backtested trading strategy.
* Transaction costs, slippage, liquidity, and portfolio risk management are not fully modeled.
* The platform should not be used as an autonomous investment system.

These limitations are important because a model can produce a prediction without necessarily providing a useful or profitable trading signal.

⸻

## Future Improvements

Machine Learning

* Improve feature selection
* Address class imbalance
* Experiment with additional models
* Improve probability calibration
* Compare model performance across market regimes
* Investigate sequence-based models such as LSTM
* Improve model-selection logic

Validation

* Expand walk-forward validation
* Add benchmark models
* Add trading-strategy backtesting
* Evaluate performance across different market regimes
* Add statistical significance testing

Platform

* Improve dashboard visual design
* Add portfolio and risk analytics
* Add model-performance monitoring
* Improve real-time market-data processing
* Add automated model-retraining monitoring

Cloud Deployment

Potential future deployment architecture:

AWS
 │
 ├── Backend API
 ├── PostgreSQL
 ├── Scheduled ETL
 ├── ML Training
 ├── Model Storage
 └── Frontend Hosting

⸻

## Project Goal

The primary goal of this project is to demonstrate the ability to take a data-science problem from raw data to a working application.

It combines:

Data Engineering
       ↓
Data Storage
       ↓
Feature Engineering
       ↓
Machine Learning
       ↓
Time-Series Validation
       ↓
Model Registry
       ↓
API Development
       ↓
Interactive Visualization

The project emphasizes not only model development, but also data quality, validation methodology, software architecture, reproducibility, and communication of model limitations.

⸻

## License

This project is licensed under the MIT License.
