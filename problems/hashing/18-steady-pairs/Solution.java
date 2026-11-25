import java.util.*;

class Solution {
    public long countSteadyPairs(int[] nums) {
        Map<Integer, Integer> count = new HashMap<>();
        long pairs = 0;
        for (int i = 0; i < nums.length; i++) {
            int key = nums[i] - i;                      // nums[j] - j == nums[i] - i
            int seen = count.getOrDefault(key, 0);
            pairs += seen;
            count.put(key, seen + 1);
        }
        return pairs;
    }
}
