# concept-design — ジャクソンの概念設計を、演繹的に理解するための作業場

ダニエル・ジャクソンの「概念設計」(概念、運用規則、状態、アクション、同期)を、ドメイン知識に縛られずに、前提から順に再構築して理解するための作業場です。
根拠は、ジャクソン本人の著作だけです。

## 場所

| 場所 | 中身 |
|---|---|
| `docs/` | ジャクソンの著作にもとづく、演繹的な説明(作成中) |
| `docs/concept-output-items.md` | 旧版の整理(ハッカソンの定義書にもとづく)。置き換え予定 |
| `examples/hackathon/` | ハッカソンの Web 地図アプリに、概念設計を当てはめた作業一式(概念、ジャーニー、API、検査ツール)。独自の `README.md` と `CLAUDE.md` がある |
| `docs/screen-grouping.md` | 概念を画面にまとめる手法(製品に依存しない)。道具は `tools/screen_groups.py` |
| `.herdr/` | tree-canvas で描いた木(旧版の項目の整理) |

作業の決まりは `CLAUDE.md` にあります。

## 使う(メンバー・AI 向け)

- 使い方: [`.claude/skills/concept-design/SKILL.md`](.claude/skills/concept-design/SKILL.md)(Claude Code の skill として、そのまま読み込める。人が読んでもよい)
- 動く実例: [`examples/hackathon/`](examples/hackathon/)(NAsVI の概念設計。`make lint` で検査できる)
- 自分のリポジトリで skill として使うには、`.claude/skills/concept-design/` をそのリポジトリにコピーし、このリポジトリを clone する。
- 画面設計を AI と進める(6 ステップ): [`.claude/skills/screen-design/SKILL.md`](.claude/skills/screen-design/SKILL.md)(検査: `tools/screen_check.py`)
