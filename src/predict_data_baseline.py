import logging
from datetime import datetime, timedelta
import pandas as pd
from prophet import Prophet

from src.load_data import load_oil_price_data


def predict_data(start_date: str, forecast_days: int):
    logging.basicConfig(level=logging.INFO)

    start_date_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    six_months_ago = start_date_datetime - timedelta(days=180)

    oil_data = load_oil_price_data(six_months_ago.strftime("%Y-%m-%d"))

    oil_data.dropna(inplace=True)
    train_data = pd.DataFrame(data=oil_data['Close'], index=oil_data.index)
    train_data.reset_index(inplace=True)
    train_data.rename(columns={'Date': 'ds', 'Close': 'y'}, inplace=True)
    train_data['ds'] = train_data['ds'].dt.tz_localize(None)

    try:
        model = Prophet(yearly_seasonality=True, daily_seasonality=True, seasonality_mode='multiplicative')
        model.fit(train_data)
    except Exception as e:
        logging.error(f"An error occurred during model fitting: {e}")
        return None

    future = model.make_future_dataframe(periods=forecast_days, freq='d')
    forecast = model.predict(future)

    forecast_dates = pd.date_range(start=start_date, periods=forecast_days, freq='D')
    forecast_df = pd.DataFrame({'Date': forecast_dates, 'Predicted_Close': forecast.yhat[-forecast_days:]})

    return forecast_df
