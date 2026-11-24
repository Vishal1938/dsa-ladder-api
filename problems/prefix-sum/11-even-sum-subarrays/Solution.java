import java.util.*;

class Solution {
    public long countEvenSum(int[] nums) {
        long[] seen = {1, 0};          // seen[parity] = prefixes so far with that parity
        long prefix = 0, answer = 0;
        for (int x : nums) {
            prefix += x;
            int p = (int) Math.floorMod(prefix, 2L);
            answer += seen[p];
            seen[p]++;
        }
        return answer;
    }
}
