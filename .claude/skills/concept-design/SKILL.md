---
name: concept-design
description: ダニエル・ジャクソンの概念設計(概念・運用規則・状態・アクション・同期)で、機能から概念を設計し、検査(lint)して、ジャーニーと API の元表まで導出する道具の使い方。「概念設計して」「概念を検査して」「ジャーニーの雛形を作って」「API の元表を作って」「未決事項を見せて」「concept-design」で使う。
---

# concept-design の使い方(AI 向け)

リポジトリ: https://github.com/naoto-anzai/concept-design (公開)

機能の集合から、ジャクソンの形の概念設計を作り、機械で検査し、画面ごとの機能(ジャーニー)と API の元表を導出する。
動く実例は `examples/hackathon/`(NAsVI: 技大祭アプリ)。別のプロジェクトで使うときは、この実例を複製して中身を差し替える。

## 手に入れる

別のリポジトリから使うとき、このリポジトリを隣に clone する(コピーしない。更新を取り込めるように)。

```
git clone https://github.com/naoto-anzai/concept-design.git ~/concept-design
```

必要なもの: Python 3 と PyYAML(`pip install -r examples/hackathon/tools/requirements.txt`)。

## 全体像

```
input.yaml ──(人が判断)──▶ concepts.yaml ──derive──▶ journey/*.md ──▶ 画面ごとの機能
 (問題・機能)              (概念・同期・対応表)    └──▶ api/actions.generated.md ──▶ api/spec.md
        ▲                         ▲
        └ criteria.yaml           └ decisions.yaml(分割・統合の判断の記録)
        └ open-questions.yaml(未決事項。決まるまで確定しない)
```

各ファイルの役割は `examples/hackathon/README.md`。概念を作る判断の基準(形式・評価基準・手順)は `examples/hackathon/docs/decision-map.md`。
ジャクソンの概念設計そのものの説明は `docs/concept-design-deductive.md`(根拠はジャクソン本人の著作だけ)。

## コマンド(`examples/hackathon/` で実行)

| コマンド | 内容 |
|---|---|
| `make lint` | 形式、独立性、被覆、参照の実在、未決事項の突き合わせを検査する |
| `make matrix` | 検査して、機能 × 概念の対応表も出す |
| `make journey` | ジャーニーの雛形を作る(既にあるファイルは上書きしない) |
| `make api` | API の元表を作り直す |
| `make open` | 未決事項だけを出す |

## 依頼ごとの手順

- **「概念を検査して」**: `make lint` を実行する。ERROR があれば、該当の行を直す。INFO の `[OQ]` は未決事項で、直さない。
- **「機能を足したい」**: `input.yaml` に機能を足す → `concepts.yaml` で、その機能を実現する概念と同期を決める(既存の概念で足りるか、新しい概念が要るか。目的が同じ概念だけを統合する)→ 判断を `decisions.yaml` に残す → `make lint`。
- **「ジャーニーを書きたい」**: `make journey` で雛形を作り、TODO を埋める。始点・終点・失敗時の扱いは人が決める。
- **「API の仕様を書きたい」**: `make api` の元表から `api/spec.md` を書く。権限や整合の扱いは、関係する未決事項が解決してから。
- **「未決事項は?」**: `make open`。決めるのはチームで、AI は決めない。

## 守ること

1. 編集の前後に `make lint` を実行する。ERROR を残さない。
2. 概念の仕様(目的・原理・状態・アクション)に、他の概念の名前、UI の語(画面、ボタン)、技術の名前を書かない。つながりと権限は同期(`syncs`)に書く。
3. 工数や実装の都合で、概念の独立性を崩さない。
4. 分割・統合・採否の判断は `decisions.yaml` に残す。捨てた案と理由も残す。
5. 未決のことは、推測で埋めない。`open-questions.yaml` に載せ、該当箇所に `OQ-n` を付ける。
6. 画像などから起こした値には ★要確認 を付ける。確認が取れるまで確定として扱わない。
7. `api/actions.generated.md` は導出結果なので、手で編集しない。`journey/*.md` は人が育てる文書で、上書きしない。
8. 評価基準は測れる形で書く(操作数、所要時間、観察で確かめられる条件)。
9. 提案と合意を区別する。作成者の提案は `status: proposed`、チームの合意後に `confirmed`。

## 変更するとき

このリポジトリは公開。個人情報、鍵、非公開の資料は入れない。変更は PR で出す。
