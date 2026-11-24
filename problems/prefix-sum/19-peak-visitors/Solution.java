import java.util.*;

class Solution {
    public int peakVisitors(int[][] visits) {
        int maxT = 0;
        for (int[] v : visits) maxT = Math.max(maxT, v[1]);
        int[] diff = new int[maxT + 1];
        for (int[] v : visits) {
            diff[v[0]]++;
            diff[v[1]]--;
        }
        int run = 0, best = 0;
        for (int t = 0; t <= maxT; t++) {
            run += diff[t];
            best = Math.max(best, run);
        }
        return best;
    }
}
