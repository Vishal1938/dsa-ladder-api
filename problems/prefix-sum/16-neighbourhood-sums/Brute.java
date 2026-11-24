import java.util.*;

class Solution {
    public long[][] neighbourhoodSum(int[][] grid, int k) {
        int R = grid.length, C = grid[0].length; long[][] o = new long[R][C];
        for (int r = 0; r < R; r++) for (int c = 0; c < C; c++) for (int i = 0; i < R; i++) for (int j = 0; j < C; j++) if (Math.abs(i - r) <= k && Math.abs(j - c) <= k) o[r][c] += grid[i][j];
        return o;
    }
}
