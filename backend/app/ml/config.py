# app/ml/config.py

# ----------------------------
# General ML Settings
# ----------------------------
TEST_SIZE = 0.2
RANDOM_STATE = 42

# ----------------------------
# Target column name
# ----------------------------
TARGET = "target"

# ----------------------------
# Feature columns used for training + prediction
# MUST MATCH FeatureEngineer output
# ----------------------------
FEATURE_COLUMNS = [
    "close",
    "volume",
    "ma7",
    "ma20",
    "daily_return",
    "volatility",
    "volume_change",
]

# ----------------------------
# Model settings (future use)
# ----------------------------
MODEL_NAME = "xgboost"
