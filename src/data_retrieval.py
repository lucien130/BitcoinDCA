from binance.client import Client
import pandas as pd
import os

DATA_FILE = "btc_binance_data.csv"

def fetch_bitcoin_data():
    """
    Fetches historical BTCUSDT klines from Binance using a 1-hour interval.
    The data covers from January 1, 2015 to December 31, 2024.
    Saves the data to a CSV file.
    """
    client = Client()  # Using public endpoint (no API keys required for historical data)
    start_str = "1 Jan 2015"
    end_str = "31 Dec 2024"
    interval = Client.KLINE_INTERVAL_1HOUR
    
    print("Fetching historical Bitcoin data from Binance...")
    klines = client.get_historical_klines("BTCUSDT", interval, start_str, end_str)
    
    # Create DataFrame with proper column names
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume', 
        'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'
    ])
    
    # Convert numeric columns
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = pd.to_numeric(df[col])
    
    # Convert timestamp to datetime and set as index
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df.set_index('timestamp')
    
    # Keep only needed columns
    df = df[['open', 'high', 'low', 'close', 'volume']]
    
    # Compute an additional indicator (e.g., last all-time-high of close price)
    df['LAST_ATH'] = df['close'].cummax()
    
    df.to_csv(DATA_FILE)
    print("Data loaded 100% and saved to", DATA_FILE)
    return df

def get_bitcoin_data():
    """
    Loads Bitcoin data from a CSV file if available; otherwise, fetches it.
    """
    if os.path.exists(DATA_FILE):
        print("Loading data from CSV file...")
        df = pd.read_csv(DATA_FILE, index_col='timestamp', parse_dates=True)
        return df
    else:
        print("CSV file not found. Fetching new data...")
        return fetch_bitcoin_data()

if __name__ == '__main__':
    df = get_bitcoin_data()
    print("Indicators loaded 100%")
    print(df.head())


