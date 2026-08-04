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
        0 = Bearish
        1 = Neutral
        2 = Bullish
    """

    if predicted_class == 2:

        return "BUY"


    elif predicted_class == 0:

        return "SELL"


    else:

        return "HOLD"



def get_confidence(probability, margin):

    """
    Calculate prediction confidence.

    Parameters
    ----------
    probability:
        Highest predicted class probability.

    margin:
        Difference between highest and second highest
        class probabilities.

    Returns
    -------
    confidence_score:
        Numeric confidence percentage.

    confidence_level:
        HIGH / MEDIUM / LOW
    """

    score = (

        (probability * 0.7)

        +

        (margin * 0.3)

    )


    confidence_score = round(

        score * 100,

        2

    )


    if confidence_score >= 70:

        confidence_level = "HIGH"


    elif confidence_score >= 50:

        confidence_level = "MEDIUM"


    else:

        confidence_level = "LOW"



    return confidence_score, confidence_level




# =====================================
# FEATURE PREPARATION
# =====================================

def prepare_features(df, features):

    """
    Prepare latest feature row for prediction.
    """

    df = df.copy()



    # Normalize database columns

    if "close_price" in df.columns:

        df["close"] = df["close_price"]



    if "volume" in df.columns:

        df["volume"] = pd.to_numeric(

            df["volume"],

            errors="coerce"

        )



    if "close" in df.columns:

        df["close"] = pd.to_numeric(

            df["close"],

            errors="coerce"

        )



    # Technical indicators

    df = add_features(
        df
    )



    df = df.dropna()



    if df.empty:

        raise ValueError(

            "No data available after feature engineering"

        )



    latest = df.iloc[-1]



    X = pd.DataFrame(

        [latest[features]]

    )


    return X, latest




# =====================================
# MAIN PREDICT FUNCTION
# =====================================

def predict(symbol):

    """
    Generate multiclass stock prediction.

    Classes:

        0 -> Bearish
        1 -> Neutral
        2 -> Bullish

    Returns:
        prediction
        probabilities
        confidence
        trading signal
    """

    symbol = symbol.upper()



    print(
        f"\nPredicting {symbol}"
    )



    # ---------------------------------
    # Load best model
    # ---------------------------------

    registry = ModelRegistry()



    model_info = registry.get_best_model(

        symbol

    )



    model_path = model_info["path"]

    model_name = model_info["model"]

    version = model_info["version"]

    features = model_info["features"]



    print(
        f"Using model: {model_name}"
    )


    print(
        f"Model version: {version}"
    )



    # ---------------------------------
    # Load model
    # ---------------------------------

    model = load_model(

        model_path

    )



    # ---------------------------------
    # Load latest data
    # ---------------------------------

    df = load_stock_data(

        symbol

    )



    X, latest = prepare_features(

        df,

        features

    )



    # ---------------------------------
    # Probability prediction
    # ---------------------------------

    probabilities = model.predict_proba(

        X

    )[0]



    predicted_index = probabilities.argmax()



    predicted_class = int(

        model.classes_[

            predicted_index

        ]

    )



    sorted_probabilities = sorted(

        probabilities,

        reverse=True

    )



    max_probability = float(

        sorted_probabilities[0]

    )



    second_probability = float(

        sorted_probabilities[1]

    )



    margin = (

        max_probability

        -

        second_probability

    )



    signal = get_signal(

        predicted_class

    )



    confidence_score, confidence_level = get_confidence(

        max_probability,

        margin

    )



    current_price = float(

        latest["close"]

    )



    # ---------------------------------
    # Response
    # ---------------------------------

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

                float(probabilities[0]),

                4

            ),


            "neutral": round(

                float(probabilities[1]),

                4

            ),


            "bullish": round(

                float(probabilities[2]),

                4

            )

        },


        "current_price": current_price,


        "metrics": model_info.get(

            "metrics",

            {}

        )

    }



    return result




# =====================================
# TEST
# =====================================

if __name__ == "__main__":


    result = predict(

        "AAPL"

    )


    print("\nPrediction Result:")

    print(result)
