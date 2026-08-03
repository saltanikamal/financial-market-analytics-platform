# System Architecture

## Overview

The Financial Market Analytics Platform follows an end-to-end data science architecture combining data ingestion, database storage, machine learning, backend services, and frontend visualization.

## Architecture Flow

Yahoo Finance API -> ETL Pipeline -> PostgreSQL Database -> Feature Engineering -> Machine Learning Models (XGBoost / Random Forest) -> FastAPI Backend -> Next.js Dashboard
