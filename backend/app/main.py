from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import (
    analytics,
    etl,
    predictions,
    stocks,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.services.scheduler_service import scheduler, start_scheduler

    start_scheduler()

    yield

    if scheduler.running:
        scheduler.shutdown()

app = FastAPI(
    title="Financial Intelligence Platform",
    version="0.1.0",
    lifespan=lifespan,
)


# -------------------------------------------------
# CORS
# -------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------
# API ROUTERS
# -------------------------------------------------

app.include_router(
    predictions.router,
    prefix="/predict",
    tags=["Predictions"],
)


app.include_router(
    analytics.router,
    prefix="/analytics",
    tags=["Analytics"],
)


app.include_router(
    etl.router,
    prefix="/etl",
    tags=["ETL"],
)


app.include_router(
    stocks.router,
    prefix="/stocks",
    tags=["Stocks"],
)


# -------------------------------------------------
# HEALTH CHECK
# -------------------------------------------------

@app.get("/")
def root():
    return {
        "status": "ok",
        "application": "Financial Intelligence Platform",
        "version": "0.1.0",
    }
