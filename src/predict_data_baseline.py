from datetime import datetime, timedelta
import pandas as pd
from statsmodels.tsa.api import SimpleExpSmoothing

from src.load_data import load_oil_price_data


# Модифицированная функция прогнозирования
def predict_data(start_date: str, forecast_days: int):
    # Загрузка данных за последние 6 месяцев до start_date
    start_date_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    six_months_ago = start_date_datetime - timedelta(days=180)
    oil_data = load_oil_price_data(six_months_ago.strftime("%Y-%m-%d"))  # Использование функции загрузки данных
    train_data = oil_data['Close']

    # Обучение модели
    smoothing_level = 0.9999999850987182
    model = SimpleExpSmoothing(train_data, initialization_method="heuristic").fit(smoothing_level=smoothing_level, optimized=False)

    # Прогнозирование на указанное количество дней
    forecast = model.forecast(forecast_days)
    forecast_dates = pd.date_range(start=start_date, periods=forecast_days, freq='D')
    forecast_df = pd.DataFrame({'Date': forecast_dates, 'Predicted_Close': forecast.values})
    return forecast_df
