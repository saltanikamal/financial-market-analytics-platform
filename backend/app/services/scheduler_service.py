from apscheduler.schedulers.background import BackgroundScheduler

from app.services.yfinance_service import run_etl


# ============================================================
# STOCK UNIVERSE
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


# ============================================================
# SCHEDULER
# ============================================================

scheduler = BackgroundScheduler()


# ============================================================
# ETL JOB
# ============================================================

def scheduled_etl():
    """
    Run the complete 5-year ETL pipeline
    for the entire stock universe.
    """

    print(
        "\nStarting scheduled market-data ETL..."
    )

    run_etl(
        symbols=WATCHLIST,
        period="5y",
    )


# ============================================================
# START SCHEDULER
# ============================================================

def start_scheduler():

    if scheduler.running:

        print(
            "Scheduler already running."
        )

        return

    scheduler.add_job(
        scheduled_etl,
        trigger="interval",
        hours=1,
        id="market_data_etl",
        replace_existing=True,
        max_instances=1,
    )

    scheduler.start()

    print(
        "Market-data scheduler started."
    )

    print(
        f"Watching {len(WATCHLIST)} stocks."
    )


# ============================================================
# STOP SCHEDULER
# ============================================================

def stop_scheduler():

    if scheduler.running:

        scheduler.shutdown()

        print(
            "Market-data scheduler stopped."
        )
