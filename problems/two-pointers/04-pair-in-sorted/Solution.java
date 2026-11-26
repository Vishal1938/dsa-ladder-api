import java.util.*;

class Solution {
    public boolean hasPairWithSum(int[] sorted, int target) {
        int left = 0, right = sorted.length - 1;
        while (left < right) {
            long sum = (long) sorted[left] + sorted[right];
            if (sum == target) return true;
            if (sum < target) left++;
            else right--;
        }
        return false;
    }
}
