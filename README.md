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
