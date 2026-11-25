import java.util.*;

class Solution {
    public long pairsDivisible(int[] nums, int m) {
        long[] seen = new long[m];
        long pairs = 0;
        for (int x : nums) {
            int r = Math.floorMod(x, m);
            pairs += seen[(m - r) % m];
            seen[r]++;
        }
        return pairs;
    }
}
