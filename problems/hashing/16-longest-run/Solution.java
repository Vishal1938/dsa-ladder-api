import java.util.*;

class Solution {
    public int longestConsecutive(int[] nums) {
        Set<Integer> occupied = new HashSet<>();
        for (int x : nums) occupied.add(x);
        int best = 0;
        for (int x : occupied) {
            if (occupied.contains(x - 1)) continue;      // not the start of a run
            int length = 1;
            while (occupied.contains(x + length)) length++;
            best = Math.max(best, length);
        }
        return best;
    }
}
