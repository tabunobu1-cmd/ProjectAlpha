# Project Alpha — Sprint 1 / EXP001

日本株の説明可能な投資研究基盤の最小実装です。

EXP001 は **60営業日モメンタム**だけを使い、週1回ランキングし、
上位10銘柄を均等保有する戦略を TOPIX 連動ETFと比較します。

## 重要な前提
- この版は研究用プロトタイプです。実売買は行いません。
- 無料データとして `yfinance` を使います。
- ユニバースは `config/universe.csv` で明示します。
- 最初は動作確認用の20銘柄です。本番の「流動性上位300銘柄」は次Sprintで過去時点の流動性から構成します。
- シグナルは当日終値までで計算し、ポジションは翌営業日から有効にします。
- 売買コストは設定可能です。
- 20営業日先リターンは研究ラベルとして生成し、売買シグナルには使いません。

## セットアップ（Windows PowerShell）
```powershell
cd $HOME\Desktop\ProjectAlpha
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 実行
```powershell
python run_exp001.py
```

成功すると `reports/EXP001/` に以下を出力します。
- `performance.csv`
- `summary.json`
- `holdings.csv`
- `scores.csv`
- `equity_curve.png`
- `experiment_log.md`

## 次Sprintで改善する点
1. 過去時点ごとの流動性上位300銘柄ユニバース
2. 上場廃止銘柄を含むサバイバーシップ・バイアス対策
3. TOPIX指数そのもの、またはより適切なベンチマークデータへの切替
4. 約定価格をシグナル翌営業日の始値にする、より厳密な執行モデル
5. 配当・株式分割・企業行動の扱いの精査

まずは「研究基盤が正しく動くこと」を確認する v0.1 です。
