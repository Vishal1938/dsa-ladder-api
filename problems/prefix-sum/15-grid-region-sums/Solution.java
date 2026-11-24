import java.util.*;

class Solution {
    public long[] regionSums(int[][] grid, int[][] queries) {
        int R = grid.length, C = grid[0].length;
        long[][] P = new long[R + 1][C + 1];
        for (int r = 0; r < R; r++)
            for (int c = 0; c < C; c++)
                P[r + 1][c + 1] = grid[r][c] + P[r][c + 1] + P[r + 1][c] - P[r][c];
        long[] ans = new long[queries.length];
        for (int i = 0; i < queries.length; i++) {
            int r1 = queries[i][0], c1 = queries[i][1], r2 = queries[i][2], c2 = queries[i][3];
            ans[i] = P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1];
        }
        return ans;
    }
}
