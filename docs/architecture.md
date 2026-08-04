
# System Architecture

## Overview

The Financial Market Analytics Platform follows an end-to-end data science architecture combining data ingestion, database storage, machine learning, backend services, and frontend visualization.

## Architecture Flow

```text
                Yahoo Finance
                     │
                     ▼
           ETL Data Ingestion
        (yfinance + APScheduler)
                     │
                     ▼
           PostgreSQL Database
                     │
      ┌──────────────┴──────────────┐
      ▼                             ▼
Feature Engineering        Historical Market Data
      │
      ▼
Machine Learning Pipeline
(XGBoost / Random Forest)
      │
      ▼
Model Registry
      │
      ▼
FastAPI REST API
      │
      ▼
Next.js Dashboard
      │
      ▼
Interactive Charts & Predictions
```
