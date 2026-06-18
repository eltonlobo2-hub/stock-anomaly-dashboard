# Stock Anomaly & Volatility Dashboard

An interactive dashboard that flags unusual single-day price movements across a basket of stocks using rolling volatility and z-score analysis, the same statistical approach used in financial risk monitoring and fraud detection systems.

**Live demo:** [add your Streamlit Cloud link here once deployed]

## What it does

- Pulls daily price history for a basket of stocks (AAPL, TSLA, JPM, SPY, NVDA) using the free `yfinance` API
- Calculates daily returns and 20-day rolling volatility for each stock
- Flags any trading day where the return is more than 2 standard deviations from its recent average as an anomaly
- Presents results through an interactive Streamlit dashboard: price charts with anomalies highlighted, a volatility trend chart, a sortable table of flagged days, and a cross-stock comparison view
- Auto-generates a plain-English summary for each stock (e.g. "AAPL had 6 anomalous trading days this period, most recently on...")

## Why this project

Anomaly detection on financial time series is directly applicable to fraud monitoring, market risk, and compliance use cases in fintech. This project demonstrates the full pipeline an analyst would own end to end: pulling and cleaning real market data, applying a defensible statistical method for outlier detection, and presenting results in a way a non-technical stakeholder could act on.

## Tech stack

- **Python** for data pipeline and analysis
- **yfinance** for free, keyless access to daily market data
- **pandas / numpy** for return and volatility calculations
- **matplotlib** for charting
- **Streamlit** for the interactive dashboard

No paid APIs or subscriptions are required anywhere in this project.

## How it works

1. `fetch_data.py` downloads a year of daily price history for each ticker and saves it locally as CSV.
2. `analyze.py` computes daily returns and 20-day rolling volatility.
3. `detect_anomalies.py` computes a z-score for each day's return relative to its trailing mean and volatility, flagging anything beyond a 2-standard-deviation threshold as anomalous.
4. `app.py` ties it all together into an interactive Streamlit dashboard.

## Running it locally

\`\`\`bash
git clone https://github.com/<your-username>/stock-anomaly-dashboard.git
cd stock-anomaly-dashboard
python -m venv venv
venv\Scripts\activate        # on Mac/Linux: source venv/bin/activate
pip install -r requirements.txt

python fetch_data.py
python analyze.py
python detect_anomalies.py
streamlit run app.py
\`\`\`

The dashboard will open automatically at `http://localhost:8501`.

## Possible extensions

- Swap the fixed z-score threshold for a dynamically tuned one based on each stock's historical anomaly rate
- Add sector or news-event overlays to explain *why* a flagged day occurred
- Extend to intraday data for faster anomaly detection
- Add email/Slack alerting for newly flagged anomalies on a daily refresh schedule

## Author

Elton Lobo
[LinkedIn](https://www.linkedin.com/in/elton-lobo-236326214/) · eltonlobo2@gmail.com
