# 刷題手札（coding-practice-notes）設計規格

日期：2026-11-14
狀態：已與使用者確認

## 1. 目標

把使用者在 `array/` 的 LeetCode 筆記（Markdown、C++）做成可以公開瀏覽的靜態網站，並建立一份 `AGENTS.md`，讓 AI 只拿到「題目網址 + 程式碼 +（選填）思路」就能依同一套格式新增題目。這是 HW9「建立自己的 AGENTS.md / CLAUDE.md」的作業成果，必須部署在 GitHub Pages。

## 2. 已確認的決策

| 項目 | 決定 |
|---|---|
| 內容格式 | 每題一個 Markdown 檔，網站在瀏覽器用 marked.js 渲染 |
| 使用者輸入 | 題目網址 + 程式碼（可多解）+ 選填的思路、是否參考別人 |
| 舊筆記 | 依新格式重整；使用者的程式碼、思路、心得原封保留，原題英文全文改為自己的話寫的「題目重點」 |
| 分類 | 依資料結構分章節（代碼隨想錄順序），另加技巧標籤；首頁依刷題順序排列 |
| 架構 | 自己寫的輕量網站：`index.html` + `problem.html?id=NNNN`，不使用框架與建置工具 |
| 部署 | GitHub Pages，repo `coding-practice-notes`（公開），帳號 Makoto1018 |
| 新對話測試 | 第 6 題（203）不由主代理轉換，交給沒有上下文的子代理只依 AGENTS.md 新增 |

## 3. 專案結構

```
hw9/                         ← repo 根目錄
├── AGENTS.md
├── CLAUDE.md                ← 內容：@AGENTS.md
├── README.md
├── .nojekyll
├── .gitignore               ← 忽略 tutorial.md
├── index.html
├── problem.html
├── problems.json
├── assets/
│   ├── style.css
│   ├── home.js
│   └── problem.js
├── templates/
│   └── problem-template.md
├── scripts/
│   └── validate.py          ← 檢查 problems.json 與筆記一致（只用 Python 標準函式庫，不是建置步驟）
├── .claude/commands/
│   └── add-problem.md       ← 只指向 AGENTS.md 的新增流程，不重複規則
├── docs/superpowers/specs/  ← 本文件
└── notes/
    ├── 01-array/
    └── 02-linked-list/      ← 由新對話測試建立
```

## 4. problems.json

```json
{
  "chapters": [
    { "id": "01-array", "name": "陣列" }
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
    }
  ]
}
```

- `chapters` 完整清單（依此順序）：`01-array` 陣列、`02-linked-list` 鏈結串列、`03-hash-table` 雜湊表、`04-string` 字串、`05-stack-queue` 堆疊與佇列、`06-binary-tree` 二元樹、`07-backtracking` 回溯、`08-greedy` 貪心、`09-dynamic-programming` 動態規劃、`10-monotonic-stack` 單調堆疊、`11-graph` 圖論。
- `tags` 為允許的技巧標籤清單；新增標籤時先加進此清單。
- `problems` 依 `order` 排列；`order` 為刷題順序，新增時取最大值 + 1。
- `difficulty` 只能是 `Easy`、`Medium`、`Hard`。

## 5. 筆記 Markdown 格式

檔名：`notes/<chapter>/<NNNN>-<slug>.md`，NNNN 為補零四位數題號，slug 取自 LeetCode 網址。

區塊依序：

1. `# <題號>. <英文題名>`
2. 資訊表格：難度｜章節｜技巧｜原題連結｜是否參考別人
3. `## 題目重點`：中文，2～3 句，用自己的話，不可貼原題全文
4. `## 解題思路`：`思路概述`、`關鍵步驟` 兩個項目
5. `## 解法`：每個解法一個 `### 解法 N：<名稱>`，內含 cpp 程式碼區塊與時間、空間複雜度
6. `## 學到的觀念`
7. `## 困難點與解法`

規則：

- 使用者的程式碼一字不改（包含註解與縮排）。
- 使用者寫的思路、觀念、困難點保留原意，只做排版。
- AI 補寫的內容一律放在以 `> 🤖 AI 補充：` 開頭的引用區塊；網站將其顯示為不同底色。
- 沒有內容的區塊寫「無」，不可留空。
- 標題與資訊表格必須和 `problems.json` 一致。

## 6. 網頁

**首頁**：標題「刷題手札」與統計（總題數、各難度題數）；難度篩選（All/Easy/Medium/Hard）與技巧標籤篩選，可同時使用；依章節分卡片，卡片內依 `order` 列出題號、題名、難度標籤、技巧標籤；沒有題目（或篩選後為空）的章節不顯示。

**題目頁**：`problem.html?id=0704`。上方「← 回首頁」；中間為渲染後的 Markdown（highlight.js 上色 C++，`🤖 AI 補充` 引用區塊加上專用 class）；下方依 `order` 的上一題／下一題。id 不存在或讀取失敗時顯示錯誤訊息與回首頁連結。頁面標題設為 `<題號>. <題名> | 刷題手札`。

**風格**：主色 `#4f46e5`；背景 `#f8fafc`、卡片 `#ffffff`；文字 `#1e293b`／次要 `#64748b`；難度 Easy `#16a34a`、Medium `#ea580c`、Hard `#dc2626`；字體 Noto Sans TC、JetBrains Mono；最大寬度 800px；卡片圓角 12px。所有顏色為 `:root` CSS 變數，並提供跟隨系統的深色模式。手機寬度 375px 無橫向捲軸。

**外部資源**：cdnjs 上固定版本的 marked.js 與 highlight.js（含 cpp），Google Fonts。

## 7. GitHub Pages 相容

純靜態、相對路徑、檔名小寫、根目錄 `.nojekyll`、Pages 來源為 `main` 分支根目錄。網址：`https://makoto1018.github.io/coding-practice-notes/`。

## 8. 新增題目流程（AGENTS.md 的核心）

輸入：網址、程式碼、選填的思路與是否參考別人。

1. 從網址取 slug，判斷題號、題名、難度、章節、技巧標籤（只能用清單內的值，不足時先擴充清單）。
2. 題號已存在 → 改為更新該題（例如加入新解法），不重複新增。
3. 複製範本到正確路徑，依第 5 節填寫。
4. 在 `problems.json` 新增一筆，`order` = 最大值 + 1。
5. 執行 `python scripts/validate.py`，必須通過；再依檢查清單逐項回報。

## 9. Git 與部署順序

1. `git init`；commit 1：只含原始 `array/`。
2. commit 2：本規格文件。
3. 後續 commit：網站、規則、轉換後的前 5 題，並刪除 `array/` 中已轉換的檔案（203 原稿保留到新對話測試完成後再刪）。
4. **推送前請使用者最後確認**，再執行 `gh repo create coding-practice-notes --public --source=. --push`。
5. 以 `gh api` 開啟 Pages（`main` 分支 `/`），等待部署後用 curl 驗證首頁、`problems.json`、一個 `.md` 皆回應 200。

## 10. 測試

- 本機 `python -m http.server` 檢查每題可渲染、篩選、上下題連結。
- `scripts/validate.py` 驗證 `problems.json` 合法、`file` 皆存在、`chapter`／`tags`／`difficulty` 值合法、`order` 不重複、md 標題與 json 一致。
- 新對話測試：子代理只拿到 203 的網址、程式碼與使用者原本的思路，依 AGENTS.md 新增；檢查結果是否通過驗證腳本與檢查清單，並把結果記錄下來，供作業說明使用。

## 11. 不在範圍內

複習進度、多語言解法切換、全文搜尋、錯題本。
