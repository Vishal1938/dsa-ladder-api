import java.util.*;

class Solution {
    public long minAbsDifference(int[] a, int[] b) {
        int[] x = a.clone(), y = b.clone();
        Arrays.sort(x);
        Arrays.sort(y);
        int i = 0, j = 0;
        long best = Long.MAX_VALUE;
        while (i < x.length && j < y.length) {
            best = Math.min(best, Math.abs((long) x[i] - y[j]));
            if (x[i] < y[j]) i++;
            else j++;
        }
        return best;
    }
}
