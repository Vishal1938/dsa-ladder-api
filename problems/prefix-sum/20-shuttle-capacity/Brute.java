import java.util.*;

class Solution {
    public boolean canCarry(int[][] trips, int capacity) {
        for (int s = 0; s <= 10; s++) { long c = 0; for (int[] t : trips) if (t[1] <= s && s < t[2]) c += t[0]; if (c > capacity) return false; }
        return true;
    }
}
