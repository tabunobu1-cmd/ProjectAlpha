import pandas as pd

def weekly_rebalance_dates(index, weekday=4):
    idx = pd.DatetimeIndex(index).sort_values()
    frame = pd.DataFrame(index=idx)
    frame["week"] = idx.to_period("W-FRI")
    selected = []
    for _, group in frame.groupby("week", sort=True):
        dates = group.index
        preferred = dates[dates.weekday == weekday]
        selected.append(preferred[-1] if len(preferred) else dates[-1])
    return pd.DatetimeIndex(selected)

def build_target_weights(scores, prices, top_n=10, rebalance_weekday=4,
                         min_price=100.0, min_history_days=80):
    dates = weekly_rebalance_dates(scores.index, rebalance_weekday)
    target = pd.DataFrame(0.0, index=scores.index, columns=scores.columns)
    history = prices.notna().cumsum()
    for dt in dates:
        valid = (
            scores.loc[dt].notna() &
            prices.loc[dt].notna() &
            (prices.loc[dt] >= min_price) &
            (history.loc[dt] >= min_history_days)
        )
        picks = scores.loc[dt, valid].sort_values(ascending=False).head(top_n).index
        if len(picks):
            target.loc[dt, picks] = 1.0 / len(picks)

    held = pd.DataFrame(0.0, index=scores.index, columns=scores.columns)
    positions = [scores.index.get_loc(d) for d in dates]
    for i, dt in enumerate(dates):
        start = positions[i]
        end = positions[i+1] if i+1 < len(positions) else len(scores.index)
        held.iloc[start:end] = target.loc[dt].values

    return held.shift(1).fillna(0.0)

def run_backtest(prices, scores, top_n, rebalance_weekday,
                 transaction_cost_bps, min_price, min_history_days):
    returns = prices.pct_change(fill_method=None).fillna(0.0)
    weights = build_target_weights(
        scores, prices, top_n, rebalance_weekday, min_price, min_history_days
    )
    gross = (weights * returns).sum(axis=1)
    turnover = weights.diff().abs().sum(axis=1)
    if len(turnover):
        turnover.iloc[0] = weights.iloc[0].abs().sum()
    cost = turnover * (transaction_cost_bps / 10000.0)
    net = gross - cost
    performance = pd.DataFrame({
        "gross_return": gross,
        "turnover": turnover,
        "transaction_cost": cost,
        "strategy_return": net,
    })
    performance["equity"] = (1 + net).cumprod()
    return performance, weights
