import java.util.*;

class Solution {
    public int longestPositive(int[] scores) {
        Map<Integer, Integer> first = new HashMap<>();
        int sum = 0, best = 0;
        for (int i = 0; i < scores.length; i++) {
            sum += scores[i] >= 7 ? 1 : -1;
            if (sum > 0) best = i + 1;
            else {
                Integer j = first.get(sum - 1);
                if (j != null) best = Math.max(best, i - j);
            }
            first.putIfAbsent(sum, i);
        }
        return best;
    }
}
