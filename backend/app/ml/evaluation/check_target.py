from app.ml.data_loader import load_stock_data
from app.ml.feature_engineering import add_features


SYMBOL = "AAPL"


def main():

    print(f"Checking target distribution for {SYMBOL}")


    df = load_stock_data(SYMBOL)

    print(
        f"Raw rows: {len(df)}"
    )


    df = add_features(df)


    print(
        f"Rows after features: {len(df)}"
    )


    print("\nTarget statistics:")
    print(
        df["target"].describe()
    )


    print("\nTarget examples:")

    print(
        df[
            [
                "date",
                "close",
                "target"
            ]
        ].tail(20)
    )


if __name__ == "__main__":
    main()
