import java.util.*;

class Solution {
    public void sortColors(int[] nums) {
        int low = 0, at = 0, high = nums.length - 1;
        while (at <= high) {
            if (nums[at] == 0) {
                int t = nums[low];
                nums[low++] = nums[at];
                nums[at++] = t;
            } else if (nums[at] == 2) {
                int t = nums[high];
                nums[high--] = nums[at];
                nums[at] = t;                            // the swapped-in part is still unknown
            } else at++;
        }
    }
}
