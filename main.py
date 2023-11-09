import yfinance as yf
import pprint
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# Define the ticker symbol
ticker_symbol = "AAPL"

# Create a ticker Object
ticker = yf.Ticker(ticker_symbol)

# Download historical data
#historical_data = []
#historical_data = ticker.history(start="1990-01-01", end="2023-11-07", interval="1d")
#historical_data = ticker.history(period="20d", interval="1d")
#df_criteria_met = pd.DataFrame(historical_data)
#df_criteria_met.to_csv("cointegrated_pairs_20d.csv")

#df=pd.read_csv("cointegrated_pairs_20d.csv")
#df=df[df['Volume']!=0]
#df=df.reset_index(drop=True)

data = yf.download(tickers='BTC-EUR', period='max', interval='1d')
data=data[data["High"]!=data["Low"]]

dfpl = data[-365:]

#fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
#                                    open=dfpl['Open'],
#                                    high=dfpl['High'],
#                                    low=dfpl['Low'],
#                                    close=dfpl['Close'])])

#fig.show()


#plt.plot(data.index, data.Close)
#plt.show()


fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                                    open=dfpl['Open'],
                                    high=dfpl['High'],
                                    low=dfpl['Low'],
                                    close=dfpl['Close'],
                                    increasing_line_color= 'green', decreasing_line_color= 'red'),
                                    go.Scatter(x=dfpl.index, y=[27000]*len(dfpl), line=dict(color='red', width=1), name='Support/Resistance')])

fig.show()