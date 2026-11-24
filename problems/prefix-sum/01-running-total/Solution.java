import java.util.*;

class Solution {
    public long[] runningTotal(int[] nums) {
        long[] total = new long[nums.length];
        long sum = 0;
        for (int i = 0; i < nums.length; i++) {
            sum += nums[i];
            total[i] = sum;
        }
        return total;
    }
}
