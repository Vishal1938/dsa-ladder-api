import java.util.*;

class Solution {
    public int maxPairRemovals(int[] nums, int k) {
        int[] a = nums.clone();
        Arrays.sort(a);
        int left = 0, right = a.length - 1, discards = 0;
        while (left < right) {
            long sum = (long) a[left] + a[right];
            if (sum == k) {
                discards++;
                left++;
                right--;
            } else if (sum < k) left++;
            else right--;
        }
        return discards;
    }
}
