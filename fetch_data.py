"""
Day 1: Pull daily stock data and save locally.

This script downloads ~1 year of daily price data for a basket of tickers
using yfinance (free, no API key needed) and saves each one as a CSV so
we don't have to re-hit the API every time we test our analysis code.
"""

import yfinance as yf
import pandas as pd
import os

# A mix of volatile and stable tickers makes anomaly detection more interesting.
# Feel free to swap these for stocks you personally follow.
TICKERS = ["AAPL", "TSLA", "JPM", "SPY", "NVDA"]

# How much history to pull
PERIOD = "1y"

# Where to save the raw data
DATA_DIR = "data"


def fetch_and_save(ticker: str, period: str, data_dir: str) -> pd.DataFrame:
    """Download daily data for one ticker and save it as a CSV."""
    print(f"Fetching {ticker}...")
    df = yf.download(ticker, period=period, interval="1d", progress=False)

    if df.empty:
        print(f"  WARNING: no data returned for {ticker}")
        return df

    # Flatten column names in case yfinance returns a MultiIndex
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    os.makedirs(data_dir, exist_ok=True)
    out_path = os.path.join(data_dir, f"{ticker}.csv")
    df.to_csv(out_path)
    print(f"  Saved {len(df)} rows to {out_path}")
    return df


def main():
    for ticker in TICKERS:
        fetch_and_save(ticker, PERIOD, DATA_DIR)

    print("\nDone. Check the 'data' folder for your CSV files.")


if __name__ == "__main__":
    main()