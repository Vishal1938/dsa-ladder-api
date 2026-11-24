import java.util.*;

class Solution {
    public long[] applyUpdates(int n, int[][] updates) {
        long[] o = new long[n];
        for (int[] u : updates) for (int i = u[0]; i <= u[1]; i++) o[i] += u[2];
        return o;
    }
}
