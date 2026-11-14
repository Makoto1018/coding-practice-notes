# 刷題手札（coding-practice-notes）Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 `array/` 的 LeetCode 筆記轉成可部署在 GitHub Pages 的靜態網站，並寫出讓 AI 只靠「網址 + 程式碼 + 選填思路」就能新增題目的 `AGENTS.md`。

**Architecture:** 純靜態網站：`problems.json` 是唯一索引，每題一個 Markdown 檔放在 `notes/<chapter>/`。`index.html` + `home.js` 讀 json 畫首頁與篩選；`problem.html` + `problem.js` 讀 json 找檔案、用 marked.js 渲染、highlight.js 上色。`scripts/validate.py`（只用標準函式庫）負責檢查 json 與筆記一致，是 AI 新增題目後的必跑檢查。

**Tech Stack:** HTML/CSS/原生 JS、marked 4.3.0 與 highlight.js 11.9.0（cdnjs）、Google Fonts、Python 3 標準函式庫（unittest）、GitHub Pages、`gh` CLI。

**Spec:** [docs/superpowers/specs/2026-11-14-coding-practice-notes-design.md](../specs/2026-11-14-coding-practice-notes-design.md)

**環境備註：** Windows、Git Bash。`python` = Python 3.14，`node` 可用（只拿來做 `node --check` 語法檢查），Edge 位於 `/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe`（用 headless 驗證 JS 渲染）。所有指令都在 repo 根目錄 `c:/working/m1_upper_semester/ai/hw9` 執行。

**設計細節決定（規格未寫明，於此定案）：**
- 資訊表格採兩欄直式（`| 項目 | 內容 |`），手機寬度不會爆版；技巧多個時用「、」連接。
- 標題題號不補零：`# 704. Binary Search`；`id` 與檔名補零：`0704`。
- `是否參考別人` 欄位：`referenced: false` ↔ `否`；`true` ↔ 以 `是` 開頭（可加括號說明）。原稿空白者視為 `否`。
- `## 題目重點` 本身就是改寫段落，不另加 AI 標記；其他 AI 補寫內容（複雜度、提醒等）一律放 `> 🤖 AI 補充：` 區塊。
- 使用者寫的數學式 `$O(n)$` 改成行內程式碼 `` `O(n)` ``（marked 不渲染 LaTeX，這屬於排版）。
- 首頁技巧篩選為單選（全部 + 有被使用的標籤），與難度篩選可同時生效。

---

## File Structure

| 檔案 | 責任 |
|---|---|
| `scripts/validate.py` | `validate(root) -> list[str]` 回傳所有錯誤；CLI 印出錯誤並以 0/1 結束 |
| `scripts/test_validate.py` | validate.py 的 unittest（在暫存目錄建假 repo） |
| `problems.json` | 章節、標籤清單、題目索引 |
| `notes/01-array/*.md` | 5 題轉換後的筆記 |
| `templates/problem-template.md` | 新題目範本 |
| `assets/style.css` | 全站樣式、CSS 變數、深色模式 |
| `index.html` / `assets/home.js` | 首頁：統計、篩選、章節卡片 |
| `problem.html` / `assets/problem.js` | 題目頁：渲染 md、AI 區塊樣式、上下題 |
| `AGENTS.md` | 給 AI 的完整規則與新增流程 |
| `CLAUDE.md` | 只有 `@AGENTS.md` |
| `.claude/commands/add-problem.md` | `/add-problem` 指令，指向 AGENTS.md |
| `README.md` | 給人看的專案說明 |
| `.nojekyll` | 關閉 Jekyll |
| `docs/new-session-test.md` | 新對話測試紀錄 |

---

### Task 1: 驗證腳本 `scripts/validate.py`（TDD）

**Files:**
- Create: `scripts/test_validate.py`
- Create: `scripts/validate.py`

- [ ] **Step 1: 寫失敗的測試**

Create `scripts/test_validate.py`:

````python
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate  # noqa: E402

VALID_NOTE = """# 704. Binary Search

| 項目 | 內容 |
|---|---|
| 難度 | Easy |
| 章節 | 陣列 |
| 技巧 | 二分搜尋 |
| 原題連結 | [LeetCode 704](https://leetcode.com/problems/binary-search/) |
| 是否參考別人 | 否 |

## 題目重點

在排序好的陣列裡找 target，找不到回傳 -1。

## 解題思路

- **思路概述**：二分搜尋
- **關鍵步驟**：左右指標往中間縮

## 解法

### 解法 1：二分搜尋

```cpp
int x = 0;
```

- 時間複雜度：`O(log n)`

## 學到的觀念

1. 二分搜尋

## 困難點與解法

無
"""


def base_data():
    return {
        "chapters": [
            {"id": "01-array", "name": "陣列"},
            {"id": "02-linked-list", "name": "鏈結串列"},
        ],
        "tags": ["二分搜尋", "雙指標"],
        "problems": [
            {
                "id": "0704",
                "title": "Binary Search",
                "slug": "binary-search",
                "difficulty": "Easy",
                "chapter": "01-array",
                "tags": ["二分搜尋"],
                "order": 1,
                "referenced": False,
                "file": "notes/01-array/0704-binary-search.md",
            }
        ],
    }


class ValidateTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.root)

    def build(self, data=None, note=VALID_NOTE, note_path="notes/01-array/0704-binary-search.md"):
        data = base_data() if data is None else data
        (self.root / "problems.json").write_text(
            json.dumps(data, ensure_ascii=False), encoding="utf-8"
        )
        if note is not None:
            path = self.root / note_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(note, encoding="utf-8")
        return validate.validate(self.root)

    def assertHasError(self, errors, fragment):
        self.assertTrue(
            any(fragment in e for e in errors),
            f"找不到包含「{fragment}」的錯誤，實際錯誤：{errors}",
        )

    def test_valid_repo_has_no_errors(self):
        self.assertEqual(self.build(), [])

    def test_invalid_json(self):
        (self.root / "problems.json").write_text("{not json", encoding="utf-8")
        self.assertHasError(validate.validate(self.root), "problems.json")

    def test_bad_difficulty(self):
        data = base_data()
        data["problems"][0]["difficulty"] = "easy"
        self.assertHasError(self.build(data), "difficulty")

    def test_unknown_tag(self):
        data = base_data()
        data["problems"][0]["tags"] = ["不存在的標籤"]
        self.assertHasError(self.build(data), "不存在的標籤")

    def test_unknown_chapter(self):
        data = base_data()
        data["problems"][0]["chapter"] = "99-nothing"
        data["problems"][0]["file"] = "notes/99-nothing/0704-binary-search.md"
        errors = self.build(data, note_path="notes/99-nothing/0704-binary-search.md")
        self.assertHasError(errors, "chapter")

    def test_duplicate_order(self):
        data = base_data()
        second = dict(data["problems"][0], id="0027", slug="remove-element",
                      title="Remove Element", file="notes/01-array/0027-remove-element.md")
        data["problems"].append(second)
        errors = self.build(data)
        self.assertHasError(errors, "order")

    def test_problems_must_be_sorted_by_order(self):
        data = base_data()
        data["problems"][0]["order"] = 2
        second = dict(data["problems"][0], id="0027", slug="remove-element", order=1,
                      title="Remove Element", file="notes/01-array/0027-remove-element.md")
        data["problems"].append(second)
        note27 = VALID_NOTE.replace("# 704. Binary Search", "# 27. Remove Element").replace(
            "binary-search", "remove-element").replace("LeetCode 704", "LeetCode 27")
        p = self.root / "notes/01-array/0027-remove-element.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(note27, encoding="utf-8")
        self.assertHasError(self.build(data), "排列")

    def test_missing_file(self):
        self.assertHasError(self.build(note=None), "不存在")

    def test_file_path_must_match_chapter_id_slug(self):
        data = base_data()
        data["problems"][0]["file"] = "notes/01-array/704.md"
        errors = self.build(data, note_path="notes/01-array/704.md")
        self.assertHasError(errors, "file")

    def test_title_mismatch(self):
        note = VALID_NOTE.replace("# 704. Binary Search", "# 0704. Binary Search")
        self.assertHasError(self.build(note=note), "標題")

    def test_table_difficulty_mismatch(self):
        note = VALID_NOTE.replace("| 難度 | Easy |", "| 難度 | Medium |")
        self.assertHasError(self.build(note=note), "難度")

    def test_table_tags_mismatch(self):
        note = VALID_NOTE.replace("| 技巧 | 二分搜尋 |", "| 技巧 | 雙指標 |")
        self.assertHasError(self.build(note=note), "技巧")

    def test_referenced_mismatch(self):
        note = VALID_NOTE.replace("| 是否參考別人 | 否 |", "| 是否參考別人 | 是（看了題解） |")
        self.assertHasError(self.build(note=note), "是否參考別人")

    def test_link_must_contain_slug(self):
        note = VALID_NOTE.replace("problems/binary-search/", "problems/other/")
        self.assertHasError(self.build(note=note), "原題連結")

    def test_missing_section(self):
        note = VALID_NOTE.replace("## 學到的觀念\n\n1. 二分搜尋\n\n", "")
        self.assertHasError(self.build(note=note), "## 學到的觀念")

    def test_empty_section(self):
        note = VALID_NOTE.replace("## 困難點與解法\n\n無\n", "## 困難點與解法\n\n")
        self.assertHasError(self.build(note=note), "空白")

    def test_solution_needs_subheading_and_cpp(self):
        note = VALID_NOTE.replace("### 解法 1：二分搜尋", "解法一")
        self.assertHasError(self.build(note=note), "### 解法")

    def test_orphan_note(self):
        self.build()
        extra = self.root / "notes/01-array/0027-remove-element.md"
        extra.write_text(VALID_NOTE, encoding="utf-8")
        self.assertHasError(validate.validate(self.root), "0027-remove-element.md")


if __name__ == "__main__":
    unittest.main()
````

- [ ] **Step 2: 執行測試，確認失敗**

Run: `python -m unittest discover -s scripts -p "test_*.py" -v`
Expected: 失敗，`ModuleNotFoundError: No module named 'validate'`

- [ ] **Step 3: 實作 `scripts/validate.py`**

```python
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
            errors.append(f"{label}: id 必須是補零的四位數字字串，例如 \"0704\"")
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
```

- [ ] **Step 4: 執行測試，確認全部通過**

Run: `python -m unittest discover -s scripts -p "test_*.py" -v`
Expected: `Ran 18 tests ... OK`

- [ ] **Step 5: Commit**

```bash
git add scripts/validate.py scripts/test_validate.py
git commit -m "feat: add validate.py for problems.json and notes consistency"
```

---

### Task 2: `problems.json`、範本與前 5 題筆記

**Files:**
- Create: `problems.json`
- Create: `templates/problem-template.md`
- Create: `notes/01-array/0704-binary-search.md`
- Create: `notes/01-array/0027-remove-element.md`
- Create: `notes/01-array/0977-squares-of-a-sorted-array.md`
- Create: `notes/01-array/0209-minimum-size-subarray-sum.md`
- Create: `notes/01-array/0059-spiral-matrix-ii.md`
- Delete: `array/1_704. Binary Search.md` … `array/5_59. Spiral Matrix II.md`（保留 `array/6_203...`）

**重要：** 程式碼區塊必須與 `array/` 原稿逐字相同（含縮排、行尾空白，例如 209 的 `need_add = true;   ` 後面有 3 個空白）。Step 8 用腳本比對。

- [ ] **Step 1: 建立 `problems.json`**

```json
{
  "chapters": [
    { "id": "01-array", "name": "陣列" },
    { "id": "02-linked-list", "name": "鏈結串列" },
    { "id": "03-hash-table", "name": "雜湊表" },
    { "id": "04-string", "name": "字串" },
    { "id": "05-stack-queue", "name": "堆疊與佇列" },
    { "id": "06-binary-tree", "name": "二元樹" },
    { "id": "07-backtracking", "name": "回溯" },
    { "id": "08-greedy", "name": "貪心" },
    { "id": "09-dynamic-programming", "name": "動態規劃" },
    { "id": "10-monotonic-stack", "name": "單調堆疊" },
    { "id": "11-graph", "name": "圖論" }
  ],
  "tags": ["二分搜尋", "雙指標", "滑動窗口", "模擬", "虛擬頭節點"],
  "problems": [
    {
      "id": "0704",
      "title": "Binary Search",
      "slug": "binary-search",
      "difficulty": "Easy",
      "chapter": "01-array",
      "tags": ["二分搜尋"],
      "order": 1,
      "referenced": false,
      "file": "notes/01-array/0704-binary-search.md"
    },
    {
      "id": "0027",
      "title": "Remove Element",
      "slug": "remove-element",
      "difficulty": "Easy",
      "chapter": "01-array",
      "tags": ["雙指標"],
      "order": 2,
      "referenced": false,
      "file": "notes/01-array/0027-remove-element.md"
    },
    {
      "id": "0977",
      "title": "Squares of a Sorted Array",
      "slug": "squares-of-a-sorted-array",
      "difficulty": "Easy",
      "chapter": "01-array",
      "tags": ["雙指標"],
      "order": 3,
      "referenced": false,
      "file": "notes/01-array/0977-squares-of-a-sorted-array.md"
    },
    {
      "id": "0209",
      "title": "Minimum Size Subarray Sum",
      "slug": "minimum-size-subarray-sum",
      "difficulty": "Medium",
      "chapter": "01-array",
      "tags": ["滑動窗口"],
      "order": 4,
      "referenced": true,
      "file": "notes/01-array/0209-minimum-size-subarray-sum.md"
    },
    {
      "id": "0059",
      "title": "Spiral Matrix II",
      "slug": "spiral-matrix-ii",
      "difficulty": "Medium",
      "chapter": "01-array",
      "tags": ["模擬"],
      "order": 5,
      "referenced": false,
      "file": "notes/01-array/0059-spiral-matrix-ii.md"
    }
  ]
}
```

- [ ] **Step 2: 建立 `templates/problem-template.md`**

````markdown
# <題號（不補零）>. <英文題名>

| 項目 | 內容 |
|---|---|
| 難度 | <Easy / Medium / Hard> |
| 章節 | <章節中文名稱，與 problems.json 的 chapters.name 相同> |
| 技巧 | <標籤1>、<標籤2> |
| 原題連結 | [LeetCode <題號>](https://leetcode.com/problems/<slug>/) |
| 是否參考別人 | <否 / 是（參考了什麼）> |

## 題目重點

<2～3 句中文，用自己的話說明要做什麼、輸入輸出與關鍵限制。不可貼原題全文。>

## 解題思路

- **思路概述**：<使用者的思路概述；沒有就寫「無」>
- **關鍵步驟**：<使用者的關鍵步驟；沒有就寫「無」>

## 解法

### 解法 1：<解法名稱>

```cpp
<使用者的程式碼，一字不改>
```

- 時間複雜度：`O(?)`

> 🤖 AI 補充：<使用者沒寫、由 AI 補的內容，例如空間複雜度>

## 學到的觀念

<使用者寫的觀念；沒有就寫「無」>

## 困難點與解法

<使用者寫的困難點；沒有就寫「無」>
````

- [ ] **Step 3: 建立 `notes/01-array/0704-binary-search.md`**

````markdown
# 704. Binary Search

| 項目 | 內容 |
|---|---|
| 難度 | Easy |
| 章節 | 陣列 |
| 技巧 | 二分搜尋 |
| 原題連結 | [LeetCode 704](https://leetcode.com/problems/binary-search/) |
| 是否參考別人 | 否 |

## 題目重點

給一個由小到大排序、元素不重複的整數陣列 `nums` 和目標值 `target`，找到就回傳它的索引，找不到回傳 -1。題目要求時間複雜度必須是 O(log n)。

## 解題思路

- **思路概述**：binary search
- **關鍵步驟**：有right跟left，然後while我是習慣用<=(閉鎖查找)

## 解法

### 解法 1：二分搜尋（左閉右閉）

```cpp
class Solution {
public:
    int search(vector<int>& nums, int target) {
        int left=0,right=nums.size()-1;
        while(left<=right){
            int mid = (right + left)/2;
            if(target<nums[mid])
                right = mid-1;
            else
                left = mid+1;
            if(target==nums[mid])
                return mid;
        }
        return -1;
    }
};
```

- 時間複雜度：`O(log(n))`

> 🤖 AI 補充：空間複雜度 `O(1)`。當 `left`、`right` 都很大時，`(right + left)/2` 可能溢位，常見寫法是 `left + (right - left) / 2`；另外把 `target==nums[mid]` 的判斷放在移動指標之前，可以讓邏輯更直觀。

## 學到的觀念

1. binary search

## 困難點與解法

無
````

- [ ] **Step 4: 建立 `notes/01-array/0027-remove-element.md`**

（注意解法 1 的 `                 k++;` 是 17 個空白，`nums[index] = nums[i];` 那行 16 個空白；解法 2 的兩行是 17 個空白——一律照原稿複製。）

````markdown
# 27. Remove Element

| 項目 | 內容 |
|---|---|
| 難度 | Easy |
| 章節 | 陣列 |
| 技巧 | 雙指標 |
| 原題連結 | [LeetCode 27](https://leetcode.com/problems/remove-element/) |
| 是否參考別人 | 否 |

## 題目重點

要直接在原陣列上移除所有等於 `val` 的元素，並回傳剩下的元素個數 `k`。只要前 `k` 格放的都是不等於 `val` 的元素就好，順序可以改變，`k` 之後放什麼都不重要。

## 解題思路

- **思路概述**：雙指標
- **關鍵步驟**：用一個for迴圈，多設定一個index當作第二個指標

## 解法

### 解法 1：雙指標（自己寫的）

```cpp
class Solution {
public:
    int removeElement(vector<int>& nums, int val) {
        if(nums.size()==0)
            return 0;
        int index = 0, k=0;
        for(int i=0;i<nums.size();i++){
            if(nums[i]==val){
                 k++;
            }
            else{
                nums[index] = nums[i];
                index++;
            }
        }
        return nums.size() - k;
    }
};
```

- 時間複雜度：`O(n)`

> 🤖 AI 補充：空間複雜度 `O(1)`，只多用了 `index` 和 `k` 兩個變數。

### 解法 2：gpt 優化過的解法

其實不需要K，也不需要先檢查是否為空，for迴圈就能處理了

```cpp
class Solution {
public:
    int removeElement(vector<int>& nums, int val) {
        int index = 0;
        for(int i=0;i<nums.size();i++){
            if(nums[i]!=val){
                 nums[index] = nums[i];
                 index++;
            }
        }
        return index;
    }
};
```

> 🤖 AI 補充：時間複雜度 `O(n)`、空間複雜度 `O(1)`。慢指標 `index` 停下來的位置剛好就是答案 `k`，所以不用另外計數。

## 學到的觀念

1. 雙指標

## 困難點與解法

無
````

- [ ] **Step 5: 建立 `notes/01-array/0977-squares-of-a-sorted-array.md`**

````markdown
# 977. Squares of a Sorted Array

| 項目 | 內容 |
|---|---|
| 難度 | Easy |
| 章節 | 陣列 |
| 技巧 | 雙指標 |
| 原題連結 | [LeetCode 977](https://leetcode.com/problems/squares-of-a-sorted-array/) |
| 是否參考別人 | 否 |

## 題目重點

給一個已經由小到大排序、可能含有負數的整數陣列，回傳每個數字平方後的新陣列，結果也要由小到大排序。

## 解題思路

- **思路概述**：雙指標
- **關鍵步驟**：因為是遞增(並且平方之後負的會變正的，所以比較小的會在比較中間的位子)，所以使用指向頭尾的雙指標，把平方後比較大的從最後一個慢慢放進去

## 解法

### 解法 1：暴力解

```cpp
class Solution {
public:
    vector<int> sortedSquares(vector<int>& nums) {
        for(int i=0;i<nums.size();i++){
            if(nums[i]<0)
                nums[i] *= (-1);
        }
        sort(nums.begin(),nums.end());
        for(int i=0;i<nums.size();i++){
            nums[i] = nums[i] * nums[i];
        }
        return nums;
    }
};
```

> 🤖 AI 補充：時間複雜度 `O(n log n)`，主要花在 `sort`；先取絕對值再排序，平方後順序不變，所以結果正確。

### 解法 2：優化過的解法: 雙指標

```cpp
class Solution {
public:
    vector<int> sortedSquares(vector<int>& nums) {
        vector<int> res(nums.size());
        int left=0, right=nums.size()-1, ptr=nums.size()-1;
        while(ptr>=0){
            int left_square = nums[left] * nums[left];
            int right_square = nums[right] * nums[right];
            if(left_square > right_square){
                res[ptr] = left_square;
                left++;
                ptr--;
            }
            else{
                res[ptr] = right_square;
                right--;
                ptr--;
            }
        }
        return res;
    }
};
```

- 時間複雜度：`O(n)`

> 🤖 AI 補充：空間複雜度 `O(n)`，來自回傳用的 `res` 陣列。

## 學到的觀念

1. 雙指標

## 困難點與解法

無
````

- [ ] **Step 6: 建立 `notes/01-array/0209-minimum-size-subarray-sum.md`**

（`need_add = true;` 後面有 3 個行尾空白，必須保留。）

````markdown
# 209. Minimum Size Subarray Sum

| 項目 | 內容 |
|---|---|
| 難度 | Medium |
| 章節 | 陣列 |
| 技巧 | 滑動窗口 |
| 原題連結 | [LeetCode 209](https://leetcode.com/problems/minimum-size-subarray-sum/) |
| 是否參考別人 | 是（滑動窗口） |

## 題目重點

給一個全是正整數的陣列和正整數 `target`，找出總和大於等於 `target` 的最短連續子陣列，回傳它的長度；如果不存在就回傳 0。

## 解題思路

- **思路概述**：滑動窗口
- **關鍵步驟**：擴張窗口，透過 fast 向右移動來累加總和。 縮小窗口：當總和大於等於 target 時，移動 slow 來找最短長度

## 解法

### 解法 1：滑動窗口

```cpp
class Solution {
public:
    int minSubArrayLen(int target, vector<int>& nums) {
        int fast=0, slow=0;
        int res=100001;
        int total=0;
        bool need_add=true;
        while(fast<nums.size()&&slow<nums.size()){
            if(need_add)
                total += nums[fast];
            if(total>=target){
                if(fast-slow+1<res){
                    res = fast-slow+1;
                }
                total -= nums[slow];
                need_add = false;
                slow++;
            }
            else{
                fast++;
                need_add = true;   
            }
        }
        if(res==100001)
            return 0;
        else
            return res;
    }
};
```

- 時間複雜度：`O(n)`

> 🤖 AI 補充：空間複雜度 `O(1)`。`res` 的初始值 100001 依賴題目限制 `nums.length <= 10^5`，也可以改用 `INT_MAX` 當作「還沒找到」的記號，比較不怕限制改變。

## 學到的觀念

1. 滑動窗口

## 困難點與解法

1. 掌握快慢指標的移動邏輯與邊界條件處理
````

- [ ] **Step 7: 建立 `notes/01-array/0059-spiral-matrix-ii.md`**

````markdown
# 59. Spiral Matrix II

| 項目 | 內容 |
|---|---|
| 難度 | Medium |
| 章節 | 陣列 |
| 技巧 | 模擬 |
| 原題連結 | [LeetCode 59](https://leetcode.com/problems/spiral-matrix-ii/) |
| 是否參考別人 | 否 |

## 題目重點

給一個正整數 `n`，產生 `n × n` 的矩陣，並依照順時針螺旋的順序把 1 到 n² 依序填進去。

## 解題思路

- **思路概述**：模擬
- **關鍵步驟**：
  - 初始時 left = 0, right = n - 1, up = 0, down = n - 1
  - 按照 左到右 → 上到下 → 右到左 → 下到上 的順序填充數字
  - 每次填充完一條邊後，縮小對應邊界 (left++, right--, up++, down--)
  - 若 n 為奇數，最後中心點需要手動填入

## 解法

### 解法 1：模擬（四個邊界指標）

```cpp
class Solution {
public:
    vector<vector<int>> generateMatrix(int n) {
        vector<vector<int>> res(n,vector<int>(n,0));
        if(n==1){
            res[0][0]=1;
            return res;
        }
        int left=0, right=n-1;
        int up=0, down=n-1;
        int ptr=0, ptr2=0;
        int ctr=1;
        for(int i=1;i<=n*n;){
            while(ptr2<right){    //左到右
                res[ptr][ptr2]=i;
                ptr2++;
                i++;
            }
            right--;
            while(ptr<down){    //上到下
                res[ptr][ptr2]=i;
                ptr++;
                i++;
            }
            down--;
            while(ptr2>left){    //右到左
                res[ptr][ptr2]=i;
                ptr2--;
                i++;
            }
            left++;
            while(ptr>up){    //下到上
                res[ptr][ptr2]=i;
                ptr--;
                i++;
            }
            up++;
            ptr=ctr;
            ptr2=ctr;
            ctr++;
            if(left==right){
                res[left][left] = i;
                i++;
            }
        }
        return res;
    }
};
```

- 時間複雜度：`O(n^2)`

> 🤖 AI 補充：除了回傳的矩陣外，額外空間是 `O(1)`。

## 學到的觀念

1. 如何用 四個邊界指標 控制螺旋填充

## 困難點與解法

1. 如何確保邊界不會超出範圍？→ 使用 left, right, up, down 來收縮範圍
2. 如何處理 n 為奇數時的情況？→ 透過 if(left == right) 處理中心點
````

- [ ] **Step 8: 比對程式碼與原稿逐字相同**

Run:
```bash
python - <<'EOF'
import re, pathlib
pairs = {
    "array/1_704. Binary Search.md": "notes/01-array/0704-binary-search.md",
    "array/2_27. Remove Element.md": "notes/01-array/0027-remove-element.md",
    "array/3_977. Squares of a Sorted Array.md": "notes/01-array/0977-squares-of-a-sorted-array.md",
    "array/4_209. Minimum Size Subarray Sum.md": "notes/01-array/0209-minimum-size-subarray-sum.md",
    "array/5_59. Spiral Matrix II.md": "notes/01-array/0059-spiral-matrix-ii.md",
}
pat = re.compile(r"```cpp\n(.*?)\n```", re.S)
read = lambda p: pathlib.Path(p).read_text(encoding="utf-8").replace("\r\n", "\n")
ok = True
for src, dst in pairs.items():
    a, b = pat.findall(read(src)), pat.findall(read(dst))
    if a != b:
        ok = False
        print("MISMATCH", dst, len(a), len(b))
print("ALL CODE IDENTICAL" if ok else "FAIL")
EOF
```
Expected: `ALL CODE IDENTICAL`。若 MISMATCH，用原稿的程式碼區塊覆蓋新檔對應區塊後重跑。

- [ ] **Step 9: 執行驗證腳本**

Run: `python scripts/validate.py`
Expected: `OK：problems.json 與所有筆記一致`

- [ ] **Step 10: 刪除已轉換的原稿並 commit**

```bash
git rm "array/1_704. Binary Search.md" "array/2_27. Remove Element.md" "array/3_977. Squares of a Sorted Array.md" "array/4_209. Minimum Size Subarray Sum.md" "array/5_59. Spiral Matrix II.md"
git add problems.json templates/problem-template.md notes/
git commit -m "feat: convert first 5 array notes to new format with problems.json"
```

---

### Task 3: 樣式與首頁

**Files:**
- Create: `assets/style.css`
- Create: `index.html`
- Create: `assets/home.js`

- [ ] **Step 1: 建立 `assets/style.css`**

```css
:root {
  --primary: #4f46e5;
  --primary-soft: #eef2ff;
  --bg: #f8fafc;
  --card: #ffffff;
  --text: #1e293b;
  --muted: #64748b;
  --border: #e2e8f0;
  --easy: #16a34a;
  --medium: #ea580c;
  --hard: #dc2626;
  --code-bg: #f1f5f9;
  --ai-bg: #fefce8;
  --ai-border: #ca8a04;
  --error: #dc2626;
  --radius: 12px;
  --font-body: "Noto Sans TC", system-ui, -apple-system, "Segoe UI", sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, Consolas, monospace;
  color-scheme: light;
}

@media (prefers-color-scheme: dark) {
  :root {
    --primary: #818cf8;
    --primary-soft: #1e1b4b;
    --bg: #0f172a;
    --card: #1e293b;
    --text: #e2e8f0;
    --muted: #94a3b8;
    --border: #334155;
    --easy: #4ade80;
    --medium: #fb923c;
    --hard: #f87171;
    --code-bg: #0b1220;
    --ai-bg: #2a2410;
    --ai-border: #facc15;
    --error: #f87171;
    color-scheme: dark;
  }
}

* { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: var(--font-body);
  line-height: 1.7;
  overflow-wrap: anywhere;
}

a { color: var(--primary); }

.container { max-width: 800px; margin: 0 auto; padding: 24px 16px 48px; }

.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  margin-bottom: 16px;
}

/* ---------- 首頁 ---------- */
.site h1 { margin: 0; font-size: 2rem; color: var(--primary); }
.subtitle { margin: 4px 0 12px; color: var(--muted); }

.stats { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px; }
.stat {
  padding: 2px 12px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: var(--card);
  font-size: 0.9rem;
}

.filters { margin-bottom: 20px; }
.filter-row { display: flex; align-items: flex-start; gap: 8px; margin-bottom: 8px; }
.filter-label { flex: none; padding-top: 4px; color: var(--muted); font-size: 0.9rem; }
.chips { display: flex; flex-wrap: wrap; gap: 6px; }
.chip {
  font: inherit;
  font-size: 0.85rem;
  padding: 2px 12px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: var(--card);
  color: var(--text);
  cursor: pointer;
}
.chip:hover { border-color: var(--primary); }
.chip.active { background: var(--primary); border-color: var(--primary); color: #ffffff; }

.chapter h2 { margin: 0 0 8px; font-size: 1.2rem; }
.problem-list { list-style: none; margin: 0; padding: 0; }
.problem-item {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 4px 12px;
  padding: 8px 0;
  border-top: 1px solid var(--border);
}
.problem-item:first-child { border-top: none; }
.problem-link { text-decoration: none; color: var(--text); font-weight: 500; }
.problem-link:hover .problem-title { color: var(--primary); text-decoration: underline; }
.problem-no { font-family: var(--font-mono); color: var(--muted); margin-right: 6px; }
.problem-meta { display: flex; flex-wrap: wrap; gap: 6px; }

.badge, .tag {
  display: inline-block;
  font-size: 0.75rem;
  line-height: 1.6;
  padding: 0 8px;
  border-radius: 999px;
  border: 1px solid currentColor;
}
.badge.easy { color: var(--easy); }
.badge.medium { color: var(--medium); }
.badge.hard { color: var(--hard); }
.tag { color: var(--primary); background: var(--primary-soft); border-color: transparent; }

.empty, .loading { color: var(--muted); }
.error { color: var(--error); font-weight: 500; }

/* ---------- 題目頁 ---------- */
.top-nav { margin-bottom: 12px; }
.top-nav a { text-decoration: none; font-weight: 500; }

.article h1 { margin-top: 0; font-size: 1.6rem; }
.article h2 {
  font-size: 1.25rem;
  margin-top: 32px;
  padding-bottom: 4px;
  border-bottom: 2px solid var(--primary-soft);
}
.article h3 { font-size: 1.05rem; margin-top: 24px; }
.article code { font-family: var(--font-mono); font-size: 0.9em; }
.article :not(pre) > code {
  background: var(--code-bg);
  padding: 1px 6px;
  border-radius: 6px;
}
.article pre {
  background: var(--code-bg);
  padding: 14px 16px;
  border-radius: 8px;
  overflow-x: auto;
  line-height: 1.5;
}
.article pre code.hljs { background: transparent; padding: 0; }
.article table { display: block; max-width: 100%; overflow-x: auto; border-collapse: collapse; }
.article th, .article td { border: 1px solid var(--border); padding: 6px 12px; text-align: left; }
.article th { background: var(--code-bg); }
.article blockquote {
  margin: 16px 0;
  padding: 8px 16px;
  border-left: 4px solid var(--border);
  color: var(--muted);
}
.article blockquote p { margin: 4px 0; }
.article blockquote.ai-note {
  background: var(--ai-bg);
  border-left-color: var(--ai-border);
  border-radius: 0 8px 8px 0;
  color: var(--text);
}
.article img { max-width: 100%; }

.pager { display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
.pager-link {
  flex: 1 1 200px;
  padding: 12px 16px;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  text-decoration: none;
}
.pager-link:hover { border-color: var(--primary); }
.pager-link.next { text-align: right; }
```

- [ ] **Step 2: 建立 `index.html`**

```html
<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>刷題手札</title>
  <meta name="description" content="LeetCode 刷題筆記，依資料結構分類，C++ 解法。">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Noto+Sans+TC:wght@400;500;700&display=swap">
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <main class="container">
    <header class="site">
      <h1>刷題手札</h1>
      <p class="subtitle">LeetCode 刷題筆記・依資料結構分類・C++</p>
      <div id="stats" class="stats"></div>
    </header>
    <section class="filters" aria-label="篩選">
      <div class="filter-row">
        <span class="filter-label">難度</span>
        <div id="difficulty-filter" class="chips"></div>
      </div>
      <div class="filter-row">
        <span class="filter-label">技巧</span>
        <div id="tag-filter" class="chips"></div>
      </div>
    </section>
    <div id="chapters"><p class="loading">載入中…</p></div>
  </main>
  <script src="assets/home.js"></script>
</body>
</html>
```

- [ ] **Step 3: 建立 `assets/home.js`**

```js
(function () {
  "use strict";

  const DIFFICULTIES = ["Easy", "Medium", "Hard"];
  const state = { difficulty: "All", tag: "All" };
  let data = null;

  function el(tag, attrs, children) {
    const node = document.createElement(tag);
    Object.entries(attrs || {}).forEach(([key, value]) => {
      if (key === "class") node.className = value;
      else if (key === "text") node.textContent = value;
      else node.setAttribute(key, value);
    });
    (children || []).forEach((child) => node.appendChild(child));
    return node;
  }

  function renderStats() {
    const box = document.getElementById("stats");
    box.replaceChildren(el("span", { class: "stat", text: `共 ${data.problems.length} 題` }));
    DIFFICULTIES.forEach((d) => {
      const n = data.problems.filter((p) => p.difficulty === d).length;
      box.appendChild(el("span", { class: `stat badge ${d.toLowerCase()}`, text: `${d} ${n}` }));
    });
  }

  function renderChips(containerId, values, key) {
    const box = document.getElementById(containerId);
    box.replaceChildren();
    ["All", ...values].forEach((value) => {
      const active = state[key] === value;
      const button = el("button", {
        type: "button",
        class: active ? "chip active" : "chip",
        "aria-pressed": String(active),
        text: value === "All" ? "全部" : value,
      });
      button.addEventListener("click", () => {
        state[key] = value;
        render();
      });
      box.appendChild(button);
    });
  }

  function matches(p) {
    return (state.difficulty === "All" || p.difficulty === state.difficulty) &&
      (state.tag === "All" || p.tags.includes(state.tag));
  }

  function problemItem(p) {
    const link = el("a", { class: "problem-link", href: `problem.html?id=${encodeURIComponent(p.id)}` }, [
      el("span", { class: "problem-no", text: `${Number(p.id)}.` }),
      el("span", { class: "problem-title", text: p.title }),
    ]);
    const meta = el("span", { class: "problem-meta" }, [
      el("span", { class: `badge ${p.difficulty.toLowerCase()}`, text: p.difficulty }),
      ...p.tags.map((t) => el("span", { class: "tag", text: t })),
    ]);
    return el("li", { class: "problem-item" }, [link, meta]);
  }

  function renderChapters() {
    const box = document.getElementById("chapters");
    box.replaceChildren();
    data.chapters.forEach((chapter) => {
      const list = data.problems
        .filter((p) => p.chapter === chapter.id && matches(p))
        .sort((a, b) => a.order - b.order);
      if (list.length === 0) return;
      box.appendChild(el("section", { class: "card chapter" }, [
        el("h2", { text: `${chapter.name}（${list.length}）` }),
        el("ul", { class: "problem-list" }, list.map(problemItem)),
      ]));
    });
    if (!box.hasChildNodes()) {
      box.appendChild(el("p", { class: "empty", text: "沒有符合條件的題目。" }));
    }
  }

  function render() {
    renderStats();
    renderChips("difficulty-filter", DIFFICULTIES, "difficulty");
    const usedTags = data.tags.filter((t) => data.problems.some((p) => p.tags.includes(t)));
    renderChips("tag-filter", usedTags, "tag");
    renderChapters();
  }

  fetch("problems.json")
    .then((res) => {
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    })
    .then((json) => {
      data = json;
      render();
    })
    .catch((err) => {
      document.getElementById("chapters").replaceChildren(
        el("p", { class: "error", text: `題目清單讀取失敗：${err.message}` })
      );
    });
})();
```

- [ ] **Step 4: 語法檢查與 headless 驗證**

Run:
```bash
node --check assets/home.js && echo SYNTAX_OK
```
Expected: `SYNTAX_OK`

在背景啟動本機伺服器（`python -m http.server 8000`，Bash 的 run_in_background），然後（`<scratchpad>` 換成本 session 的 scratchpad 絕對路徑）：
```bash
EDGE="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
OUT="<scratchpad>/dom"; mkdir -p "$OUT"
"$EDGE" --headless=new --disable-gpu --virtual-time-budget=8000 --dump-dom "http://localhost:8000/index.html" > "$OUT/index.html" 2>/dev/null
grep -o "共 5 題\|Binary Search\|Spiral Matrix II\|陣列（5）" "$OUT/index.html" | sort -u
```
Expected: 四個字串都出現：`Binary Search`、`Spiral Matrix II`、`共 5 題`、`陣列（5）`。

- [ ] **Step 5: Commit**

```bash
git add assets/style.css assets/home.js index.html
git commit -m "feat: add home page with stats, filters and chapter cards"
```

---

### Task 4: 題目頁

**Files:**
- Create: `problem.html`
- Create: `assets/problem.js`

- [ ] **Step 1: 建立 `problem.html`**

```html
<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>刷題手札</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Noto+Sans+TC:wght@400;500;700&display=swap">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css" media="(prefers-color-scheme: light)">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css" media="(prefers-color-scheme: dark)">
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <main class="container">
    <nav class="top-nav"><a href="index.html">← 回首頁</a></nav>
    <article id="content" class="card article"><p class="loading">載入中…</p></article>
    <nav id="pager" class="pager" aria-label="上一題與下一題"></nav>
  </main>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/marked/4.3.0/marked.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/cpp.min.js"></script>
  <script src="assets/problem.js"></script>
</body>
</html>
```

- [ ] **Step 2: 建立 `assets/problem.js`**

```js
(function () {
  "use strict";

  const AI_PREFIX = "🤖 AI 補充";
  const content = document.getElementById("content");
  const pager = document.getElementById("pager");

  function showError(message) {
    const p = document.createElement("p");
    p.className = "error";
    p.textContent = message;
    const back = document.createElement("a");
    back.href = "index.html";
    back.textContent = "← 回首頁";
    content.replaceChildren(p, back);
    pager.replaceChildren();
    document.title = "找不到題目 | 刷題手札";
  }

  function markAiNotes(root) {
    root.querySelectorAll("blockquote").forEach((bq) => {
      if (bq.textContent.trim().startsWith(AI_PREFIX)) bq.classList.add("ai-note");
    });
  }

  function pagerLink(problem, text, cls) {
    const a = document.createElement("a");
    a.className = `pager-link ${cls}`;
    a.href = `problem.html?id=${encodeURIComponent(problem.id)}`;
    a.textContent = text;
    return a;
  }

  function renderPager(problems, current) {
    const sorted = problems.slice().sort((a, b) => a.order - b.order);
    const i = sorted.findIndex((p) => p.id === current.id);
    const prev = sorted[i - 1];
    const next = sorted[i + 1];
    pager.replaceChildren();
    if (prev) pager.appendChild(pagerLink(prev, `← 上一題：${Number(prev.id)}. ${prev.title}`, "prev"));
    if (next) pager.appendChild(pagerLink(next, `下一題：${Number(next.id)}. ${next.title} →`, "next"));
  }

  async function main() {
    const raw = new URLSearchParams(window.location.search).get("id");
    if (!raw) {
      showError("網址缺少題號，例如 problem.html?id=0704。");
      return;
    }
    const id = /^\d+$/.test(raw) ? raw.padStart(4, "0") : raw;
    try {
      const res = await fetch("problems.json");
      if (!res.ok) throw new Error(`problems.json 回應 ${res.status}`);
      const data = await res.json();
      const problem = data.problems.find((p) => p.id === id);
      if (!problem) {
        showError(`找不到題號 ${raw} 的筆記。`);
        return;
      }
      const mdRes = await fetch(problem.file);
      if (!mdRes.ok) throw new Error(`${problem.file} 回應 ${mdRes.status}`);
      const markdown = await mdRes.text();
      content.innerHTML = marked.parse(markdown);
      content.querySelectorAll("pre code").forEach((block) => hljs.highlightElement(block));
      markAiNotes(content);
      content.querySelectorAll('a[href^="http"]').forEach((a) => {
        a.target = "_blank";
        a.rel = "noopener";
      });
      document.title = `${Number(problem.id)}. ${problem.title} | 刷題手札`;
      renderPager(data.problems, problem);
    } catch (err) {
      showError(`讀取失敗：${err.message}`);
    }
  }

  main();
})();
```

- [ ] **Step 3: 語法檢查與 headless 驗證**

Run: `node --check assets/problem.js && echo SYNTAX_OK`
Expected: `SYNTAX_OK`

伺服器仍在 8000 埠執行時（若已停止就重新在背景啟動），對每一題與兩個錯誤情境 dump DOM：
```bash
EDGE="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
OUT="<scratchpad>/dom"; mkdir -p "$OUT"
for id in 0704 0027 0977 0209 0059 9999 ""; do
  "$EDGE" --headless=new --disable-gpu --virtual-time-budget=8000 --dump-dom "http://localhost:8000/problem.html?id=$id" > "$OUT/p_$id.html" 2>/dev/null
  echo "== $id: title=$(grep -o '<title>[^<]*</title>' "$OUT/p_$id.html") ai=$(grep -c 'ai-note' "$OUT/p_$id.html") hljs=$(grep -c 'hljs-keyword' "$OUT/p_$id.html") err=$(grep -c 'class="error"' "$OUT/p_$id.html") next=$(grep -o '下一題：[^<]*' "$OUT/p_$id.html")"
done
```
Expected:
- 0704：title `704. Binary Search | 刷題手札`、ai ≥ 1、hljs ≥ 1、err 0、next `下一題：27. Remove Element →`
- 0059：沒有「下一題」（最後一題）
- 9999：err 1、title `找不到題目 | 刷題手札`
- 空 id：err 1

- [ ] **Step 4: 手機寬度截圖檢查**

```bash
"$EDGE" --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=8000 --window-size=375,1400 --screenshot="$OUT/mobile_0059.png" "http://localhost:8000/problem.html?id=0059"
"$EDGE" --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=8000 --window-size=375,1000 --screenshot="$OUT/mobile_index.png" "http://localhost:8000/index.html"
```
用 Read 工具打開兩張截圖：內容不超出右邊界、AI 補充區塊有黃色底、程式碼有上色、表格完整顯示。

- [ ] **Step 5: Commit**

```bash
git add problem.html assets/problem.js
git commit -m "feat: add problem page with markdown rendering and prev/next links"
```

---

### Task 5: AGENTS.md、CLAUDE.md、指令、README、.nojekyll

**Files:**
- Create: `AGENTS.md`
- Create: `CLAUDE.md`
- Create: `.claude/commands/add-problem.md`
- Create: `README.md`
- Create: `.nojekyll`（空檔）

- [ ] **Step 1: 建立 `AGENTS.md`**

````markdown
# AGENTS.md — 刷題手札

這個 repo 是 LeetCode 刷題筆記網站（GitHub Pages 純靜態）。你最常被要求做的事是：**使用者給「題目網址 + 程式碼 +（選填）思路」，你把它變成一篇筆記並登記到網站。** 請完全依照本文件，不要自創格式。

## 專案結構

```
problems.json                 唯一的題目索引（章節、標籤清單、題目）
notes/<chapter>/<NNNN>-<slug>.md   每題一篇筆記
templates/problem-template.md 新筆記範本
scripts/validate.py           一致性檢查（新增或修改後必跑）
index.html / problem.html     網站頁面（assets/ 內為 css 與 js）
```

網站沒有建置步驟：瀏覽器直接讀 `problems.json` 和 `.md`。**不要**加入框架、套件管理器、建置工具或 Jekyll 設定。

## 新增題目流程

### 輸入

- 必填：LeetCode 題目網址、程式碼（可以有多個解法）
- 選填：思路、學到的觀念、困難點、是否參考別人（沒說就當作「否」）

缺少必填項目時先向使用者詢問，不要自己生出程式碼。

### 步驟

1. **判斷題目資料**：從網址取 `slug`（`https://leetcode.com/problems/<slug>/...`）。確認題號、英文題名、難度。不確定時用網路工具查 LeetCode 或問使用者，**不要猜**。
2. **檢查是否已存在**：在 `problems.json` 搜尋這個題號。已存在 → 改為更新該篇筆記（例如在 `## 解法` 加一個新的 `### 解法 N`），不要新增第二筆，`order` 不變。
3. **決定章節**：依主要資料結構，從下表選一個（只能用這些 id）：

   | id | 名稱 | 放哪些題 |
   |---|---|---|
   | `01-array` | 陣列 | 陣列操作、二分搜尋、雙指標、滑動窗口、矩陣模擬 |
   | `02-linked-list` | 鏈結串列 | 操作 ListNode 的題目 |
   | `03-hash-table` | 雜湊表 | 主要靠 set / map 計數或查找 |
   | `04-string` | 字串 | 字串處理、KMP |
   | `05-stack-queue` | 堆疊與佇列 | stack、queue、heap、優先佇列 |
   | `06-binary-tree` | 二元樹 | 樹的走訪與構造、BST |
   | `07-backtracking` | 回溯 | 組合、排列、切割、子集 |
   | `08-greedy` | 貪心 | 貪心策略題 |
   | `09-dynamic-programming` | 動態規劃 | DP |
   | `10-monotonic-stack` | 單調堆疊 | 下一個更大元素類 |
   | `11-graph` | 圖論 | DFS/BFS、並查集、最短路徑 |

4. **決定技巧標籤**：1～3 個，只能用 `problems.json` 的 `tags` 清單。清單裡沒有合適的 → 先把新標籤加到 `tags` 陣列最後，再使用。
5. **建立筆記**：複製 `templates/problem-template.md` 到 `notes/<chapter>/<NNNN>-<slug>.md`（`NNNN` 是補零四位數題號，例如 `0203`），依下方「筆記格式」填寫。
6. **登記到 `problems.json`**：在 `problems` 陣列**最後**加一筆，`order` = 現有最大 `order` + 1：
   ```json
   {
     "id": "0203",
     "title": "Remove Linked List Elements",
     "slug": "remove-linked-list-elements",
     "difficulty": "Easy",
     "chapter": "02-linked-list",
     "tags": ["虛擬頭節點"],
     "order": 6,
     "referenced": true,
     "file": "notes/02-linked-list/0203-remove-linked-list-elements.md"
   }
   ```
   - `id`：補零四位數字串；`difficulty`：`Easy` / `Medium` / `Hard`；`referenced`：有參考別人為 `true`。
7. **驗證**：執行 `python scripts/validate.py`，必須印出 `OK`。有錯就修正後重跑。
8. **回報**：依下方「完成檢查清單」逐項回報 ✅/❌，並列出你新增或修改的檔案。

## 筆記格式

檔名：`notes/<chapter>/<NNNN>-<slug>.md`。區塊順序固定如下（二級標題文字必須一字不差）：

````markdown
# 203. Remove Linked List Elements

| 項目 | 內容 |
|---|---|
| 難度 | Easy |
| 章節 | 鏈結串列 |
| 技巧 | 虛擬頭節點 |
| 原題連結 | [LeetCode 203](https://leetcode.com/problems/remove-linked-list-elements/) |
| 是否參考別人 | 是（說明參考了什麼） |

## 題目重點

（2～3 句）

## 解題思路

- **思路概述**：…
- **關鍵步驟**：…

## 解法

### 解法 1：<名稱>

```cpp
（程式碼）
```

- 時間複雜度：`O(n)`

## 學到的觀念

…

## 困難點與解法

…
````

細節規則：

- **標題**：`# <題號不補零>. <英文題名>`，題名與 `problems.json` 的 `title` 完全相同。
- **資訊表格**：兩欄直式表格，五列依序為 難度、章節、技巧、原題連結、是否參考別人。
  - 章節寫中文名稱（例如「鏈結串列」），技巧多個時用「、」連接，順序與 json 相同。
  - 是否參考別人：`referenced: false` 寫 `否`；`true` 寫 `是` 開頭，可加括號說明（例如 `是（滑動窗口）`）。
- **題目重點**：中文 2～3 句，用自己的話寫要做什麼、輸入輸出、關鍵限制。**絕對不可貼上或逐句翻譯原題全文**（著作權）。這個區塊本身就是改寫，不需要加 AI 標記。
- **解題思路**：固定 `思路概述`、`關鍵步驟` 兩項；步驟有多行時用縮排的子清單。
- **解法**：每個解法一個 `### 解法 N：<名稱>`（N 從 1 開始，冒號是全形「：」），底下依序是 ` ```cpp ` 程式碼區塊、複雜度。使用者有給解法說明文字時放在程式碼區塊上方。名稱沿用使用者的說法（例如「暴力解」「自己寫的」「gpt 優化過的解法」）。
- **複雜度**：使用者寫的放在 `- 時間複雜度：` 清單；使用者沒寫的由你補，放進 AI 補充區塊。
- 使用者寫的 LaTeX（例如 `$O(n)$`）改成行內程式碼 `` `O(n)` ``。

### 內容保留規則（最重要）

1. **程式碼一字不改**：包含註解、空白、縮排、行尾空白、看起來像 bug 的地方。想提出改進就寫在 AI 補充區塊。
2. **使用者寫的文字保留原意**：思路、觀念、困難點只能調整排版（清單、換行、粗體），不可改寫、潤飾、翻譯或刪減。錯字也保留。
3. **AI 補寫的內容一律放在 AI 補充區塊**，格式是以 `> 🤖 AI 補充：` 開頭的引用區塊（網站會用黃色底顯示）：
   ```markdown
   > 🤖 AI 補充：空間複雜度 `O(1)`。
   ```
   一般的 `>` 引用不要用在其他用途。AI 補充要短（1～3 句），可放在任一區塊內。
4. **沒有內容的區塊寫「無」**，不可留空。（例如使用者沒寫困難點 → `## 困難點與解法` 底下寫 `無`。）

## 完成檢查清單

回報時逐項標示 ✅ 或 ❌：

1. 檔案路徑是 `notes/<chapter>/<NNNN>-<slug>.md`，且 `problems.json` 的 `file` 一致
2. 標題、資訊表格與 `problems.json` 一致（題名、難度、章節、技巧、參考別人）
3. 章節與標籤都在清單內（新標籤已先加入 `tags`）
4. `order` = 原本最大值 + 1（更新既有題目時 `order` 不變）
5. 題目重點是自己的話、2～3 句，沒有原題全文
6. 程式碼與使用者提供的逐字相同
7. 使用者的思路、觀念、困難點都保留原意
8. 所有 AI 補寫的內容都在 `> 🤖 AI 補充：` 區塊
9. 沒有空白區塊（沒內容寫「無」）
10. `python scripts/validate.py` 印出 `OK`

## 其他工作

- **本機預覽**：`python -m http.server 8000`，開 `http://localhost:8000/`。直接雙擊 html 檔會因為 fetch 被瀏覽器擋而無法載入。
- **驗證腳本測試**：`python -m unittest discover -s scripts -p "test_*.py"`。
- **部署**：push 到 `main` 後 GitHub Pages 自動更新（https://makoto1018.github.io/coding-practice-notes/）。所有路徑用相對路徑、檔名用小寫。
- **不要**：修改使用者程式碼、刪除舊筆記、改動既有題目的 `order`、加入建置工具、在未經使用者同意下 push。
````

- [ ] **Step 2: 建立 `CLAUDE.md`**

```markdown
@AGENTS.md
```

- [ ] **Step 3: 建立 `.claude/commands/add-problem.md`**

```markdown
---
description: 新增或更新一題 LeetCode 筆記（依 AGENTS.md 流程）
argument-hint: <LeetCode 網址> [程式碼與思路]
---

請完全依照 @AGENTS.md 的「新增題目流程」處理以下輸入，格式與規則都以 AGENTS.md 為準：

$ARGUMENTS

如果還缺程式碼，先請使用者提供程式碼（可多個解法），並詢問選填的思路與是否參考別人。
```

- [ ] **Step 4: 建立 `README.md`**

````markdown
# 刷題手札

我的 LeetCode 刷題筆記（C++），依資料結構分章節，網站部署在 GitHub Pages：

👉 https://makoto1018.github.io/coding-practice-notes/

## 特色

- 每題一篇 Markdown 筆記：題目重點、解題思路、多種解法與複雜度、學到的觀念、困難點
- 首頁可依難度與技巧標籤篩選
- AI 補充的內容會以黃色區塊標示，和我自己寫的內容分開
- 純靜態網站，沒有建置步驟

## 新增題目

這個 repo 附有 [AGENTS.md](AGENTS.md)，給 AI 助手（Claude Code、Codex 等）看的規則。只要提供題目網址和程式碼：

```
/add-problem https://leetcode.com/problems/two-sum/
（貼上程式碼與思路）
```

AI 會建立筆記、更新 `problems.json`，並執行 `python scripts/validate.py` 檢查。

## 本機預覽

```bash
python -m http.server 8000
# 開啟 http://localhost:8000/
```

## 結構

| 路徑 | 說明 |
|---|---|
| `problems.json` | 題目索引 |
| `notes/` | 筆記，依章節分資料夾 |
| `templates/problem-template.md` | 筆記範本 |
| `scripts/validate.py` | 一致性檢查 |
| `AGENTS.md` | AI 新增題目的規則 |
````

- [ ] **Step 5: 建立 `.nojekyll` 並驗證**

```bash
touch .nojekyll
python scripts/validate.py
```
Expected: `OK：problems.json 與所有筆記一致`

- [ ] **Step 6: Commit**

```bash
git add AGENTS.md CLAUDE.md .claude/commands/add-problem.md README.md .nojekyll
git commit -m "docs: add AGENTS.md rules, CLAUDE.md, add-problem command and README"
```

---

### Task 6: 新對話測試（第 6 題 203）

**Files:**
- Create（由子代理）: `notes/02-linked-list/0203-remove-linked-list-elements.md`
- Modify（由子代理）: `problems.json`
- Create: `docs/new-session-test.md`
- Delete: `array/6_203. Remove Linked List Elements.md`（測試完成後）

- [ ] **Step 1: 派出沒有上下文的子代理**

用 Agent 工具（`subagent_type: general-purpose`），prompt 只包含以下內容（不要提供任何本對話的設計細節、也不要指向 `array/`）：

````text
你在 repo c:\working\m1_upper_semester\ai\hw9 工作。請先閱讀根目錄的 AGENTS.md，然後完全依照其中的「新增題目流程」新增下面這一題。只使用我給你的輸入，不要讀取 array/ 資料夾，不要 git commit。完成後依 AGENTS.md 的完成檢查清單逐項回報，並列出修改的檔案。

題目網址：https://leetcode.com/problems/remove-linked-list-elements/description/

是否參考別人：有，忘記linked list是甚麼

思路：
- 思路概述：熟悉 **linked list** 跟 **pointer** 的運作方式。dummy node 的觀念
- 關鍵步驟：head 的部分可以先用 while 慢慢縮短整個 list。可以用dummy node (虛設的在 head 之前的新頭) 的概念來處理 head 也要刪掉的問題
- 時間複雜度：$O(n)$

學到的新觀念：
1. linked list 跟 pointer
2. dummy node

遇到的困難點與解法：
1. 無

程式碼 1（自己寫的）：
```cpp
<把 array/6_203. Remove Linked List Elements.md 第一個 cpp 區塊原文貼在這裡>
```

程式碼 2（dummy node）：
```cpp
<把第二個 cpp 區塊原文貼在這裡>
```
````

主代理在送出前，用 Read 讀原稿並把兩段程式碼**原文**貼進 prompt（取代角括號內文字）。

- [ ] **Step 2: 檢查子代理成果**

```bash
python scripts/validate.py
python - <<'EOF'
import re, pathlib
pat = re.compile(r"```cpp\n(.*?)\n```", re.S)
read = lambda p: pathlib.Path(p).read_text(encoding="utf-8").replace("\r\n", "\n")
a = pat.findall(read("array/6_203. Remove Linked List Elements.md"))
b = pat.findall(read("notes/02-linked-list/0203-remove-linked-list-elements.md"))
print("CODE IDENTICAL" if a == b else f"MISMATCH {len(a)} vs {len(b)}")
EOF
git diff problems.json
```
Expected: `OK…`、`CODE IDENTICAL`、`problems.json` 只多一筆 `0203`、`order: 6`、`chapter: 02-linked-list`、`referenced: true`。

再用 Read 讀新筆記，由主代理依 AGENTS.md 檢查清單第 5、7、8、9 項人工核對（題目重點是否自己的話、使用者文字是否保留、AI 內容是否都有標記、沒有空白區塊）。用 headless Edge dump `problem.html?id=0203` 與 `index.html`，確認標題 `203. Remove Linked List Elements | 刷題手札`、首頁出現「鏈結串列（1）」、59 的頁面出現「下一題：203. …」。

- [ ] **Step 3: 若有問題，修正規則而非只修結果**

如果子代理的結果有任何不符合規格的地方，先判斷是 AGENTS.md 寫得不清楚還是子代理沒遵守。若是規則不清楚：修改 AGENTS.md、`git checkout -- problems.json` 並刪除新筆記，再重派一個新的子代理（同一個 prompt）重測，直到一次通過。每一輪都記錄下來。

- [ ] **Step 4: 寫 `docs/new-session-test.md`**

內容包含：測試目的、給子代理的完整 prompt（程式碼可以用「（略，與原稿相同）」代替）、子代理的回報摘要、主代理的驗證結果（validate 輸出、程式碼比對、檢查清單 10 項 ✅/❌）、發現的問題與對 AGENTS.md 的修改（若無則寫「無」）、結論。依實際結果撰寫，不可預先填寫。

- [ ] **Step 5: 刪除 203 原稿並 commit**

```bash
git rm "array/6_203. Remove Linked List Elements.md"
git add notes/02-linked-list problems.json docs/new-session-test.md AGENTS.md
git commit -m "feat: add 203 via fresh-agent test following AGENTS.md"
```

---

### Task 7: 全站最終檢查

- [ ] **Step 1: 全部測試**

```bash
python -m unittest discover -s scripts -p "test_*.py"
python scripts/validate.py
node --check assets/home.js && node --check assets/problem.js && echo SYNTAX_OK
git status --short
ls array 2>/dev/null || echo "array/ removed"
```
Expected: 測試 OK、validate OK、SYNTAX_OK、工作目錄乾淨、`array/ removed`。

- [ ] **Step 2: 首頁篩選檢查（透過 Chrome DevTools Protocol 點按鈕）**

在背景啟動 headless Edge 並開啟遠端除錯（run_in_background）：
```bash
"/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" --headless=new --disable-gpu --remote-debugging-port=9222 --user-data-dir="<scratchpad>/edge-profile" "http://localhost:8000/index.html"
```

建立 `<scratchpad>/filter-check.mjs`（Node 24 內建 `fetch` 與 `WebSocket`）：
```js
const targets = await (await fetch("http://127.0.0.1:9222/json")).json();
const page = targets.find((t) => t.type === "page" && t.url.includes("index.html"));
const ws = new WebSocket(page.webSocketDebuggerUrl);
const pending = new Map();
let seq = 0;
ws.onmessage = (e) => {
  const m = JSON.parse(e.data);
  if (pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
};
await new Promise((r) => (ws.onopen = r));
const evaluate = (expression) => new Promise((r) => {
  const id = ++seq;
  pending.set(id, r);
  ws.send(JSON.stringify({ id, method: "Runtime.evaluate", params: { expression, returnByValue: true } }));
}).then((m) => m.result.result.value);
const click = (box, label) => evaluate(
  `[...document.querySelectorAll('#${box} .chip')].find((b) => b.textContent === ${JSON.stringify(label)}).click()`);
const shown = () => evaluate(
  `[...document.querySelectorAll('.problem-no')].map((e) => e.textContent).join(' ') || document.querySelector('.empty').textContent`);
console.log("初始      :", await shown());
await click("difficulty-filter", "Medium");
console.log("Medium    :", await shown());
await click("tag-filter", "雙指標");
console.log("Medium+雙 :", await shown());
await click("difficulty-filter", "全部");
console.log("雙指標    :", await shown());
ws.close();
```

Run: `node "<scratchpad>/filter-check.mjs"`
Expected:
```
初始      : 704. 27. 977. 209. 59. 203.
Medium    : 209. 59.
Medium+雙 : 沒有符合條件的題目。
雙指標    : 27. 977.
```
結束後停止背景 Edge。

- [ ] **Step 3: 停止本機伺服器**

停止 Task 3 啟動的背景 `http.server`。

---

### Task 8: 部署到 GitHub Pages

- [ ] **Step 1: 請使用者最後確認（必要）**

停下來詢問使用者：「即將建立公開 repo `Makoto1018/coding-practice-notes` 並 push 所有 commit，是否繼續？」得到明確同意前不可執行下一步。

- [ ] **Step 2: 建立 repo 並推送**

```bash
gh repo create coding-practice-notes --public --source=. --push
```
Expected: 印出 `https://github.com/Makoto1018/coding-practice-notes`

- [ ] **Step 3: 開啟 Pages**

```bash
gh api -X POST repos/Makoto1018/coding-practice-notes/pages -f "source[branch]=main" -f "source[path]=/"
```
Expected: JSON 內含 `"html_url": "https://makoto1018.github.io/coding-practice-notes/"`

- [ ] **Step 4: 等待部署完成**

每 30 秒查一次（最多 10 分鐘）：
```bash
gh api repos/Makoto1018/coding-practice-notes/pages/builds/latest --jq .status
```
Expected: 最終為 `built`

- [ ] **Step 5: 線上驗證**

```bash
for u in "" "problems.json" "notes/01-array/0704-binary-search.md"; do
  echo "$(curl -s -o /dev/null -w '%{http_code}' "https://makoto1018.github.io/coding-practice-notes/$u") $u"
done
```
Expected: 三行都是 `200`。再用 headless Edge dump 線上的 `problem.html?id=0203`，確認標題正確。

- [ ] **Step 6: 回報**

回報網址、所有 commit、新對話測試結論，以及需要使用者手動確認的篩選功能。
