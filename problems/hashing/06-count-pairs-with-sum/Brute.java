import java.util.*;

class Solution {
    public long countPairsWithSum(int[] nums, int target) {
        long pairs = 0;
        for (int i = 0; i < nums.length; i++)
            for (int j = i + 1; j < nums.length; j++)
                if ((long) nums[i] + nums[j] == target) pairs++;
        return pairs;
    }
}
