from twelvedata import TDClient

# Initialize client - apikey parameter is requiered
td = TDClient(apikey="36fee84cc17249d3b0ada76c777b2ab4")

# Construct the necessary time series
ts = td.time_series(
    symbol="AAPL",
    interval="1min",
    outputsize=2,
    timezone="America/New_York",
)

# Get the response from the server
aapl = ts.as_json()

# Print the response from the server
print(aapl)
