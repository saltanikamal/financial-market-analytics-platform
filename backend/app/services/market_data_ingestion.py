import yfinance as yf
import pandas as pd

from app.models.stock_price import StockPrice


# ---------------------------------------------------
# Fetch data from Yahoo Finance
# ---------------------------------------------------
def fetch_stock_data(symbol: str, period: str = "1mo", interval: str = "1d"):
    """
    Downloads stock data using yfinance
    """
    df = yf.download(symbol, period=period, interval=interval)

    if df.empty:
        return pd.DataFrame()

    df = df.reset_index()

    return df


# ---------------------------------------------------
# Transform + Save into database
# ---------------------------------------------------
def fetch_and_store_data(symbol: str, db):
    """
    IMPORTANT:
    - db comes from SessionLocal() in scheduler
    - DO NOT commit here (scheduler handles commit/rollback)
    """

    df = fetch_stock_data(symbol)

    if df.empty:
        print(f"[WARN] No data fetched for {symbol}")
        return

    for _, row in df.iterrows():

        try:
            record = StockPrice(
                symbol=symbol,
                date=row["Date"].date() if "Date" in row else row["date"],
                open_price=float(row["Open"]),
                close_price=float(row["Close"]),
                high_price=float(row["High"]),
                low_price=float(row["Low"]),
                volume=int(row["Volume"]),
            )

            db.add(record)

        except Exception as e:
            print(f"[ERROR] Failed row insert for {symbol}: {e}")
            continue


# ---------------------------------------------------
# Optional helper (manual run outside scheduler)
# ---------------------------------------------------
def run_ingestion(symbols=None):
    """
    Used for manual testing (NOT scheduler)
    """
    from app.database.connection import SessionLocal

    if symbols is None:
        symbols = ["AAPL", "MSFT", "NVDA"]

    db = SessionLocal()

    try:
        for symbol in symbols:
            fetch_and_store_data(symbol, db)

        db.commit()

        print("[INFO] Ingestion completed successfully")

    except Exception as e:
        db.rollback()
        print("[ERROR] Ingestion failed:", e)

    finally:
        db.close()
