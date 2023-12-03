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


def calculate_slope(series, period: int = 5):
    slopes = [0 for _ in range(period-1)]
    for i in range(period-1, len(series)):
        x = np.arange(period)
        y = series[i-period+1:i+1].values
        slope = np.polyfit(x, y, 1)[0] # Calculate the slope using linear regression
        percent_slope = (slope / y[0]) * 100 # Convert the slope to a percentage
        slopes.append(percent_slope)
    return slopes
    
# Calculate the slope
data['Slope'] = calculate_slope(data['SMA'])
data[40:55]
#pprint(data[40:55])

dfpl = data[:]
fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                open=dfpl['Open'],
                high=dfpl['High'],
                low=dfpl['Low'],
                close=dfpl['Close'])])

fig.add_scatter(x=dfpl.index, y=dfpl['SMA'], mode="markers",
                marker=dict(size=5, color="MediumPurple"),
                name="pivot")
fig.update_layout(xaxis_rangeslider_visible=False)
fig.show()