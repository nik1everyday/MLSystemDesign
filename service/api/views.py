from fastapi import APIRouter, HTTPException
from starlette.responses import FileResponse
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from src.predict_data import train_model, predict_data
from src.load_data import load_oil_price_data

router = APIRouter()


class HistoricalAndPredictiveRequest(BaseModel):
    start_date: str
    forecast_days: int


class CombinedResponse(BaseModel):
    date: str
    historical_value: Optional[float]
    predicted_value: Optional[float]


model = train_model()


@router.post("/historical-and-predictive-data", response_model=List[CombinedResponse])
async def get_historical_and_predictive_data(request: HistoricalAndPredictiveRequest):
    try:
        start_date_str = datetime.strptime(request.start_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        historical_data = load_oil_price_data(start_date_str)

        forecast_data = predict_data(request.forecast_days, model)

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


@router.get('/')
async def get_frontend():
    """Получить фронт

    Returns:
        HTML: HTML-страница
    """
    return FileResponse("service/static/index.html")
