#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BeReady 全库自检脚本。

用法（在仓库任意位置执行都可以，脚本自动定位仓库根）：

    python3 _spec/scripts/check.py              # 结构校验 + 未解析链接（默认视图）
    python3 _spec/scripts/check.py --brief      # 只看两行结论
    python3 _spec/scripts/check.py --stale      # 追加：过期标注检查（（方向）/「尚未展开」段落）
    python3 _spec/scripts/check.py --shallow    # 追加：浅句候选（疑似「正确的废话」）
    python3 _spec/scripts/check.py --all        # 全部检查

检查项：
  结构：front matter 顶格、filename 与路径一致、title 全库唯一、title 与 H1 一致、
        level 与所在目录一致（index 用 capability、scenarios 用 topic/scenario）。
  链接：未解析的 [[...]]（index 里指向未建节点的是「预告清单」，不是死链，故只列出不报错）。
  过期标注：标「（方向）」「待建」「尚未展开」但目标其实已经建好的地方。
  浅句：短、无数字、无指向、只有告诫词的句子——core.md 阶段2 要删的「正确的废话」。

退出码：0 = 无结构错误；1 = 有结构错误。
"""

import argparse
import collections
import os
import re
import sys

# ---------------------------------------------------------------- 定位仓库根

def find_root():
    here = os.path.dirname(os.path.abspath(__file__))       # <root>/_spec/scripts
    root = os.path.dirname(os.path.dirname(here))
    if os.path.isdir(os.path.join(root, "capabilities")):
        return root
    # 兜底：从当前目录往上找
    cur = os.path.abspath(os.getcwd())
    while cur != "/":
        if os.path.isdir(os.path.join(cur, "capabilities")):
            return cur
        cur = os.path.dirname(cur)
    sys.exit("找不到仓库根（应包含 capabilities/ 目录）")


ROOT = find_root()
LINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]")
SECTIONS_WITH_EXTRAS = ("capabilities", "scenarios")
LEVEL_OF_DIR = {"L1", "L2", "L3", "L4"}


# ---------------------------------------------------------------- 收集文件

def collect():
    files = []
    for base in SECTIONS_WITH_EXTRAS:
        for dp, _dn, fn in os.walk(os.path.join(ROOT, base)):
            for f in fn:
                if f.endswith(".md"):
                    files.append(os.path.join(dp, f))
    for extra in ("index.md", "_nav.md"):
        p = os.path.join(ROOT, extra)
        if os.path.exists(p):
            files.append(p)
    return sorted(files)


def parse(path):
    text = open(path, encoding="utf-8").read()
    m = re.search(r"^---\n(.*?)\n---\n", text, re.S)
    front = m.group(1) if m else ""
    d = {"text": text}
    for key in ("filename", "title", "level", "category", "status"):
        mm = re.search(r"^%s:\s*(.+)$" % key, front, re.M)
        d[key] = mm.group(1).strip() if mm else None
    # front matter 各键必须顶格；缩进写法会让上面的 ^key: 匹配静默失效
    d["bad_indent"] = bool(
        re.search(r"^\s+filename:", front, re.M) or re.search(r"^\s+title:", front, re.M)
    )
    h1 = re.search(r"^#\s+(.+)$", text, re.M)
    d["h1"] = h1.group(1).strip() if h1 else None
    return d


# ---------------------------------------------------------------- 结构校验

def check_structure(info):
    errors, titles = [], {}
    for rel in sorted(info):
        d = info[rel]
        if d["bad_indent"]:
            errors.append("front matter 缩进（各键须顶格）: " + rel)

        if not rel.startswith(SECTIONS_WITH_EXTRAS):
            continue                                   # index.md / _nav.md 非知识节点
        if not d["title"]:
            errors.append("缺 title: " + rel)
        else:
            if d["title"] in titles:
                errors.append("title 重复: %s（%s 与 %s）" % (d["title"], titles[d["title"]], rel))
            titles[d["title"]] = rel
        if d["filename"] != rel:
            errors.append("filename 与路径不一致: %s -> %s" % (rel, d["filename"]))
        if d["h1"] != d["title"]:
            errors.append("H1 与 title 不一致: %s（%s / %s）" % (rel, d["h1"], d["title"]))

        parts = rel.split("/")
        lv = d["level"]
        if parts[0] == "scenarios":
            if lv not in ("topic", "scenario"):
                errors.append("scenarios 下 level 异常: %s -> %s" % (rel, lv))
        elif rel.endswith("/index.md"):
            if lv != "capability":
                errors.append("capability index 的 level 应为 capability: %s -> %s" % (rel, lv))
        else:
            dir_lv = os.path.basename(os.path.dirname(rel)).upper()
            if dir_lv in LEVEL_OF_DIR and lv != dir_lv:
                errors.append("level 与目录不一致: %s -> %s（目录 %s）" % (rel, lv, dir_lv))
    return errors, titles


# ---------------------------------------------------------------- 链接解析

def check_links(info, titles):
    names = {os.path.splitext(os.path.basename(p))[0] for p in info}
    unresolved = collections.defaultdict(list)
    total = 0
    for rel, d in info.items():
        if rel in ("index.md", "_nav.md"):
            continue
        for mm in LINK_RE.finditer(d["text"]):
            total += 1
            tgt = mm.group(1).strip()
            if tgt in titles or tgt in names:
                continue
            unresolved[tgt].append(rel)
    return unresolved, total


# ---------------------------------------------------------------- 过期标注

DIRECTION_RE = re.compile(r"[（(]方向[)）]|待建|未建|尚未创建")
SECTION_STALE_RE = re.compile(r"尚未展开|未展开|待建立|待建")
OVERSEEN_RE = re.compile(r"已解决|已定案|已建成|已补完|~~")


def check_stale(info):
    """找出「标着方向/未展开，其实已经建好」的段落。"""
    warns = []
    names = {os.path.splitext(os.path.basename(p))[0] for p in info}
    titles = {d["title"]: rel for rel, d in info.items() if d.get("title")}

    def built(name):
        return name in titles or name in names

    for rel in sorted(info):
        if not rel.endswith("/index.md"):
            continue
        lines = info[rel]["text"].split("\n")
        # 1) 单行标注「（方向）」「待建」，但链接目标已建
        for i, line in enumerate(lines, 1):
            if not DIRECTION_RE.search(line):
                continue
            if OVERSEEN_RE.search(line):         # 已标「已解决/已定案」的历史记录，跳过
                continue
            hit = [t.strip() for t in LINK_RE.findall(line) if built(t.strip())]
            if hit:
                warns.append("%s:%d 标为方向/待建但已建：%s" % (rel, i, "、".join(hit)))
        # 2) 整段标「尚未展开」，但段内链接全部已建（含子标题，作用域到同级/更高级标题为止）
        scope, head, start, links = 99, None, 0, []
        def flush():
            if head and links and all(built(x) for x in links):
                warns.append("%s:%d 「%s」段落标为未展开，但列出的 %d 个链接全部已建"
                             % (rel, start, head.strip("# ").strip(), len(links)))
        for i, line in enumerate(lines, 1):
            if line.startswith("#"):
                lvl = len(line) - len(line.lstrip("#"))
                if scope < 99:
                    if lvl <= scope:
                        flush()
                        scope, head, links = 99, None, []
                    # 子标题不结束作用域，继续累积
                if head is None and SECTION_STALE_RE.search(line):
                    scope, head, start, links = lvl, line, i, []
                continue
            if head is not None:
                links += [t.strip() for t in LINK_RE.findall(line)]
        flush()
    return warns


# ---------------------------------------------------------------- 浅句扫描

SHALLOW_WORDS = re.compile(r"(注意|保持|定期|避免|尽量|务必|小心|切记|预防)")


def check_shallow(info):
    """短、无数字、无链接、只有告诫词的句子——阶段2 要删的「正确的废话」候选。"""
    hits = []
    for rel in sorted(info):
        if rel.endswith("/index.md") or rel in ("index.md", "_nav.md"):
            continue
        for i, line in enumerate(info[rel]["text"].split("\n"), 1):
            s = line.strip()
            if not s.startswith(("*", "-")) and not re.match(r"^\d+\.", s):
                continue
            body = re.sub(r"^([*-]|\d+\.)\s*", "", s).strip()
            if len(body) > 30 or not SHALLOW_WORDS.search(body):
                continue
            if re.search(r"\d", body) or "[[" in body:
                continue
            hits.append("%s:%d  %s" % (rel, i, body))
    return hits


# ---------------------------------------------------------------- 硬信息密度

#: 带单位的量（1 厘米、20 分钟、5～6 次/分……）
HARD_QTY = re.compile(
    r"\d+\s*(?:cm|mm|km|m\b|℃|%|"
    r"厘米|毫米|米|公里|升|毫升|克|公斤|斤|小时|分钟|秒|天|周|月|年|度|倍|次|人|份|层|步)")
#: 编号步骤开头（"1." "1、" "**第 N 步"）
PROC_STEP = re.compile(r"^\s*(?:\d+\s*[.、)]|\*\*\s*第)")
#: 具体材料 / 手法词
SPECIFIC = re.compile(
    r"(石灰|木炭|硼砂|碘伏|酒精|绷带|纱布|夹板|盐|糖|醋|蜂蜜|松脂|黏土|泥土|树皮|"
    r"干草|尿液|明矾|缝|引流|压迫|覆盖|掩埋|烟熏|蒸|煮|烧|焊|鞣|熬|滤)")


def check_density(info, worst=40):
    """按「硬信息密度」给每个节点打分，密度越低越可能是「只有原则、没有做法」。

    .. warning:: 误伤率高——食物 / 火 / 庇护三章的低分节点读后大半扎实。
       本项只用来**缩小人工抽读名单**，不能把分数直接当结论（043 经验）。
    """
    rows = []
    for rel in sorted(info):
        if rel.endswith("/index.md") or rel in ("index.md", "_nav.md"):
            continue
        text = info[rel]["text"]
        lines = text.split("\n")
        qty = len(HARD_QTY.findall(text))
        step = sum(1 for l in lines if PROC_STEP.match(l))
        spec = len(SPECIFIC.findall(text))
        score = qty * 3 + step * 2 + spec
        rows.append((score / max(len(lines), 1), score, qty, step, len(lines), rel))
    rows.sort()
    return rows[:worst]


# ---------------------------------------------------------------- 主流程

def main():
    ap = argparse.ArgumentParser(description="BeReady 全库自检")
    ap.add_argument("--brief", action="store_true", help="只输出结论两行")
    ap.add_argument("--stale", action="store_true", help="检查过期标注")
    ap.add_argument("--shallow", action="store_true", help="列出浅句候选")
    ap.add_argument("--density", action="store_true",
                    help="按硬信息密度列出最「空」的节点（缩小抽读名单，分数有误伤）")
    ap.add_argument("--all", action="store_true", help="等于 --stale --shallow --density")
    args = ap.parse_args()
    do_stale = args.stale or args.all
    do_shallow = args.shallow or args.all
    do_density = args.density or args.all

    info = {os.path.relpath(p, ROOT): parse(p) for p in collect()}
    errors, titles = check_structure(info)
    unresolved, total_links = check_links(info, titles)

    print("仓库根 %s" % ROOT)
    print("== 文件 %d / title %d / 链接 %d 条 ==" % (len(info), len(titles), total_links))
    print("== 结构错误 %d ==" % len(errors))
    for e in errors:
        print("  !", e)
    if not args.brief:
        print("== 未解析链接 %d 条 / %d 目标（index 里的属预告清单，不是死链）=="
              % (sum(len(v) for v in unresolved.values()), len(unresolved)))
        for k in sorted(unresolved):
            print("  - %s -> %s" % (k, "、".join(sorted(set(unresolved[k])))))

    if do_stale:
        warns = check_stale(info)
        print("== 过期标注 %d ==" % len(warns))
        for w in warns:
            print("  ~", w)
    if do_shallow:
        hits = check_shallow(info)
        print("== 浅句候选 %d（人工复核，多数带具体动作，无需强改）==" % len(hits))
        for h in hits:
            print("  ?", h)
    if do_density:
        rows = check_density(info)
        print("== 硬信息密度最低的 %d 个节点（抽读名单；分数有误伤，须逐条读原文）==" % len(rows))
        print("   密度   分  量  步  行   文件")
        for dens, score, qty, step, nlines, rel in rows:
            print("  %.2f  %3d %3d %3d %4d  %s" % (dens, score, qty, step, nlines, rel))

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
