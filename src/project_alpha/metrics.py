import math
import numpy as np

TRADING_DAYS = 252

def cagr(returns):
    r = returns.dropna()
    if len(r) < 2:
        return float("nan")
    total = float((1+r).prod())
    years = len(r) / TRADING_DAYS
    return total ** (1/years) - 1 if total > 0 and years > 0 else float("nan")

def annualized_volatility(returns):
    return float(returns.dropna().std(ddof=1) * math.sqrt(TRADING_DAYS))

def sharpe(returns):
    vol = annualized_volatility(returns)
    return cagr(returns) / vol if vol > 0 and not np.isnan(vol) else float("nan")

def max_drawdown(equity):
    peak = equity.cummax()
    return float((equity / peak - 1).min())

def summarize(strategy_returns, benchmark_returns):
    s = strategy_returns.dropna()
    b = benchmark_returns.reindex(s.index).fillna(0.0)
    eq = (1+s).cumprod()
    beq = (1+b).cumprod()
    active = s - b
    te = float(active.std(ddof=1) * math.sqrt(TRADING_DAYS))
    ir = float(active.mean() * TRADING_DAYS / te) if te > 0 else float("nan")
    return {
        "strategy_total_return": float(eq.iloc[-1]-1),
        "benchmark_total_return": float(beq.iloc[-1]-1),
        "strategy_cagr": cagr(s),
        "benchmark_cagr": cagr(b),
        "strategy_volatility": annualized_volatility(s),
        "strategy_sharpe": sharpe(s),
        "strategy_max_drawdown": max_drawdown(eq),
        "information_ratio_vs_benchmark": ir,
    }
