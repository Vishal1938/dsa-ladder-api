import java.util.*;

class Solution {
    public long maxWater(int[] heights) {
        long best = 0;
        for (int i = 0; i < heights.length; i++)
            for (int j = i + 1; j < heights.length; j++)
                best = Math.max(best, (long) Math.min(heights[i], heights[j]) * (j - i));
        return best;
    }
}
