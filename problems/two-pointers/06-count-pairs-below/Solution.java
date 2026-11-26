import java.util.*;

class Solution {
    public long countPairsBelow(int[] sorted, int target) {
        long pairs = 0;
        int left = 0, right = sorted.length - 1;
        while (left < right) {
            if ((long) sorted[left] + sorted[right] < target) {
                pairs += right - left;                // left pairs with everything up to right
                left++;
            } else right--;
        }
        return pairs;
    }
}
