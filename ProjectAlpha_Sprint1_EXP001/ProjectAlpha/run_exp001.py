import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from project_alpha.config import load_settings, load_universe
from project_alpha.data import download_close_prices, save_prices
from project_alpha.features import momentum, forward_return
from project_alpha.backtest import run_backtest
from project_alpha.metrics import summarize
from project_alpha.experiment import ensure_dir, save_json, plot_equity, write_log

def main():
    settings = load_settings(ROOT / "config" / "settings.yaml")
    universe = load_universe(ROOT / "config" / "universe.csv")
    benchmark = settings["data"]["benchmark_ticker"]
    tickers = universe["ticker"].tolist()
    all_tickers = list(dict.fromkeys(tickers + [benchmark]))

    print(f"[1/6] Downloading {len(all_tickers)} tickers...")
    close = download_close_prices(
        all_tickers,
        settings["data"]["start"],
        settings["data"]["end"],
        settings["data"]["auto_adjust"],
    )
    if benchmark not in close.columns:
        raise RuntimeError(f"Benchmark {benchmark} was not downloaded.")

    bench_price = close[benchmark].dropna()
    prices = close.drop(columns=[benchmark], errors="ignore").dropna(axis=1, how="all")
    save_prices(close, ROOT / "data/raw/close_prices.csv")

    print("[2/6] Building features...")
    scores = momentum(prices, settings["strategy"]["momentum_lookback_days"])
    labels = forward_return(prices, settings["strategy"]["forward_return_days"])

    processed = ROOT / "data/processed"
    processed.mkdir(parents=True, exist_ok=True)
    scores.to_csv(processed / "momentum_60.csv")
    labels.to_csv(processed / "forward_return_20.csv")

    print("[3/6] Running backtest...")
    perf, weights = run_backtest(
        prices, scores,
        settings["strategy"]["top_n"],
        settings["strategy"]["rebalance_weekday"],
        settings["strategy"]["transaction_cost_bps"],
        settings["filters"]["min_price"],
        settings["filters"]["min_history_days"],
    )

    bench_ret = bench_price.pct_change(fill_method=None).reindex(perf.index).fillna(0.0)
    perf["benchmark_return"] = bench_ret
    perf["benchmark_equity"] = (1 + bench_ret).cumprod()

    print("[4/6] Computing metrics...")
    summary = summarize(perf["strategy_return"], perf["benchmark_return"])

    report_dir = ensure_dir(ROOT / settings["output"]["report_dir"])
    perf.to_csv(report_dir / "performance.csv")
    weights.to_csv(report_dir / "holdings.csv")
    scores.to_csv(report_dir / "scores.csv")
    save_json(summary, report_dir / "summary.json")
    plot_equity(perf["strategy_return"], perf["benchmark_return"], report_dir / "equity_curve.png")
    write_log(summary, settings, report_dir / "experiment_log.md")

    print("[5/6] Reports saved.")
    initial = settings["strategy"]["initial_capital"]
    ending = initial * (1 + summary["strategy_total_return"])
    print("[6/6] Done.")
    print(f"Initial capital: ¥{initial:,.0f}")
    print(f"Simulated ending value: ¥{ending:,.0f}")
    print(summary)

if __name__ == "__main__":
    main()
