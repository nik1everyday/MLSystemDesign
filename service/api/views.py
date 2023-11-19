from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

# Предполагаем, что функции load_oil_price_data и predict_data уже определены
from src.predict_data_baseline import predict_data
from src.load_data import load_oil_price_data

router = APIRouter()


class HistoricalAndPredictiveRequest(BaseModel):
    start_date: str  # Дата начала для исторических данных
    forecast_days: int  # Количество дней для прогноза


class CombinedResponse(BaseModel):
    date: str
    historical_value: Optional[float]
    predicted_value: Optional[float]


@router.post("/historical-and-predictive-data", response_model=List[CombinedResponse])
async def get_historical_and_predictive_data(request: HistoricalAndPredictiveRequest):
    try:
        start_date_str = datetime.strptime(request.start_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        historical_data = load_oil_price_data(start_date_str)

        current_date_str = datetime.now().strftime("%Y-%m-%d")
        forecast_data = predict_data(current_date_str, request.forecast_days)

        combined_data = []
        for index, row in historical_data.iterrows():
            combined_data.append({
                "date": index.strftime("%Y-%m-%d"),
                "historical_value": row.Close,
                "predicted_value": None
            })

        for index, row in forecast_data.iterrows():
            combined_data.append({
                "date": row.Date.strftime("%Y-%m-%d"),
                "predicted_value": row.Predicted_Close,
                "historical_value": None
            })

        return combined_data

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Invalid start date format: {ve}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in processing data: {str(e)}")
