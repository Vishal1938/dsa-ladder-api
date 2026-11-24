import java.util.*;

class Solution {
    public int peakVisitors(int[][] visits) {
        int b = 0;
        for (int t = 0; t <= 20; t++) { int c = 0; for (int[] v : visits) if (v[0] <= t && t < v[1]) c++; b = Math.max(b, c); }
        return b;
    }
}
