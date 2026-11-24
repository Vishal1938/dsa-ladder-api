import java.util.*;

class Solution {
    public long bestWindow(int[] nums, int k) {
        long[] prefix = new long[nums.length + 1];
        for (int i = 0; i < nums.length; i++) prefix[i + 1] = prefix[i] + nums[i];
        long best = Long.MIN_VALUE;
        for (int i = 0; i + k <= nums.length; i++) best = Math.max(best, prefix[i + k] - prefix[i]);
        return best;
    }
}
