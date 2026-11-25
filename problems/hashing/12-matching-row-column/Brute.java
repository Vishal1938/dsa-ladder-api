import java.util.*;

class Solution {
    public int equalPairs(int[][] grid) {
        int n = grid.length, pairs = 0;
        for (int r = 0; r < n; r++)
            for (int c = 0; c < n; c++) {
                int[] column = new int[n];
                for (int i = 0; i < n; i++) column[i] = grid[i][c];
                if (Arrays.equals(grid[r], column)) pairs++;
            }
        return pairs;
    }
}
