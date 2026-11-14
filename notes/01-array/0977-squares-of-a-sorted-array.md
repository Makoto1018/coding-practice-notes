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
