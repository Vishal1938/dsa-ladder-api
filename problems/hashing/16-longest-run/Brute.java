import java.util.*;

class Solution {
    public int longestConsecutive(int[] nums) {
        int best = 0;
        for (int x : nums) {
            int length = 1;
            while (holds(nums, x + length)) length++;
            best = Math.max(best, length);
        }
        return best;
    }

    private boolean holds(int[] nums, int v) {
        for (int x : nums) if (x == v) return true;
        return false;
    }
}
