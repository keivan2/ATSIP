import yfinance as yf
import pandas as pd

dataF = yf.download("BTC-USD", start="2022-04-1", end="2023-04-1", interval='1d')

dataF=dataF[dataF["High"]!=dataF['Low']]
dataF.reset_index(inplace=True)
dataF

def rejection_signal(df): 
    #bullish signal
    if ( df.Open.iloc[-1] < df.Close.iloc[-1] and
       (df.High.iloc[-1] - df.Close.iloc[-1]) < abs(df.Open.iloc[-1]-df.Close.iloc[-1])/10 and
       (df.Open.iloc[-1] - df.Low.iloc[-1]) > abs(df.Open.iloc[-1]-df.Close.iloc[-1])*5):
        return 2
    
    #bearish signal
    elif ( df.Open.iloc[-1] > df.Close.iloc[-1] and
       (df.High.iloc[-1] - df.Open.iloc[-1]) > abs(df.Open.iloc[-1]-df.Close.iloc[-1])*5 and
       (df.Close.iloc[-1] - df.Low.iloc[-1]) < abs(df.Open.iloc[-1]-df.Close.iloc[-1])/10):
        return 1
    
    #nosignal
    else:
        return 0

def engulfing_signal(df):
    # Get the current and previous candles
    previous_candle = df.iloc[-2]
    current_candle = df.iloc[-1]

    # Check for bullish engulfing
    if ( (current_candle['Close'] > previous_candle['Open']) 
        and (current_candle['Open'] < previous_candle['Close'])
        and (previous_candle['Open'] > previous_candle['Close']) ):
        return 2

    # Check for bearish engulfing
    elif ( (current_candle['Open'] > previous_candle['Close']) 
          and (current_candle['Close'] < previous_candle['Open']) 
          and (previous_candle['Close'] > previous_candle['Open']) ):
        return 1

    # Return 0 for any other case
    else:
        return 0
    

signal = [0]*len(dataF)
for i in range(3,len(dataF)):
    df = dataF[i-3:i+1]
    signal[i]= rejection_signal(df)
dataF["rejection_signal"] = signal

signal = [0]*len(dataF)
for i in range(1,len(dataF)):
    df = dataF[i-1:i+1]
    signal[i]= engulfing_signal(df)
dataF["engulfing_signal"] = signal


up_count = 0
down_count = 0
total_count = 0

for i in range(len(dataF) - 1):
    if dataF.engulfing_signal.iloc[i] == 1:
        total_count += 1
        if dataF.Close.iloc[i+1] > dataF.Open.iloc[i+1]:
            up_count += 1
        elif dataF.Close.iloc[i+1] < dataF.Open.iloc[i+1]:
            down_count += 1

up_percentage = (up_count / total_count) * 100
down_percentage = (down_count / total_count) * 100

print(up_percentage, down_percentage, total_count)

dataF[dataF["engulfing_signal"]==1]

import plotly.graph_objects as go

st = 0
dfpl = dataF[st:st+150].copy()
fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                open=dfpl['Open'],
                high=dfpl['High'],
                low=dfpl['Low'],
                close=dfpl['Close'])])

fig.show()