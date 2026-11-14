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
