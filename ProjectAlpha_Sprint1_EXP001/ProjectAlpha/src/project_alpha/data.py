from pathlib import Path
import pandas as pd
import yfinance as yf

def _normalize_download(raw, tickers):
    if raw.empty:
        raise RuntimeError("No market data was downloaded.")
    if isinstance(raw.columns, pd.MultiIndex):
        if "Close" in raw.columns.get_level_values(0):
            close = raw["Close"].copy()
        elif "Close" in raw.columns.get_level_values(1):
            close = raw.xs("Close", axis=1, level=1).copy()
        else:
            raise RuntimeError("Could not locate Close in yfinance response.")
    else:
        if "Close" not in raw.columns:
            raise RuntimeError("Could not locate Close in yfinance response.")
        close = raw[["Close"]].copy()
        close.columns = [tickers[0]]
    close.index = pd.to_datetime(close.index).tz_localize(None)
    return close.sort_index()

def download_close_prices(tickers, start, end=None, auto_adjust=True):
    raw = yf.download(
        tickers=tickers, start=start, end=end, auto_adjust=auto_adjust,
        progress=False, group_by="column", threads=True
    )
    return _normalize_download(raw, tickers)

def save_prices(prices, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    prices.to_csv(path)
