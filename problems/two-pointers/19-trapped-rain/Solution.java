import java.util.*;

class Solution {
    public long trappedRain(int[] heights) {
        int left = 0, right = heights.length - 1, maxLeft = 0, maxRight = 0;
        long water = 0;
        while (left < right) {
            if (heights[left] < heights[right]) {
                maxLeft = Math.max(maxLeft, heights[left]);
                water += maxLeft - heights[left];
                left++;
            } else {
                maxRight = Math.max(maxRight, heights[right]);
                water += maxRight - heights[right];
                right--;
            }
        }
        return water;
    }
}
