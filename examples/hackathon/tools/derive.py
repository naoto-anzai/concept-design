#!/usr/bin/env python3
"""概念設計から、次の段階の元になる雛形を導く。

  python3 tools/derive.py journey [--force]   機能ごとのジャーニーの雛形を journey/ に作る
  python3 tools/derive.py api                 API の元表を api/actions.generated.md に作る(毎回上書き)
  python3 tools/derive.py all [--force]

ジャーニーの雛形は、手で書き足すファイルなので、既にあれば上書きしない(--force で上書き)。
API の元表は導出結果なので、毎回作り直す。手で書く仕様は api/spec.md に置く。
導くのは「材料」までで、始点・終点・失敗時の扱いなど、決めるべきことは TODO として残す。
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REF = re.compile(r"\b([A-Z][A-Za-z]*)\.([a-z][A-Za-z]*)\b")
READ_PREFIX = ("list", "show", "search", "browse", "read", "get", "current")


def load(name):
    return yaml.safe_load((ROOT / name).read_text(encoding="utf-8"))


def as_list(v):
    return v if isinstance(v, list) else [v]


def data():
    return load("input.yaml"), load("concepts.yaml"), load("open-questions.yaml")["questions"], load("criteria.yaml")


def oq_blocking(qs, prefix_keys):
    out = []
    for q in qs:
        if q["status"] != "open":
            continue
        if any(b.startswith(k) for b in q.get("blocks", []) for k in prefix_keys):
            out.append(q)
    return out


def journey(force):
    inp, out, qs, crit = data()
    concepts = {c["name"]: c for c in out["concepts"]}
    syncs = {s["name"]: s for s in out["syncs"]}
    trace = {t["feature"]: t for t in out["trace"]}
    stake = {s["name"]: s["role"] for s in inp["problem"]["stakeholders"]}
    (ROOT / "journey").mkdir(exist_ok=True)

    for f in inp["features"]:
        fid = f["id"]
        path = ROOT / "journey" / f"{fid}.md"
        if path.exists() and not force:
            print(f"skip   {path.relative_to(ROOT.parent)} (既にある。--force で上書き)")
            continue
        t = trace.get(fid, {})
        c = (crit.get("features") or {}).get(fid, {})
        L = []
        L.append(f"# {fid} {f['name']}" + ("(optional)" if f.get("optional") else ""))
        L.append("")
        L.append("> derive.py が作った雛形。TODO を埋めて育てる。導出元は input / concepts / criteria。")
        L.append("")
        L.append("## 1. 目的")
        L.append("")
        L.append(f"- 価値: {f['value']}")
        L.append(f"- 目的(評価基準側): {c.get('purpose', 'TODO')}  [{c.get('status', '-')}]")
        L.append("- 登場する人: " + "、".join(f"{stake.get(s, s)}" for s in f["stakeholders"]))
        L.append("")
        L.append("## 2. 使う概念と原理(基本シナリオの骨格)")
        L.append("")
        for cn in t.get("concepts", []):
            L.append(f"- **{cn}**: {str(concepts[cn]['principle']).strip()}")
        L.append("")
        L.append("## 3. ジャーニー")
        L.append("")
        L.append("| 項目 | 内容 |")
        L.append("|---|---|")
        L.append("| 始点(何をきっかけに使い始めるか) | TODO |")
        L.append("| 前提(どこで、どの端末で、何を持っているか) | TODO |")
        L.append(f"| 想定の場面(入力の scenario) | {f['scenario']} |")
        L.append("| 終点(何が起きたら終わりか) | TODO |")
        L.append("")
        L.append("### 基本シナリオ(同期から導いた手順の候補)")
        L.append("")
        n = 0
        for sn in t.get("syncs", []):
            s = syncs[sn]
            when = str(s["when"])
            if not when.startswith("Request."):
                continue
            n += 1
            where = f"(条件: {s['where']})" if s.get("where") else ""
            L.append(f"{n}. 利用者が `{when}` を求める{where} → システムが `{', '.join(as_list(s['then']))}` を実行する。 TODO: 利用者に見えること")
        chained = [syncs[sn] for sn in t.get("syncs", []) if not str(syncs[sn]["when"]).startswith("Request.")]
        if chained:
            L.append("")
            L.append("連動(利用者の操作に続いてシステムが行うこと):")
            for s in chained:
                L.append(f"- `{s['when']}` のあと `{', '.join(as_list(s['then']))}`" + (f"(条件: {s['where']})" if s.get("where") else ""))
        L.append("")
        L.append("### 失敗・中断したとき(事前条件から導いた候補)")
        L.append("")
        used = set()
        for sn in t.get("syncs", []):
            # 利用者の操作(Request.*)が直接呼ぶアクションだけを対象にする。連動で動くものは利用者に見えない。
            if not str(syncs[sn]["when"]).startswith("Request."):
                continue
            for ref in as_list(syncs[sn]["then"]):
                for cn, an in REF.findall(str(ref)):
                    used.add((cn, an))
        for cn, an in sorted(used):
            if cn == "Request" or cn not in concepts:
                continue
            a = next((x for x in concepts[cn]["actions"] if x["name"] == an), None)
            if a and a.get("requires") not in ("なし", None, ""):
                L.append(f"- `{cn}.{an}` の事前条件「{a['requires']}」を満たさないとき、利用者に何を見せ、次に何ができるか。 TODO")
        L.append("- 通信が切れたとき・応答が遅いとき。 TODO")
        L.append("- 権限が無いとき。 TODO" + ("(OQ-1)" if fid == "F3" else ""))
        L.append("")
        L.append("## 4. 評価基準")
        L.append("")
        L.append("成功条件:")
        for x in c.get("success", ["TODO"]):
            L.append(f"- {x}")
        L.append("")
        L.append("失敗時の扱い:")
        for x in c.get("failure_handling", ["TODO"]):
            L.append(f"- {x}")
        L.append("")
        L.append(f"デモの場面: {c.get('demo_scene', 'TODO')}")
        L.append("")
        L.append(f"作らないこと: {', '.join(c.get('non_goals', [])) or 'TODO'}")
        L.append("")
        L.append("## 5. この機能の確定を止めている未決事項")
        L.append("")
        blocking = oq_blocking(qs, [f"journey.{fid}", "input", "concepts.syncs"])
        # 使う概念に関わる未決も加える
        for q in qs:
            if q["status"] == "open" and any(b.startswith(f"concepts.{cn}") for b in q.get("blocks", []) for cn in t.get("concepts", [])) and q not in blocking:
                blocking.append(q)
        if blocking:
            for q in blocking:
                L.append(f"- {q['id']}: {q['question']}")
        else:
            L.append("- なし")
        L.append("")
        path.write_text("\n".join(L), encoding="utf-8")
        print(f"wrote  {path.relative_to(ROOT.parent)}")


def guess_method(req_action):
    return "GET" if req_action.startswith(READ_PREFIX) else "POST"


def api():
    inp, out, qs, crit = data()
    concepts = {c["name"]: c for c in out["concepts"]}
    syncs = out["syncs"]
    feature_of = {}
    for t in out["trace"]:
        for sn in t.get("syncs", []):
            feature_of.setdefault(sn, []).append(t["feature"])
    L = []
    L.append("# API の元表(導出結果。毎回上書きされるので手で編集しない)")
    L.append("")
    L.append("導出元: concepts.yaml。手で書く仕様は `api/spec.md` に置く。")
    L.append("メソッドとパスは概念から機械的に付けた仮の値で、決める作業は TODO として残る。")
    L.append("")
    L.append("## 1. 外から呼ぶ操作(`Request.*` で始まる同期)")
    L.append("")
    L.append("| 要求 | 機能 | 実行する概念のアクション | メソッド(仮) | パス(仮) | 権限・条件(where) | 事前条件 → エラーの候補 |")
    L.append("|---|---|---|---|---|---|---|")
    for s in syncs:
        m = REF.findall(str(s["when"]))
        if not m or m[0][0] != "Request":
            continue
        req = m[0][1]
        thens = []
        for ref in as_list(s["then"]):
            thens += REF.findall(str(ref))
        target = thens[0][0] if thens else "?"
        path = "/" + re.sub(r"(?<!^)(?=[A-Z])", "-", target).lower()
        pre = []
        for cn, an in thens:
            a = next((x for x in concepts.get(cn, {}).get("actions", []) if x["name"] == an), None)
            if a and a.get("requires") not in ("なし", None, ""):
                pre.append(f"{cn}.{an}: {a['requires']}")
        L.append("| {} | {} | {} | {} | {} TODO | {} | {} |".format(
            req, ",".join(feature_of.get(s["name"], [])),
            ", ".join(f"{c}.{a}" for c, a in thens), guess_method(req), path,
            (s.get("where") or "-").replace("|", "/"), "; ".join(pre) or "-"))
    L.append("")
    L.append("## 2. 1 回の要求で複数の概念が動く連動(整合の扱いを決める)")
    L.append("")
    L.append("連動の途中で失敗したとき、全体を失敗にするか、一部だけ成功にするか。決めてから API の応答を書く。")
    L.append("")
    for s in syncs:
        if str(s["when"]).startswith("Request."):
            continue
        L.append(f"- `{s['when']}` のあと `{', '.join(as_list(s['then']))}`" + (f"(条件: {s['where']})" if s.get("where") else "") + "  TODO: 失敗時の扱い")
    L.append("")
    L.append("## 3. 外から呼ばない操作(`system: true`)")
    L.append("")
    for c in out["concepts"]:
        for a in c["actions"]:
            if a.get("system"):
                L.append(f"- `{c['name']}.{a['name']}`: {a['effects']}  (時刻や端末の出来事で動く。呼び出し口を作るかは TODO)")
    L.append("")
    L.append("## 4. 概念の状態 → リソースの候補")
    L.append("")
    for c in out["concepts"]:
        L.append(f"### {c['name']}")
        L.append("")
        L.append("```")
        L.append(str(c["state"]).strip())
        L.append("```")
        L.append("")
    L.append("## 5. 決まっていない前提")
    L.append("")
    for q in qs:
        if q["status"] == "open" and any(b.startswith("api") or b.startswith("concepts") for b in q.get("blocks", [])):
            L.append(f"- {q['id']}: {q['question']}")
    L.append("")
    (ROOT / "api").mkdir(exist_ok=True)
    p = ROOT / "api" / "actions.generated.md"
    p.write_text("\n".join(L), encoding="utf-8")
    print(f"wrote  {p.relative_to(ROOT.parent)}")


def main():
    args = sys.argv[1:]
    force = "--force" in args
    cmd = next((a for a in args if not a.startswith("--")), None)
    if cmd == "journey":
        journey(force)
    elif cmd == "api":
        api()
    elif cmd == "all":
        journey(force)
        api()
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
