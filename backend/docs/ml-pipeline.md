# Machine Learning Pipeline

## Overview

The Financial Market Analytics Platform uses a machine learning pipeline to predict future market direction based on historical financial data and engineered technical indicators.

The pipeline transforms raw market data into machine-learning features, trains classification models, evaluates performance using time-series validation techniques, and registers trained models for prediction services.

The objective is to classify future market movements into three categories:

- BUY
- HOLD
- SELL

---

## Data Preparation

The data preparation stage converts raw market data into a structured dataset suitable for machine learning.

The pipeline begins with historical OHLCV data stored in PostgreSQL and prepares it for feature engineering and model training.

### Data Sources

The platform uses historical market data containing:

- Date
- Symbol
- Open price
- High price
- Low price
- Closing price
- Trading volume

### Data Processing Steps

The preparation workflow includes:

1. Loading historical market data from PostgreSQL.
2. Sorting data chronologically by trading date.
3. Handling missing values.
4. Removing invalid records.
5. Preparing time-series datasets for feature generation.

Because financial data is sequential, the pipeline preserves chronological order to prevent future information from leaking into the training process.

---

## Feature Engineering

Feature engineering transforms historical market data into numerical features that can be used by machine learning models.

The platform generates technical indicators and statistical features that capture price behavior, momentum, volatility, and market trends.

### Price-Based Features

The pipeline creates features based on historical price movements:

- Daily returns
- Multi-day returns (5-day, 10-day, 20-day)
- Lagged price values
- Candlestick patterns

### Trend Indicators

The platform calculates moving averages to identify market trends:

- Moving Average (MA7)
- Moving Average (MA20)
- Moving Average (MA50)
- Moving Average (MA100)
- Moving Average (MA200)
- Exponential Moving Average (EMA12)
- Exponential Moving Average (EMA26)

### Momentum Indicators

Momentum-based features include:

- Relative Strength Index (RSI)
- MACD
- Momentum indicators

### Volatility Features

The pipeline includes measures of market risk and price variability:

- Rolling volatility
- Bollinger Bands
- Price range features

### Volume Features

Trading activity is represented using:

- Volume changes
- Volume-based indicators

These engineered features create the input dataset used by the machine learning classification models.

---

## Target Generation

The target generation stage defines the prediction objective for the machine learning models.

Instead of predicting exact future prices, the platform performs a classification task by predicting future market direction.

### Prediction Horizon

The model predicts market movement over a future time window.

The target is generated using future returns:

---

## Model Training

The model training stage uses engineered financial features to train machine learning classifiers capable of predicting future market direction.

The training pipeline separates feature preparation, model fitting, evaluation, and model storage to support reproducible experiments.

### Training Workflow

The training process follows these steps:

1. Load prepared feature datasets.
2. Split data while preserving chronological order.
3. Train machine learning models.
4. Evaluate model performance.
5. Store trained models and metadata.

### Models Implemented

The platform currently supports two classification algorithms:

### XGBoost Classifier

XGBoost is used as the primary machine learning model because of its strong performance on structured tabular data and its ability to capture complex relationships between financial features.

Advantages:

- Handles nonlinear relationships.
- Works well with engineered features.
- Provides feature importance information.
- Supports multiclass classification.

### Random Forest Classifier

Random Forest provides an additional tree-based model for comparison and evaluation.

Advantages:

- Robust against overfitting.
- Handles mixed feature types.
- Provides a baseline ensemble approach.

### Model Output

The models generate probabilities for three possible market states:

- SELL
- HOLD
- BUY

The prediction service uses these outputs to generate the final trading signal and confidence score.


---

## Model Validation

Financial market data is time-dependent, meaning future observations must not be used during model training.

To address this challenge, the platform uses time-series validation techniques instead of traditional random train/test splitting.

### Walk-Forward Validation

The validation process follows a rolling evaluation approach:

---

## Model Evaluation

The model evaluation stage measures how well the classification models predict future market direction.

Because the platform performs a multiclass classification task, multiple evaluation metrics are used to understand different aspects of model performance.

### Evaluation Metrics

#### Accuracy

Measures the percentage of correct predictions across all classes.

Accuracy provides an overall view of model performance but may not fully represent performance when classes are imbalanced.

#### Precision

Measures how many predicted signals were correct.

For example:

- Of all predicted BUY signals, how many were actually BUY?

#### Recall

Measures how many actual signals were successfully identified.

For example:

- Of all actual BUY opportunities, how many did the model detect?

#### F1-Score

The F1-score combines precision and recall into a single metric and provides a balanced measure of classification performance.

#### ROC-AUC

ROC-AUC measures the model's ability to distinguish between different market direction classes.

### Confusion Matrix

The confusion matrix provides detailed insight into prediction errors by showing:

- Correct predictions.
- False BUY signals.
- Missed BUY opportunities.
- Incorrect HOLD or SELL predictions.

This analysis helps identify model weaknesses and guides future improvements.

---

## Model Registry

The model registry manages trained machine learning models throughout their lifecycle.

Instead of replacing models manually, the platform stores model versions and associated metadata to support reproducibility, comparison, and future improvements.

### Registry Responsibilities

The model registry handles:

- Saving trained model files.
- Tracking model versions.
- Storing training metadata.
- Recording evaluation metrics.
- Selecting models for prediction.

### Stored Metadata

Each registered model contains information such as:

- Model type
- Symbol
- Version identifier
- Training timestamp
- Feature set
- Performance metrics
- Model file path

### Model Selection

When generating predictions, the platform retrieves the appropriate registered model based on:

- Financial instrument.
- Model availability.
- Model version information.

The registry provides a foundation for future MLOps capabilities such as automated retraining, model comparison, and deployment monitoring.

---

## Prediction Workflow

The prediction workflow connects the trained machine learning models with the application layer to generate market direction signals.

When a prediction request is received, the platform processes the latest available market data and applies the registered machine learning model.

### Prediction Steps

### 1. Data Retrieval

The system retrieves the latest historical market data for the requested financial instrument.

### 2. Feature Generation

The same feature engineering pipeline used during training is applied to new data to ensure consistency between training and inference.

### 3. Model Loading

The prediction service loads the selected model from the model registry.

### 4. Prediction Generation

The model produces probability scores for each market class:

- SELL
- HOLD
- BUY

### 5. Signal Generation

The highest probability class is converted into the final market signal.

The prediction response includes:

- Symbol
- Predicted signal
- Confidence score
- Model version

### Prediction Flow

```text
Latest Market Data
        |
        v
Feature Engineering
        |
        v
Registered ML Model
        |
        v
Prediction Probabilities
        |
        v
BUY / HOLD / SELL Signal
        |
        v
FastAPI Response
