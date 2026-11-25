import java.util.*;

class Solution {
    public int[] pairWithSum(int[] nums, int target) {
        for (int j = 0; j < nums.length; j++)
            for (int i = 0; i < j; i++)
                if ((long) nums[i] + nums[j] == target) return new int[]{i, j};
        return new int[]{-1, -1};
    }
}
