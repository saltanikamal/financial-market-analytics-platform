from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
import logging

from app.database.connection import SessionLocal
from app.services.yfinance_service import YFinanceService

# ---------------------------
# Logger setup
# ---------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------
# Scheduler instance
# ---------------------------
scheduler = BackgroundScheduler()


# ---------------------------
# CORE ETL JOB
# ---------------------------
def run_ingestion_job():
    db: Session = SessionLocal()
    service = YFinanceService(db)

    try:
        symbols = ["AAPL", "MSFT", "NVDA", "SPY"]

        logger.info("🔥 SCHEDULER TRIGGERED INGESTION JOB")

        for symbol in symbols:
            logger.info(f"➡️ Calling ETL for {symbol}")

            service.run_etl(symbol)

        logger.info("✅ SCHEDULER JOB COMPLETED SUCCESSFULLY")

    except Exception as e:
        db.rollback()
        logger.error(f"❌ Scheduler ETL failed: {e}")

    finally:
        db.close()


# ---------------------------
# START SCHEDULER
# ---------------------------
def start_scheduler():
    if scheduler.running:
        logger.info("⚠️ Scheduler already running")
        return

    scheduler.add_job(
        run_ingestion_job,
        trigger="interval",
        minutes=15,        # production interval
        max_instances=1,
        coalesce=True
    )

    scheduler.start()

    logger.info("🟢 Scheduler started successfully (15-min interval)")


# ---------------------------
# STOP SCHEDULER
# ---------------------------
def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        logger.info("🔴 Scheduler stopped")
