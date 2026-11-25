import java.util.*;

class Solution {
    public long countPairsWithSum(int[] nums, int target) {
        Map<Integer, Integer> count = new HashMap<>();
        long pairs = 0;
        for (int x : nums) {
            pairs += count.getOrDefault(target - x, 0);
            count.merge(x, 1, Integer::sum);
        }
        return pairs;
    }
}
