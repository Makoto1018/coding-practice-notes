# 59. Spiral Matrix II

| 項目 | 內容 |
|---|---|
| 難度 | Medium |
| 章節 | 陣列 |
| 技巧 | 模擬 |
| 原題連結 | [LeetCode 59](https://leetcode.com/problems/spiral-matrix-ii/) |
| 是否參考別人 | 否 |

## 題目重點

給一個正整數 `n`，產生 `n × n` 的矩陣，並依照順時針螺旋的順序把 1 到 n² 依序填進去。

## 解題思路

- **思路概述**：模擬
- **關鍵步驟**：
  - 初始時 left = 0, right = n - 1, up = 0, down = n - 1
  - 按照 左到右 → 上到下 → 右到左 → 下到上 的順序填充數字
  - 每次填充完一條邊後，縮小對應邊界 (left++, right--, up++, down--)
  - 若 n 為奇數，最後中心點需要手動填入

## 解法

### 解法 1：模擬（四個邊界指標）

```cpp
class Solution {
public:
    vector<vector<int>> generateMatrix(int n) {
        vector<vector<int>> res(n,vector<int>(n,0));
        if(n==1){
            res[0][0]=1;
            return res;
        }
        int left=0, right=n-1;
        int up=0, down=n-1;
        int ptr=0, ptr2=0;
        int ctr=1;
        for(int i=1;i<=n*n;){
            while(ptr2<right){    //左到右
                res[ptr][ptr2]=i;
                ptr2++;
                i++;
            }
            right--;
            while(ptr<down){    //上到下
                res[ptr][ptr2]=i;
                ptr++;
                i++;
            }
            down--;
            while(ptr2>left){    //右到左
                res[ptr][ptr2]=i;
                ptr2--;
                i++;
            }
            left++;
            while(ptr>up){    //下到上
                res[ptr][ptr2]=i;
                ptr--;
                i++;
            }
            up++;
            ptr=ctr;
            ptr2=ctr;
            ctr++;
            if(left==right){
                res[left][left] = i;
                i++;
            }
        }
        return res;
    }
};
```

- 時間複雜度：`O(n^2)`

> 🤖 AI 補充：除了回傳的矩陣外，額外空間是 `O(1)`。

## 學到的觀念

1. 如何用 四個邊界指標 控制螺旋填充

## 困難點與解法

1. 如何確保邊界不會超出範圍？→ 使用 left, right, up, down 來收縮範圍
2. 如何處理 n 為奇數時的情況？→ 透過 if(left == right) 處理中心點
