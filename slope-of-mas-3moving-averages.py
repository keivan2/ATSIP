# Slope of MAs
import yfinance as yf
import pandas_ta as ta
from pprint import pprint
import numpy as np
import plotly.graph_objects as go

def get_data(symbol: str):
    data = yf.download(tickers=symbol, period='100d', interval='1d')
    data.reset_index(inplace=True, drop=True)
    return data
# Get the data
data = get_data('BTC-USD')
#pprint(data)

def calculate_sma(data, length: int):
    return ta.sma(data['Close'], length)

# Calculate the movin avarage
data['SMA'] = calculate_sma(data, 20)
data.dropna(inplace=True)


def determine_trend(data):
    if data['SMA_10'] > data['SMA_20'] > data['SMA_30']:
        return 2 # Uptrend
    elif data['SMA_10'] < data['SMA_20'] < data['SMA_30']:
        return 1 # Downtrend
    else:
        return 0 # No trend
    

data['SMA_10'] = calculate_sma(data, 10)
data['SMA_20'] = calculate_sma(data, 20)
data['SMA_30'] = calculate_sma(data, 30)

# Determine the trend and add it as a new column to the DataFrame
data['Trend'] = data.apply(determine_trend, axis=1)

dfpl = data[:]
fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                open=dfpl['Open'],
                high=dfpl['High'],
                low=dfpl['Low'],
                close=dfpl['Close'])])



fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl['SMA_10'], mode='lines', name='SMA 10', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl['SMA_20'], mode='lines', name='SMA 20', line=dict(color='red')))
fig.add_trace(go.Scatter(x=dfpl.index, y=dfpl['SMA_30'], mode='lines', name='SMA 30', line=dict(color='green')))

fig.update_layout(xaxis_rangeslider_visible=False)
fig.show()