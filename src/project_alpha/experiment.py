from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt

def ensure_dir(path):
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def save_json(data, path):
    clean = {k: (None if isinstance(v, float) and pd.isna(v) else v) for k,v in data.items()}
    Path(path).write_text(json.dumps(clean, ensure_ascii=False, indent=2), encoding="utf-8")

def plot_equity(strategy_returns, benchmark_returns, path):
    s = (1 + strategy_returns.fillna(0)).cumprod()
    b = (1 + benchmark_returns.reindex(s.index).fillna(0)).cumprod()
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(s.index, s.values, label="EXP001 strategy")
    ax.plot(b.index, b.values, label="Benchmark")
    ax.set_title("Project Alpha EXP001 — Equity Curve")
    ax.set_ylabel("Growth of 1")
    ax.legend()
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)

def write_log(summary, settings, path):
    lines = [
        "# EXP001 実験ログ", "",
        "## 仮説",
        "60営業日モメンタムが高い銘柄は、その後も相対的に強い可能性がある。", "",
        "## 設定",
        f"- Top N: {settings['strategy']['top_n']}",
        f"- 売買コスト: {settings['strategy']['transaction_cost_bps']} bps / turnover",
        "", "## 結果"
    ]
    for k,v in summary.items():
        lines.append(f"- {k}: {v}")
    Path(path).write_text("\n".join(lines), encoding="utf-8")
