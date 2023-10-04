import pandas as pd
import numpy as np

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from src import load_data, predict_data_baseline

app = FastAPI()

data = load_data()

model = predict_data_baseline()
X = data[['Date']]
y = data['OilPrice']
model.train(X, y)


class DateRange(BaseModel):
    start_date: str
    end_date: str


@app.post("/predict/")
async def predict_prices(date_range: DateRange):
    try:
        start_date = datetime.strptime(date_range.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(date_range.end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Неверный формат даты. Используйте YYYY-MM-DD.")

    date_range = pd.date_range(start_date, end_date)

    predictions = model.predict(np.array(date_range).reshape(-1, 1))

    result = {
        "dates": date_range.strftime("%Y-%m-%d").tolist(),
        "predictions": predictions.tolist()
    }

    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
