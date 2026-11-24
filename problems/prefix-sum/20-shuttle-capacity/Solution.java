import java.util.*;

class Solution {
    public boolean canCarry(int[][] trips, int capacity) {
        int maxStop = 0;
        for (int[] t : trips) maxStop = Math.max(maxStop, t[2]);
        long[] diff = new long[maxStop + 1];
        for (int[] t : trips) {
            diff[t[1]] += t[0];
            diff[t[2]] -= t[0];
        }
        long onBoard = 0;
        for (int s = 0; s <= maxStop; s++) {
            onBoard += diff[s];
            if (onBoard > capacity) return false;
        }
        return true;
    }
}
