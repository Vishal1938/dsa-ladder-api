import java.util.*;

class Solution {
    public long pairsDivisible(int[] nums, int m) {
        long pairs = 0;
        for (int i = 0; i < nums.length; i++)
            for (int j = i + 1; j < nums.length; j++)
                if (((long) nums[i] + nums[j]) % m == 0) pairs++;
        return pairs;
    }
}
