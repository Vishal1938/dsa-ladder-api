import java.util.*;

class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        int n = nums.length;
        int[] freq = new int[n];
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                if (nums[i] == nums[j]) freq[i]++;
        List<Integer> taken = new ArrayList<>();
        int[] top = new int[k];
        for (int r = 0; r < k; r++) {
            int best = -1;
            for (int i = 0; i < n; i++) {
                if (taken.contains(nums[i])) continue;
                if (best < 0 || freq[i] > freq[best] || (freq[i] == freq[best] && nums[i] < nums[best])) best = i;
            }
            top[r] = nums[best];
            taken.add(nums[best]);
        }
        return top;
    }
}
