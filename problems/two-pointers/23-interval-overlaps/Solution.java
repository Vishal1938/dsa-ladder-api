import java.util.*;

class Solution {
    public int[][] intervalIntersections(int[][] a, int[][] b) {
        List<int[]> out = new ArrayList<>();
        int i = 0, j = 0;
        while (i < a.length && j < b.length) {
            int start = Math.max(a[i][0], b[j][0]), end = Math.min(a[i][1], b[j][1]);
            if (start <= end) out.add(new int[]{start, end});
            if (a[i][1] < b[j][1]) i++;
            else j++;
        }
        return out.toArray(new int[0][]);
    }
}
