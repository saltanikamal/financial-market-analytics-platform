from fastapi import APIRouter, HTTPException
import math
import pandas as pd

from app.ml.data_loader import load_stock_data


router = APIRouter()


@router.get("/ohlc/{symbol}")
def get_ohlc(symbol: str):
    """
    Return complete historical OHLC data for a symbol.

    This endpoint is intended for dashboard visualization.
    It deliberately does not run the full ML feature-engineering
    pipeline because indicators such as MA200 and future_return
    would remove otherwise valid historical OHLC rows.

    The dashboard currently uses MA7 and MA20 to determine its
    simple trend signal, so those two indicators are calculated
    locally here.
    """

    try:

        # Load complete raw historical market data
        df = load_stock_data(symbol)

        if df.empty:
            return {
                "symbol": symbol,
                "available": False,
                "message": f"No historical data available for {symbol}",
                "data": []
            }

        # Ensure chronological ordering
        df = df.sort_values("date").copy()

        # Dashboard trend indicators
        df["ma7"] = (
            df["close"]
            .rolling(7)
            .mean()
        )

        df["ma20"] = (
            df["close"]
            .rolling(20)
            .mean()
        )

        # Convert dates to strings
        if "date" in df.columns:
            df["date"] = df["date"].astype(str)

        # Convert DataFrame to Python records
        records = df.to_dict(orient="records")

        # Replace NaN and infinite numeric values with None.
        # This ensures the response is valid JSON.
        for record in records:
            for key, value in record.items():

                # Handle None and NaN values
                if value is None or pd.isna(value):
                    record[key] = None
                    continue

                # Handle numeric infinity
                if isinstance(value, (int, float)):
                    if not math.isfinite(value):
                        record[key] = None

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
