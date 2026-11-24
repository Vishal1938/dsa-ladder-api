import java.util.*;

class Solution {
    public long countZeroSum(int[] nums) {
        Map<Long, Integer> count = new HashMap<>();
        count.put(0L, 1);
        long prefix = 0, answer = 0;
        for (int x : nums) {
            prefix += x;
            int c = count.getOrDefault(prefix, 0);
            answer += c;
            count.put(prefix, c + 1);
        }
        return answer;
    }
}
