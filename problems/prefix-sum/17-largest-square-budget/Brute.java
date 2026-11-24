import java.util.*;

class Solution {
    public int largestSquare(int[][] grid, int budget) {
        int R = grid.length, C = grid[0].length, b = 0;
        for (int r = 0; r < R; r++) for (int c = 0; c < C; c++) for (int k = 1; r + k <= R && c + k <= C; k++) { long s = 0; for (int i = r; i < r + k; i++) for (int j = c; j < c + k; j++) s += grid[i][j]; if (s <= budget) b = Math.max(b, k); }
        return b;
    }
}
