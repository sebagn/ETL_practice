from twelvedata import TDClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Initialize client - apikey parameter is requiered
td = TDClient(apikey=API_KEY)

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
