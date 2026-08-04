from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from app.ml.predictor import predict
from app.database.connection import get_db
from app.models.prediction_history import PredictionHistory

import traceback


router = APIRouter()


# =====================================================
# Generate Prediction + Save History
# =====================================================

@router.get("/{symbol}")
def get_prediction(
    symbol: str,
    db: Session = Depends(get_db)
):

    try:

        # Run ML prediction pipeline
        result = predict(symbol)


        # Save prediction result
        history = PredictionHistory(

            symbol=result["symbol"],

            model_name=result["model_used"],

            model_version=result["model_version"],

            prediction_class=result["prediction_class"],

            signal=result["signal"],

            probability=result["probability"],

            confidence=result["confidence"],

            confidence_level=result["confidence_level"],

            current_price=result["current_price"]

        )


        db.add(history)

        db.commit()

        db.refresh(history)


        return result


    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )



# =====================================================
# Prediction History
# =====================================================

@router.get("/history/{symbol}")
def get_prediction_history(
    symbol: str,
    limit: int = Query(
        10,
        description="Number of prediction records to return"
    ),
    db: Session = Depends(get_db)
):

    try:

        history = (

            db.query(PredictionHistory)

            .filter(
                PredictionHistory.symbol == symbol.upper()
            )

            .order_by(
                PredictionHistory.prediction_date.desc()
            )

            .limit(limit)

            .all()

        )


        if not history:

            raise HTTPException(
                status_code=404,
                detail=f"No prediction history found for {symbol}"
            )


        return history



    except HTTPException:

        raise


    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
