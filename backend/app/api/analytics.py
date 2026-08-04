from fastapi import APIRouter, HTTPException
import pandas as pd

from app.ml.data_loader import load_stock_data
from app.ml.feature_engineering import add_features

router = APIRouter()


@router.get("/ohlc/{symbol}")
def get_ohlc(symbol: str):

    try:

        # Load raw historical prices
        df = load_stock_data(symbol)

        if df.empty:
            return {
                "symbol": symbol,
                "available": False,
                "message": f"No historical data available for {symbol}",
                "data": []
            }

        # Compute technical indicators
        df = add_features(df)

        # Convert NaN values to None for JSON serialization
        df = df.where(pd.notnull(df), None)

        # Convert dates to strings
        if "date" in df.columns:
            df["date"] = df["date"].astype(str)

        records = df.to_dict(orient="records")

        return {
            "symbol": symbol,
            "available": True,
            "count": len(records),
            "data": records
        }

    except ValueError as e:

        return {
            "symbol": symbol,
            "available": False,
            "message": str(e),
            "data": []
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
