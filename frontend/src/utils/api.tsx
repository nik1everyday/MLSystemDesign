class Api {
  private _url: string
  private _headers: any;
  constructor() {
    this._url = 'http://localhost:8005'
    // this._headers = config.headers
  }
  _checkResponse(res: any) {
    if (res.ok) {
      return res.json();
    }
    return Promise.reject(`Ошибка: ${res.status}`);
  }

  getPredictions() {
    return fetch(this._url + '/predict')
      .then(this._checkResponse)
  }

}
const api = new Api()
export default api