import java.util.*;

class Solution {
    public long trappedRain(int[] heights) {
        long water = 0;
        for (int i = 0; i < heights.length; i++) {
            int tallestLeft = 0, tallestRight = 0;
            for (int j = 0; j <= i; j++) tallestLeft = Math.max(tallestLeft, heights[j]);
            for (int j = i; j < heights.length; j++) tallestRight = Math.max(tallestRight, heights[j]);
            water += Math.min(tallestLeft, tallestRight) - heights[i];
        }
        return water;
    }
}
