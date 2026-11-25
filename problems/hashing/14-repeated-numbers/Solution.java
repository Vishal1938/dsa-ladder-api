import java.util.*;

class Solution {
    public List<Integer> findRepeated(int[] nums) {
        List<Integer> hits = new ArrayList<>();
        for (int x : nums) {
            int v = Math.abs(x), slot = v - 1;
            if (nums[slot] < 0) hits.add(v);            // slot already marked: v is not new
            else nums[slot] = -nums[slot];
        }
        Collections.sort(hits);
        List<Integer> repeated = new ArrayList<>();
        for (int v : hits) if (repeated.isEmpty() || repeated.get(repeated.size() - 1) != v) repeated.add(v);
        return repeated;
    }
}
