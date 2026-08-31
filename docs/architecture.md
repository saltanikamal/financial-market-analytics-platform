# System Architecture

## Overview

The Financial Market Analytics Platform is an end-to-end data science and software engineering system that combines automated market-data ingestion, PostgreSQL storage, feature engineering, machine learning, model management, REST APIs, and interactive financial visualization.

The architecture separates the platform into several logical layers:

- Data ingestion
- Data validation and storage
- Feature engineering
- Machine learning
- Model registry
- Prediction serving
- Backend API
- Frontend visualization

These components work together as a single application while remaining modular and independently maintainable.

---

## Architecture Flow

```text
                         Yahoo Finance
                              │
                              ▼
                    APScheduler / ETL
                              │
                              ▼
                     Data Validation
                              │
                              ▼
                     PostgreSQL Database
                              │
                              ▼
                    Feature Engineering
                              │
                              ▼
                  40 Model Input Features
                              │
                              ▼
                 Machine Learning Pipeline
                 (XGBoost / Random Forest)
                              │
                              ▼
                 5-Fold Expanding
                 Walk-Forward Validation
                              │
                              ▼
              Final Chronological 80/20
                    Evaluation
                              │
                              ▼
                   Model Artifact
                              │
                              ▼
                Model Registry / Selection
                              │
                              ▼
                    FastAPI Backend
                              │
                              ▼
                       REST API
                              │
                              ▼
                    Next.js Dashboard
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
              Interactive Charts   ML Predictions
                                  & Market Signals
```text
                         Yahoo Finance
                              │
                              ▼
                    APScheduler / ETL
                              │
                              ▼
                     Data Validation
                              │
                              ▼
                     PostgreSQL Database
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
        Feature Engineering          Historical Data
                 │                         │
                 ▼                         │
        40 Model Input Features            │
                 │                         │
                 ▼                         │
        Machine Learning Pipeline          │
        (XGBoost / Random Forest)          │
                 │                         │
                 ▼                         │
        5-Fold Expanding                  │
        Walk-Forward Validation            │
                 │                         │
                 └────────────┬────────────┘
                              ▼
            Final Chronological 80/20 Evaluation
                              │
                              ▼
            Model Registry / Model Selection
                 │                         │
                 ▼                         │
            Model Registry                 │
                 │                         │
                 └────────────┬────────────┘
                              ▼
                       FastAPI Backend
                              │
                          REST API
                              │
                              ▼
                       Next.js Dashboard
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
              Interactive Charts   ML Predictions
                                  & Market Signals
