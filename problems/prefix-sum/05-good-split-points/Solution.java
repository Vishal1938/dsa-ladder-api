import java.util.*;

class Solution {
    public int countSplits(int[] nums) {
        long total = 0;
        for (int x : nums) total += x;
        long left = 0;
        int good = 0;
        for (int i = 0; i < nums.length - 1; i++) {
            left += nums[i];
            if (left >= total - left) good++;
        }
        return good;
    }
}
