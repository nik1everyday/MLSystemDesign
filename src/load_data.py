import yfinance as yf

def load_oil_price_data(start: str):
    """
    Загрузить данные о ценах на нефть из Yahoo Finance.

    :return: DataFrame с данными о ценах на нефть.
    """
    try:
        oil_etf = yf.Ticker("USO")
        oil_price_data = oil_etf.history(period="1d", start=start)

        return oil_price_data
    except Exception as e:
        print(f"Произошла ошибка при загрузке данных: {str(e)}")
        return None
