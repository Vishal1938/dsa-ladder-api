import java.util.*;

class Solution {
    public long countSteadyPairs(int[] nums) {
        long pairs = 0;
        for (int i = 0; i < nums.length; i++)
            for (int j = i + 1; j < nums.length; j++)
                if ((long) nums[j] - nums[i] == j - i) pairs++;
        return pairs;
    }
}
