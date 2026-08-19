# System Architecture

## Overview

The Financial Market Analytics Platform follows an end-to-end data science and software engineering architecture combining automated market-data ingestion, PostgreSQL storage, feature engineering, machine learning, backend APIs, and interactive frontend visualization.

The architecture separates the data pipeline, machine-learning workflow, and application layer while allowing the components to work together as a single platform.

## Architecture Flow

```text
                         Yahoo Finance
                              │
                              ▼
                    APScheduler / ETL
                              │
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
        Machine Learning Pipeline          │
        (XGBoost / Random Forest)          │
                 │                         │
                 ▼                         │
            Model Registry                 │
                 │                         │
                 └────────────┬────────────┘
                              ▼
                       FastAPI Backend
                         │        │
                    REST API    WebSocket
                         │        │
                         └────┬───┘
                              ▼
                       Next.js Dashboard
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
              Interactive Charts   ML Predictions
                                  & Market Signals
