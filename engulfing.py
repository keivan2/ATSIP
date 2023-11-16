import yfinance as yf
import pandas as pd

dataF = yf.download("BTC-USD", start="2022-04-1", end="2023-04-1", interval='1d')

dataF=dataF[dataF["High"]!=dataF['Low']]
dataF.reset_index(inplace=True)
dataF

def average_next_n_candles(df, i, N):
    # Check if there are N candles after the current one
    if i + N >= len(df):
        return None

    # Compute the average closing price of the next N candles
    avg_price = df['Close'].iloc[i+1:i+N+1].mean()

    # Compare the average price to the current closing price
    if avg_price < df['Close'].iloc[i]:
        return 1
    elif avg_price > df['Close'].iloc[i]:
        return 2
    else:
        return 0

N=4
signal = [0]*len(dataF)
for i in range(len(dataF)-N):
    signal[i]= average_next_n_candles(dataF, i, N)
dataF["price_target"] = signal

dataF[dataF["engulfing_signal"]==dataF["price_target"]].count()

equal_count = 0
different_count = 0
total_count = 0

for i in range(len(dataF)):
    if dataF.engulfing_signal.iloc[i] != 0:
        total_count += 1
        if dataF.engulfing_signal.iloc[i] == dataF.price_target.iloc[i]:
            equal_count += 1
        else:
            different_count += 1

equal_percentage = (equal_count / total_count) * 100
different_percentage = (different_count / total_count) * 100

print(equal_percentage, different_percentage)