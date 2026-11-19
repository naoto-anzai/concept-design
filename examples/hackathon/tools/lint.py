#!/usr/bin/env python3
"""概念設計の検査。定義 6.3 の制約 C1〜C4 と、入力の性質 I3・I4、未決事項の突き合わせを確かめる。

使い方: python3 tools/lint.py [--matrix]
終了コード: ERROR があれば 1。WARN と INFO だけなら 0。
C5(不変条件の保持)は人が推論するので、ここでは確かめない。
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

UI_WORDS = ["ボタン", "画面", "タップ", "クリック", "ページ", "タブ", "メニュー", "アイコン"]
TECH_WORDS = ["React", "Vue", "Next", "Nuxt", "Leaflet", "MapLibre", "Firebase", "Supabase",
              "Cloudflare", "API", "REST", "SQL", "JSON", "DB", "データベース", "スプレッドシート"]
REF = re.compile(r"\b([A-Z][A-Za-z]*)\.([a-z][A-Za-z]*)\b")
OQ = re.compile(r"OQ-\d+")


def load(name):
    return yaml.safe_load((ROOT / name).read_text(encoding="utf-8"))


def raw(name):
    return (ROOT / name).read_text(encoding="utf-8")


class Report:
    def __init__(self):
        self.items = []

    def add(self, level, code, msg):
        self.items.append((level, code, msg))

    def count(self, level):
        return sum(1 for lv, _, _ in self.items if lv == level)


def as_list(v):
    return v if isinstance(v, list) else [v]


def spec_text(c):
    """概念の仕様の検査対象テキスト。notes は含めない。"""
    parts = [c.get("purpose", ""), c.get("principle", ""), c.get("state", "")]
    for a in c.get("actions", []) or []:
        parts += [a.get("name", ""), str(a.get("requires", "")), str(a.get("effects", ""))]
    return "\n".join(str(p) for p in parts)


def main():
    show_matrix = "--matrix" in sys.argv
    inp, out = load("input.yaml"), load("concepts.yaml")
    oq = load("open-questions.yaml")["questions"]
    dec = load("decisions.yaml")["decisions"]
    crit = load("criteria.yaml")
    r = Report()

    concepts = {c["name"]: c for c in out.get("concepts", [])}
    syncs = {s["name"]: s for s in out.get("syncs", [])}
    features = {f["id"]: f for f in inp.get("features", [])}
    trace = {t["feature"]: t for t in out.get("trace", [])}

    # --- 入力の性質 ---
    for fid, f in features.items():
        for key in ("name", "value", "stakeholders", "scenario"):
            if not f.get(key):
                r.add("ERROR", "I1/I2", f"機能 {fid}: {key} が空")
        text = f"{f.get('value', '')} {f.get('scenario', '')}"
        for w in UI_WORDS:
            if w in text:
                r.add("WARN", "I3", f"機能 {fid}: UI の語「{w}」(画面の手順を書かない)")
        for w in TECH_WORDS:
            if w in text:
                r.add("WARN", "I4", f"機能 {fid}: 技術の語「{w}」(技術は passthrough に置く)")
    stake_names = {s["name"] for s in inp["problem"].get("stakeholders", [])}
    for fid, f in features.items():
        for s in f.get("stakeholders", []) or []:
            if s not in stake_names:
                r.add("ERROR", "I2", f"機能 {fid}: 利害関係者 {s} が problem.stakeholders に無い")

    # --- C1 形式 ---
    for name, c in concepts.items():
        for key in ("purpose", "principle", "state", "actions"):
            if not c.get(key):
                r.add("ERROR", "C1", f"概念 {name}: {key} が空")
        seen = set()
        for a in c.get("actions", []) or []:
            an = a.get("name")
            if not an:
                r.add("ERROR", "C1", f"概念 {name}: 名前の無いアクション")
                continue
            if an in seen:
                r.add("ERROR", "C1", f"概念 {name}: アクション {an} が重複")
            seen.add(an)
            for key in ("requires", "effects"):
                if a.get(key) in (None, ""):
                    r.add("ERROR", "C1", f"{name}.{an}: {key} が空(「なし」と明記する)")
    for sname, s in syncs.items():
        for key in ("when", "then"):
            if not s.get(key):
                r.add("ERROR", "C1", f"同期 {sname}: {key} が空")

    # --- C2 独立性 + UI・技術の語 ---
    for name, c in concepts.items():
        text = spec_text(c)
        for other in concepts:
            if other != name and re.search(rf"\b{re.escape(other)}\b", text):
                r.add("ERROR", "C2", f"概念 {name} の仕様に、他の概念 {other} が現れる(同期に出す)")
        if re.search(r"\bRequest\b", text):
            r.add("ERROR", "C2", f"概念 {name} の仕様に Request が現れる(呼び出し元は同期に書く)")
        for w in UI_WORDS:
            if w in text:
                r.add("WARN", "UI", f"概念 {name}: UI の語「{w}」")
        for w in TECH_WORDS:
            if re.search(rf"\b{re.escape(w)}\b", text) or (not w.isascii() and w in text):
                r.add("WARN", "TECH", f"概念 {name}: 技術の語「{w}」")

    # --- C4 参照の実在 ---
    def resolve(ref, where):
        for cname, aname in REF.findall(str(ref)):
            if cname == "Request":
                continue
            if cname not in concepts:
                r.add("ERROR", "C4", f"{where}: 概念 {cname} が無い")
            elif aname not in {a["name"] for a in concepts[cname].get("actions", [])}:
                r.add("ERROR", "C4", f"{where}: {cname}.{aname} というアクションが無い")

    for sname, s in syncs.items():
        for key in ("when", "then"):
            for ref in as_list(s.get(key, "")):
                resolve(ref, f"同期 {sname}.{key}")
        when_refs = REF.findall(str(s.get("when", "")))
        if not when_refs:
            r.add("ERROR", "C4", f"同期 {sname}: when に 概念.アクション の形が無い")
    for t in out.get("trace", []):
        if t["feature"] not in features:
            r.add("ERROR", "C4", f"trace: 機能 {t['feature']} が input.yaml に無い")
        for c in t.get("concepts", []) or []:
            if c not in concepts:
                r.add("ERROR", "C4", f"trace {t['feature']}: 概念 {c} が無い")
        for s in t.get("syncs", []) or []:
            if s not in syncs:
                r.add("ERROR", "C4", f"trace {t['feature']}: 同期 {s} が無い")

    # --- C3 被覆 ---
    for fid, f in features.items():
        t = trace.get(fid)
        if not t or not t.get("concepts"):
            lv = "INFO" if f.get("optional") else "ERROR"
            r.add(lv, "C3", f"機能 {fid}({f['name']}) が、どの概念でも実現されていない")
    used_by = {n: [] for n in concepts}
    for t in out.get("trace", []):
        for c in t.get("concepts", []) or []:
            if c in used_by:
                used_by[c].append(t["feature"])
    for n, fs in used_by.items():
        if not fs:
            r.add("WARN", "最小性", f"概念 {n} は、どの機能にも使われない(削除を検討)")
        elif all(features.get(f, {}).get("optional") for f in fs):
            r.add("INFO", "最小性", f"概念 {n} は optional の機能({', '.join(fs)})だけで使われる")
    traced_syncs = {s for t in out.get("trace", []) for s in (t.get("syncs") or [])}
    for sname in syncs:
        if sname not in traced_syncs:
            r.add("WARN", "C3", f"同期 {sname} が、どの機能の trace にも無い")
    # 同期が使う概念が、その機能の trace の concepts に入っているか
    for t in out.get("trace", []):
        tc = set(t.get("concepts") or [])
        for sn in t.get("syncs") or []:
            s = syncs.get(sn)
            if not s:
                continue
            for key in ("when", "then"):
                for ref in as_list(s.get(key, "")):
                    for cname, _ in REF.findall(str(ref)):
                        if cname != "Request" and cname in concepts and cname not in tc:
                            r.add("WARN", "C3", f"trace {t['feature']}: 同期 {sn} が使う {cname} が concepts に無い")

    # --- 未決事項の突き合わせ ---
    oq_ids = {q["id"]: q for q in oq}
    referenced = set()
    for fname in ("input.yaml", "concepts.yaml", "decisions.yaml", "criteria.yaml"):
        for m in OQ.findall(raw(fname)):
            referenced.add(m)
            if m not in oq_ids:
                r.add("ERROR", "OQ", f"{fname}: {m} が open-questions.yaml に無い")
    for qid, q in oq_ids.items():
        if q["status"] == "open":
            r.add("INFO", "OQ", f"未決 {qid}: {q['question']} (blocks: {', '.join(q.get('blocks', []))})")
    for qid, q in oq_ids.items():
        if q["status"] == "resolved" and not q.get("answer"):
            r.add("WARN", "OQ", f"{qid} は resolved なのに answer が空")

    for fname, label in (("input.yaml", "input"), ("concepts.yaml", "concepts")):
        n = raw(fname).count("★")
        if n:
            r.add("INFO", "★", f"{label}.yaml に ★要確認 が {n} 件")
    if inp.get("status") != "confirmed":
        r.add("INFO", "status", f"input.yaml の status は {inp.get('status')}(confirmed ではない)")

    # --- 評価基準 ---
    for fid, f in features.items():
        c = (crit.get("features") or {}).get(fid)
        if not c:
            r.add("WARN", "criteria", f"機能 {fid} の評価基準が criteria.yaml に無い")
            continue
        for key in ("purpose", "success", "failure_handling", "demo_scene"):
            if not c.get(key):
                r.add("WARN", "criteria", f"{fid}: {key} が空")
        if c.get("status") != "confirmed":
            r.add("INFO", "criteria", f"{fid} の評価基準は {c.get('status')}(チームの合意前)")
    if (crit.get("judging") or {}).get("status") == "unknown":
        r.add("INFO", "criteria", "審査基準が未入力(OQ-6)")

    # --- 決定の記録 ---
    for d in dec:
        for key in ("problem", "options", "adopted", "reason"):
            if not d.get(key):
                r.add("WARN", "decisions", f"{d.get('id')}: {key} が空")

    # --- 出力 ---
    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    for lv, code, msg in sorted(r.items, key=lambda x: order[x[0]]):
        print(f"{lv:5} [{code}] {msg}")
    print(f"\nERROR {r.count('ERROR')} / WARN {r.count('WARN')} / INFO {r.count('INFO')}")

    if show_matrix:
        print("\n機能 × 概念の対応表")
        names = list(concepts)
        head = "| 機能 | " + " | ".join(names) + " | 同期 |"
        print(head)
        print("|" + "---|" * (len(names) + 2))
        for fid, f in features.items():
            t = trace.get(fid, {})
            tc = set(t.get("concepts") or [])
            cells = ["○" if n in tc else "" for n in names]
            label = f"{fid} {f['name']}" + ("(optional)" if f.get("optional") else "")
            print(f"| {label} | " + " | ".join(cells) + f" | {', '.join(t.get('syncs') or [])} |")

    sys.exit(1 if r.count("ERROR") else 0)


if __name__ == "__main__":
    main()
