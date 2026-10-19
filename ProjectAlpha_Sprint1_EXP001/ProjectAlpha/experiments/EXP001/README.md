# EXP001 — 60日モメンタム

## 仮説
過去60営業日の上昇率が相対的に高い日本株は、その後も短期的に相対優位を維持する可能性がある。

## シグナル
`momentum_60 = adjusted_close(t) / adjusted_close(t-60) - 1`

## 売買
- 週1回
- シグナル値上位10銘柄
- 均等ウェイト
- ロングのみ

## ラベル
`forward_return_20 = adjusted_close(t+20) / adjusted_close(t) - 1`

ラベルは研究・検証用で、同日の売買シグナル生成には使用しない。
