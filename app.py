"""
Day 4: Interactive Streamlit dashboard for stock anomaly detection.

Lets the user pick a ticker from a dropdown, then displays:
- Closing price chart with anomalies marked
- Rolling volatility chart
- A table listing the flagged anomalous trading days

Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

DATA_DIR = "data"
TICKERS = ["AAPL", "TSLA", "JPM", "SPY", "NVDA"]


@st.cache_data
def load_data(ticker: str) -> pd.DataFrame:
    """Load the fully processed CSV (with returns, volatility, z-score, anomaly flag)."""
    path = os.path.join(DATA_DIR, f"{ticker}_with_anomalies.csv")
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    return df


def plot_price_with_anomalies(df: pd.DataFrame, ticker: str):
    anomalies = df[df["Is_Anomaly"]]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df.index, df["Close"], label="Close Price", color="steelblue", linewidth=1)
    ax.scatter(anomalies.index, anomalies["Close"], color="red", label="Anomaly", zorder=5, s=40)
    ax.set_title(f"{ticker} - Closing Price with Flagged Anomalies")
    ax.set_ylabel("Price ($)")
    ax.legend()
    return fig


def plot_volatility(df: pd.DataFrame, ticker: str):
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(df.index, df["Rolling_Volatility"], color="darkorange", label="20-Day Rolling Volatility")
    ax.set_title(f"{ticker} - Rolling Volatility")
    ax.set_ylabel("Volatility")
    ax.legend()
    return fig


def build_summary_text(df: pd.DataFrame, ticker: str) -> str:
    """Auto-generated narrative summary, written like a business analyst note."""
    anomalies = df[df["Is_Anomaly"]]
    count = len(anomalies)

    if count == 0:
        return f"{ticker} had no anomalous trading days flagged in this period."

    most_recent = anomalies.index.max().strftime("%B %d, %Y")
    biggest_idx = anomalies["Z_Score"].abs().idxmax()
    biggest_date = biggest_idx.strftime("%B %d, %Y")
    biggest_return = anomalies.loc[biggest_idx, "Daily_Return"] * 100

    return (
        f"**{ticker}** had **{count}** anomalous trading day(s) over the period shown. "
        f"The most recent was on **{most_recent}**. "
        f"The largest single-day move was on **{biggest_date}**, "
        f"a **{biggest_return:.2f}%** change, well outside its typical daily range."
    )


def main():
    st.set_page_config(page_title="Stock Anomaly Dashboard", layout="wide")
    st.title("📈 Stock Anomaly & Volatility Dashboard")
    st.caption("Flags unusual daily price moves using rolling z-score analysis.")

    ticker = st.selectbox("Select a stock", TICKERS)

    df = load_data(ticker)

    st.markdown(build_summary_text(df, ticker))

    col1, col2 = st.columns([3, 2])

    with col1:
        st.pyplot(plot_price_with_anomalies(df, ticker))
        st.pyplot(plot_volatility(df, ticker))

    with col2:
        st.subheader("Flagged Anomaly Days")
        anomalies = df[df["Is_Anomaly"]][["Close", "Daily_Return", "Z_Score"]].copy()
        anomalies["Daily_Return"] = (anomalies["Daily_Return"] * 100).round(2).astype(str) + "%"
        anomalies["Z_Score"] = anomalies["Z_Score"].round(2)
        anomalies = anomalies.sort_index(ascending=False)
        st.dataframe(anomalies, use_container_width=True)

    st.divider()
    st.subheader("Compare anomaly counts across the basket")
    comparison = []
    for t in TICKERS:
        d = load_data(t)
        comparison.append({"Ticker": t, "Anomaly Count": int(d["Is_Anomaly"].sum())})
    comp_df = pd.DataFrame(comparison).set_index("Ticker")
    st.bar_chart(comp_df)


if __name__ == "__main__":
    main()