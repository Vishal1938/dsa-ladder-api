import java.util.*;

class Solution {
    public long[] productExceptSelf(int[] nums) {
        int n = nums.length;
        long[] out = new long[n];
        long run = 1;
        for (int i = 0; i < n; i++) { out[i] = run; run *= nums[i]; }      // everything to the left of i
        run = 1;
        for (int i = n - 1; i >= 0; i--) { out[i] *= run; run *= nums[i]; } // times everything to its right
        return out;
    }
}
