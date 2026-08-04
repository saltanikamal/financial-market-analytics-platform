# app/core/schema.py

import pandas as pd

REQUIRED_COLUMNS = [
    "date",
    "symbol",
    "open",
    "high",
    "low",
    "close",
    "volume",
]


def enforce_schema(df: pd.DataFrame) -> pd.DataFrame:
    """
    Forces all ETL outputs into a strict, consistent format.
    This is the SINGLE source of truth for all downstream layers.
    """

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]

    if missing:
        raise ValueError(f"Schema error - missing columns: {missing}")

    # enforce order + drop extra junk columns
    df = df[REQUIRED_COLUMNS].copy()

    return df
