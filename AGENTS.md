# AGENTS.md — 刷題手札

這個 repo 是 LeetCode 刷題筆記網站（GitHub Pages 純靜態）。你最常被要求做的事是：**使用者給「題目網址 + 程式碼 +（選填）思路」，你把它變成一篇筆記並登記到網站。** 請完全依照本文件，不要自創格式。

## 專案目的

- 「刷題手札」是我的 LeetCode 解題筆記網站，讀者是我自己（面試前複習）與一起準備演算法的同學。
- 每題一篇筆記，首頁依資料結構分章節（順序參考代碼隨想錄），可依難度與技巧標籤篩選。
- 程式碼與心得是我寫的；AI 負責排版、整理格式，以及標示清楚的補充說明。

## 技術限制

- 只用純 HTML、CSS、原生 JavaScript；不使用框架、npm 或任何建置工具。
- 外部資源只允許：cdnjs 上固定版本的 marked 4.3.0、highlight.js 11.9.0（含 cpp），以及 Google Fonts 的 Noto Sans TC、JetBrains Mono。
- 部署在 GitHub Pages：所有路徑用相對路徑、檔名一律小寫，根目錄保留 `.nojekyll`。
- `scripts/validate.py` 只能使用 Python 標準函式庫。

## 視覺風格

所有顏色都定義在 `assets/style.css` 的 `:root` CSS 變數，HTML 不寫 inline style；要調整樣式只改 `style.css`。

| 項目 | 規格 |
|---|---|
| 主色 | `#4f46e5`（標題、連結、篩選按鈕、技巧標籤） |
| 背景／卡片 | 背景 `#f8fafc`、卡片 `#ffffff`，卡片圓角 `12px` |
| 文字 | 內文 `#1e293b`、次要文字 `#64748b` |
| 難度 | Easy `#16a34a`、Medium `#ea580c`、Hard `#dc2626` |
| AI 補充區塊 | 底色 `#fefce8`、左邊框 `#ca8a04` |
| 字體 | 內文 `"Noto Sans TC"`；程式碼 `"JetBrains Mono"`（關閉連字，避免 `<=` 被顯示成 `≤`） |
| 版面 | 內容置中，最大寬度 `800px` |
| 深色模式 | 跟隨系統 `prefers-color-scheme: dark`，在同一個 `:root` 變數組內覆寫 |
| 手機 | 375px 寬度下整頁不可橫向捲動；程式碼區塊與表格可在區塊內捲動 |

## 專案結構

```
problems.json                      唯一的題目索引（章節、標籤清單、題目）
notes/<chapter>/<NNNN>-<slug>.md   每題一篇筆記
templates/problem-template.md      新筆記範本
scripts/validate.py                一致性檢查（新增或修改後必跑）
index.html / problem.html          網站頁面（assets/ 內為 css 與 js）
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
6. **登記到 `problems.json`**：在 `problems` 陣列**最後**加一筆，`order` = 現有最大 `order` + 1。範例：
   ```json
   {
     "id": "0001",
     "title": "Two Sum",
     "slug": "two-sum",
     "difficulty": "Easy",
     "chapter": "03-hash-table",
     "tags": ["雜湊"],
     "order": 7,
     "referenced": false,
     "file": "notes/03-hash-table/0001-two-sum.md"
   }
   ```
   - `id`：補零四位數字串；`difficulty`：`Easy` / `Medium` / `Hard`；`referenced`：有參考別人為 `true`。
7. **驗證**：執行 `python scripts/validate.py`，必須印出 `OK`。有錯就修正後重跑。
8. **回報**：依下方「完成檢查清單」逐項回報 ✅/❌，並列出你新增或修改的檔案。

## 筆記格式

檔名：`notes/<chapter>/<NNNN>-<slug>.md`。區塊順序固定如下（二級標題文字必須一字不差）：

````markdown
# 1. Two Sum

| 項目 | 內容 |
|---|---|
| 難度 | Easy |
| 章節 | 雜湊表 |
| 技巧 | 雜湊 |
| 原題連結 | [LeetCode 1](https://leetcode.com/problems/two-sum/) |
| 是否參考別人 | 否 |

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
