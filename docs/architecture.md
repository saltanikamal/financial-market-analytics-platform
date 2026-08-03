
# System Architecture

## Overview

The Financial Market Analytics Platform follows an end-to-end data science architecture combining data ingestion, database storage, machine learning, backend services, and frontend visualization.

## Architecture Flow

```text
Yahoo Finance API
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
(XGBoost / Random Forest)
        |
        v
FastAPI Backend
        |
        v
Next.js Dashboard
