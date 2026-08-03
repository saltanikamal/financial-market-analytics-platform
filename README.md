# financial-market-analytics-platform
📈 Financial Market Analytics Platform

An end-to-end financial data science platform that automates market data collection, feature engineering, machine learning, and interactive visualization.

⸻

Overview

The Financial Market Analytics Platform is an end-to-end data science project designed to demonstrate the complete machine learning lifecycle using historical stock market data.

The platform automatically collects market data, stores it in a PostgreSQL database, engineers technical indicators, trains machine learning models to classify future market movements into Buy, Hold, and Sell signals, and exposes predictions through a FastAPI backend. A modern Next.js dashboard provides interactive candlestick charts, technical indicators, and analytics for exploring the results.

Rather than focusing solely on building a prediction model, this project showcases the integration of data engineering, machine learning, backend development, database management, and frontend visualization into a single production-style application.

⸻

Key Features

* Automated ETL pipeline for historical stock market data
* PostgreSQL database for reliable data storage
* Feature engineering with 30+ technical indicators
* Machine learning using XGBoost and Random Forest classifiers
* Walk-forward validation for time-series evaluation
* Model registry for version management
* FastAPI REST API for analytics and prediction services
* Interactive Next.js dashboard with candlestick charts
* Modular architecture separating data, ML, backend, and frontend components

⸻

Tech Stack

Category	Technologies
Programming	Python, TypeScript
Data Processing	Pandas, NumPy
Machine Learning	Scikit-learn, XGBoost
Backend	FastAPI
Frontend	Next.js, React
Database	PostgreSQL
Visualization	Lightweight Charts, Matplotlib
Scheduling	APScheduler
Version Control	Git, GitHub
