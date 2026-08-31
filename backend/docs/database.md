# Database Architecture

## Overview

The Financial Market Analytics Platform uses PostgreSQL as the primary data storage system for historical financial market data.

The database provides persistent storage for OHLCV market information collected through the ETL pipeline and serves as the foundation for analytics, feature engineering, and machine learning workflows.

The database layer separates data storage from application logic, allowing backend services and machine learning components to access consistent and structured market data.

---

## Database Technology

The platform uses PostgreSQL as the primary relational database management system for storing and managing financial market data.

PostgreSQL was selected because it provides:

- Reliable structured data storage.
- Strong support for analytical queries.
- Data consistency through relational constraints.
- Scalability for growing historical datasets.

### ORM Integration

The backend communicates with PostgreSQL using SQLAlchemy.

SQLAlchemy provides:

- Database abstraction through Python models.
- Simplified query operations.
- Separation between application logic and database implementation.

### Database Role in the Platform

The database layer supports:

- Historical market data storage.
- Analytics API requests.
- Machine learning feature generation.
- Model training dataset preparation.

The database acts as the central data source connecting the ETL pipeline, backend services, and machine learning workflows.

---

## Schema Design

The database schema is designed to store historical financial market data in a structured format that supports analytics, visualization, and machine learning workflows.

The primary table used by the platform is the `stock_prices` table.

This table stores historical OHLCV data for multiple financial instruments.

### Schema Overview

```text
stock_prices

+----------------+
| id             |
| date           |
| symbol         |
| open           |
| high           |
| low            |
| close          |
| volume         |
+----------------+
```

### Design Considerations

The schema follows these principles:

- Each record represents one trading day for one financial instrument.
- Historical observations are stored chronologically.
- Multiple symbols are supported within the same table.
- The structure supports analytics queries and machine learning feature generation.

The schema provides a consistent data foundation for the ETL pipeline, backend services, and prediction workflows.

---

## Stock Prices Table

The `stock_prices` table stores historical market observations collected through the ETL pipeline.

Each row represents the trading information for a specific financial instrument on a specific date.

### Table Columns

| Column | Description |
|--------|-------------|
| id | Unique record identifier |
| date | Trading date |
| symbol | Financial instrument ticker symbol |
| open | Opening price |
| high | Highest price during the trading session |
| low | Lowest price during the trading session |
| close | Closing price |
| volume | Trading volume |

### Example Record

```text
Date        Symbol   Open     High     Low      Close
------------------------------------------------------
2026-07-27  AAPL     214.45   216.30   213.80   215.50
```

---

## Data Pipeline Integration

The database layer is integrated with the platform's end-to-end data pipeline.

Market data flows through several stages before being consumed by analytics and machine learning services.

### Data Ingestion Flow

```text
Yahoo Finance API
        |
        v
ETL Pipeline
        |
        v
Data Validation
        |
        v
PostgreSQL Database
        |
        v
Analytics and ML Services
```

### Database Workflow

The database participates in the following workflow:

1. Market data is collected through the ETL pipeline.
2. Data is validated before storage.
3. Historical OHLCV records are stored in PostgreSQL.
4. Backend analytics endpoints retrieve market data.
5. Machine learning workflows retrieve historical data for feature engineering.
6. Prediction services use processed market data to generate model predictions.

---

## Query Optimization

As the number of stored financial records increases, efficient database queries become important for maintaining application performance.

The platform uses database optimization strategies to improve retrieval speed for analytics and prediction services.

### Indexing Strategy

Indexes can be created on frequently queried columns:

- `symbol`
- `date`
- `(symbol, date)`

Example:

```sql
CREATE INDEX idx_stock_symbol_date
ON stock_prices(symbol, date);
```

A composite index on `symbol` and `date` can improve queries that retrieve historical data for a specific financial instrument over a time range.

---

## Data Integrity

Data integrity is important because historical market data is used by both analytics services and machine learning workflows.

The database design supports:

- Structured OHLCV records.
- Consistent ticker symbols.
- Trading-date tracking.
- Numeric market-price fields.
- Historical data retrieval by symbol and date.

Validation is also performed during the ETL process before market data is used by downstream services.

---

## Relationship to Machine Learning

PostgreSQL provides the historical dataset used by the machine learning pipeline.

The workflow is:

```text
PostgreSQL
     |
     v
Historical OHLCV Data
     |
     v
Feature Engineering
     |
     v
Training Dataset
     |
     v
Classification Models
     |
     v
Predictions
```

The machine learning pipeline generates technical and statistical features from historical market observations.

These features are then used by classification models to predict future market direction as:

- SELL
- HOLD
- BUY

The database therefore serves as an important data foundation for the machine learning workflow.

---

## Relationship to Backend Services

The FastAPI backend retrieves financial data from PostgreSQL for analytics and prediction endpoints.

The general request flow is:

```text
Next.js Dashboard
        |
        v
FastAPI Backend
        |
        v
SQLAlchemy
        |
        v
PostgreSQL
        |
        v
Historical Market Data
```

For prediction requests, the backend combines database data with the machine learning pipeline:

```text
Prediction Request
        |
        v
FastAPI
        |
        v
PostgreSQL
        |
        v
Feature Engineering
        |
        v
Registered ML Model
        |
        v
Prediction
        |
        v
Dashboard
```

---

## Future Improvements

The current PostgreSQL implementation provides a reliable foundation for financial data storage and analytics.

Future enhancements can improve scalability, performance, and real-time capabilities.

### Cloud Database Deployment

Potential improvements include:

- Migration to managed PostgreSQL services.
- Automated backups.
- High availability configuration.
- Cloud-based scaling.

### Real-Time Data Processing

The platform can be extended to support:

- Streaming market data ingestion.
- Real-time database updates.
- Event-driven processing pipelines.

### Advanced Data Architecture

Future improvements may include:

- Data warehouse integration for large-scale analytics.
- Separate analytical storage for historical datasets.
- Data partitioning strategies for long-term market data.

### Data Quality Monitoring

Additional capabilities could include:

- Automated data validation.
- Missing data detection.
- Anomaly monitoring.
- ETL pipeline quality metrics.
