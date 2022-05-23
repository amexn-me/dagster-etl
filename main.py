from fastapi import FastAPI
from typing import Optional
import requests
import json
import pandas as pd
import datetime as dt


# Data Fetching Function
def get_hourly_cryptodata(symbol: str, startTime: str, endTime: str):
    url = "https://api.binance.com/api/v3/klines"    
    symbol = symbol
    interval = "1h"
    limit = '1000'
    req_params = {'symbol': symbol, 'interval':interval, 'startTime': startTime, 'endTime':endTime, 'limit': limit}
    data = json.loads(requests.get(url, params = req_params).text)

    # Workaround since FastAPI has some issues pending with iteration of Dataframe
    # Issue link: https://github.com/tiangolo/fastapi/issues/1733
    for i in range(len(data)):
        data[i] = list(map(float, data[i]))

    candles = pd.DataFrame(data)
    candles = candles.iloc[:, 0:5]
    candles.columns = ['datetime', 'open', 'high', 'low', 'close']
    candles.datetime = [dt.datetime.fromtimestamp(x / 1000.0) for x in candles.datetime]

    return candles


# FastAPI intialization
app = FastAPI()

# Routes
@app.get("/")
async def root():
    return {"message": "Please add URL+Symbol to get the OHLCV Data"}

@app.get("/{symbol}")
async def get_data(
        symbol: str,
        startTime: Optional[dt.datetime] = dt.datetime(2020,1,1),
        endTime: Optional[dt.datetime] = dt.datetime(2020,2,1)):
    
    symbol = symbol.upper()+"USDT"
    startTime = str(int(startTime.timestamp() * 1000))
    endTime = str(int(endTime.timestamp() * 1000))

    data = get_hourly_cryptodata(symbol, startTime, endTime)
    return data