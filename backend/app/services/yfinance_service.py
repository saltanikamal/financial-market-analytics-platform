import os
from datetime import datetime

import pandas as pd
import yfinance as yf
from sqlalchemy import text

from app.database.connection import SessionLocal


# ============================================================
# CONFIGURATION
# ============================================================

WATCHLIST = [
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

DEFAULT_PERIOD = "5y"
DEFAULT_INTERVAL = "1d"


# ============================================================
# DOWNLOAD MARKET DATA
# ============================================================

def download_stock_data(
    symbol: str,
    period: str = DEFAULT_PERIOD,
    interval: str = DEFAULT_INTERVAL,
) -> pd.DataFrame:
    """
    Download historical market data from Yahoo Finance.

    Default:
        5 years
        1 day interval
    """

    symbol = symbol.upper()

    print()
    print("=" * 70)
    print(
        f"Downloading {symbol} "
        f"({period}, {interval})"
    )
    print("=" * 70)

    df = yf.download(
        symbol,
        period=period,
        interval=interval,
        auto_adjust=False,
        progress=False,
    )

    if df is None or df.empty:
        print(
            f"{symbol}: No data returned from Yahoo Finance."
        )
        return pd.DataFrame()

    # --------------------------------------------------------
    # Handle Yahoo Finance MultiIndex columns
    # --------------------------------------------------------

    if isinstance(df.columns, pd.MultiIndex):

        df.columns = [
            str(column[0]).lower()
            for column in df.columns
        ]

    else:

        df.columns = [
            str(column).lower()
            for column in df.columns
        ]

    # --------------------------------------------------------
    # Reset index
    # --------------------------------------------------------

    df = df.reset_index()

    # Yahoo Finance can return Date or Datetime
    if "Date" in df.columns:

        df.rename(
            columns={"Date": "date"},
            inplace=True,
        )

    elif "Datetime" in df.columns:

        df.rename(
            columns={"Datetime": "date"},
            inplace=True,
        )

    # Normalize all column names
    df.columns = [
        str(column).lower()
        for column in df.columns
    ]

    # --------------------------------------------------------
    # Required Yahoo Finance columns
    # --------------------------------------------------------

    required_columns = [
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            f"{symbol}: Missing columns: "
            f"{missing_columns}"
        )

    df = df[
        required_columns
    ].copy()

    # --------------------------------------------------------
    # Normalize dates
    # --------------------------------------------------------

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce",
    )

    # Remove timezone if present
    if hasattr(df["date"].dt, "tz"):

        if df["date"].dt.tz is not None:

            df["date"] = (
                df["date"]
                .dt
                .tz_localize(None)
            )

    # Store only calendar date
    df["date"] = df["date"].dt.date

    # --------------------------------------------------------
    # Numeric conversion
    # --------------------------------------------------------

    numeric_columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    # --------------------------------------------------------
    # Remove invalid rows
    # --------------------------------------------------------

    df.dropna(
        subset=required_columns,
        inplace=True,
    )

    # --------------------------------------------------------
    # Remove duplicate dates
    # --------------------------------------------------------

    df.drop_duplicates(
        subset=["date"],
        keep="last",
        inplace=True,
    )

    # --------------------------------------------------------
    # Sort by date
    # --------------------------------------------------------

    df.sort_values(
        "date",
        inplace=True,
    )

    df.reset_index(
        drop=True,
        inplace=True,
    )

    print(
        f"{symbol}: downloaded "
        f"{len(df)} rows"
    )

    if not df.empty:

        print(
            f"{symbol}: "
            f"{df['date'].min()} -> "
            f"{df['date'].max()}"
        )

    return df


# ============================================================
# UPDATE EXISTING DATABASE ROWS
# ============================================================

def update_existing_rows(
    symbol: str,
    df: pd.DataFrame,
) -> int:
    """
    Update existing rows in PostgreSQL.

    IMPORTANT:
    The PostgreSQL table uses:

        open_price
        high_price
        low_price
        close_price
        volume

    not:

        open
        high
        low
        close
    """

    symbol = symbol.upper()

    if df.empty:
        return 0

    db = SessionLocal()

    updated = 0

    try:

        for _, row in df.iterrows():

            result = db.execute(
                text(
                    """
                    UPDATE stock_prices
                    SET
                        open_price = :open_price,
                        high_price = :high_price,
                        low_price = :low_price,
                        close_price = :close_price,
                        volume = :volume
                    WHERE symbol = :symbol
                    AND date = :date
                    RETURNING symbol
                    """
                ),
                {
                    "symbol": symbol,
                    "date": row["date"],
                    "open_price": float(row["open"]),
                    "high_price": float(row["high"]),
                    "low_price": float(row["low"]),
                    "close_price": float(row["close"]),
                    "volume": int(row["volume"]),
                },
            )

            if result.fetchone():

                updated += 1

        db.commit()

        print(
            f"{symbol}: updated "
            f"{updated} existing rows"
        )

        return updated

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()


# ============================================================
# INSERT MISSING DATABASE ROWS
# ============================================================

def save_stock_data(
    symbol: str,
    df: pd.DataFrame,
) -> int:
    """
    Insert missing historical rows into PostgreSQL.

    Existing dates are skipped.

    PostgreSQL schema:

        symbol
        date
        open_price
        high_price
        low_price
        close_price
        volume
    """

    symbol = symbol.upper()

    if df.empty:

        print(
            f"{symbol}: Nothing to save."
        )

        return 0

    db = SessionLocal()

    inserted = 0
    skipped = 0

    try:

        for _, row in df.iterrows():

            # ------------------------------------------------
            # Check whether row already exists
            # ------------------------------------------------

            result = db.execute(
                text(
                    """
                    SELECT 1
                    FROM stock_prices
                    WHERE symbol = :symbol
                    AND date = :date
                    LIMIT 1
                    """
                ),
                {
                    "symbol": symbol,
                    "date": row["date"],
                },
            ).fetchone()

            if result:

                skipped += 1

                continue

            # ------------------------------------------------
            # Insert missing row
            # ------------------------------------------------

            db.execute(
                text(
                    """
                    INSERT INTO stock_prices
                    (
                        symbol,
                        date,
                        open_price,
                        high_price,
                        low_price,
                        close_price,
                        volume
                    )
                    VALUES
                    (
                        :symbol,
                        :date,
                        :open_price,
                        :high_price,
                        :low_price,
                        :close_price,
                        :volume
                    )
                    """
                ),
                {
                    "symbol": symbol,
                    "date": row["date"],
                    "open_price": float(row["open"]),
                    "high_price": float(row["high"]),
                    "low_price": float(row["low"]),
                    "close_price": float(row["close"]),
                    "volume": int(row["volume"]),
                },
            )

            inserted += 1

        db.commit()

        print(
            f"{symbol}: "
            f"inserted {inserted} rows | "
            f"skipped {skipped}"
        )

        return inserted

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()


# ============================================================
# DATABASE COVERAGE
# ============================================================

def get_database_coverage(
    symbol: str,
):
    """
    Return row count and date range for a symbol.
    """

    symbol = symbol.upper()

    db = SessionLocal()

    try:

        result = db.execute(
            text(
                """
                SELECT
                    COUNT(*) AS row_count,
                    MIN(date) AS start_date,
                    MAX(date) AS end_date
                FROM stock_prices
                WHERE symbol = :symbol
                """
            ),
            {
                "symbol": symbol,
            },
        ).fetchone()

        return result

    finally:

        db.close()


# ============================================================
# COMPLETE ETL FOR ONE STOCK
# ============================================================

def run_etl_for_symbol(
    symbol: str,
    period: str = DEFAULT_PERIOD,
):
    """
    Complete ETL process for one stock.

    1. Download 5 years from Yahoo Finance
    2. Clean the data
    3. Update existing database rows
    4. Insert missing historical rows
    5. Verify database coverage
    """

    symbol = symbol.upper()

    print()
    print("#" * 70)
    print(f"ETL START: {symbol}")
    print("#" * 70)

    # --------------------------------------------------------
    # Download
    # --------------------------------------------------------

    df = download_stock_data(
        symbol=symbol,
        period=period,
        interval=DEFAULT_INTERVAL,
    )

    if df.empty:

        print(
            f"{symbol}: No data available."
        )

        return

    # --------------------------------------------------------
    # Update existing rows
    # --------------------------------------------------------

    updated = update_existing_rows(
        symbol=symbol,
        df=df,
    )

    # --------------------------------------------------------
    # Insert missing historical rows
    # --------------------------------------------------------

    inserted = save_stock_data(
        symbol=symbol,
        df=df,
    )

    # --------------------------------------------------------
    # Verify database
    # --------------------------------------------------------

    result = get_database_coverage(
        symbol
    )

    print()
    print(
        f"{symbol} DATABASE COVERAGE"
    )
    print("-" * 50)

    print(
        f"Rows:     {result.row_count}"
    )

    print(
        f"Start:    {result.start_date}"
    )

    print(
        f"End:      {result.end_date}"
    )

    print(
        f"Inserted: {inserted}"
    )

    print(
        f"Updated:  {updated}"
    )

    print()
    print(
        f"ETL COMPLETE: {symbol}"
    )


# ============================================================
# RUN ETL FOR ALL STOCKS
# ============================================================

def run_etl(
    symbols=None,
    period: str = DEFAULT_PERIOD,
):
    """
    Run ETL for all stocks.

    Default:
        All 30 stocks
        5 years
        Daily data
    """

    if symbols is None:

        symbols = WATCHLIST

    print()
    print("=" * 70)
    print("STARTING YFINANCE ETL")
    print("=" * 70)

    print(
        f"Stocks: {len(symbols)}"
    )

    print(
        f"Historical period: {period}"
    )

    print(
        f"Interval: {DEFAULT_INTERVAL}"
    )

    start_time = datetime.now()

    successful = []
    failed = []

    # --------------------------------------------------------
    # Process each stock
    # --------------------------------------------------------

    for symbol in symbols:

        try:

            run_etl_for_symbol(
                symbol=symbol,
                period=period,
            )

            successful.append(
                symbol
            )

        except Exception as error:

            print()
            print(
                f"ERROR processing "
                f"{symbol}: {error}"
            )

            failed.append(
                (
                    symbol,
                    str(error),
                )
            )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    duration = (
        datetime.now()
        - start_time
    )

    print()
    print("=" * 70)
    print("ETL COMPLETE")
    print("=" * 70)

    print(
        f"Successful: {len(successful)}"
    )

    print(
        f"Failed: {len(failed)}"
    )

    print(
        f"Duration: {duration}"
    )

    if failed:

        print()
        print("Failed stocks:")

        for symbol, error in failed:

            print(
                f"{symbol}: {error}"
            )


# ============================================================
# TEST ENTRY POINT
# ============================================================

if __name__ == "__main__":

    run_etl()
