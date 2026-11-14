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
