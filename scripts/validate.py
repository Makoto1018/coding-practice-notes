#!/usr/bin/env python3
"""檢查 problems.json 與 notes/ 底下的筆記是否一致。只使用 Python 標準函式庫。

用法（在 repo 根目錄）：python scripts/validate.py
全部通過印出 OK 並回傳 0；否則逐條列出錯誤並回傳 1。
"""
import json
import re
import sys
from pathlib import Path

DIFFICULTIES = {"Easy", "Medium", "Hard"}
REQUIRED_KEYS = ["id", "title", "slug", "difficulty", "chapter", "tags",
                 "order", "referenced", "file"]
SECTIONS = ["## 題目重點", "## 解題思路", "## 解法", "## 學到的觀念", "## 困難點與解法"]
TABLE_FIELDS = ["難度", "章節", "技巧", "原題連結", "是否參考別人"]


def parse_table(lines):
    """讀取第一個 Markdown 表格，回傳 {第一欄: 第二欄}。"""
    rows = {}
    started = False
    for line in lines:
        s = line.strip()
        if s.startswith("|"):
            started = True
            cells = [c.strip() for c in s.strip("|").split("|")]
            if len(cells) == 2 and not set(cells[0]) <= set("-: "):
                rows[cells[0]] = cells[1]
        elif started:
            break
    return rows


def check_sections(lines, where):
    errors = []
    heading_idx = [i for i, line in enumerate(lines) if line.startswith("## ")]
    headings = [lines[i].strip() for i in heading_idx]
    if headings != SECTIONS:
        missing = [s for s in SECTIONS if s not in headings]
        if missing:
            errors.append(f"{where}: 缺少區塊 {', '.join(missing)}")
        else:
            errors.append(f"{where}: 二級標題順序必須是 {' → '.join(SECTIONS)}，實際為 {headings}")
        return errors
    bounds = heading_idx + [len(lines)]
    for k, start in enumerate(heading_idx):
        body = "\n".join(lines[start + 1:bounds[k + 1]]).strip()
        if not body:
            errors.append(f"{where}: 區塊「{headings[k]}」空白，沒有內容請寫「無」")
        if headings[k] == "## 解法":
            if not re.search(r"^### 解法 \d+：.+", body, re.M):
                errors.append(f"{where}: 「## 解法」底下至少要有一個「### 解法 N：名稱」")
            if "```cpp" not in body:
                errors.append(f"{where}: 「## 解法」底下至少要有一個 ```cpp 程式碼區塊")
    return errors


def check_note(problem, text, chapter_names):
    where = problem["file"]
    errors = []
    lines = text.replace("\r\n", "\n").split("\n")
    expected_title = f"# {int(problem['id'])}. {problem['title']}"
    if not lines or lines[0].strip() != expected_title:
        errors.append(f"{where}: 標題必須是「{expected_title}」，實際為「{lines[0].strip() if lines else ''}」")

    table = parse_table(lines[1:])
    expected = {
        "難度": problem["difficulty"],
        "章節": chapter_names.get(problem["chapter"], "?"),
        "技巧": "、".join(problem["tags"]),
    }
    for field in TABLE_FIELDS:
        if field not in table:
            errors.append(f"{where}: 資訊表格缺少「{field}」")
    for field, value in expected.items():
        if field in table and table[field] != value:
            errors.append(f"{where}: 資訊表格「{field}」應為「{value}」，實際為「{table[field]}」")
    link = table.get("原題連結", "")
    if link and f"leetcode.com/problems/{problem['slug']}/" not in link:
        errors.append(f"{where}: 資訊表格「原題連結」必須包含 leetcode.com/problems/{problem['slug']}/")
    ref = table.get("是否參考別人")
    if ref is not None and ref.startswith("是") != bool(problem["referenced"]):
        errors.append(f"{where}: 資訊表格「是否參考別人」與 referenced={problem['referenced']} 不一致"
                      "（true 要以「是」開頭，false 寫「否」）")

    errors.extend(check_sections(lines, where))
    return errors


def validate(root):
    root = Path(root)
    try:
        data = json.loads((root / "problems.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"problems.json 無法讀取或不是合法 JSON：{exc}"]

    errors = []
    for key in ("chapters", "tags", "problems"):
        if not isinstance(data.get(key), list):
            errors.append(f"problems.json: 缺少陣列欄位「{key}」")
    if errors:
        return errors

    chapter_names = {c.get("id"): c.get("name") for c in data["chapters"]}
    allowed_tags = set(data["tags"])
    seen_ids, seen_orders, listed_files = set(), set(), set()
    previous_order = None

    for index, p in enumerate(data["problems"]):
        label = f"problems[{index}]（id={p.get('id')}）"
        missing = [k for k in REQUIRED_KEYS if k not in p]
        if missing:
            errors.append(f"{label}: 缺少欄位 {', '.join(missing)}")
            continue
        if not re.fullmatch(r"\d{4}", str(p["id"])):
            errors.append(f"{label}: id 必須是補零的四位數字串，例如 \"0704\"")
            continue
        if p["id"] in seen_ids:
            errors.append(f"{label}: id 重複")
        seen_ids.add(p["id"])
        if p["difficulty"] not in DIFFICULTIES:
            errors.append(f"{label}: difficulty 只能是 Easy/Medium/Hard，實際為 {p['difficulty']!r}")
        if p["chapter"] not in chapter_names:
            errors.append(f"{label}: chapter {p['chapter']!r} 不在 chapters 清單")
        if not isinstance(p["tags"], list) or not p["tags"]:
            errors.append(f"{label}: tags 必須是非空陣列")
        else:
            for tag in p["tags"]:
                if tag not in allowed_tags:
                    errors.append(f"{label}: 標籤「{tag}」不在 tags 清單，請先加進清單")
        if not isinstance(p["order"], int):
            errors.append(f"{label}: order 必須是整數")
        else:
            if p["order"] in seen_orders:
                errors.append(f"{label}: order {p['order']} 重複")
            if previous_order is not None and p["order"] < previous_order:
                errors.append(f"{label}: problems 必須依 order 由小到大排列")
            seen_orders.add(p["order"])
            previous_order = p["order"]
        if not isinstance(p["referenced"], bool):
            errors.append(f"{label}: referenced 必須是 true/false")
        expected_file = f"notes/{p['chapter']}/{p['id']}-{p['slug']}.md"
        if p["file"] != expected_file:
            errors.append(f"{label}: file 應為 {expected_file}，實際為 {p['file']}")
        listed_files.add(p["file"])
        note_path = root / p["file"]
        if not note_path.is_file():
            errors.append(f"{label}: 筆記檔 {p['file']} 不存在")
            continue
        if p["chapter"] in chapter_names:
            errors.extend(check_note(p, note_path.read_text(encoding="utf-8"), chapter_names))

    notes_dir = root / "notes"
    if notes_dir.is_dir():
        for md in sorted(notes_dir.rglob("*.md")):
            rel = md.relative_to(root).as_posix()
            if rel not in listed_files:
                errors.append(f"{rel}: 筆記檔沒有登記在 problems.json")
    return errors


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    root = Path(__file__).resolve().parent.parent
    errors = validate(root)
    if errors:
        print(f"發現 {len(errors)} 個問題：")
        for e in errors:
            print(f"- {e}")
        return 1
    print("OK：problems.json 與所有筆記一致")
    return 0


if __name__ == "__main__":
    sys.exit(main())
