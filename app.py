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
import plotly.graph_objects as go
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
    """Plot price with anomalies marked using plotly."""
    anomalies = df[df["Is_Anomaly"]]
    
    fig = go.Figure()
    
    # Add price line
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["Close"],
        mode="lines",
        name="Close Price",
        line=dict(color="steelblue", width=2)
    ))
    
    # Add anomaly points
    fig.add_trace(go.Scatter(
        x=anomalies.index,
        y=anomalies["Close"],
        mode="markers",
        name="Anomaly",
        marker=dict(color="red", size=8)
    ))
    
    fig.update_layout(
        title=f"{ticker} - Closing Price with Flagged Anomalies",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        hovermode="x unified",
        height=400
    )
    
    return fig


def plot_volatility(df: pd.DataFrame, ticker: str):
    """Plot rolling volatility using plotly."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["Rolling_Volatility"],
        mode="lines",
        name="20-Day Rolling Volatility",
        line=dict(color="darkorange", width=2)
    ))
    
    fig.update_layout(
        title=f"{ticker} - Rolling Volatility",
        xaxis_title="Date",
        yaxis_title="Volatility",
        hovermode="x unified",
        height=300
    )
    
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
        st.plotly_chart(plot_price_with_anomalies(df, ticker), use_container_width=True)
        st.plotly_chart(plot_volatility(df, ticker), use_container_width=True)

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
