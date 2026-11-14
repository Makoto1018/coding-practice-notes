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
