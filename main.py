import yfinance as yf
import pprint
import pandas as pd

# Define the ticker symbol
ticker_symbol = "AAPL"

# Create a ticker Object
ticker = yf.Ticker(ticker_symbol)

# Download historical data
historical_data = []
#historical_data = ticker.history(start="1990-01-01", end="2023-11-07", interval="1d")
historical_data = ticker.history(period="20d", interval="1d")
df_criteria_met = pd.DataFrame(historical_data)
df_criteria_met.to_csv("cointegrated_pairs_20d.csv")