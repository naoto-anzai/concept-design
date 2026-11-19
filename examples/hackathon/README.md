# concept-design — 概念設計から、ジャーニー・API までを進めるワークスペース

意思決定写像 `g`(問題記述 + 機能 → 概念 + 同期)の出力を、ダニエル・ジャクソンの概念設計の形で持ち、
そこから画面ごとの機能(ジャーニー)と API の仕様へ進むための作業場です。勉強資料ではなく道具として使います。

```
input.yaml ──g(人が判断)──▶ concepts.yaml ──derive──▶ journey/*.md ──▶ 画面ごとの機能
 (問題・機能)               (概念・同期・対応表)    └──▶ api/actions.generated.md ──▶ api/spec.md
        ▲                          ▲
        └── criteria.yaml          └── decisions.yaml(分割・統合の判断の記録)
        └── open-questions.yaml(未決事項。決まるまで確定しない)
```

## ファイル

| ファイル | 役割 | 誰が書くか |
|---|---|---|
| `input.yaml` | 問題、利害関係者、機能(価値の単位)、後の写像へ渡す条件 | 人 |
| `concepts.yaml` | 概念(目的・原理・状態・アクション)、同期、機能 × 概念の対応表 | 人(AI の案を人が判断) |
| `criteria.yaml` | 機能ごとの目的と評価基準、デモの場面、作らないこと、審査基準 | 人 |
| `open-questions.yaml` | 未決事項。どの段階を止めているか(`blocks`)を持つ | 人 |
| `decisions.yaml` | 設計上の課題の記録(問題 → 選択肢 → 採用案と理由) | 人 |
| `journey/<機能 ID>.md` | ジャーニーの雛形から育てる文書 | 雛形は導出、中身は人 |
| `api/actions.generated.md` | API の元表(導出結果。手で編集しない) | 導出 |
| `api/spec.md` | 手で書く API の仕様(まだ無い) | 人 |
| `docs/decision-map.md` | 写像 `g` の定義(形式、評価基準、手順)。判断に迷ったときの基準 | 参照のみ |

## コマンド(`concept-design/` で実行)

```
make lint      # 検査: 形式(C1)、独立性(C2)、被覆(C3)、参照の実在(C4)、未決事項の突き合わせ
make matrix    # 検査 + 機能 × 概念の対応表
make journey   # ジャーニーの雛形を作る(既にあるファイルは上書きしない。--force は derive.py を直接)
make api       # API の元表を作り直す
make open      # 未決事項だけを出す
```

必要なもの: Python 3 と PyYAML(`pip install -r tools/requirements.txt`)。

## 進め方

1. **入力を確定する。** `input.yaml` の ★要確認 を消し、OQ-7 を解決して、status を `confirmed` にする。
2. **概念を整える。** 分割・統合の判断は `decisions.yaml` に残す。`make lint` の ERROR をなくす。
3. **評価基準を合意する。** `criteria.yaml` の status を `proposed` から `confirmed` にする(OQ-6)。
4. **ジャーニーを書く。** `make journey` で雛形を作り、TODO を埋める。始点・終点・失敗時の扱いは、ここで決める。
5. **API を書く。** `make api` の元表から `api/spec.md` を書く。権限や整合の扱いは、未決事項が解決してから。

差し戻しもあります。ジャーニーや API を書いていて概念の足りなさに気づいたら、`concepts.yaml` に戻り、
理由を `decisions.yaml` に残します。

## 概念を書くときの規則(`lint.py` が確かめるもの)

- 概念の仕様に、他の概念の名前を書かない。つながりは `syncs` に書く(独立性)。
- 呼び出し元(誰が実行できるか)は概念に書かず、同期の `where` に書く。
- UI の語(画面、ボタンなど)と技術の名前(Leaflet など)を書かない。
- すべての機能が、概念と同期の組で実現される。どの機能にも使われない概念は作らない。
- 事前条件が無いアクションにも「なし」と書く。書き忘れと区別するため。

`lint.py` が確かめないもの: C5(各アクションが不変条件を保つか)。人が推論する。
