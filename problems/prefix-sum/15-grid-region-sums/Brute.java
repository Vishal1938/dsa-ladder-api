import java.util.*;

class Solution {
    public long[] regionSums(int[][] grid, int[][] queries) {
        long[] a = new long[queries.length];
        for (int i = 0; i < queries.length; i++) for (int r = queries[i][0]; r <= queries[i][2]; r++) for (int c = queries[i][1]; c <= queries[i][3]; c++) a[i] += grid[r][c];
        return a;
    }
}
