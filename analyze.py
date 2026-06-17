"""
Day 2: Compute daily returns and rolling volatility.

Loads the CSVs saved by fetch_data.py, calculates daily percentage returns,
then computes a rolling 20-day standard deviation of those returns as a
volatility measure. Also plots the result so we can sanity-check it visually.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

DATA_DIR = "data"
TICKERS = ["AAPL", "TSLA", "JPM", "SPY", "NVDA"]
ROLLING_WINDOW = 20  # trading days (~1 month)


def load_ticker_data(ticker: str, data_dir: str) -> pd.DataFrame:
    """Load a single ticker's CSV and parse the date column properly."""
    path = os.path.join(data_dir, f"{ticker}.csv")
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    return df


def add_returns_and_volatility(df: pd.DataFrame, window: int) -> pd.DataFrame:
    """Add daily return and rolling volatility columns to the dataframe."""
    df = df.copy()

    # Daily percentage return based on closing price
    df["Daily_Return"] = df["Close"].pct_change()

    # Rolling volatility = standard deviation of returns over the window
    df["Rolling_Volatility"] = df["Daily_Return"].rolling(window=window).std()

    return df


def plot_price_and_volatility(df: pd.DataFrame, ticker: str):
    """Quick visual sanity check: price vs rolling volatility over time."""
    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    axes[0].plot(df.index, df["Close"], label="Close Price", color="steelblue")
    axes[0].set_title(f"{ticker} - Closing Price")
    axes[0].set_ylabel("Price ($)")
    axes[0].legend()

    axes[1].plot(df.index, df["Rolling_Volatility"], label="20-Day Rolling Volatility", color="darkorange")
    axes[1].set_title(f"{ticker} - Rolling Volatility")
    axes[1].set_ylabel("Volatility (std of daily returns)")
    axes[1].legend()

    plt.tight_layout()
    out_path = os.path.join(DATA_DIR, f"{ticker}_volatility_check.png")
    plt.savefig(out_path)
    print(f"  Saved chart to {out_path}")
    plt.close(fig)


def main():
    for ticker in TICKERS:
        print(f"Processing {ticker}...")
        df = load_ticker_data(ticker, DATA_DIR)
        df = add_returns_and_volatility(df, ROLLING_WINDOW)

        # Save the enriched data back out so Day 3's anomaly script can use it
        out_path = os.path.join(DATA_DIR, f"{ticker}_enriched.csv")
        df.to_csv(out_path)
        print(f"  Saved enriched data to {out_path}")

        plot_price_and_volatility(df, ticker)

    print("\nDone. Open the *_volatility_check.png files to eyeball the results.")
    print("You should see volatility spike around days when the price moved sharply.")


if __name__ == "__main__":
    main()