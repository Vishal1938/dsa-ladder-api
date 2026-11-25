import java.util.*;

class Solution {
    public long countEqualPairs(int[] nums) {
        Map<Integer, Integer> count = new HashMap<>();
        long pairs = 0;
        for (int x : nums) {
            int seen = count.getOrDefault(x, 0);
            pairs += seen;                 // x pairs with every earlier copy of x
            count.put(x, seen + 1);
        }
        return pairs;
    }
}
