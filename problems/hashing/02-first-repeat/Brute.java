import java.util.*;

class Solution {
    public int firstRepeat(int[] nums) {
        for (int j = 0; j < nums.length; j++)
            for (int i = 0; i < j; i++)
                if (nums[i] == nums[j]) return nums[j];
        return -1;
    }
}
