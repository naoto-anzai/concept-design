# ジャクソンの概念設計: 前提から順に組み立てる

作成: 2026-11-17 / 状態: draft(作成者の草稿。利用者の確認前)

## 0. この文書について

**目的。** ダニエル・ジャクソンが提唱する「概念設計」の形を、前提から順に組み立てて示す。この文書を読んで、利用者が、自分のイメージとジャクソンの形が合っているかを確かめる。

**根拠。** ジャクソン本人が著者または共著者の資料だけ。他の資料(定義書、他人の解説)は使っていない。引用は原文(英語)のまま、1 つ 25 語以内。各引用に、作成者による日本語訳を付けた。

| 略号 | 資料 |
|---|---|
| WYSIWID | Meng & Jackson, *What You See Is What It Does*(Onward! 2025)。https://arxiv.org/html/2508.14511 |
| NFM | Jackson, *Concept Design Moves*(NASA Formal Methods 2022) |
| CCSD | Wilczynski, Gregoire-Wright, Jackson, *Concept-Centric Software Development*(arXiv 2304.14975) |
| AB2、AB3、AB5 | Autodesk Boston ワークショップ(2025-03)のスライド。AB3 は *designing concepts* |
| WA、WB、WC | Autodesk Online ワークショップ(2025-06)のスライド。part 1〜3 |
| CHEAT | *Concept design cheatsheet*(2 ページ) |
| RUBRIC | *Criteria for modularity in concept design*(1 ページ) |
| T-… | essenceofsoftware.com のチュートリアル(T-criteria、T-purpose、T-principle、T-state、T-machine、T-modularity、T-dependency、T-sync) |

読めなかった資料: 本 *The Essence of Software* の全文、`autodesk/schedule/pdfs/3-concept-design.pdf` と `6-the-QDM.pdf`(404)。

**読み方。** 各段は、「前提 → 言えること → 新しく出てくる言葉」の順に書く。前の段で定義していない言葉は、後の段の前提に使わない。

- 【引用】は、ジャクソンの原文。Markdown の引用ブロックで示し、「訳」は作成者の翻訳、最後の「—」に出典を付ける。
- 【解釈】は、作成者の読み方。ジャクソンの言葉ではない。
- 【未確認】は、読んだ資料では確認できなかったこと。推論で埋めない。

**用語の訳。**

| 英語 | 日本語 |
|---|---|
| concept | 概念 |
| purpose | 目的 |
| operational principle(principle) | 運用規則 |
| state | 状態 |
| action | アクション |
| precondition / postcondition | 事前条件 / 事後条件 |
| synchronization(sync) | 同期 |
| type parameter(generic type) | 型パラメータ |
| independence / specificity / completeness | 独立性 / 特定性 / 完全性 |

運用規則は、資料により `principle` と `operational principle` の 2 つの綴りがある。同じものを指す。

**書き方の方針。** 資料により書き方が違う所は、次のように揃える(違いの全体は 14 章)。

- 概念の仕様: 2025 年のスライド(AB3、WB)の書き方。
- 同期: 2025 年のスライド(WA、WC、AB3)の `when` / `where` / `then`。
- 型パラメータの当てはめだけ: 古い資料(T-modularity、NFM)の書き方。新しい資料には、書く場所が無い(11 章)。この組み合わせは、ジャクソンの資料には書かれていない。整合性の点検は 15 章。

---

## 1. 段 1: 概念とは何か

**前提。** ソフトウェアは、利用者が使う機能の集まりである。

**言えること 1。** 概念は、機能を、利用者に見える単位に分けたもの。

> "Concepts are user-facing units of functionality that have a well defined purpose and thus deliver some recognizable value."
>
> 訳: 概念は、利用者に見える機能の単位であり、明確に定められた目的を持ち、したがって、認識できる何らかの価値を届ける。
>
> — WYSIWID 2 節

**言えること 2。** 機能の単位が、概念と呼べるための基準が 3 つある。

> "A concept is a bundling of functionality that meets three modularity criteria"
>
> 訳: 概念は、3 つのモジュール性の基準を満たす、機能のまとまりである。
>
> — T-modularity

> "Specificity: The concept fulfills a specific purpose that brings real value to the user, and does not mix, multiple separable purposes."
>
> 訳: 特定性: 概念は、利用者に本物の価値をもたらす特定の目的を果たし、分けられる複数の目的を混ぜない。
>
> — T-modularity

> "Completeness: The concept’s functionality meets its purpose fully."
>
> 訳: 完全性: 概念の機能は、その目的を十分に満たす。
>
> — T-modularity

> "Independence: The concept stands by itself, without reference to other concepts."
>
> 訳: 独立性: 概念は、他の概念に言及せず、それだけで成り立つ。
>
> — T-modularity

**新しく出てくる言葉。** 概念、目的(次の段で詳しく)、特定性、完全性、独立性。

- 以降の段は、この 3 つの基準を満たす概念を、どう書くかを順に示す。
- 資料により、1 つめの基準の呼び名が違う(特定性 / separation of concerns / non-conflation)。14 章を参照。

---

## 2. 段 2: 概念を、5 つの部分で書く

**前提。** 概念は、特定性・完全性・独立性を満たす機能の単位(段 1)。

**言えること。** 概念の仕様は、5 つの部分で書く。

> "Name: pithy and mnemonic, one word if possible"
>
> 訳: 名前: 簡潔で覚えやすく、できれば 1 語。
>
> — CHEAT p.1

> "Purpose: what motivated the concept, what value it brings"
>
> 訳: 目的: 概念のきっかけとなったもの。概念がもたらす価値。
>
> — CHEAT p.1

> "Principle: archetypal scenario showing how it’s used"
>
> 訳: 原則(運用規則): 使われ方を示す、典型的なシナリオ。
>
> — CHEAT p.1

> "Actions: performed by user or concept, read/write state"
>
> 訳: アクション: 利用者または概念が行う。状態を読み書きする。
>
> — CHEAT p.1

> "State: a data model, what the running concept remembers"
>
> 訳: 状態: データモデル。動いている概念が覚えていること。
>
> — CHEAT p.1

**新しく出てくる言葉。** 名前、目的、運用規則、アクション、状態。各部分の詳しい定義は、次の段以降に置く。

**設計する順序。** 1 つの概念を設計する手順は、5 段。名前 → 目的 → 物語 → アクション → 状態。

> "process for designing a concept"
>
> 訳: 概念を設計する手順
>
> — AB3 スライド 2、11、34

- 5 段の見出し(原文): "pick a name"(訳: 名前を選ぶ)、"describe purpose"(訳: 目的を述べる)、"tell story"(訳: 物語を語る)、"list actions"(訳: アクションを列挙する)、"specify state"(訳: 状態を定める)。AB3 スライド 34 は、この 5 段を、仕様の 5 つの部分に 1 つずつ対応させている。
- 【解釈】この文書は、この順序で説明する。仕様に書く順序(完成した仕様は purpose、principle、state、actions の順。AB3 スライド 23)とは違う。
- 【解釈】3 つの基準のうち、独立性は、アクションと状態を書く段で効いてくる(6 章)。完全性は、運用規則と、アクション・状態の見直しで確かめる(5、8 章)。特定性は、目的と、分け方の段で効く(4、13 章)。

**概念の中の「欠かせない 3 つ」と、振る舞いを定める 2 つ。**

> "three essential parts of a concept: the name (“restaurant reservation”), the purpose (ensuring a table will be available) and the operational principle"
>
> 訳: 概念の欠かせない 3 つの部分: 名前(「restaurant reservation」)、目的(席が確保されること)、そして運用規則。
>
> — T-criteria

- 状態とアクションは、振る舞いを詳しく定めるために、後から足す(WA スライド 48、50)。
- 5 つの部分を数える資料(CHEAT、AB3 スライド 34、CCSD)と、3 つを数える資料(T-criteria、WA スライド 48)がある。この文書は、5 つを仕様として扱う。【解釈】3 つは説明のための最小限、5 つは振る舞いまで定めた仕様、という使い分けに読める。

---

## 3. 段 3: 名前

**前提。** 概念を指し示す呼び名が要る。

**言えること。**

> "pick a name / specific to function / but for general use"
>
> 訳: 名前を選ぶ / 機能に特定的に / ただし一般に使えるように
>
> — AB3 スライド 2、12

> "Name: pithy and mnemonic, one word if possible"
>
> 訳: 名前: 簡潔で覚えやすく、できれば 1 語。
>
> — CHEAT p.1

- 例(AB3 スライド 12): 候補 Event / EventTicket / EventTicketing / Ticket から、`EventTicket` を採った。

**新しく出てくる言葉。** なし。

**注。** 名前の後ろに `[User]` のような型パラメータを付けることがある。これは、6 章で定義する。

---

## 4. 段 4: 目的

**前提。** 概念は、特定の目的を持つ(段 1 の特定性)。

**言えること 1。** 目的は、概念がなぜあるかの説明である。

> "A concept purpose is an explanation of why the concept exists"
>
> 訳: 概念の目的とは、その概念がなぜ存在するかの説明である。
>
> — T-purpose

> "describe purpose / why design or use it? / value to stakeholders"
>
> 訳: 目的を述べる / なぜ設計し、使うのか / 関係者にとっての価値
>
> — AB3 スライド 2、13

**言えること 2。** 良い目的の基準が 3 つある。

> "Need-focused. The purpose should be stated in terms of the needs of the user."
>
> 訳: 必要に焦点を当てる。目的は、利用者の必要の言葉で述べる。
>
> — T-purpose

> "Specific. The purpose should be specific to the design of the concept at hand."
>
> 訳: 特定的であること。目的は、いま扱っている概念の設計に特定的でなければならない。
>
> — T-purpose

> "Evaluable. A purpose should be a yardstick against which to measure a concept design."
>
> 訳: 評価できること。目的は、概念の設計を測る物差しでなければならない。
>
> — T-purpose

**言えること 3。** 1 つの概念の目的は、1 つ。

> "a concept should have at most one purpose"
>
> 訳: 概念は、多くても 1 つの目的を持つべきである
>
> — T-purpose

- 同じ節に、"a concept should have at least one purpose"(訳: 概念は、少なくとも 1 つの目的を持つべきである) もある。

**例(AB3 スライド 13)。** 候補は organizing events / raising money for events / issuing tickets for events / managing event attendance。採ったのは `managing event attendance`。

**新しく出てくる言葉。** なし(目的は、段 1 で出ていた言葉を定義した)。

**【未確認】** 目的の文の形(動名詞か、不定詞か)に決まりは無い。資料の例は、`managing event attendance`(AB3)、`rank items by popularity`(WA)、`to securely store and validate user credentials`(WYSIWID)、`authenticate users`(T-sync)と、ばらばらである。

---

## 5. 段 5: 運用規則(物語)

**前提。** 目的が決まった(段 4)。目的が本当に果たされるかは、目的の文だけでは確かめられない。

**言えること 1。** 目的が果たされる典型の流れを、物語として書く。これが運用規則である。

> "Each concept has one or more such stories that explain how to use the concept, and show that the concept fulfills its purpose."
>
> 訳: どの概念にも、概念の使い方を説明し、概念が目的を果たすことを示す、そのような物語が 1 つ以上ある。
>
> — T-principle

> "a kind of archetypal scenario that describes how the concept fulfills its purpose"
>
> 訳: 概念がどのように目的を果たすかを述べる、一種の典型的なシナリオ
>
> — WYSIWID 4 節

> "if you perform some actions, then some result occurs that fulfills a useful purpose"
>
> 訳: いくつかのアクションを行えば、有用な目的を果たす何らかの結果が起こる
>
> — T-principle

**言えること 2。** なぜ、物語が要るか。

> "the OP helps by distinguishing the archetypal scenario from other scenarios that are equally plausible"
>
> 訳: 運用規則は、典型的なシナリオを、同じくらいもっともらしい他のシナリオから区別することで、役に立つ
>
> — T-principle

> "if it takes the form “when this action happens, the state is updated in this way” you’ll know something is missing"
>
> 訳: 「このアクションが起きたら、状態はこのように更新される」という形になるなら、何かが欠けているとわかる
>
> — T-criteria

- 【解釈】物語が書けない概念は、目的を果たすのに足りない。段 1 の完全性を確かめる道具になる。

**言えること 3。** 書き方の注意。

- 準備(setup)を含める。

  > "tell story / a simple scenario / of how it’s used / including setup"
  >
  > 訳: 物語を語る / 単純なシナリオ / 使われ方の / 準備を含めて
  >
  > — AB3 スライド 14

- 1 つの概念だけを書く。

  > "If your OP looks complicated, you may be mixing the OPs of distinct concepts."
  >
  > 訳: 運用規則が複雑に見えるなら、別々の概念の運用規則を混ぜているのかもしれない。
  >
  > — T-principle

- 画面ではなく、アクションと状態の言葉で書く。

  > "Write the OP in terms of the actions and states that form the concept"
  >
  > 訳: 運用規則は、概念を成すアクションと状態の言葉で書く
  >
  > — T-principle

- 全部の詳細を書かない。

  > "the OPs of a concept aren’t intended to specify it fully, so they can be few and brief"
  >
  > 訳: 概念の運用規則は、概念を完全に定めるためのものではないので、少なく短くてよい
  >
  > — T-principle

**例(AB3 スライド 23)。** `EventTicket` の運用規則。

> an event organizer creates an event (and announces it or invites people to it); they can then register, and the organizer can see who registered; eventually the people who registered can attend the event
>
> 訳: イベントの主催者がイベントを作る(そして、告知するか、人々を招待する)。人々はそこで登録でき、主催者は誰が登録したかを見られる。やがて、登録した人々はイベントに出席できる。
>
> — AB3 スライド 23

**新しく出てくる言葉。** 運用規則。

- **注。** この例の「event を作る」「register する」「attend する」が、次の段のアクションの手がかりになる。

> "let’s return to our story / for hints about the actions"
>
> 訳: 物語に戻ろう / アクションの手がかりを探しに
>
> — AB3 スライド 16

---

## 6. 段 6: アクション(名前・引数・戻り値・型)と、型パラメータ

**前提。** 物語(段 5)には、起こる出来事がある。出来事に名前を付け、何を渡し、何が返るかを決める。

**言えること 1。** 物語の出来事を、アクションにする。

> "list actions / by user or system / key steps, not UI"
>
> 訳: アクションを列挙する / 利用者またはシステムによる / 鍵になる手順であり、画面操作ではない
>
> — AB3 スライド 2、15〜16

- 画面の細かい操作は、アクションではない。

  > "no! these are / all low-level / UI interactions"
  >
  > 訳: だめ! これらは / すべて低水準の / 画面操作である
  >
  > — AB3 スライド 15

- 他の概念に属する手順も、入れない。

  > "no! these belong / to other concepts"
  >
  > 訳: だめ! これらは / 他の概念に属する
  >
  > — WB スライド 14

**言えること 2。** アクションは、見出し(名前と引数)と、本体を持つ。この段では、見出しを決める。本体は、8 章。

> "Each action has a header that names the action and lists some arguments, and a body that defines the action’s behavior"
>
> 訳: どのアクションも、アクションに名前を付けて引数を並べる見出しと、アクションの振る舞いを定める本体を持つ。
>
> — T-machine

- 引数を決めるのは、名前を付けた後。(AB3 スライド 17 "formalizing actions"(訳: アクションを形式化する))
- 戻り値は、見出しの後ろに `: 型` と書く。

  > "create (by: User, on: Date): Event"
  >
  > 訳: (アクションの見出しの例。引数は `by`(`User`)と `on`(`Date`)、戻り値の型は `Event`)
  >
  > — AB3 スライド 17

**言えること 3。** 引数や戻り値には、型を付ける。型は、「どんな種類のものか」の名前である。

- 基本の型(`String` など)は、どの概念からも使える。

  > "The standard primitive types are assumed to be defined globally"
  >
  > 訳: 標準の基本の型は、全体で定義されていると仮定する
  >
  > — T-state

- それ以外の型は、概念の外から見ると、同一性だけを持つ。

  > "a concept is a state machine whose non-primitive types denote objects only in the sense that they have identity"
  >
  > 訳: 概念は状態機械であり、その基本でない型は、同一性を持つという意味でのみ、オブジェクトを表す
  >
  > — T-state

**言えること 4。** 引数や戻り値の型に、他の概念が作るものが出てくることがある。そのとき、その型を、他の概念の名前で書けない。

- 前提(段 1 の独立性)。

  > "Concept does not refer to another concept by name."
  >
  > 訳: 概念は、他の概念を名前で参照しない。
  >
  > — RUBRIC

> "a concept’s state should never refer to types that are introduced in another concept"
>
> 訳: 概念の状態は、他の概念で導入された型を、決して参照してはならない
>
> — T-state

> "there’s no other way to say that a type in one concept matches a type in another (except for the primitive types such as String)"
>
> 訳: ある概念の型が、別の概念の型と対応することを言う方法は、ほかに無い(`String` のような基本の型を除く)
>
> — T-state

**結論: 型パラメータ。** 他の概念から来るものの型は、型パラメータとして宣言する。

> "any type whose objects will (at runtime) come from another concept should be declared as a type parameter"
>
> 訳: (実行時に)他の概念からオブジェクトが来る型は、型パラメータとして宣言すべきである
>
> — T-state

> "listing the generic types as parameters of the concept"
>
> 訳: 総称的な型を、概念のパラメータとして並べること
>
> — WC スライド 23

- 書き方は、概念の名前の後ろに `[User]` と書く。

  > "User is a generic type"
  >
  > 訳: User は総称的な型である
  >
  > — AB3 スライド 20。`concept EventTicket [User]` への注記

- 型パラメータには制約を付けられない。

  > "Type parameters cannot be constrained, so this ensures no external coupling or dependence on whatever type is actually used to represent users."
  >
  > 訳: 型パラメータは制約できない。したがって、利用者を表すのに実際に使われる型が何であっても、外部との結合や依存が無いことが保証される。
  >
  > — WYSIWID 4 節

- 型パラメータは、「概念を使うときに与えられる具体的な型の置き場所」である。

  > "placeholders for concrete types that will be provided when the concept is used"
  >
  > 訳: 概念を使うときに与えられる、具体的な型の置き場所
  >
  > — T-state

**例(AB3 スライド 23)。** `EventTicket [User]` のアクション。

```
create (by: User, on: Date): Event
register (e: Event, u: User)
attend (e: Event, u: User)
```

- `Event` は、`create` が作って返す。この概念の中で作られるので、型パラメータではない。
- `User` は、この概念のどのアクションも作らない。他の概念が作る利用者が、引数として渡される。だから型パラメータ `[User]` にする。
- 逆の例。

  > "the Task type is not treated as a type parameter; the assumption is that task objects are generated by this concept"
  >
  > 訳: Task 型は、型パラメータとして扱わない。タスクのオブジェクトは、この概念が生成すると仮定する
  >
  > — NFM 2 節

- 【解釈】判定の問いは、「その型のものは、実行時に、この概念の外から来るか」。来るなら型パラメータ、この概念が作るなら、型パラメータにしない。

**新しく出てくる言葉。** アクション(見出し、引数、戻り値)、型、基本の型、型パラメータ。

**【未確認】** 型パラメータに具体的な型を当てる方法は、この段では決まらない。11 章で扱う。

---

## 7. 段 7: 状態

**前提。** アクションが決まった(段 6)。アクションが働くには、概念が覚えていることが要る。

**言えること 1。** 状態は、概念が実行時に覚えていること。アクションに要るものだけを入れる。

> "The state is the concept’s memory."
>
> 訳: 状態は、概念の記憶である。
>
> — T-state

> "If some piece of information is needed in an action, then it will have to be in the memory"
>
> 訳: ある情報がアクションに必要なら、それは記憶の中になければならない
>
> — T-state

> "if it will never be needed, it shouldn’t be there, even if it’s interesting"
>
> 訳: 決して必要にならないなら、たとえ興味深くても、そこにあってはならない
>
> — T-state

> "Sufficiency. The state must be rich enough to support the actions."
>
> 訳: 十分性。状態は、アクションを支えられるだけ豊かでなければならない。
>
> — T-state

> "the state should not include components that are not necessary to support the actions"
>
> 訳: 状態には、アクションを支えるのに必要でない成分を含めるべきではない
>
> — T-state

> "To design the state, you consider what must be remembered by the concept in order to support the actions."
>
> 訳: 状態を設計するには、アクションを支えるために、概念が何を覚えておかなければならないかを考える。
>
> — T-machine

**言えること 2。** 状態は、変数の宣言の列。変数は、集合か、関係である。

> "We’ll define the state of a concept as a series of variable declarations. Each variable will correspond to a set, or to a relation."
>
> 訳: 概念の状態を、変数の宣言の列として定義する。各変数は、集合か関係に対応する。
>
> — T-state

- この考え方と記法は、Alloy から来ている。

  > "This way of thinking about state is taken from the Alloy language"
  >
  > 訳: 状態についてのこの考え方は、Alloy 言語から取られている
  >
  > — T-state

**言えること 3。** 言葉での書き方と、記法を並べる(AB3 スライド 18)。

| 言葉(informally) | 記法 |
|---|---|
| a set of events | `events: set Event` |
| for each event, a date/time | `date: Event -> one Date` |
| for each event, an organizer | `organizer: Event -> one User` |
| for each event, a set of registrants | `registrants: Event -> set User` |

- `set`(宣言の左): 集合の宣言。

  > "As an example of a set declaration, we might have a set of pending invitations"
  >
  > 訳: 集合の宣言の例として、保留中の招待の集合がありうる
  >
  > — T-state

- `A -> B`: 関係の宣言。多重度の語が無い `->` は、制限の無い関係。
- `one`:

  > "The multiplicity keyword one says that each pair of users maps to a single date."
  >
  > 訳: 多重度のキーワード `one` は、利用者の各組が、1 つの日付に対応することを言う。
  >
  > — T-state

- `lone`:

  > "we have to weaken the multiplicity from one to lone (zero or one)"
  >
  > 訳: 多重度を `one` から `lone`(0 個か 1 個)に弱めなければならない
  >
  > — T-state

- `-> set`: 左の 1 つに、集合が対応する。【解釈】`set` を多重度として説明する文は、読んだ資料に無い。AB3 スライド 18 の、言葉と記法の対応から読み取った。

**言えること 4。** 状態は、型パラメータの型(段 6)も使える。`organizer: Event -> one User` の `User` は、`EventTicket [User]` の型パラメータである。

**言えること 5。** 状態は、集合と 2 項関係だけで表せる。

> "states can be represented as just sets & binary relations"
>
> 訳: 状態は、集合と 2 項関係だけで表せる
>
> — WB スライド 46

> "abstract enough to avoid making any premature implementation commitments, but at the same time is easily translated into code"
>
> 訳: 実装について早まった約束をしないほど抽象的で、同時に、コードに容易に翻訳できる
>
> — T-state

- 1 つのオブジェクトのフィールドのように書くのは、悪い兆候。

  > "Symptom: State is defined like fields of an object"
  >
  > 訳: 兆候: 状態が、オブジェクトのフィールドのように定義されている
  >
  > — CHEAT p.2

**新しく出てくる言葉。** 状態、集合(`set`)、関係(`->`)、多重度(`one`、`lone`)。

**【未確認】**

- `set` を、矢印の右の多重度として定義する文。`opt`、`const` の意味を説明する文。例(T-sync: `shortFor: String -> opt Target`、T-machine: `const shorthands: set String`)には出てくる。
- 矢印の左側が、型を指すのか、状態の集合を指すのか。AB3 は `date: Event -> one Date`(左が型)、T-machine は `shortFor: used -> one URL`(左が状態の集合の名前)と書く。説明の文は、読んだ資料に無い。
- 初期状態を書く節。"initially"(訳: 最初は) という語は WB スライド 18、42 に出るが、仕様の節ではない。

---

## 8. 段 8: アクションの事前条件・事後条件と、見直し

**前提。** 見出しが決まった(段 6)。状態が決まった(段 7)。アクションの本体が、状態の言葉で書ける。

**言えること 1。** アクションの本体は、事前条件と事後条件から成る。

> "preconditions that limit when the action can occur, and postconditions that say what effect the action has"
>
> 訳: アクションがいつ起こりうるかを制限する事前条件と、アクションがどんな効果を持つかを述べる事後条件
>
> — T-machine

> "“precondition” / what’s true of state before"
>
> 訳: 「事前条件」 / 前の状態で成り立っていること
>
> — WB スライド 17

> "“postcondition” / relates state after to before"
>
> 訳: 「事後条件」 / 後の状態を前の状態に関係づける
>
> — WB スライド 17

**言えること 2。** 事前条件・事後条件の見出しは、`requires` と `ensures`。

- 例(WB スライド 17): `reserve (u: User, t: Time): Reservation` / `requires` some slot at time t not yet reserved / `ensures` creates & returns a fresh reservation
- 事前条件が成り立たないとき、概念はアクションを拒める。

  > "A concept can refuse an action"
  >
  > 訳: 概念は、アクションを拒否できる
  >
  > — NFM 2.2 節

- 事前条件の強さが、概念のモード的な度合いを決める。

  > "strength of preconditions / determines how modal"
  >
  > 訳: 事前条件の強さが / 概念がどれだけモード的かを決める
  >
  > — WB スライド 28

**言えること 3。** 事後条件は、くだけた言葉でもよい。

- 例(AB3 スライド 21): `create` の本体を、`// set e.date to on`、`// set e.organizer to by` と書く。`register` は `// add u to e.registrants`。

> "the specification of the action is only partial"
>
> 訳: アクションの仕様は、部分的でしかない
>
> — WYSIWID 4 節

- 理由は "these details are not needed for synchronizations"(訳: これらの細部は、同期には必要ない)。

**言えること 4。** アクションの本体を書くと、状態の不足が見つかる。状態に戻って足す。

- 例(AB3 スライド 21〜22): `attend` の本体が、"// ???"(訳: (コメントで「???」。まだ書けていない)) になる。「出席した人」を覚える状態が無いから。`attendees: Event -> set User` を足して、書けるようになる。

> "specifying the actions, take two"
>
> 訳: アクションの仕様を書く、2 回目
>
> — AB3 スライド 22 の見出し

> "Write careful specs of each actions and expand the state accordingly"
>
> 訳: 各アクションの仕様を注意深く書き、それに応じて状態を広げる
>
> — CHEAT p.2

- 【解釈】手順は一方向ではなく、戻りがある。段 7 と段 8 は、行き来する。

**言えること 5。** アクションの抜け、概念の完全性の確かめ。

> "have you covered the whole life cycle? / is there an initial setup? a winding down?"
>
> 訳: 生涯の全体をカバーしているか / 最初の準備はあるか。終わりのアクションはあるか
>
> — WB スライド 21

> "are there ways to undo previous actions?"
>
> 訳: 以前のアクションを取り消す方法はあるか
>
> — WB スライド 21

**新しく出てくる言葉。** 事前条件(`requires`)、事後条件(`ensures`)。

**【未確認】** `effects` という見出しは、読んだ資料に無い(出てくるのは `requires` / `ensures` と、precondition / postcondition)。

---

## 9. 段 9: 完成した仕様(ここまでの確認)

段 1〜8 で出てきた 5 つの部分が、そろった。AB3 スライド 23 の、完成した仕様(原文のまま)。

```
concept EventTicket [User]
purpose managing event attendance
principle an event organizer creates an event (and
announces it or invites people to it); they can then register,
and the organizer can see who registered; eventually the
people who registered can attend the event
state
 events: set Event
 date: Event -> one Date
 organizer: Event -> one User
 registrants: Event -> set User
 attendees: Event -> set User
actions
create (by: User, on: Date): Event
register (e: Event, u: User)
attend (e: Event, u: User)
```

- 名前(段 3)、目的(段 4)、運用規則(段 5)、状態(段 7)、アクション(段 6、8)が、対応している。
- 型パラメータ `[User]`(段 6)が、状態とアクションの両方に出ている。
- この例では、アクションの本体(事前条件・事後条件)は、省かれている。
- 仕様に書く順序は、名前、目的、運用規則、状態、アクション。設計する順序(段 3〜8)とは違う。

---

## 10. 段 10: 概念をつなぐ(同期)

**前提。** 概念は独立している(段 1)。1 つの機能は、複数の概念が協力して実現することがある。独立のまま、つなぐ方法が要る。

**言えること 1。** 概念の外に、つなぎを書く場所を置く。これが同期である。

> "All data and control flow between concepts is expressed in the code of this layer."
>
> 訳: 概念の間のデータと制御の流れは、すべて、この層のコードで表される。
>
> — WYSIWID 3 節

> "This is how coupling between the concepts themselves is avoided"
>
> 訳: こうして、概念そのものの間の結合が避けられる
>
> — WYSIWID 3 節

> "app-specific behaviors / often in syncs alone / so concepts stay pure"
>
> 訳: アプリ固有の振る舞いは / しばしば同期だけに / だから概念は純粋なままでいる
>
> — AB3 スライド 27

> "runtime coupling / but no design coupling / or code coupling"
>
> 訳: 実行時の結合はあるが / 設計上の結合は無く / コード上の結合も無い
>
> — AB3 スライド 27

**言えること 2。** 同期は、`when` / `where` / `then` の 3 つの部分から成る。

> "when these actions happen, where the current state of things are so, then these actions should follow"
>
> 訳: これらのアクションが起きたとき、物事の現在の状態がこうであれば、これらのアクションが続くべきである
>
> — WYSIWID 5 節

> "when: a pattern for matching action completions"
>
> 訳: when: アクションの完了に合うパターン
>
> — WYSIWID 5.1 節

> "where: a query on the states of one or more concepts, as well as any calculations not requiring state"
>
> 訳: where: 1 つ以上の概念の状態への問い合わせと、状態を必要としない計算
>
> — WYSIWID 5.1 節

> "then: a list of action invocations to be executed by their associated concepts"
>
> 訳: then: 関連づけられた概念が実行する、アクション呼び出しの並び
>
> — WYSIWID 5.1 節

> "The parts (all required except for where)"
>
> 訳: 部分(where 以外は、すべて必須)
>
> — WYSIWID 5.1 節

**言えること 3。** アクションの記録を読むのは `when` だけ。概念の状態を読むのは `where` だけ。

> "Synchronizations confine reads of action records to the when clause and reads of concept state to the where clause."
>
> 訳: 同期は、アクションの記録を読むことを when 節に、概念の状態を読むことを where 節に限る。
>
> — WYSIWID 7.2 節

> "Concepts do not query each other’s states, but synchronizations can query them, often across multiple concepts"
>
> 訳: 概念どうしは互いの状態に問い合わせないが、同期は、しばしば複数の概念にまたがって、問い合わせられる
>
> — WYSIWID 6.5 節

- したがって、状態を読むだけのアクション(getter)は、要らない。

  > "Our solution to this is simply to have no getters."
  >
  > 訳: これへの解決は、単に getter を持たないことである。
  >
  > — WYSIWID 6.4 節

- CHEAT p.2 の law #10 も同じ趣旨。
- ただし、利用者にとって意味がある場合は、状態を変えないアクションがあってもよい。

  > "the check action of the Password concept is genuinely an action that would make sense to a user"
  >
  > 訳: Password 概念の `check` アクションは、利用者にとって意味がある、本物のアクションである
  >
  > — WYSIWID 4 節

**例 1: `when` と `then` だけ(AB3 スライド 26、原文)。**

```
when Web.req (register, email, fst, lst, event)
then u = UserProfile.create (fst, lst, email)
     EventTicket.register (event, u)
```

- 意味: 外から「登録」の要求が来たら、`UserProfile` で利用者を作り、その利用者を `EventTicket` の `register` に渡す。
- `UserProfile` と `EventTicket` は、互いを知らない。つなぎは、この同期だけにある。
- `UserProfile` の仕様は、AB3 スライド 24〜25 にある(`create (fst, lst: String, e: Email): User`)。
- この例は、`u` が `UserProfile` の作った利用者であり、`EventTicket.register` の引数 `u: User`(型パラメータ)に渡る様子を示している。11 章で使う。

**例 2: `where` で条件を付ける(WA スライド 56、原文)。**

```
when WebRequest (downvote, post, session)
where active user is u (in Session state)
      u has at least 20 points (in Karma state)
then Post.downvote (post, u)
```

- 意味: ダウンボートの要求が来て、利用者が 20 ポイント以上なら、ダウンボートを実行する。
- 概念 `Session`、`Karma`、`Post` は、スライドで別に定義されている。ここでは省略する。
- 【解釈】権限や、他の概念の状態に依る条件は、`where` に書く。権限を書くための専用の構文は、読んだ資料に無い。例はすべて、`where` に条件を書く形。

**言えること 4。** 外からの要求も、アクションとして扱う。

> "regard the incoming request as itself an action to which a synchronization reacts"
>
> 訳: 入ってくる要求を、同期が反応するアクションそのものとみなす
>
> — WYSIWID 3 節

> "These actions are treated as the actions of a special bootstrap concept."
>
> 訳: これらのアクションは、特別な bootstrap concept のアクションとして扱われる。
>
> — WYSIWID 6.7 節

> "the Web concept encapsulates the details of HTTP request and response structures"
>
> 訳: Web 概念は、HTTP の要求と応答の構造の細部を包み込む
>
> — WYSIWID 6.7 節

- この擬似的な概念の名前は、資料により違う: `Web/request`(WYSIWID)、`Web.req`(AB3)、`Web.request`(WC)、`WebRequest`(WA)。この文書では、「外からの要求のアクション」と呼ぶ。

**新しく出てくる言葉。** 同期、`when`、`where`、`then`、bootstrap concept(外からの要求を扱う擬似的な概念)。

**【未確認】**

- 時間の経過で起きるアクション(期限切れなど)を、新しい書き方でどう書くか。WYSIWID は、アクションを始められるのは bootstrap concept だけと書くが、時間の経過の扱いは述べていない。古い資料(T-machine)には、`system expire` という、システムが行うアクションがある。
- 同期の `then` の中の `u = ...` の代入と、`et.catalog = ec`(AB3 スライド 26)の意味。`catalog` は、どの概念の状態の宣言にも無い。この文書は、後者を使わない。

---

## 11. 段 11: 型パラメータには、何を当てるか

**前提。** 型パラメータは、概念を使うときに与えられる具体的な型の置き場所(段 6)。

**言えること 1。** 当てはめは、概念の外で決まる。概念の中では書けない。

- 段 6 の独立性から。型パラメータを、他の概念の型の名前で書くと、独立性に反する。

**言えること 2(古い資料)。** アプリの定義で、概念を取り込むときに、具体的な型を渡す。

> "to describe our application we need to instantiate the type parameters"
>
> 訳: アプリケーションを記述するには、型パラメータを具体化する必要がある
>
> — T-modularity「Genericity」

- 例(T-modularity、原文): `app EmailClient includes User, Email [User.User], Label [Email.Msg]`
- 例(T-sync、原文): `include Shorthand [HTTP.URL]`、`include Session [User.User]`

> "The instantiation of the Label concept passes in the Task type of the Todo concept as a parameter"
>
> 訳: Label 概念の具体化は、Todo 概念の Task 型を、パラメータとして渡す
>
> — NFM 2.2 節。`Label [Todo.Task]`

> "it makes it clear that Label is a more general concept that allows the organization and filtering of any kind of item"
>
> 訳: Label が、あらゆる種類のものの整理と絞り込みを可能にする、より一般的な概念であることが明らかになる
>
> — T-modularity「Genericity」

**言えること 3(新しい資料)。** 当てはめを宣言する場所は、書かれていない。

> "We avoid this by representing all external references with UUIDs."
>
> 訳: これを避けるため、外部への参照はすべて UUID で表す。
>
> — WYSIWID 6.4 節

> "static checking cannot yet ensure that such references are used consistently"
>
> 訳: 静的な検査は、そのような参照が一貫して使われていることを、まだ保証できない
>
> — WYSIWID 6.4 節

> "Users are created in this User concept and shared with other concepts by syncs"
>
> 訳: 利用者は、この User 概念で作られ、同期によって他の概念と共有される
>
> — WC スライド 22

- 【解釈】新しい資料では、型パラメータに何が入るかは、同期が、どの値を渡すかで決まる、と読める。ただし、そう明言した文は無い。

**この文書での扱い。** 10 章の例 1 に、古い書き方を当てはめる。

- `UserProfile` が作る `User` が、`EventTicket.register` の引数に渡る。
- 古い書き方で当てはめを書くなら、`EventTicket [UserProfile.User]` となる(**作成者の推論。この組み合わせは、ジャクソンの資料には書かれていない**。古い書き方 `Label [Todo.Task]` の形を、この例に当てはめたもの)。
- 新しい書き方の同期(10 章)は、当てはめを書く欄を持たない。同期が値を渡す流れ(`u = UserProfile.create (...)` から `EventTicket.register (event, u)`)で、当てはめが、事実上決まる(【解釈】)。

**新しく出てくる言葉。** 型パラメータの当てはめ(instantiate)。

**【未確認】** 新しい書き方の同期と、古い書き方の当てはめの宣言を、併せて使う例。読んだ資料に無い。整合性は 15 章で点検した。

---

## 12. 段 12: 概念の分け方・まとめ方

**前提。** 概念は、特定性・完全性・独立性を満たす(段 1)。設計の途中で、これが破れていることに気づく。そのとき、分ける、まとめる、広げる。

**言えること 1。** 特定性: 目的と概念は 1 対 1。

> "specificity / purposes:concepts are 1:1"
>
> 訳: 特定性 / 目的と概念は 1 対 1
>
> — WC スライド 33、AB5 スライド 7

- 1 つの目的に概念が 2 つ以上ある場合(冗長)は、まとめてよい。

  > "redundancy / >1 concept per purpose"
  >
  > 訳: 冗長 / 1 つの目的に、概念が 2 つ以上
  >
  > — WC スライド 33

- 1 つの概念に目的が 2 つ以上ある場合(過負荷)は、分ける。

  > "overloading / >1 purpose per concept"
  >
  > 訳: 過負荷 / 1 つの概念に、目的が 2 つ以上
  >
  > — WC スライド 33

> "A concept should not conflate separable functions"
>
> 訳: 概念は、分けられる機能を混同してはならない
>
> — CHEAT p.1 law #1

**言えること 2。** 完全性: 機能の一部だけで、価値を生まない概念は、広げる。

> "A concept includes only part of a function, doesn’t deliver full value"
>
> 訳: 概念が、機能の一部だけを含み、十分な価値を届けない
>
> — CHEAT p.1 law #2

> "completeness only means that the purpose is minimally satisfied"
>
> 訳: 完全性は、目的が最低限満たされることだけを意味する
>
> — T-modularity

**言えること 3。** なじみ。

> "Concept invents new way of doing something familiar, for no good reason"
>
> 訳: 概念が、良い理由なく、なじみのあることの新しいやり方を発明している
>
> — CHEAT p.2 law #8

> "familiarity—that whenever possible a design should reuse a concept that is familiar to users from other applications"
>
> 訳: なじみ。可能なときはいつでも、設計は、他のアプリケーションから利用者になじみのある概念を再利用すべきである
>
> — CCSD 2 節

**言えること 4。** 設計の動きは 6 つ。3 組の対。

> "There are six design moves, organized into three pairs of duals."
>
> 訳: 設計の動きは 6 つあり、双対の 3 組に整理される。
>
> — NFM 3 節

- split / merge(分ける / まとめる)、unify / specialize(一般化 / 特殊化)、tighten / loosen(同期を締める / 緩める)。

> "trade off simplicity and directness of usage on the one hand with flexibility on the other"
>
> 訳: 使い方の単純さと直接さを一方に、柔軟さを他方にして、引き換える
>
> — NFM 3.1 節。分割と統合

**【未確認】**

- アプリ全体を概念に分ける、番号付きの手順。基準と例(WC スライド 26〜30)はあるが、順序を定めた手順は確認できなかった。
- 工数や実装の都合で、概念を統合してよいか、の規則。NFM 4.4 節に、「実装の手間を減らすために一般化を好みがち」という観察はあるが、可否を定めた文は無い。

---

## 13. 不変条件について

- ジャクソンの著作は、不変条件を、概念の仕様の必須の節としては求めていない。構成要素の一覧(CHEAT p.1)にも、完成した仕様(AB3 スライド 23、WB スライド 19)にも、`invariant` の節は無い。
- 不変条件は、次の 3 つの形で出てくる。
  - 状態の宣言の多重度に織り込む。例: `remindOn: Pending -> one Date`。

    > "introducing sets lets you include certain invariants in the declaration of the state"
    >
    > 訳: 集合を導入すると、状態の宣言の中に、ある種の不変条件を含められる
    >
    > — T-state

  - 設計の検討で挙げて、アクションが保つことを確かめる。WB スライド 36〜42(例: "at most one user with a given username"(訳: 与えられた利用者名を持つ利用者は、多くても 1 人))。

    > "(1) check that the initial state is good / (2) and no action goes from a good to a bad state"
    >
    > 訳: (1) 初期状態が良いことを確かめる / (2) どのアクションも、良い状態から悪い状態に移らない
    >
    > — WB スライド 41

  - 概念をまたぐものは、同期が保つ。

    > "The synchronizations of actions between the two concepts preserve an invariant"
    >
    > 訳: 2 つの概念の間のアクションの同期が、不変条件を保つ
    >
    > — NFM 2.2 節

---

## 14. 資料どうしの食い違いと、この文書の採り方

| 論点 | 資料の違い | この文書の採り方 |
|---|---|---|
| 同期の書き方 | 古い(T-sync、NFM): `sync 名前 when A.x B.y`、`where` も `then` も無い。新しい(WYSIWID、WA、WC、AB3): `when` / `where` / `then` | 新しい書き方 |
| 同期はトランザクションか | NFM: "A synchronization is thus a kind of transaction, and its execution is all or nothing."(訳: こうして、同期は一種のトランザクションであり、その実行は全部か無かである。)。WYSIWID: "This scheme eliminates the need for transactional semantics"(訳: この方式は、トランザクションの意味づけの必要を無くす) | 触れない。新しい方式の説明だけを使う |
| 状態を読むだけのアクション | CHEAT law #10、WYSIWID: 入れない。AB2、AB3、T-sync: 持つ(`get_details` など) | 持たない(10 章) |
| 権限の確かめ方 | AB2: `Karma.permit` というアクションを `when` に並べる。WC、WA: `where` で状態に問い合わせる | `where`(10 章) |
| 戻り値の書き方 | T-machine: `out` 付きの引数。AB3、WB、NFM: `): 型`。WYSIWID: `=> [ 名前: 型 ]` | `): 型`(AB3 の書き方) |
| 事前・事後条件の書き方 | WA、WB、WC: `requires` / `ensures`。AB3: コメント。T-machine、NFM: 見出し無しで式を並べる。WYSIWID: 見出し無しでくだけた言葉 | `requires` / `ensures`(WB)と、コメント(AB3)の両方を示した |
| 型パラメータの記法 | `[User]`(AB3、WC、NFM、WYSIWID、T-sync)、`<User, Item>`(T-state) | `[User]` |
| 運用規則の見出し | `principle`(AB3、WA、WB、WC、CHEAT、T-machine、T-sync)。`operational principle`(WYSIWID、NFM、ABZ) | 日本語は「運用規則」。仕様の中の見出しは `principle` |
| 仕様の節の順序 | AB3、T-machine、T-sync: purpose → principle → state → actions。WYSIWID、NFM: purpose → state → actions → operational principle | AB3 の順(9 章) |
| 3 つの基準の 1 つめの呼び名 | T-modularity: Specificity。RUBRIC: Separation of concerns。WC スライド 9: non-conflation。ABZ(2018): singularity rule | 「特定性」。他の呼び名を、注記する |
| 構成要素の数 | T-criteria、WA: 3 つ。CHEAT、AB3、CCSD: 5 つ | 5 つを仕様、3 つを欠かせない部分として扱う(2 章) |
| アクションを誰が行うか | AB3、WB: "by user or system"(訳: 利用者またはシステムによる)。CHEAT: "performed by user or concept"(訳: 利用者または概念が行う)。WYSIWID: "actions that can be performed by the user"(訳: 利用者が行えるアクション) | 「利用者または概念」(6 章で引用) |
| 外から来る型の説明 | T-state「Polymorphism」: "Types of objects that are not specific to the concept (and are generated by it) should be represented by type parameters"(訳: 概念に特定的でない(かつ、その概念が生成する)オブジェクトの型は、型パラメータで表すべきである)。括弧の部分が、他の説明と合わない | この一文は使わない。T-state「No external types」と NFM を使う |

---

## 15. 組み合わせの整合性の点検

この文書は、新しい書き方の同期と、古い書き方の型の当てはめを併せて使う。矛盾が生まれないか、点検した。

| # | 点検する点 | 結果 |
|---|---|---|
| 1 | 古い書き方の「同期は実行を制約する(CSP 風)」「同期に出ないアクションは起きない」「トランザクション」を、この文書に持ち込んでいないか | 持ち込んでいない。当てはめには、古い資料の「型パラメータに型を渡す」という 1 点だけを使った(11 章)。新しい方式の説明は、WYSIWID と 2025 年のスライドだけを使った |
| 2 | 新しい書き方の「アクションを始められるのは bootstrap concept だけ」(WYSIWID 7.2 節)と、古い資料の `system`(システムが行うアクション)が、衝突しないか | **衝突しうる。** この文書では、(a) アクションは「利用者または概念が行う」と書き(6 章)、(b) 同期の章で、「始まりは外からの要求のアクション」とだけ書いた。`system` の印は使っていない。時間の経過で起きるアクションの扱いは、10 章で【未確認】とした |
| 3 | 「getter を持たない」(新しい)と、AB3 の例(`get_details`、`find`)が衝突しないか | 衝突する。この文書は、getter を使う例(AB3 スライド 26 の `view`、`find`)を使わず、`create` と `register` の例だけを使った(10 章の例 1) |
| 4 | 新しい資料の「外への参照はすべて UUID」と、古い資料の「型を静的に当てはめる」が、矛盾しないか | 層が違う。UUID は、実行時に外のものを表す方法。当てはめは、型の宣言。WYSIWID は、当てはめの宣言を禁じていない(書く場所が無いだけ)。ただし、両者を併せた例は、ジャクソンの資料に無い。11 章で、作成者の推論と明記した |
| 5 | 記法が混ざっていないか | 概念の仕様は AB3 の記法、同期は AB3・WA の記法(`when … where … then …`)で揃えた。WYSIWID の記法(`sync` ブロック、`=> [ ]`)は、引用の中以外では使っていない |
| 6 | 状態の記法の `set` が 2 通りの意味で使われていないか | 7 章で、「宣言の左の `set`」(集合の宣言)と、「`-> set`」(関係の右)を分けて書き、後者を【解釈】と明記した |
| 7 | 目的の数。「多くても 1 つ」と「少なくとも 1 つ」が、矛盾しないか | 矛盾しない。同じ節(T-purpose「Concept specificity」)に、両方がある。4 章で、両方を書いた |
| 8 | 型パラメータの判定が、資料の例と合うか | 合う。`EventTicket [User]`(User は外から来る、Event は `create` が作る)、`Label [Todo.Task]`(Task は Todo が作る)、NFM「the Task type is not treated as a type parameter」 |

---

## 16. 確認できなかったことの一覧

読んだ資料の範囲で、確認できなかったこと。推論で埋めていない。

1. 本 *The Essence of Software* の本文(入手していない)。
2. `effects` という見出し(あるのは `requires` / `ensures`)。
3. 型パラメータに制約を付ける書き方(「制約できない」とだけある)。
4. 新しい書き方の同期の中で、型パラメータの当てはめを宣言する構文。
5. `set`(矢印の右)、`opt`、`const` を定義する文。矢印の左側が、型を指すのか、状態の集合を指すのかの説明。
6. 初期状態を書く節。
7. 不変条件を書く節。
8. 目的の文の文法上の形。
9. `Request` という名前だけの擬似的な概念(あるのは `Web`、`WebRequest`)。
10. 新しい書き方で、時間の経過によるアクション(システムが行うアクション)をどう書くか。
11. アプリ全体を概念に分ける、番号付きの手順。
12. 権限を書くための専用の構文(例はすべて `where`)。
13. 工数や実装の都合で、概念を統合してよいか、の規則。
14. AB3 スライド 26 の `et.catalog = ec` の意味。
15. 新しい書き方の同期と、古い書き方の当てはめを併せて使う例。
