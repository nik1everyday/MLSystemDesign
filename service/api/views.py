from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from statsmodels.tsa.api import SimpleExpSmoothing

from src.load_data import load_oil_price_data
from src.predict_data_baseline import predict_exp_smoothing_next_day

router = APIRouter()


@router.get("/oil_price/")
def get_oil_price(start_date: str, days: int):
    try:
        oil_data = load_oil_price_data(start_date)
        historical_data = {
            "dates": list(oil_data.index.strftime('%Y-%m-%d')),
            "values": list(oil_data['Close'].values)
        }

        smoothing_level = 0.9999999850987182
        model_exp_smoothing = SimpleExpSmoothing(oil_data['Close'].values, initialization_method="heuristic").fit(
            smoothing_level=smoothing_level, optimized=False
        )

        predicted_values = [predict_exp_smoothing_next_day(model_exp_smoothing) for _ in range(days)]
        predicted_dates = [(datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i + 1)).strftime('%Y-%m-%d') for
                           i in range(days)]

        forecast_data = {
            "dates": predicted_dates,
            "values": predicted_values
        }

        return {"historical_data": historical_data, "forecast_data": forecast_data}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
