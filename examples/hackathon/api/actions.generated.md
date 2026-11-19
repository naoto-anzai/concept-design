# API の元表(導出結果。毎回上書きされるので手で編集しない)

導出元: concepts.yaml。手で書く仕様は `api/spec.md` に置く。
メソッドとパスは概念から機械的に付けた仮の値で、決める作業は TODO として残る。

## 1. 外から呼ぶ操作(`Request.*` で始まる同期)

| 要求 | 機能 | 実行する概念のアクション | メソッド(仮) | パス(仮) | 権限・条件(where) | 事前条件 → エラーの候補 |
|---|---|---|---|---|---|---|
| listPlaces | F1 | Place.list | GET | /place TODO | - | - |
| showPlace | F1 | Place.get | GET | /place TODO | - | Place.get: place が places に含まれる |
| registerPlace | F1 | Place.register | POST | /place TODO | 実行者が場所を管理できる | Place.register: location が与えられている |
| search | F1 | Search.query | GET | /search TODO | - | Search.query: keyword が空でない |
| browseKind | F4 | Labeling.itemsWith | GET | /labeling TODO | - | Labeling.itemsWith: label が labels に含まれる |
| assignLabel | F4 | Labeling.attach | POST | /labeling TODO | place が Place.places に含まれ、実行者が場所を管理できる | Labeling.attach: label が labels に含まれる |
| locate | F2 | Position.request | POST | /position TODO | - | Position.request: permission が 拒否 でない |
| setPosition | F2 | Position.setManually | POST | /position TODO | - | Position.setManually: point が与えられている |
| chooseDestination | F2 | Destination.choose | POST | /destination TODO | place が Place.places に含まれる | - |
| reportCongestion | F3 | Congestion.report | POST | /congestion TODO | place が Place.places に含まれ、実行者が報告できる | Congestion.report: level が 空き・やや混雑・混雑 のいずれか |
| readCongestion | F3 | Congestion.read | GET | /congestion TODO | - | - |

## 2. 1 回の要求で複数の概念が動く連動(整合の扱いを決める)

連動の途中で失敗したとき、全体を失敗にするか、一部だけ成功にするか。決めてから API の応答を書く。

- `Place.register` のあと `Search.index`  TODO: 失敗時の扱い
- `Place.update` のあと `Search.index`(条件: name が更新された)  TODO: 失敗時の扱い
- `Place.remove` のあと `Search.unindex`  TODO: 失敗時の扱い
- `Place.remove` のあと `Labeling.release`  TODO: 失敗時の扱い
- `Place.remove` のあと `Congestion.forget`  TODO: 失敗時の扱い
- `Place.remove` のあと `Destination.clear`(条件: Destination.chosen が、取り除かれた place である)  TODO: 失敗時の扱い

## 3. 外から呼ばない操作(`system: true`)

- `Position.update`: 端末から得た位置・精度・時刻で current・accuracy・takenAt を更新する  (時刻や端末の出来事で動く。呼び出し口を作るかは TODO)
- `Congestion.expire`: item を level・reportedAt から取り除く(不明に戻る)  (時刻や端末の出来事で動く。呼び出し口を作るかは TODO)

## 4. 概念の状態 → リソースの候補

### Place

```
places: set Place
name: Place -> String
kind: Place -> {企画, 駐車場}
location: Place -> Point
description: Place -> String
```

### Search

```
text: Item -> String
```

### Labeling

```
labels: set Label
labeled: Item -> set Label
```

### Position

```
permission: {未確認, 許可, 拒否}
current: Point?
accuracy: Number?
takenAt: Time?
```

### Destination

```
chosen: Item?
```

### Congestion

```
level: Item -> {空き, やや混雑, 混雑}
reportedAt: Item -> Time
```

## 5. 決まっていない前提

- OQ-1: 混雑の報告と場所の登録を、誰が、どの端末で、いつ行うか(運営のみか、出展者か、来場者の通報も含めるか)
- OQ-2: GPS が取れないとき、現在地を手で指定する操作を P1 に入れるか
- OQ-3: 種類(カテゴリ)で選ぶ F4 を P1 に入れるか。Place.kind(企画 / 駐車場)との線引きはどうするか
- OQ-4: 混雑の段階数(3 段階でよいか)と、報告が古いとみなす時間
- OQ-5: 場所のデータをどう入れるか(運営が操作して登録するか、スプレッドシートから取り込むか)
- OQ-7: input.yaml の課題・機能 F1〜F4 は、ボードの P1 案と合っているか(画像から推測した下書き)
