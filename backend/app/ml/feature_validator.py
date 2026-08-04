import pandas as pd

REQUIRED_FEATURES = [
    "close",
    "volume",
    "ma7",
    "ma20",
    "volatility",
    "daily_return"
]


class FeatureValidator:
    """
    Ensures ML input data is safe, complete, and model-ready.
    """

    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        if df is None or df.empty:
            raise ValueError("Input DataFrame is empty")

        # check missing columns
        missing = [col for col in REQUIRED_FEATURES if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required features: {missing}")

        # check NaN values
        if df[REQUIRED_FEATURES].isnull().any().any():
            raise ValueError("NaN values found in feature columns")

        # enforce numeric types
        for col in REQUIRED_FEATURES:
            df[col] = pd.to_numeric(df[col], errors="raise")

        return df
