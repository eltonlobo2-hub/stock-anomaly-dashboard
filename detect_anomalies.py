"""
Day 3: Flag anomalous trading days using z-scores.

Loads the *_enriched.csv files from Day 2 (which already have Daily_Return
and Rolling_Volatility), computes a rolling mean of returns, then calculates
a z-score for each day's return relative to its trailing 20-day mean and
std dev. Any day where |z-score| exceeds the threshold gets flagged as
an anomaly.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

DATA_DIR = "data"
TICKERS = ["AAPL", "TSLA", "JPM", "SPY", "NVDA"]
ROLLING_WINDOW = 20
Z_SCORE_THRESHOLD = 2.0  # flag anything beyond 2 standard deviations


def load_enriched_data(ticker: str, data_dir: str) -> pd.DataFrame:
    """Load the enriched CSV from Day 2."""
    path = os.path.join(data_dir, f"{ticker}_enriched.csv")
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    return df


def add_zscore_and_flags(df: pd.DataFrame, window: int, threshold: float) -> pd.DataFrame:
    """Add rolling mean, z-score, and anomaly flag columns."""
    df = df.copy()

    # Rolling mean of returns (we already have rolling std as Rolling_Volatility)
    df["Rolling_Mean"] = df["Daily_Return"].rolling(window=window).mean()

    # Z-score: how many std devs is today's return from the recent average?
    df["Z_Score"] = (df["Daily_Return"] - df["Rolling_Mean"]) / df["Rolling_Volatility"]

    # Flag anomalies where |z-score| exceeds threshold
    df["Is_Anomaly"] = df["Z_Score"].abs() > threshold

    return df


def plot_with_anomalies(df: pd.DataFrame, ticker: str, data_dir: str):
    """Plot price with anomalous days marked as red dots."""
    anomalies = df[df["Is_Anomaly"]]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df.index, df["Close"], label="Close Price", color="steelblue", linewidth=1)
    ax.scatter(anomalies.index, anomalies["Close"], color="red", label="Anomaly", zorder=5, s=40)
    ax.set_title(f"{ticker} - Price with Flagged Anomalies")
    ax.set_ylabel("Price ($)")
    ax.legend()

    plt.tight_layout()
    out_path = os.path.join(data_dir, f"{ticker}_anomalies.png")
    plt.savefig(out_path)
    print(f"  Saved chart to {out_path}")
    plt.close(fig)


def summarize_anomalies(df: pd.DataFrame, ticker: str):
    """Print a short narrative summary, like a business analyst would write."""
    anomalies = df[df["Is_Anomaly"]]
    count = len(anomalies)

    if count == 0:
        print(f"  {ticker}: no anomalies flagged in this period.")
        return

    most_recent = anomalies.index.max().strftime("%Y-%m-%d")
    biggest = anomalies["Z_Score"].abs().idxmax()
    biggest_date = biggest.strftime("%Y-%m-%d")
    biggest_return = anomalies.loc[biggest, "Daily_Return"] * 100

    print(f"  {ticker}: {count} anomalous trading day(s) flagged.")
    print(f"    Most recent: {most_recent}")
    print(f"    Largest single-day move: {biggest_date} ({biggest_return:.2f}%)")


def main():
    for ticker in TICKERS:
        print(f"Processing {ticker}...")
        df = load_enriched_data(ticker, DATA_DIR)
        df = add_zscore_and_flags(df, ROLLING_WINDOW, Z_SCORE_THRESHOLD)

        out_path = os.path.join(DATA_DIR, f"{ticker}_with_anomalies.csv")
        df.to_csv(out_path)
        print(f"  Saved to {out_path}")

        plot_with_anomalies(df, ticker, DATA_DIR)
        summarize_anomalies(df, ticker)
        print()

    print("Done. Open the *_anomalies.png files to see flagged days marked in red.")


if __name__ == "__main__":
    main()