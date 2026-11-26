import java.util.*;

class Solution {
    public int[] removeValue(int[] nums, int val) {
        int n = nums.length, i = 0;
        while (i < n) {
            if (nums[i] == val) {
                for (int j = i; j < n - 1; j++) nums[j] = nums[j + 1];   // delete it and close the gap
                n--;
            } else i++;
        }
        return Arrays.copyOf(nums, n);
    }
}
