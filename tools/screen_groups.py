#!/usr/bin/env python3
"""概念を画面にまとめる分け方を、全部数えて点数を付ける(docs/screen-grouping.md)。

使い方: python3 tools/screen_groups.py groups.yaml [--top N] [--concepts concepts.yaml]
入力(groups.yaml)の形は docs/screen-grouping.md の 3 章。製品に依存しない。
"""
import argparse
import itertools
import sys

import yaml

WEIGHT = {"must": 3, "prefer": 1, "neutral": 0}
KINDS = set(WEIGHT) | {"apart"}


def load(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def lint(doc, concept_names):
    errors, warns = [], []
    scope = list(doc.get("concepts") or [])
    shared = list(doc.get("shared") or [])
    if len(set(scope)) != len(scope):
        errors.append("concepts に重複がある")
    for s in shared:
        if s not in scope:
            errors.append(f"shared の {s} が concepts にない")
    if concept_names is not None:
        for c in scope:
            if c not in concept_names:
                errors.append(f"concepts の {c} が concepts.yaml にない")
    grouped = [c for c in scope if c not in shared]
    seen = {}
    for p in doc.get("pairs") or []:
        a, b, kind = p.get("a"), p.get("b"), p.get("kind")
        key = frozenset((a, b))
        if a not in grouped or b not in grouped or a == b:
            errors.append(f"組 {a}-{b}: concepts(shared を除く)にない名前、または同じ名前")
            continue
        if kind not in KINDS:
            errors.append(f"組 {a}-{b}: kind は {sorted(KINDS)} のどれか(今は {kind})")
        if kind in ("must", "prefer", "apart") and not (p.get("reason") or "").strip():
            errors.append(f"組 {a}-{b}: kind が {kind} なのに reason がない")
        if key in seen:
            errors.append(f"組 {a}-{b} が重複している")
        seen[key] = p
    for a, b in itertools.combinations(grouped, 2):
        if frozenset((a, b)) not in seen:
            warns.append(f"組 {a}-{b} が未記入(neutral として数える)")
    return grouped, seen, errors, warns


def partitions(items):
    """集合の分割を、すべて出す(制限付き成長列)。"""
    n = len(items)
    if n == 0:
        yield []
        return

    def rec(i, groups):
        if i == n:
            yield [list(g) for g in groups]
            return
        for g in groups:
            g.append(items[i])
            yield from rec(i + 1, groups)
            g.pop()
        groups.append([items[i]])
        yield from rec(i + 1, groups)
        groups.pop()

    yield from rec(0, [])


def evaluate(part, pairs, limit):
    """分け方を点数にする。不可なら理由を返す。"""
    where = {c: i for i, g in enumerate(part) for c in g}
    if limit and any(len(g) > limit for g in part):
        return None, "1 画面の概念数が上限を超える"
    score, lost = 0, []
    for key, p in pairs.items():
        a, b = tuple(key)
        same = where[a] == where[b]
        kind = p.get("kind", "neutral")
        if kind == "apart" and same:
            return None, f"分けたい {a}-{b} が同じ画面にある"
        if kind == "must" and not same:
            return None, f"必須の {a}-{b} が別の画面にある"
        if same:
            score += WEIGHT.get(kind, 0)
        elif kind == "prefer":
            lost.append(f"{a}-{b}")
    return (score, lost), None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("groups")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--concepts", help="概念の名前を確かめる concepts.yaml(任意)")
    args = ap.parse_args()

    doc = load(args.groups)
    names = None
    if args.concepts:
        names = {c["name"] for c in load(args.concepts).get("concepts", [])}
    grouped, pairs, errors, warns = lint(doc, names)
    for w in warns:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    if errors:
        print(f"\nERROR {len(errors)} / WARN {len(warns)}")
        return 1

    limit = (doc.get("limits") or {}).get("max_concepts_per_screen")
    ranked, rejected = [], 0
    for part in partitions(grouped):
        res, why = evaluate(part, pairs, limit)
        if res is None:
            rejected += 1
            continue
        score, lost = res
        ranked.append((-score, len(part), len(lost), part, lost))
    ranked.sort(key=lambda r: (r[0], r[1], r[2]))

    total = len(ranked) + rejected
    shared = doc.get("shared") or []
    print(f"\n分け方 {total} 通りのうち、条件を満たすもの {len(ranked)} 通り(不可 {rejected})")
    if shared:
        print(f"共有の概念(複数の画面に出てよい): {', '.join(shared)}")
    if not ranked:
        print("条件を満たす分け方がない。must と apart の矛盾、または上限が厳しすぎる。")
        return 1
    for i, (ns, ng, nl, part, lost) in enumerate(ranked[: args.top], 1):
        screens = "  |  ".join("{" + ", ".join(g) + "}" for g in part)
        print(f"\n案 {i}: 点数 {-ns} / 画面 {ng} / 一緒にできなかった『望ましい』{nl}")
        print(f"  {screens}")
        if lost:
            print(f"  一緒にできなかった組: {', '.join(lost)}")
    print(f"\nERROR 0 / WARN {len(warns)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
