import java.util.*;

class Solution {
    public int largestSquare(int[][] grid, int budget) {
        int R = grid.length, C = grid[0].length;
        long[][] P = new long[R + 1][C + 1];
        for (int r = 0; r < R; r++)
            for (int c = 0; c < C; c++)
                P[r + 1][c + 1] = grid[r][c] + P[r][c + 1] + P[r + 1][c] - P[r][c];
        int best = 0;
        for (int r = 0; r < R; r++)
            for (int c = 0; c < C; c++) {
                // try to beat the current best by one: answers only grow, so this is O(R*C)
                int k = best + 1;
                while (r + k <= R && c + k <= C && P[r + k][c + k] - P[r][c + k] - P[r + k][c] + P[r][c] <= budget) {
                    best = k;
                    k++;
                }
            }
        return best;
    }
}
