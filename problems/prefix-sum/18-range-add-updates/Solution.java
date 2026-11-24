import java.util.*;

class Solution {
    public long[] applyUpdates(int n, int[][] updates) {
        long[] diff = new long[n + 1];
        for (int[] u : updates) {
            diff[u[0]] += u[2];
            diff[u[1] + 1] -= u[2];
        }
        long[] out = new long[n];
        long run = 0;
        for (int i = 0; i < n; i++) {
            run += diff[i];
            out[i] = run;
        }
        return out;
    }
}
