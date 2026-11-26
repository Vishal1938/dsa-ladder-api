import java.util.*;

class Solution {
    public int[][] intervalIntersections(int[][] a, int[][] b) {
        List<int[]> out = new ArrayList<>();
        for (int[] x : a)
            for (int[] y : b) {
                int start = Math.max(x[0], y[0]), end = Math.min(x[1], y[1]);
                if (start <= end) out.add(new int[]{start, end});
            }
        return out.toArray(new int[0][]);
    }
}
