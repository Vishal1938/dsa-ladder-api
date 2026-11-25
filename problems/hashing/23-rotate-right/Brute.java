import java.util.*;

class Solution {
    public void rotate(int[] nums, int k) {
        for (int step = 0; step < k; step++) {
            int last = nums[nums.length - 1];
            for (int i = nums.length - 1; i > 0; i--) nums[i] = nums[i - 1];
            nums[0] = last;
        }
    }
}
