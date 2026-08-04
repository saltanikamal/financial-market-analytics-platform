from fastapi import APIRouter
from app.services.yfinance_service import run_etl

router = APIRouter()

@router.get("/{symbol}")
def etl(symbol: str):
    return run_etl(symbol)
