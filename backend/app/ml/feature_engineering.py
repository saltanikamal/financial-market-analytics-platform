import numpy as np
import pandas as pd


# =====================================
# CONFIGURATION
# =====================================

PREDICTION_HORIZON = 5

BUY_THRESHOLD = 0.02

SELL_THRESHOLD = -0.02



def add_features(df):

    df = df.copy()


    print(f"Raw rows: {len(df)}")


    # =====================================
    # SORT DATA
    # =====================================

    df = df.sort_values(
        "date"
    )



    # =====================================
    # DAILY RETURNS
    # =====================================

    df["daily_return"] = (

        df["close"]
        .pct_change()

    )


    # Multi-period returns

    for period in [5,10,20]:

        df[f"return_{period}d"] = (

            df["close"]
            .pct_change(period)

        )



    # =====================================
    # MOVING AVERAGES
    # =====================================

    for window in [7,20,50,100,200]:

        df[f"ma{window}"] = (

            df["close"]
            .rolling(window)
            .mean()

        )



    # =====================================
    # EMA FEATURES
    # =====================================

    df["ema12"] = (

        df["close"]
        .ewm(span=12, adjust=False)
        .mean()

    )


    df["ema26"] = (

        df["close"]
        .ewm(span=26, adjust=False)
        .mean()

    )


    df["ema_ratio"] = (

        df["ema12"]
        /
        df["ema26"]

    )



    # =====================================
    # PRICE VS TREND
    # =====================================

    df["price_ma20_ratio"] = (

        df["close"]
        /
        df["ma20"]

    )


    df["price_ma50_ratio"] = (

        df["close"]
        /
        df["ma50"]

    )


    df["trend_strength"] = (

        df["ma20"]
        /
        df["ma50"]
        - 1

    )



    # =====================================
    # LAG FEATURES
    # =====================================

    for lag in [1,2,3,5]:

        df[f"return_lag{lag}"] = (

            df["daily_return"]
            .shift(lag)

        )



    # =====================================
    # RSI (WILDER RSI)
    # =====================================

    delta = df["close"].diff()


    gain = delta.clip(
        lower=0
    )


    loss = -delta.clip(
        upper=0
    )


    avg_gain = (

        gain
        .ewm(
            alpha=1/14,
            adjust=False
        )
        .mean()

    )


    avg_loss = (

        loss
        .ewm(
            alpha=1/14,
            adjust=False
        )
        .mean()

    )


    rs = avg_gain / avg_loss


    df["rsi"] = (

        100 -
        (100 / (1 + rs))

    )



    # =====================================
    # MACD
    # =====================================

    df["macd"] = (

        df["ema12"]
        -
        df["ema26"]

    )


    df["macd_signal"] = (

        df["macd"]
        .ewm(
            span=9,
            adjust=False
        )
        .mean()

    )


    df["macd_histogram"] = (

        df["macd"]
        -
        df["macd_signal"]

    )



    # =====================================
    # BOLLINGER BANDS
    # =====================================

    df["bb_middle"] = (

        df["close"]
        .rolling(20)
        .mean()

    )


    bb_std = (

        df["close"]
        .rolling(20)
        .std()

    )


    df["bb_upper"] = (

        df["bb_middle"]
        +
        2 * bb_std

    )


    df["bb_lower"] = (

        df["bb_middle"]
        -
        2 * bb_std

    )


    df["bb_position"] = (

        (df["close"] - df["bb_lower"])
        /
        (df["bb_upper"] - df["bb_lower"])

    )



    # =====================================
    # ATR - VOLATILITY
    # =====================================

    high_low = (

        df["high"]
        -
        df["low"]

    )


    high_close = (

        abs(
            df["high"]
            -
            df["close"].shift()
        )

    )


    low_close = (

        abs(
            df["low"]
            -
            df["close"].shift()
        )

    )


    true_range = pd.concat(
        [
            high_low,
            high_close,
            low_close
        ],
        axis=1
    ).max(axis=1)


    df["atr"] = (

        true_range
        .rolling(14)
        .mean()

    )



    # =====================================
    # ADX TREND STRENGTH
    # =====================================

    plus_dm = (

        df["high"]
        .diff()

    )


    minus_dm = (

        -df["low"]
        .diff()

    )


    plus_dm = plus_dm.where(

        (plus_dm > minus_dm) &
        (plus_dm > 0),

        0

    )


    minus_dm = minus_dm.where(

        (minus_dm > plus_dm) &
        (minus_dm > 0),

        0

    )


    tr14 = (

        true_range
        .rolling(14)
        .sum()

    )


    plus_di = (

        100 *
        plus_dm
        .rolling(14)
        .sum()
        /
        tr14

    )


    minus_di = (

        100 *
        minus_dm
        .rolling(14)
        .sum()
        /
        tr14

    )


    dx = (

        abs(
            plus_di - minus_di
        )
        /
        (plus_di + minus_di)

    )


    df["adx"] = (

        100 *
        dx
        .rolling(14)
        .mean()

    )



    # =====================================
    # OBV VOLUME INDICATOR
    # =====================================

    direction = np.where(

        df["close"]
        >
        df["close"].shift(),

        1,

        -1

    )


    df["obv"] = (

        direction *
        df["volume"]

    ).cumsum()



    df["volume_change"] = (

        df["volume"]
        .pct_change()

    )



    # =====================================
    # MOMENTUM
    # =====================================

    df["momentum_10"] = (

        df["close"]
        /
        df["close"].shift(10)
        - 1

    )


    df["momentum_20"] = (

        df["close"]
        /
        df["close"].shift(20)
        - 1

    )



    # =====================================
    # CANDLE FEATURES
    # =====================================

    df["high_low_range"] = (

        (df["high"] - df["low"])
        /
        df["close"]

    )


    df["close_position"] = (

        (df["close"] - df["low"])
        /
        (df["high"] - df["low"])

    )



    # =====================================
    # FUTURE TARGET
    # =====================================

    df["future_return"] = (

        df["close"]
        .shift(-PREDICTION_HORIZON)
        /
        df["close"]
        - 1

    )


    # =====================================
    # TARGET
    #
    # 0 SELL
    # 1 HOLD
    # 2 BUY
    #
    # =====================================

    df["target"] = 1


    df.loc[
        df["future_return"] > BUY_THRESHOLD,
        "target"
    ] = 2


    df.loc[
        df["future_return"] < SELL_THRESHOLD,
        "target"
    ] = 0



    # =====================================
    # CLEAN DATA
    # =====================================

    df = (

        df
        .replace(
            [np.inf, -np.inf],
            np.nan
        )
        .dropna()

    )


    print(
        f"Rows after features: {len(df)}"
    )


    print(
        df["target"]
        .value_counts()
    )


    return df
