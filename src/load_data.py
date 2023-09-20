import yfinance as yf
import pandas as pd


def load_oil_price_data(start: str) -> pd.DataFrame:
    """
    Загружает данные о ценах на нефть из Yahoo Finance.

    :param start: Начальная дата в формате 'гггг-мм-дд' для загрузки данных.
    :type start: str

    :return: DataFrame с данными о ценах на нефть,
             включая столбцы 'Open', 'High', 'Low', 'Close', 'Volume', и 'Dividends'.
    :rtype: pd.DataFrame
    """
    try:
        oil_etf = yf.Ticker("USO")
        oil_price_data = oil_etf.history(period="1d", start=start)

        return oil_price_data
    except Exception as e:
        print(f"Произошла ошибка при загрузке данных: {str(e)}")
        return pd.DataFrame()
