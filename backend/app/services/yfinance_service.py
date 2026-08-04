import yfinance as yf
import pandas as pd
from datetime import datetime

from app.database.connection import SessionLocal
from app.models.stock_price import StockPrice


# =====================================
# NORMALIZE YFINANCE COLUMNS
# =====================================

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:

    if isinstance(df.columns, pd.MultiIndex):

        df.columns = [
            col[0].lower()
            if isinstance(col, tuple)
            else str(col).lower()
            for col in df.columns
        ]

    else:

        df.columns = [
            str(col).lower()
            for col in df.columns
        ]

    return df



# =====================================
# ETL PIPELINE
# =====================================

def run_etl(symbol: str):

    db = SessionLocal()

    try:

        print(f"\nDownloading {symbol}...")


        # ---------------------------------
        # Download 5 years of daily data
        # ---------------------------------

        df = yf.download(
            symbol,
            period="5y",
            interval="1d",
            auto_adjust=False,
            progress=False
        )


        if df.empty:

            raise ValueError(
                f"No data returned for {symbol}"
            )


        # ---------------------------------
        # Prepare dataframe
        # ---------------------------------

        df = df.reset_index()


        df.rename(
            columns={
                df.columns[0]: "date"
            },
            inplace=True
        )


        df = normalize_columns(df)


        print("Columns after normalization:")
        print(df.columns.tolist())



        required_columns = [

            "date",
            "open",
            "high",
            "low",
            "close",
            "volume"

        ]


        missing = [

            col
            for col in required_columns
            if col not in df.columns

        ]


        if missing:

            raise ValueError(
                f"Missing columns: {missing}"
            )



        # ---------------------------------
        # Convert numeric columns
        # ---------------------------------

        numeric_columns = [

            "open",
            "high",
            "low",
            "close",
            "volume"

        ]


        for col in numeric_columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )



        df.dropna(
            subset=numeric_columns,
            inplace=True
        )



        df["symbol"] = symbol.upper()



        # =================================
        # Basic technical features
        # =================================


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


        df["daily_return"] = (

            df["close"]
            .pct_change()

        )


        df["volatility"] = (

            df["daily_return"]
            .rolling(7)
            .std()

        )


        df.dropna(
            inplace=True
        )



        # =================================
        # Insert into PostgreSQL
        # =================================


        inserted = 0

        skipped = 0



        for _, row in df.iterrows():


            exists = (

                db.query(StockPrice)

                .filter(

                    StockPrice.symbol == symbol.upper(),

                    StockPrice.date == row["date"]

                )

                .first()

            )



            if exists:

                skipped += 1

                continue



            stock = StockPrice(

                symbol=symbol.upper(),

                date=row["date"],

                open_price=float(
                    row["open"]
                ),

                high_price=float(
                    row["high"]
                ),

                low_price=float(
                    row["low"]
                ),

                close_price=float(
                    row["close"]
                ),

                volume=int(
                    row["volume"]
                ),

                ma7=float(
                    row["ma7"]
                ),

                ma20=float(
                    row["ma20"]
                ),

                daily_return=float(
                    row["daily_return"]
                ),

                volatility=float(
                    row["volatility"]
                ),

                timestamp=datetime.utcnow()

            )


            db.add(stock)

            inserted += 1



        db.commit()



        result = {

            "symbol": symbol.upper(),

            "inserted": inserted,

            "skipped": skipped,

            "rows_processed": len(df),

            "start_date": str(
                df["date"].min()
            ),

            "end_date": str(
                df["date"].max()
            )

        }



        print(

            f"✅ {symbol}: "
            f"inserted {inserted} rows | "
            f"skipped {skipped}"

        )


        print(result)


        return result



    except Exception as e:


        db.rollback()


        print(
            f"❌ ETL failed for {symbol}: {e}"
        )


        raise



    finally:

        db.close()



# =====================================
# STANDALONE EXECUTION TEST
# =====================================

if __name__ == "__main__":


    print(
        "Starting yfinance ETL test..."
    )


    symbols = [

        "AAPL",
        "MSFT",
        "NVDA",
        "SPY"

    ]


    for symbol in symbols:


        try:


            run_etl(symbol)



        except Exception as e:


            print(

                f"{symbol} failed: {e}"

            )
