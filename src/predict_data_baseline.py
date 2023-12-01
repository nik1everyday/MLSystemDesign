import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from prophet import Prophet

from src.load_data import load_oil_price_data


def train_model():

    current_date = datetime.strptime(current_date_str, "%Y-%m-%d")

    three_months_earlier = current_date - relativedelta(months=3)
    three_months_earlier_str = three_months_earlier.strftime("%Y-%m-%d")

    oil_data = load_oil_price_data(three_months_earlier_str)

    train_data = pd.DataFrame(data=oil_data['Close'], index=oil_data.index)
    train_data.reset_index(inplace=True)
    train_data.rename(columns={'Date': 'ds', 'Close': 'y'}, inplace=True)
    train_data['ds'] = train_data['ds'].dt.tz_localize(None)

    try:
        model = Prophet(yearly_seasonality=True,
                        weekly_seasonality=True,
                        daily_seasonality=True,
                        seasonality_mode='multiplicative')
        model.fit(train_data)
        return model
    except Exception as e:
        logging.error(f"An error occurred during model fitting: {e}")
        raise


def predict_data(forecast_days: int, model):
    current_date_str = datetime.now().strftime("%Y-%m-%d")

    future = model.make_future_dataframe(periods=forecast_days, freq='d')
    forecast = model.predict(future)

    forecast_dates = pd.date_range(start=current_date_str, periods=forecast_days, freq='D')
    forecast_df = pd.DataFrame({'Date': forecast_dates, 'Predicted_Close': forecast.yhat[-forecast_days:]})

    return forecast_df
