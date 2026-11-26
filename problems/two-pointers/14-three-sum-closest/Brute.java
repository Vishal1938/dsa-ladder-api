import java.util.*;

class Solution {
    public int threeSumClosest(int[] nums, int target) {
        int n = nums.length;
        int bestSum = nums[0] + nums[1] + nums[2];
        long bestGap = Math.abs((long) bestSum - target);
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++)
                for (int k = j + 1; k < n; k++) {
                    int sum = nums[i] + nums[j] + nums[k];
                    long gap = Math.abs((long) sum - target);
                    if (gap < bestGap || (gap == bestGap && sum < bestSum)) {
                        bestGap = gap;
                        bestSum = sum;
                    }
                }
        return bestSum;
    }
}
