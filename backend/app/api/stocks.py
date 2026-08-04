from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models import StockPrice


router = APIRouter()


@router.get("")
def get_stocks(db: Session = Depends(get_db)):

    symbols = (
        db.query(StockPrice.symbol)
        .distinct()
        .order_by(StockPrice.symbol)
        .all()
    )

    return {
        "stocks": [
            symbol[0]
            for symbol in symbols
        ]
    }
