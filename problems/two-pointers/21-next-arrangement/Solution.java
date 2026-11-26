import java.util.*;

class Solution {
    public void nextPermutation(int[] nums) {
        int n = nums.length, dip = n - 2;
        while (dip >= 0 && nums[dip] >= nums[dip + 1]) dip--;
        if (dip >= 0) {
            int swapWith = n - 1;                        // rightmost value bigger than nums[dip]
            while (nums[swapWith] <= nums[dip]) swapWith--;
            int t = nums[dip];
            nums[dip] = nums[swapWith];
            nums[swapWith] = t;
        }
        for (int left = dip + 1, right = n - 1; left < right; left++, right--) {
            int t = nums[left];
            nums[left] = nums[right];
            nums[right] = t;
        }
    }
}
