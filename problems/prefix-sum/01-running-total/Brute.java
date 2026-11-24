import java.util.*;

class Solution {
    public long[] runningTotal(int[] nums) {
        long[] t = new long[nums.length];
        for (int i = 0; i < nums.length; i++) for (int j = 0; j <= i; j++) t[i] += nums[j];
        return t;
    }
}
