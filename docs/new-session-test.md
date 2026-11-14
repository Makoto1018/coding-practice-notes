# 新對話測試紀錄：用 AGENTS.md 新增第 6 題（203）

日期：2026-11-14

## 目的

確認一個**完全沒有本專案對話脈絡**的 AI，只靠 repo 裡的 `AGENTS.md`，加上使用者提供的「題目網址 + 程式碼 + 思路」，就能依照同一套格式新增題目。

## 方法

- 前 5 題（陣列）由主代理依規格轉換，並寫好 `AGENTS.md`、範本與 `scripts/validate.py`。
- 第 6 題 203. Remove Linked List Elements 不由主代理轉換，改由一個全新的子代理（Claude Code `general-purpose` agent，不繼承主對話）處理。
- 子代理只拿到下面的 prompt，沒有設計規格、沒有其他題目的轉換過程，也被要求不要讀取 `array/` 原稿。
- 為了避免洩題，`AGENTS.md` 裡的範例刻意使用 Two Sum，而不是 203。

### 給子代理的 prompt

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

程式碼 1（自己寫的）：（略，與原稿 array/6_203 第一段相同）
程式碼 2（dummy node）：（略，與原稿 array/6_203 第二段相同）
````

## 子代理的成果

- 新增 `notes/02-linked-list/0203-remove-linked-list-elements.md`
- `problems.json` 最後新增一筆：`id 0203`、`chapter 02-linked-list`、`tags ["虛擬頭節點"]`、`order 6`、`referenced true`
- 一次完成，6 次工具呼叫，約 32 秒；自行執行 `validate.py` 並逐項回報檢查清單（10 項全部 ✅）

## 主代理的獨立驗證

| 檢查 | 結果 |
|---|---|
| `python scripts/validate.py` | ✅ `OK：problems.json 與所有筆記一致` |
| 兩段程式碼與原稿逐字比對（腳本） | ✅ `CODE IDENTICAL` |
| `git diff problems.json` | ✅ 只新增 0203 一筆，其他題目未被改動 |
| 網站題目頁 `problem.html?id=0203` | ✅ 標題「203. Remove Linked List Elements \| 刷題手札」、2 個 AI 補充區塊、上一題為 59 |
| 網站首頁 | ✅ 共 6 題，新增「鏈結串列（1）」章節卡片；59 的「下一題」變成 203 |

檢查清單逐項核對：

1. ✅ 路徑 `notes/02-linked-list/0203-remove-linked-list-elements.md` 與 json 一致
2. ✅ 標題、資訊表格與 json 一致
3. ✅ 章節、標籤皆在清單內（沿用既有的「虛擬頭節點」）
4. ✅ `order` = 6（原最大值 5）
5. ✅ 題目重點為自己的話，2 句，沒有原題全文
6. ✅ 程式碼逐字相同
7. ✅ 使用者的思路、觀念、困難點保留原文；只把「關鍵步驟」依句號拆成兩行子清單、`$O(n)$` 改為 `` `O(n)` ``
8. ✅ AI 內容（兩個空間複雜度、一句 dummy node 說明）都在 `> 🤖 AI 補充：` 區塊
9. ✅ 沒有空白區塊（困難點保留使用者寫的「1. 無」）
10. ✅ validate 通過

## 觀察與小問題

- 使用者只寫了一個時間複雜度，子代理把它放在兩個解法底下各一次。結果正確，但 `AGENTS.md` 沒有規定「一個複雜度對多個解法」時要怎麼放，這是規則裡唯一沒寫清楚的地方。
- 子代理說題號和難度是它自己就知道的，沒有上網查。`AGENTS.md` 要求「不確定時」才查，所以沒有違反規則，結果也正確。
- 沒有發現需要修改 `AGENTS.md` 才能通過的問題，因此**沒有修改規則、也沒有重測**。

## 結論

全新的 AI 只靠 `AGENTS.md` 就一次完成新增，格式與前 5 題一致，也通過自動驗證與人工核對。`AGENTS.md` 加上 `validate.py` 足以讓 AI 依固定格式新增題目。
