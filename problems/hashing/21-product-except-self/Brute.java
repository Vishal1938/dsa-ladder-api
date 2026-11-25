import java.util.*;

class Solution {
    public long[] productExceptSelf(int[] nums) {
        long[] out = new long[nums.length];
        for (int i = 0; i < nums.length; i++) {
            long p = 1;
            for (int j = 0; j < nums.length; j++) if (j != i) p *= nums[j];
            out[i] = p;
        }
        return out;
    }
}
