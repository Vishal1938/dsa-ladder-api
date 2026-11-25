import java.util.*;

class Solution {
    public int equalPairs(int[][] grid) {
        int n = grid.length;
        Map<String, Integer> rows = new HashMap<>();
        for (int[] row : grid) rows.merge(key(row), 1, Integer::sum);
        int pairs = 0;
        int[] column = new int[n];
        for (int c = 0; c < n; c++) {
            for (int r = 0; r < n; r++) column[r] = grid[r][c];
            pairs += rows.getOrDefault(key(column), 0);
        }
        return pairs;
    }

    private String key(int[] line) {
        StringBuilder sb = new StringBuilder();
        for (int x : line) sb.append(x).append(',');
        return sb.toString();
    }
}
