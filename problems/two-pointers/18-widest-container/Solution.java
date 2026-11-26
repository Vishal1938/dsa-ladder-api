import java.util.*;

class Solution {
    public long maxWater(int[] heights) {
        int left = 0, right = heights.length - 1;
        long best = 0;
        while (left < right) {
            long height = Math.min(heights[left], heights[right]);
            best = Math.max(best, height * (right - left));
            if (heights[left] < heights[right]) left++;
            else right--;
        }
        return best;
    }
}
