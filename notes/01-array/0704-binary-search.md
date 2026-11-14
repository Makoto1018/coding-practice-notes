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
