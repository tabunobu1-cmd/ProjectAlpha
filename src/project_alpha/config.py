from pathlib import Path
import yaml
import pandas as pd

def load_settings(path):
    with Path(path).open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_universe(path):
    df = pd.read_csv(path)
    required = {"ticker", "name"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"universe.csv is missing columns: {sorted(missing)}")
    if df["ticker"].duplicated().any():
        raise ValueError("Duplicate tickers found in universe.csv")
    return df
