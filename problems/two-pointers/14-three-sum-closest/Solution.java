import java.util.*;

class Solution {
    public int threeSumClosest(int[] nums, int target) {
        int[] a = nums.clone();
        Arrays.sort(a);
        int bestSum = a[0] + a[1] + a[2];
        long bestGap = Math.abs((long) bestSum - target);
        for (int i = 0; i < a.length - 2; i++) {
            int left = i + 1, right = a.length - 1;
            while (left < right) {
                int sum = a[i] + a[left] + a[right];
                long gap = Math.abs((long) sum - target);
                if (gap < bestGap || (gap == bestGap && sum < bestSum)) {
                    bestGap = gap;
                    bestSum = sum;
                }
                if (sum == target) return sum;                   // nothing can be closer
                if (sum < target) left++;
                else right--;
            }
        }
        return bestSum;
    }
}
