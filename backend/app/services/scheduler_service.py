from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging

from app.services.yfinance_service import run_etl
from app.ml.train import train_model, MODELS
logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

WATCHLIST = ["AAPL", "MSFT", "NVDA", "SPY"]


def ingest_all():
    logger.info("🔄 ETL start")

    for symbol in WATCHLIST:
        try:
            run_etl(symbol)
        except Exception as e:
            logger.error(f"ETL failed {symbol}: {e}")


def retrain_models():
    logger.info("🧠 Training start")

    for symbol in WATCHLIST:
        for model_name in MODELS:
            try:
                logger.info(
                    f"Training {model_name} for {symbol}"
                )

                train_model(symbol, model_name)

            except Exception as e:
                logger.error(
                    f"Training failed {symbol} {model_name}: {e}"
                )

def start_scheduler():

    if scheduler.running:
        return

    scheduler.add_job(ingest_all, IntervalTrigger(hours=1), id="etl")
    scheduler.add_job(retrain_models, IntervalTrigger(hours=24), id="train")

    scheduler.start()
