import java.util.*;

class Solution {
    public long countSumK(int[] nums, int k) {
        Map<Long, Integer> count = new HashMap<>();
        count.put(0L, 1);
        long prefix = 0, answer = 0;
        for (int x : nums) {
            prefix += x;
            answer += count.getOrDefault(prefix - k, 0);
            count.merge(prefix, 1, Integer::sum);
        }
        return answer;
    }
}
