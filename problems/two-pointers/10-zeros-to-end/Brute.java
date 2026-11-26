import java.util.*;

class Solution {
    public void moveZeros(int[] nums) {
        int n = nums.length, parked = 0, i = 0;
        while (i < n - parked) {
            if (nums[i] == 0) {
                for (int j = i; j < n - 1; j++) nums[j] = nums[j + 1];   // slide the zero all the way down
                nums[n - 1] = 0;
                parked++;
            } else i++;
        }
    }
}
