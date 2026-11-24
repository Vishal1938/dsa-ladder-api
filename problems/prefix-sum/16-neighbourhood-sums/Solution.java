import java.util.*;

class Solution {
    public long[][] neighbourhoodSum(int[][] grid, int k) {
        int R = grid.length, C = grid[0].length;
        long[][] P = new long[R + 1][C + 1];
        for (int r = 0; r < R; r++)
            for (int c = 0; c < C; c++)
                P[r + 1][c + 1] = grid[r][c] + P[r][c + 1] + P[r + 1][c] - P[r][c];
        long[][] out = new long[R][C];
        for (int r = 0; r < R; r++)
            for (int c = 0; c < C; c++) {
                int r1 = Math.max(0, r - k), c1 = Math.max(0, c - k), r2 = Math.min(R - 1, r + k), c2 = Math.min(C - 1, c + k);
                out[r][c] = P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1];
            }
        return out;
    }
}
