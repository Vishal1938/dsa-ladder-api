import java.util.*;

class Solution {
    public long minAbsDifference(int[] a, int[] b) {
        long best = Long.MAX_VALUE;
        for (int x : a)
            for (int y : b)
                best = Math.min(best, Math.abs((long) x - y));
        return best;
    }
}
