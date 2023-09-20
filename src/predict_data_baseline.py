from statsmodels.tsa.api import SimpleExpSmoothing
from src.load_data import load_oil_price_data
import numpy as np


# Достанем исторические данные
start_date = "2023-03-20"  # Задайте дату начала в формате "гггг-мм-дд"
oil_data = load_oil_price_data(start_date)
train_data = oil_data['Close']


# Подготовим модель
smoothing_level = 0.9999999850987182
model_exp_smoothing = SimpleExpSmoothing(train_data, initialization_method="heuristic").fit(
    smoothing_level=smoothing_level, optimized=False
)


def predict_exp_smoothing_next_day():
    """
    Возвращает прогноз цены закрытия на следующий день

    :return: float цена на следующий день
    """
    try:
        return model_exp_smoothing.forecast(1).values[0]
    except Exception as ex:
        print(f'Произошла ошибка \n{ex}')
        return np.nan
