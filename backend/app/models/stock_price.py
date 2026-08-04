from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from datetime import datetime

from app.database.base import Base
from sqlalchemy import UniqueConstraint

class StockPrice(Base):
    __tablename__ = "stock_prices"
    __table_args__ = (
        UniqueConstraint("symbol", "date", name="uq_symbol_date"),
    )

    id = Column(Integer, primary_key=True, index=True)

    symbol = Column(String, index=True, nullable=False)
    date = Column(Date, index=True, nullable=False)

    open_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)

    volume = Column(Integer, nullable=True)

    # 🔥 ADD THESE (THIS FIXES YOUR ISSUE)
    ma7 = Column(Float, nullable=True)
    ma20 = Column(Float, nullable=True)

    daily_return = Column(Float, nullable=True)
    volatility = Column(Float, nullable=True)

    timestamp = Column(DateTime, default=datetime.utcnow)
