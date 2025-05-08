import requests

API_KEY = "WXE6G5QXY6VTKLUI"

def fetch_stock_data(symbol, time_series):
    base_url = "https://www.alphavantage.co/query"

    function_map = {
    "TIME_SERIES_DAILY": "TIME_SERIES_DAILY",
    "TIME_SERIES_WEEKLY": "TIME_SERIES_WEEKLY",
    "TIME_SERIES_MONTHLY": "TIME_SERIES_MONTHLY"
}

    interval = "60min"  # Needed for INTRADAY
    params = {
        "function": function_map[time_series],
        "symbol": symbol,
        "apikey": API_KEY
    }

    if time_series == "INTRADAY":
        params["interval"] = interval

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("API Error:", response.status_code)
        return None