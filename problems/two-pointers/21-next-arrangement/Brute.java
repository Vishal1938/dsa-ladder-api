import java.util.*;

class Solution {
    public void nextPermutation(int[] nums) {
        int n = nums.length, dip = -1;
        for (int i = n - 2; i >= 0; i--) if (nums[i] < nums[i + 1]) { dip = i; break; }
        if (dip < 0) {                                   // already the largest: wrap to the smallest
            Arrays.sort(nums);
            return;
        }
        int pick = -1;                                   // smallest value after dip that still beats it
        for (int j = dip + 1; j < n; j++)
            if (nums[j] > nums[dip] && (pick < 0 || nums[j] <= nums[pick])) pick = j;
        int t = nums[dip];
        nums[dip] = nums[pick];
        nums[pick] = t;
        Arrays.sort(nums, dip + 1, n);                   // make the tail as small as possible
    }
}
