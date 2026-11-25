import java.util.*;

class Solution {
    public int[] pairWithSum(int[] nums, int target) {
        Map<Integer, Integer> firstIndex = new HashMap<>();
        for (int j = 0; j < nums.length; j++) {
            Integer i = firstIndex.get(target - nums[j]);
            if (i != null) return new int[]{i, j};
            firstIndex.putIfAbsent(nums[j], j);
        }
        return new int[]{-1, -1};
    }
}
