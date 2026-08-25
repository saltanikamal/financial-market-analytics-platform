import math
import pandas as pd

from app.ml.registry.model_registry import ModelRegistry
from app.ml.utils import load_model
from app.ml.data_loader import load_stock_data
from app.ml.feature_engineering import add_features


# =====================================
# SIGNAL MAPPING
# =====================================

def get_signal(predicted_class):
    """
    Convert classification output into trading signal.

    Classes:
        0 = Bearish / SELL
        1 = Neutral / HOLD
        2 = Bullish / BUY
    """

    if predicted_class == 2:
        return "BUY"

    elif predicted_class == 0:
        return "SELL"

    else:
        return "HOLD"


# =====================================
# CONFIDENCE
# =====================================

def get_confidence(probability, margin):
    """
    Calculate prediction confidence.

    probability:
        Highest class probability.

    margin:
        Difference between highest and
        second-highest probability.
    """

    score = (
        probability * 0.7
        +
        margin * 0.3
    )

    confidence_score = round(
        score * 100,
        2
    )

    if confidence_score >= 75:
        confidence_level = "HIGH"

    elif confidence_score >= 50:
        confidence_level = "MEDIUM"

    else:
        confidence_level = "LOW"

    return (
        confidence_score,
        confidence_level
    )


# =====================================
# SAFE FLOAT
# =====================================

def safe_float(
    value,
    default=0.0
):
    """
    Convert a value to a JSON-safe float.

    NaN and Infinity are not valid JSON values.
    """

    try:

        value = float(value)

        if not math.isfinite(value):
            return default

        return value

    except (
        TypeError,
        ValueError
    ):

        return default


# =====================================
# CLEAN METRICS
# =====================================

def clean_metrics(metrics):
    """
    Convert model metrics into JSON-safe values.

    NaN and Infinity become None.
    """

    if not metrics:
        return {}

    cleaned = {}

    for key, value in metrics.items():

        if value is None:

            cleaned[key] = None

            continue

        try:

            numeric_value = float(value)

            if math.isfinite(
                numeric_value
            ):

                cleaned[key] = numeric_value

            else:

                cleaned[key] = None

        except (
            TypeError,
            ValueError
        ):

            cleaned[key] = value

    return cleaned


# =====================================
# CLASS PROBABILITY MAPPING
# =====================================

def map_class_probabilities(
    model,
    probabilities
):
    """
    Map predicted probabilities according
    to the model's actual class labels.

    Example:

        model.classes_ = [0, 1, 2]

    produces:

        bearish = P(0)
        neutral = P(1)
        bullish = P(2)

    For a two-class model:

        model.classes_ = [1, 2]

    produces:

        bearish = 0
        neutral = P(1)
        bullish = P(2)

    This prevents index errors such as:

        index 2 is out of bounds
    """

    class_probabilities = {
        0: 0.0,
        1: 0.0,
        2: 0.0
    }

    for class_id, probability in zip(
        model.classes_,
        probabilities
    ):

        class_id = int(
            class_id
        )

        if class_id in class_probabilities:

            class_probabilities[
                class_id
            ] = safe_float(
                probability
            )

    return class_probabilities


# =====================================
# MAIN PREDICTION
# =====================================

def predict(symbol):
    """
    Generate an ML prediction for a stock.

    Returns:

        symbol
        model_used
        model_version
        prediction_class
        signal
        probability
        confidence
        confidence_level
        probability_margin
        probabilities
        current_price
        metrics
    """

    symbol = symbol.upper()

    print(
        f"Predicting {symbol}"
    )

    # =================================
    # MODEL REGISTRY
    # =================================

    registry = ModelRegistry()

    model_info = registry.get_best_model(
        symbol
    )

    model_name = model_info[
        "model"
    ]

    version = model_info[
        "version"
    ]

    model_path = model_info[
        "path"
    ]

    metrics = model_info.get(
        "metrics",
        {}
    )

    features = model_info.get(
        "features",
        []
    )

    print(
        f"Using model: {model_name}"
    )

    print(
        f"Model version: {version}"
    )

    # =================================
    # LOAD MODEL
    # =================================

    model = load_model(
        model_path
    )

    # =================================
    # LOAD STOCK DATA
    # =================================

    df = load_stock_data(
        symbol
    )

    if df is None or df.empty:

        raise ValueError(
            f"No stock data available for {symbol}"
        )

    print(
        f"Raw rows: {len(df)}"
    )

    # =================================
    # FEATURE ENGINEERING
    # =================================

    df = add_features(
        df
    )

    if df is None or df.empty:

        raise ValueError(
            f"Feature engineering produced no data for {symbol}"
        )

    print(
        f"Rows after features: {len(df)}"
    )

    # =================================
    # LATEST ROW
    # =================================

    latest = df.iloc[-1]

    # =================================
    # VALIDATE FEATURES
    # =================================

    missing_features = [
        feature
        for feature in features
        if feature not in df.columns
    ]

    if missing_features:

        raise ValueError(
            f"Missing features for {symbol}: "
            f"{missing_features}"
        )

    # =================================
    # PREDICTION INPUT
    # =================================

    X = (
        df[features]
        .iloc[[-1]]
        .copy()
    )

    # =================================
    # PREDICT PROBABILITIES
    # =================================

    probabilities = model.predict_proba(
        X
    )[0]

    probabilities = [
        safe_float(
            probability
        )
        for probability in probabilities
    ]

    # =================================
    # MODEL CLASSES
    # =================================

    classes = [
        int(class_id)
        for class_id in model.classes_
    ]

    # =================================
    # PREDICTED CLASS
    # =================================

    predicted_index = max(
        range(
            len(probabilities)
        ),
        key=lambda i:
            probabilities[i]
    )

    predicted_class = classes[
        predicted_index
    ]

    # =================================
    # SORT PROBABILITIES
    # =================================

    sorted_probabilities = sorted(
        probabilities,
        reverse=True
    )

    max_probability = (
        sorted_probabilities[0]
    )

    if len(
        sorted_probabilities
    ) > 1:

        second_probability = (
            sorted_probabilities[1]
        )

    else:

        second_probability = 0.0

    margin = (
        max_probability
        -
        second_probability
    )

    # =================================
    # SIGNAL
    # =================================

    signal = get_signal(
        predicted_class
    )

    # =================================
    # CONFIDENCE
    # =================================

    confidence_score, confidence_level = (
        get_confidence(
            max_probability,
            margin
        )
    )

    # =================================
    # CURRENT PRICE
    # =================================

    current_price = safe_float(
        latest["close"]
    )

    # =================================
    # CLASS PROBABILITIES
    # =================================

    class_probabilities = (
        map_class_probabilities(
            model,
            probabilities
        )
    )

    # =================================
    # CLEAN METRICS
    # =================================

    cleaned_metrics = clean_metrics(
        metrics
    )

    # =================================
    # RESULT
    # =================================

    result = {

        "symbol": symbol,

        "model_used": model_name,

        "model_version": version,

        "prediction_class": predicted_class,

        "signal": signal,

        "probability": round(
            max_probability,
            4
        ),

        "confidence": confidence_score,

        "confidence_level": confidence_level,

        "probability_margin": round(
            margin,
            4
        ),

        "probabilities": {

            "bearish": round(
                class_probabilities.get(
                    0,
                    0.0
                ),
                4
            ),

            "neutral": round(
                class_probabilities.get(
                    1,
                    0.0
                ),
                4
            ),

            "bullish": round(
                class_probabilities.get(
                    2,
                    0.0
                ),
                4
            )
        },

        "current_price": current_price,

        "metrics": cleaned_metrics
    }

    return result
