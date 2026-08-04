from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
)

from datetime import datetime

from app.database.base import Base

class PredictionHistory(Base):

    __tablename__ = "prediction_history"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    symbol = Column(
        String,
        nullable=False,
        index=True
    )


    prediction_date = Column(
        DateTime,
        default=datetime.utcnow
    )


    model_name = Column(
        String,
        nullable=False
    )


    model_version = Column(
        String,
        nullable=False
    )


    prediction_class = Column(
        Integer,
        nullable=False
    )


    signal = Column(
        String,
        nullable=False
    )


    probability = Column(
        Float,
        nullable=False
    )


    confidence = Column(
        Float,
        nullable=False
    )


    confidence_level = Column(
        String,
        nullable=False
    )


    current_price = Column(
        Float,
        nullable=False
    )
