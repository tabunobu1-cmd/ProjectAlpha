import sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from project_alpha.features import momentum, forward_return
from project_alpha.backtest import run_backtest

def test_features():
    idx = pd.bdate_range("2024-01-01", periods=120)
    prices = pd.DataFrame({"A": np.linspace(100,160,len(idx)),
                           "B": np.linspace(100,110,len(idx))}, index=idx)
    assert momentum(prices, 60).iloc[:60].isna().all().all()
    assert forward_return(prices, 20).iloc[-20:].isna().all().all()

def test_backtest_runs():
    idx = pd.bdate_range("2024-01-01", periods=150)
    rng = np.random.default_rng(42)
    rets = pd.DataFrame(rng.normal(0.0005,0.01,(len(idx),12)),
                        index=idx, columns=[f"S{i}" for i in range(12)])
    prices = 100 * (1+rets).cumprod()
    perf, weights = run_backtest(prices, momentum(prices,60), 10, 4, 15, 1, 61)
    assert len(perf) == len(prices)
    assert weights.shape == prices.shape
