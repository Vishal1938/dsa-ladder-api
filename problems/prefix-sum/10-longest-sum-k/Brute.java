import java.util.*;

class Solution {
    public int longestSumK(int[] nums, int k) {
        int b = 0;
        for (int i = 0; i < nums.length; i++) { long s = 0; for (int j = i; j < nums.length; j++) { s += nums[j]; if (s == k) b = Math.max(b, j - i + 1); } }
        return b;
    }
}
