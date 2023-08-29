import yfinance as yf
import dotenv
import os
from sqlalchemy import create_engine
import pandas as pd

# load variables
dotenv.load_dotenv()
user = os.getenv("user")
password = os.getenv("password")
host = "data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com"
port = 5439
database = 'data-engineer-database'

engine = create_engine(
    f'redshift+psycopg2://{user}:{password}@{host}:{port}/{database}')

tickers = ["AAPL", "MSFT"] # list of tickers

df = pd.DataFrame()

for i in tickers:
    tickerDf = yf.download(
        tickers=i,
        start="2021-01-01",
        end="2021-01-31",
        interval="1d"
    )
    tickerDf = tickerDf.reset_index()

    tickerDf["Close"] = tickerDf["Adj Close"]
    tickerDf = tickerDf.drop(columns=["Adj Close"])
                                 
    tickerDf = tickerDf.rename(columns={
        "Date": "date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume",
    })

    tickerDf["symbol"] = i
    tickerDf["change"] = tickerDf["close"].diff()
    tickerDf["change_percent"] = tickerDf["close"].pct_change().mul(100)
    
    tickerDf[["open", "close", "high", "low", "change_percent", "change"]] = tickerDf[[
        "open", "close", "high", "low", "change_percent", "change"]].round(2)

    # insert data into the redshift table
    tickerDf.to_sql("stock", engine, schema=user, if_exists='append', index=True, index_label='id')

    df = pd.concat([df, tickerDf], ignore_index=True)

# create an aggregate table (in memory)
df = df.groupby("symbol").agg({
    "open": "first",
    "close": "last",
    "change": "sum",
    "change_percent": "sum"
}).reset_index()
print(df)