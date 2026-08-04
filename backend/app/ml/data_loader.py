import pandas as pd

from app.models.stock_price import StockPrice
from app.database.connection import SessionLocal


def load_stock_data(symbol: str) -> pd.DataFrame:
    """
    Load historical stock data for a given symbol from PostgreSQL.
    """

    db = SessionLocal()

    try:
        rows = (
            db.query(StockPrice)
            .filter(StockPrice.symbol == symbol)
            .order_by(StockPrice.date)
            .all()
        )

        if not rows:
            raise ValueError(f"No data found for symbol: {symbol}")

        data = [
            {
                "date": row.date,
                "symbol": row.symbol,
                "open": row.open_price,
                "high": row.high_price,
                "low": row.low_price,
                "close": row.close_price,
                "volume": row.volume,
            }
            for row in rows
        ]

        return pd.DataFrame(data)

    finally:
        db.close()


def get_symbols() -> list[str]:
    """
    Return all unique stock symbols stored in the database.
    """

    db = SessionLocal()

    try:
        symbols = (
            db.query(StockPrice.symbol)
            .distinct()
            .order_by(StockPrice.symbol)
            .all()
        )

        return [row[0] for row in symbols]

    finally:
        db.close()
