import java.util.*;

class Solution {
    public int[] sortedSquares(int[] nums) {
        int n = nums.length;
        int[] out = new int[n];
        int left = 0, right = n - 1;
        for (int slot = n - 1; slot >= 0; slot--) {
            int lo = nums[left] * nums[left], hi = nums[right] * nums[right];
            if (lo > hi) { out[slot] = lo; left++; }
            else { out[slot] = hi; right--; }
        }
        return out;
    }
}
