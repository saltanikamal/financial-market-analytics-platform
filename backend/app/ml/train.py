import os
from datetime import datetime

import numpy as np

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)

from app.ml.data_loader import load_stock_data
from app.ml.feature_engineering import add_features

from app.ml.core.model_factory import ModelFactory
from app.ml.evaluation.walk_forward import walk_forward_validation
from app.ml.registry.model_registry import ModelRegistry


# ==========================================
# CONFIGURATION
# ==========================================

SYMBOLS = [
    "AAPL",
    "AMD",
    "AMZN",
    "AVGO",
    "BAC",
    "CAT",
    "COST",
    "CVX",
    "DIA",
    "GE",
    "GOOGL",
    "GS",
    "HD",
    "JNJ",
    "JPM",
    "LLY",
    "MA",
    "META",
    "MS",
    "MSFT",
    "NFLX",
    "NVDA",
    "ORCL",
    "QQQ",
    "SPY",
    "TSLA",
    "UNH",
    "V",
    "WMT",
    "XOM",
]


MODELS = [
    "xgboost",
    "random_forest",
]


# ==========================================
# FEATURES
# MUST MATCH feature_engineering.py
# ==========================================

FEATURES = [

    "open",
    "high",
    "low",
    "close",
    "volume",

    "daily_return",

    "return_5d",
    "return_10d",
    "return_20d",

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

    "trend_strength",

    "return_lag1",
    "return_lag2",
    "return_lag3",
    "return_lag5",

    "rsi",

    "macd",
    "macd_signal",
    "macd_histogram",

    "bb_middle",
    "bb_upper",
    "bb_lower",
    "bb_position",

    "atr",
    "adx",
    "obv",

    "volume_change",

    "high_low_range",
    "close_position",
]


MODEL_DIR = "app/ml/models/latest"



# ==========================================
# JSON SAFE CONVERTER
# ==========================================

def json_safe(value):

    if isinstance(value, np.generic):
        return value.item()

    return value



# ==========================================
# TRAIN ONE MODEL
# ==========================================

def train_model(symbol, model_name):

    print("\n")
    print("=" * 70)
    print(f"Training {symbol} using {model_name}")
    print("=" * 70)



    # -------------------------------
    # Load data
    # -------------------------------

    df = load_stock_data(symbol)

    print(f"Raw rows: {len(df)}")



    # -------------------------------
    # Feature engineering
    # -------------------------------

    df = add_features(df)



    print(f"Rows after features: {len(df)}")

    print(df["target"].value_counts())



    df = df.dropna()



    # Check features

    missing = [
        col for col in FEATURES
        if col not in df.columns
    ]


    if missing:

        raise ValueError(
            f"Missing features: {missing}"
        )



    X = df[FEATURES]

    y = df["target"]



    print("\nTarget distribution")
    print(y.value_counts())


    print("\nClasses:")
    print(sorted(y.unique()))



    # -------------------------------
    # Time split
    # -------------------------------

    split = int(len(df) * 0.8)



    X_train = X.iloc[:split]

    X_test = X.iloc[split:]


    y_train = y.iloc[:split]

    y_test = y.iloc[split:]



    print(
        f"Training rows: {len(X_train)}"
    )


    print(
        f"Testing rows: {len(X_test)}"
    )



    # -------------------------------
    # Create model
    # -------------------------------

    model = ModelFactory.create_model(
        model_name
    )


    print("Created model")



    # -------------------------------
    # Walk Forward Validation
    # -------------------------------

    print(
        "\nRunning walk-forward validation..."
    )


    walk_results = walk_forward_validation(
        model,
        X_train,
        y_train
    )


    print(
        "\nWalk-forward results"
    )


    print(
        walk_results
    )



    # -------------------------------
    # Final Training
    # -------------------------------

    model.train(
        X_train,
        y_train
    )


    print(
        "Training completed"
    )



    # -------------------------------
    # Evaluation
    # -------------------------------

    predictions = model.predict(
        X_test
    )


    probabilities = None


    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(
            X_test
        )



    accuracy = accuracy_score(
        y_test,
        predictions
    )


    precision = precision_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )


    recall = recall_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )


    f1 = f1_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )



    roc_auc = 0



    if probabilities is not None:

        try:

            roc_auc = roc_auc_score(
                y_test,
                probabilities,
                multi_class="ovr"
            )


        except Exception:

            roc_auc = 0



    metrics = {

        "accuracy": float(accuracy),

        "precision": float(precision),

        "recall": float(recall),

        "f1": float(f1),

        "roc_auc": float(roc_auc),

    }



    print("\nFINAL RESULTS")


    for key, value in metrics.items():

        print(
            f"{key}: {value:.4f}"
        )



    print(
        "\nConfusion Matrix"
    )


    print(
        confusion_matrix(
            y_test,
            predictions
        )
    )



    print(
        "\nClassification Report"
    )


    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )



    # -------------------------------
    # Feature importance
    # -------------------------------

    if hasattr(
        model,
        "get_feature_importance"
    ):

        importance = model.get_feature_importance(
            FEATURES
        )


        print(
            "\nTop Features"
        )


        for feature, score in list(
            importance.items()
        )[:10]:

            print(
                f"{feature}: {score:.4f}"
            )



    # -------------------------------
    # Save model
    # -------------------------------

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )


    filename = (
        f"{symbol}_{model_name}_{timestamp}.pkl"
    )


    path = os.path.join(
        MODEL_DIR,
        filename
    )


    os.makedirs(
        MODEL_DIR,
        exist_ok=True
    )



    model.save(
        path
    )


    print(
        f"\nSaved model: {path}"
    )



    # -------------------------------
    # Register model
    # -------------------------------

    registry = ModelRegistry()


    registry.register_model(
        symbol,
        model_name,
        timestamp,
        path,
        metrics,
        FEATURES
    )


    print(
        "Model registered successfully"
    )



# ==========================================
# MAIN PIPELINE
# ==========================================

def main():

    print(
        "\nStarting classification training pipeline..."
    )


    for symbol in SYMBOLS:


        for model_name in MODELS:


            try:

                train_model(
                    symbol,
                    model_name
                )


            except Exception as e:

                print(
                    f"ERROR {symbol} {model_name}: {e}"
                )



if __name__ == "__main__":

    main()
