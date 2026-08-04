import joblib
import numpy as np
import pandas as pd

from app.ml.data_loader import load_stock_data
from app.ml.feature_engineering import add_features


# ======================================
# CONFIG
# ======================================

SYMBOL = "AAPL"

MODEL_PATH = (
    "app/ml/models/latest/"
    "AAPL_xgboost_20260720_211454.pkl"
)


FEATURES = [
    "open",
    "high",
    "low",
    "close",
    "volume",
    "daily_return",
    "ma7",
    "ma20",
    "ma50",
    "ma100",
    "ma200",
    "ema12",
    "ema26",
    "ema_ratio",
    "price_ma20_ratio",
    "price_ma50_ratio",
    "return_lag1",
    "return_lag2",
    "return_lag3",
    "rsi",
    "macd",
    "macd_signal",
    "macd_histogram",
    "bb_middle",
    "bb_upper",
    "bb_lower",
    "bb_position",
    "momentum_10",
    "momentum_20",
    "trend_strength",
    "volatility",
    "volume_change",
    "high_low_range",
    "close_position"
]


# ======================================
# LOAD MODEL
# ======================================

print("\nLoading model...")

model = joblib.load(
    MODEL_PATH
)

print("Model loaded")


# ======================================
# LOAD DATA
# ======================================

print("\nLoading stock data...")

df = load_stock_data(
    SYMBOL
)


print(
    "Raw rows:",
    len(df)
)


# ======================================
# FEATURE ENGINEERING
# ======================================

df = add_features(df)


print(
    "Rows after features:",
    len(df)
)


# remove missing values

df = df.dropna()


print(
    "Rows after dropna:",
    len(df)
)


# ======================================
# GET LAST SAMPLE
# ======================================

X = df[
    FEATURES
]


latest = X.tail(1)


print("\nFeatures used:")
print(latest.columns.tolist())


print(
    "\nFeature count:",
    latest.shape[1]
)



# ======================================
# PREDICTION
# ======================================

prediction = model.predict(
    latest
)


probabilities = model.predict_proba(
    latest
)



print("\nPrediction class:")
print(prediction[0])


print("\nProbabilities:")
print(
    probabilities[0]
)


# ======================================
# CONFIDENCE
# ======================================

confidence = np.max(
    probabilities[0]
)


print(
    "\nConfidence:",
    round(float(confidence),4)
)


# map classes

classes = model.classes_


print("\nClass probabilities:")

for cls, prob in zip(
    classes,
    probabilities[0]
):
    print(
        f"Class {cls}: {prob:.4f}"
    )
