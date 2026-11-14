# 203. Remove Linked List Elements

| 項目 | 內容 |
|---|---|
| 難度 | Easy |
| 章節 | 鏈結串列 |
| 技巧 | 虛擬頭節點 |
| 原題連結 | [LeetCode 203](https://leetcode.com/problems/remove-linked-list-elements/) |
| 是否參考別人 | 是（忘記linked list是甚麼） |

## 題目重點

給一條單向鏈結串列的頭節點和一個整數 `val`，要把所有值等於 `val` 的節點從串列中拿掉，最後回傳新的頭節點。要注意頭節點本身也可能被刪掉，甚至整條串列被刪光而回傳空串列。

## 解題思路

- **思路概述**：熟悉 **linked list** 跟 **pointer** 的運作方式。dummy node 的觀念
- **關鍵步驟**：
  - head 的部分可以先用 while 慢慢縮短整個 list。
  - 可以用dummy node (虛設的在 head 之前的新頭) 的概念來處理 head 也要刪掉的問題

## 解法

### 解法 1：自己寫的

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* removeElements(ListNode* head, int val) {
        while(head != NULL && head->val == val){
            ListNode* tmp = head;
            head = head->next;
            delete tmp;
        }
        ListNode* ptr = head;
        while(ptr!=NULL && ptr->next != NULL){
            if(ptr->next->val == val){
                ListNode* tmp = ptr->next;
                ptr->next = ptr->next->next;
                delete tmp;
            }else{
                ptr = ptr->next;
            }
        }
        return head;
    }
};
```

- 時間複雜度：`O(n)`

> 🤖 AI 補充：空間複雜度 `O(1)`，只用了幾個指標變數。

### 解法 2：dummy node

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* removeElements(ListNode* head, int val) {
        ListNode* dummy = new ListNode(0,head);
        ListNode* ptr = dummy;
        while(ptr->next != NULL){
            if(ptr->next->val == val){
                ListNode* tmp = ptr->next;
                ptr->next = ptr->next->next;
                delete tmp;
            }else{
                ptr = ptr->next;
            }
        }
        head = dummy->next;
        delete dummy;
        return head;
    }
};
```

- 時間複雜度：`O(n)`

> 🤖 AI 補充：空間複雜度 `O(1)`；dummy node 讓刪除 head 和刪除中間節點可以用同一套邏輯處理。

## 學到的觀念

1. linked list 跟 pointer
2. dummy node

## 困難點與解法

1. 無
