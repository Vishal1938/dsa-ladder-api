import java.util.*;

class Solution {
    public void rotate(int[] nums, int k) {
        int n = nums.length;
        k %= n;
        reverse(nums, 0, n - 1);
        reverse(nums, 0, k - 1);
        reverse(nums, k, n - 1);
    }

    private void reverse(int[] nums, int from, int to) {
        while (from < to) {
            int t = nums[from];
            nums[from++] = nums[to];
            nums[to--] = t;
        }
    }
}
