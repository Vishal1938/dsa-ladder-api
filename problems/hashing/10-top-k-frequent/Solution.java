import java.util.*;

class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> count = new HashMap<>();
        for (int x : nums) count.merge(x, 1, Integer::sum);
        List<Integer> values = new ArrayList<>(count.keySet());
        values.sort((p, q) -> {
            int byCount = Integer.compare(count.get(q), count.get(p));
            return byCount != 0 ? byCount : Integer.compare(p, q);
        });
        int[] top = new int[k];
        for (int i = 0; i < k; i++) top[i] = values.get(i);
        return top;
    }
}
