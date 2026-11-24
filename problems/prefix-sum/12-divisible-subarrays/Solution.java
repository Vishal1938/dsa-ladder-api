import java.util.*;

class Solution {
    public long countDivisible(int[] nums, int k) {
        long[] seen = new long[k];
        seen[0] = 1;
        long prefix = 0, answer = 0;
        for (int x : nums) {
            prefix += x;
            int r = (int) Math.floorMod(prefix, (long) k);
            answer += seen[r];
            seen[r]++;
        }
        return answer;
    }
}
