import java.util.*;

class Solution {
    public int[] removeValue(int[] nums, int val) {
        int write = 0;
        for (int read = 0; read < nums.length; read++)
            if (nums[read] != val) nums[write++] = nums[read];
        return Arrays.copyOf(nums, write);
    }
}
