class Api {
  private _url: string
  private _headers: any;
  constructor() {
    this._url = 'http://localhost:8000'
    // this._headers = config.headers
  }
  _checkResponse(res: any) {
    if (res.ok) {
      return res.json();
    }
    return Promise.reject(`Ошибка: ${res.status}`);
  }

  getPredictions(startDate: string, numNextDays: number) {
    return fetch(this._url + '/historical-and-predictive-data', {
      method: 'POST',
      body: JSON.stringify({ 'start_date': startDate, 'forecast_days': numNextDays })
    })
      .then(this._checkResponse)
  }

}
const api = new Api()
export default api