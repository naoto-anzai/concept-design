#!/usr/bin/env python3
"""screens.yaml を検査する(docs/screen-grouping.md の評価基準 A・B・C・G)。

使い方: python3 tools/screen_check.py screens.yaml [--concepts concepts.yaml]
製品に依存しない。--concepts を渡すと、アクションの実在と被覆(A)も確かめる。
"""
import argparse
import sys

import yaml

READ_WORDS = ("get", "list", "query", "read", "current", "itemsWith", "readAll", "show", "view")


def load(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def act_id(x):
    return x["do"] if isinstance(x, dict) else x


def is_read(action_id):
    name = action_id.split(".")[-1]
    return any(name == w or name.startswith(w) for w in READ_WORDS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("screens")
    ap.add_argument("--concepts")
    args = ap.parse_args()
    doc = load(args.screens)
    errors, warns, infos = [], [], []

    screens = {s["id"]: s for s in doc.get("screens") or []}
    limits = doc.get("limits") or {}
    max_c = limits.get("max_concepts_per_screen")
    max_a = limits.get("max_actions_per_screen", 4)
    max_t = limits.get("max_transitions_per_journey", 3)
    shared = set(doc.get("shared") or [])
    excluded = {e["action"] if isinstance(e, dict) else e: e for e in doc.get("excluded_actions") or []}

    # 画面の形
    for sid, s in screens.items():
        if not s.get("title"):
            errors.append(f"画面 {sid}: title(利用者の言葉のタイトル)がない")
        own = [c for c in s.get("concepts") or [] if c not in shared]
        if max_c and len(own) > max_c:                                   # C
            errors.append(f"画面 {sid}: 概念が {len(own)} 個で、上限 {max_c} を超える")
        acts = [act_id(a) for a in s.get("actions") or [] if not is_read(act_id(a))]
        if len(acts) > max_a:                                            # C(読み取りは「見せるもの」なので数えない)
            warns.append(f"画面 {sid}: 状態を変える操作が {len(acts)} 個で、目安 {max_a} を超える")
        for a in s.get("actions") or []:                                 # G
            aid = act_id(a)
            if is_read(aid):
                continue
            undo = a.get("undo") if isinstance(a, dict) else None
            if not undo:
                warns.append(f"画面 {sid}: 状態を変える操作 {aid} に undo がない(戻す操作、または 'none: 理由')")
            elif str(undo).startswith("none") and ":" not in str(undo):
                warns.append(f"画面 {sid}: {aid} の undo が none だが、理由がない('none: 理由')")

    # A 被覆
    if args.concepts:
        cdoc = load(args.concepts)
        scope = set(doc.get("concepts") or [])
        all_actions = {}
        for c in cdoc.get("concepts", []):
            for a in c.get("actions", []):
                all_actions[f"{c['name']}.{a['name']}"] = a
        placed = {act_id(a) for s in screens.values() for a in s.get("actions") or []}
        placed |= {a["undo"] for s in screens.values() for a in s.get("actions") or []
                   if isinstance(a, dict) and a.get("undo") and not str(a["undo"]).startswith("none")}
        for aid in placed:
            if aid not in all_actions:
                errors.append(f"操作 {aid} が concepts.yaml にない")
        for aid, a in all_actions.items():
            cname = aid.split(".")[0]
            if cname in scope and not a.get("system") and aid not in placed and aid not in excluded:
                errors.append(f"被覆: {aid} が、どの画面にもない(画面に置くか excluded_actions に理由つきで書く)")
        for k, e in excluded.items():
            if not (isinstance(e, dict) and e.get("reason")):
                warns.append(f"excluded_actions の {k} に reason がない")

    # B ジャーニー
    used_screens = set()
    for j in doc.get("journeys") or []:
        steps = j.get("steps") or []
        if not steps:
            errors.append(f"ジャーニー {j.get('id')}: steps がない")
            continue
        trans, prev = 0, None
        for st in steps:
            sid = st.get("screen")
            if sid not in screens:
                errors.append(f"ジャーニー {j.get('id')}: 画面 {sid} が screens にない")
                continue
            used_screens.add(sid)
            if prev is not None and sid != prev:
                trans += 1
            prev = sid
            aid = st.get("do")
            if aid and aid not in {act_id(a) for a in screens[sid].get("actions") or []}:
                errors.append(f"ジャーニー {j.get('id')}: 画面 {sid} に操作 {aid} がない(その画面の actions に足す)")
        if trans > max_t:
            warns.append(f"ジャーニー {j.get('id')}: 画面遷移が {trans} 回で、上限 {max_t} を超える")
        infos.append(f"ジャーニー {j.get('id')}: 操作 {len(steps)} 回、画面遷移 {trans} 回")
    for sid in screens:
        if (doc.get("journeys")) and sid not in used_screens:
            warns.append(f"画面 {sid} は、どのジャーニーにも出ない(要らない画面かもしれない)")

    for i in infos:
        print("INFO ", i)
    for w in warns:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    prog = doc.get("progress") or {}
    if prog:
        print(f"INFO  進み具合: ステップ {prog.get('step')} / 6、完了 {prog.get('done', [])}")
    print(f"\nERROR {len(errors)} / WARN {len(warns)} / INFO {len(infos)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
