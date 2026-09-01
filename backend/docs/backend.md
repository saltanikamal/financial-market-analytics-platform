Backend Documentation

1. Backend Architecture

The backend of the Financial Market Analytics Platform provides the API, data-access, analytics, machine-learning prediction, and scheduling services that support the application.

The backend is implemented with FastAPI and uses PostgreSQL as the persistent storage layer.

The main backend workflow is:

Market Data
    │
    ▼
ETL / Scheduler
    │
    ▼
PostgreSQL
    │
    ├───────────────┐
    ▼               ▼
Analytics       Feature Engineering
    │               │
    │               ▼
    │          ML Models
    │               │
    │               ▼
    │          Model Registry
    │               │
    └───────┬───────┘
            ▼
        FastAPI API
            │
            ▼
      Next.js Dashboard

The backend separates data ingestion, database access, analytics, machine learning, and API responsibilities so that each component can be developed and tested independently.


2. Backend Overview

The backend is responsible for:

* Providing REST API endpoints.
* Retrieving historical market data.
* Serving OHLC financial data to the dashboard.
* Calculating dashboard-oriented technical indicators.
* Loading trained machine-learning models.
* Generating BUY, HOLD, and SELL predictions.
* Returning prediction probabilities and confidence information.
* Managing model versions through a model registry.
* Running scheduled market-data ingestion.
* Supporting machine-learning training workflows.
* Validating financial data before it is used by downstream components.

The backend is designed as a modular application rather than a single monolithic script.


3. Technology Stack

Backend Framework

* FastAPI
* Uvicorn
* Python

Database

* PostgreSQL
* SQLAlchemy ORM

Data Processing

* Pandas
* NumPy
* yfinance

Machine Learning

* Scikit-learn
* Random Forest
* XGBoost

Scheduling

* APScheduler

API Documentation

FastAPI automatically provides interactive API documentation.

The primary documentation interfaces are:

http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc


4. Backend Directory Structure

The backend is organized into application, API, database, machine-learning, and supporting components.

A simplified structure is:

backend/
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── stocks.py
│   │   ├── analytics.py
│   │   └── predictions.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   └── models.py
│   │
│   ├── ml/
│   │   ├── data_loader.py
│   │   ├── feature_engineering.py
│   │   ├── feature_validator.py
│   │   ├── train.py
│   │   ├── predictor.py
│   │   ├── model_registry.py
│   │   └── models/
│   │
│   └── ...
│
├── docs/
│   └── backend.md
│
└── requirements.txt


5. FastAPI Application

The main FastAPI application is defined in:

backend/app/main.py

The application initializes the API and registers the different API routers.

The backend exposes functionality through separate route modules rather than placing all endpoints inside main.py.

This separation improves maintainability and makes it easier to extend the platform.


6. API Modules

6.1 Stocks API

The stocks API provides access to supported market symbols and stock-related functionality.

The application currently supports a 30-symbol market universe, including:

AAPL
AMD
AMZN
AVGO
BAC
CAT
COST
CVX
DIA
GE
GOOGL
GS
HD
JNJ
JPM
LLY
MA
META
MS
MSFT
NFLX
NVDA
ORCL
QQQ
SPY
TSLA
UNH
V
WMT
XOM

The primary dashboard watchlist focuses on:

AAPL
MSFT
NVDA
SPY


7. Analytics API

The analytics functionality is implemented in:

backend/app/api/analytics.py

The main dashboard endpoint is:

GET /analytics/ohlc/{symbol}

For example:

GET /analytics/ohlc/AAPL

The endpoint returns historical OHLC data used by the frontend financial chart.

The response contains market information such as:

date
open
high
low
close
volume

The endpoint also supports dashboard-oriented moving averages.

The current dashboard implementation calculates:

MA7
MA20

These indicators are calculated for visualization without requiring the complete machine-learning feature-engineering pipeline.

This design keeps the chart endpoint lightweight and avoids unnecessary ML processing when the dashboard only needs historical price information.


8. OHLC Data Flow

The OHLC request follows this general workflow:

Frontend
   │
   │ GET /analytics/ohlc/AAPL
   ▼
FastAPI
   │
   ▼
Analytics Router
   │
   ▼
PostgreSQL
   │
   ▼
Historical OHLC Data
   │
   ▼
MA7 / MA20 Calculation
   │
   ▼
JSON Response
   │
   ▼
Next.js Dashboard

The frontend converts the returned numerical values into chart data and displays them using the financial chart component.


9. Database Integration

The backend uses PostgreSQL as the persistent storage layer for historical financial market data.

The database layer provides structured access to market information used by analytics services and machine-learning workflows.

Database Technology

* PostgreSQL
* SQLAlchemy ORM

Database Responsibilities

The database layer handles:

* Storing historical OHLCV market data.
* Retrieving financial data for analytics endpoints.
* Providing datasets for feature engineering.
* Maintaining structured market information.
* Supporting historical analysis.
* Providing training data to machine-learning workflows.

Database

The primary project database is:

stockdb

The main market-data table is:

stock_prices


10. Stock Price Data Model

The stock_prices table stores historical market information for each supported symbol.

The primary market fields include:

symbol
date
open
high
low
close
volume

The combination of symbol and date identifies a unique market observation.

Data validation is used to ensure that duplicate symbol/date records are not introduced into the dataset.


11. Data Ingestion and ETL

Market data is collected using yfinance.

The ETL workflow retrieves historical financial data and stores it in PostgreSQL.

The general process is:

Yahoo Finance
      │
      ▼
Data Retrieval
      │
      ▼
Validation
      │
      ▼
Transformation
      │
      ▼
PostgreSQL

The scheduler supports automated market-data ingestion.

The current system monitors a 30-symbol watchlist.

The ETL process has been validated across the supported universe, with successful ingestion for the monitored symbols.


12. Scheduler

The backend uses APScheduler to automate recurring operations.

The scheduler is responsible for maintaining current market data and supporting periodic model-related workflows.

The architecture supports scheduled operations such as:

Market-data ingestion
Model retraining

The market-data scheduler runs independently of individual API requests.

This allows the API to serve stored data without having to download market data every time a user opens the dashboard.


13. Machine Learning Integration

The machine-learning components are located under:

backend/app/ml/

The ML subsystem contains separate components for:

* Data loading.
* Feature engineering.
* Feature validation.
* Model training.
* Model prediction.
* Model registration.
* Model selection.

The current machine-learning workflow uses classification rather than regression.

The model predicts market direction using three classes:

0 = SELL
1 = HOLD
2 = BUY


14. Feature Engineering

Feature engineering is implemented in:

backend/app/ml/feature_engineering.py

The feature pipeline derives technical and statistical information from historical OHLCV data.

The current feature set includes indicators such as:

* Moving averages.
* EMA12.
* EMA26.
* RSI.
* MACD.
* Bollinger Bands.
* Momentum.
* Volatility.
* Volume change.

The prediction horizon is:

5 trading periods

The target is generated from future price movement.

The classification framework uses thresholds to distinguish BUY, HOLD, and SELL outcomes.

The feature-engineering process is applied consistently during training and prediction.


15. Feature Validation

Feature validation is handled by:

backend/app/ml/feature_validator.py

The purpose of feature validation is to identify invalid or unusable model inputs before they reach the prediction stage.

Validation helps detect issues such as:

* Missing values.
* Invalid numerical values.
* Unexpected feature columns.
* Incorrect feature dimensions.
* Incompatible model inputs.

This provides an additional protection layer between raw financial data and the machine-learning models.


16. Machine-Learning Models

The platform currently supports:

Random Forest
XGBoost

Both models are trained as classification models.

The models are stored as versioned artifacts and registered in the model registry.

The ML system can therefore maintain multiple trained models and compare their evaluation results.


17. Walk-Forward Validation

Financial time-series data cannot be evaluated reliably using a conventional random train/test split because randomly mixing historical observations can introduce future information into the training dataset.

The project therefore uses walk-forward validation.

The general process is:

Historical Data
Training Window
       │
       ▼
Validation/Test Window
       │
       ▼
Expand Training Window
       │
       ▼
Next Test Window
       │
       ▼
Repeat

This approach preserves chronological ordering and provides a more realistic estimate of how the model would behave on future observations.

The evaluation process measures classification performance using metrics including:

* Accuracy.
* Precision.
* Recall.
* F1 score.
* ROC-AUC.

Because the financial classification problem is imbalanced, weighted metrics are particularly important when comparing models.


18. Model Registry

The model registry manages trained model artifacts and their associated metadata.

The registry contains information such as:

model type
symbol
model version
training information
evaluation metrics
model artifact location

A registry file is maintained under the ML model infrastructure.

The model registry allows the prediction system to identify registered models without hard-coding a single model file into the API.


19. Model Selection

The platform supports model comparison through evaluation metrics.

The model-selection strategy considers model performance rather than simply selecting a model because it is newer or more complex.

The current registry can compare Random Forest and XGBoost models using evaluation metrics such as weighted F1.

This is important because a more sophisticated model is not automatically a better model.

For example, if two models have nearly identical evaluation results, the registry can select the model with the stronger measured performance rather than assuming XGBoost must outperform Random Forest.


20. Prediction API

The prediction functionality is implemented through:

GET /predict/{symbol}

Example:

GET /predict/AAPL

The prediction workflow is:

API Request
    │
    ▼
Load Historical Data
    │
    ▼
Feature Engineering
    │
    ▼
Feature Validation
    │
    ▼
Load Registered Model
    │
    ▼
Generate Prediction
    │
    ▼
Calculate Probabilities
    │
    ▼
Calculate Confidence
    │
    ▼
Return JSON


21. Prediction Response

A prediction response contains information describing the current model prediction.

Typical fields include:

symbol
signal
probability
confidence
current_price
model
model_version

The signal is translated into a human-readable market classification:

BUY
HOLD
SELL

The response also identifies the model and model version used to produce the prediction.

This improves reproducibility and makes the prediction traceable to a specific trained model.


22. Prediction Confidence

The prediction system calculates a confidence score using model probability and the separation between the strongest and competing probabilities.

The confidence calculation combines:

Prediction probability
+
Probability margin

The implementation uses a weighted combination of these values.

The purpose of the confidence score is to provide additional context around the model prediction rather than presenting the classification alone.

Confidence should not be interpreted as a guarantee that the prediction will be correct.


23. Important Model Limitation

The machine-learning component is an experimental analytical system and should not be interpreted as a financial-advisory system.

Financial markets are affected by many variables that are not represented in the current feature set.

Examples include:

* Macroeconomic events.
* Interest-rate changes.
* Earnings announcements.
* Geopolitical events.
* Market sentiment.
* Unexpected company-specific events.
* Changes in market regime.

Therefore:

Model prediction ≠ guaranteed future market movement

The purpose of the ML component is to demonstrate an end-to-end data-science workflow involving financial data, feature engineering, time-series validation, classification, model comparison, and API deployment.


24. API Error Handling

The backend validates requested symbols and handles failures from the underlying data and model layers.

Potential API failures include:

* Unsupported symbols.
* Missing historical data.
* Database connection problems.
* Missing registered models.
* Missing model artifacts.
* Invalid feature data.
* Model prediction errors.

Errors should be returned through appropriate HTTP responses rather than allowing internal exceptions to produce unexplained application failures.


25. Backend and Frontend Integration

The backend communicates with the Next.js frontend through HTTP REST endpoints.

The primary data flow is:

Next.js Dashboard
       │
       │ HTTP Request
       ▼
FastAPI Backend
       │
       ├── Analytics API
       │
       └── Prediction API
       │
       ▼
PostgreSQL / ML Models
       │
       ▼
JSON Response
       │
       ▼
Next.js Dashboard

The frontend is therefore separated from the backend data and machine-learning implementation.

This allows the backend to be tested independently using API tools such as curl or the FastAPI Swagger interface.


26. API Testing

Backend endpoints can be tested directly without the frontend.

For example:

curl http://127.0.0.1:8000/analytics/ohlc/AAPL

Prediction testing can be performed with:

curl http://127.0.0.1:8000/predict/AAPL

FastAPI’s interactive documentation can also be used to inspect and test endpoints:

http://127.0.0.1:8000/docs

Testing the backend independently helps isolate API, database, and machine-learning issues from frontend problems.


27. Data Validation Results

The market-data pipeline has been validated against the supported dataset.

Validation checks include:

* Record counts.
* Date ranges.
* Duplicate symbol/date records.
* NULL OHLC values.
* Successful ETL execution.
* API response status.
* Consistency between database and API data.

The platform has successfully ingested the monitored 30-symbol universe through the ETL workflow.

The primary dashboard symbols are:

AAPL
MSFT
NVDA
SPY

These symbols are used for the primary portfolio demonstration and dashboard visualization.


28. Backend Development Principles

The backend follows several design principles.

Separation of Responsibilities

Each component has a specific responsibility:

API
Data Access
ETL
Feature Engineering
Model Training
Model Registry
Prediction

Reproducibility

Model versions and metadata are maintained so predictions can be associated with the model that generated them.

Validation

Data and model inputs are validated before being used downstream.

Maintainability

The backend is organized into independent modules so individual components can be modified without rewriting the entire application.

Testability

API endpoints can be tested independently of the frontend.


29. Security Considerations

Database credentials and other sensitive configuration values should not be hard-coded into source code.

The project separates application configuration from source-code logic and avoids committing database credentials to GitHub.

Production deployments should additionally use:

* Environment variables or secret-management services.
* Restricted database permissions.
* HTTPS.
* Authentication and authorization where appropriate.
* Secure production configuration.
* Logging and monitoring.


30. Current Backend Architecture Summary

The complete backend architecture can be summarized as:

                    ┌─────────────────────┐
                    │     yfinance        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    ETL / Scheduler  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     PostgreSQL      │
                    │      stockdb        │
                    └──────────┬──────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
       ┌─────────────────┐          ┌────────────────────┐
       │ Analytics API   │          │ Feature Engineering│
       └────────┬────────┘          └─────────┬──────────┘
                │                             │
                │                             ▼
                │                    ┌────────────────────┐
                │                    │ ML Models          │
                │                    │ RF / XGBoost       │
                │                    └─────────┬──────────┘
                │                              │
                │                              ▼
                │                    ┌────────────────────┐
                │                    │ Model Registry     │
                │                    └─────────┬──────────┘
                │                              │
                └──────────────┬───────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │       Backend       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Next.js Dashboard │
                    └─────────────────────┘


31. Future Backend Improvements

Potential future improvements include:

* Authentication and authorization.
* Production deployment.
* API rate limiting.
* Structured application logging.
* Automated backend tests.
* Expanded API monitoring.
* Improved model monitoring.
* Automated model-performance tracking.
* Additional financial data sources.
* More advanced feature engineering.
* Additional time-series models.
* LSTM or other deep-learning experiments.
* Improved confidence calibration.
* Automated model retraining and validation.
* Cloud deployment using AWS infrastructure.

These improvements are intentionally separated from the current portfolio implementation so that the existing platform remains understandable, testable, and maintainable.


32. Portfolio Project Perspective

The backend demonstrates an end-to-end data-science engineering workflow:

Data Acquisition
      ↓
ETL
      ↓
Data Storage
      ↓
Data Validation
      ↓
Feature Engineering
      ↓
Machine Learning
      ↓
Model Evaluation
      ↓
Model Registry
      ↓
Prediction API
      ↓
Dashboard

This architecture demonstrates the integration of:

* Python.
* SQL.
* PostgreSQL.
* FastAPI.
* Pandas.
* Scikit-learn.
* XGBoost.
* Financial time-series data.
* Machine-learning evaluation.
* REST APIs.
* Scheduled data pipelines.
* Next.js visualization.

The backend therefore serves as the central integration layer connecting the data-engineering, machine-learning, and frontend components of the Financial Market Analytics Platform.
