import java.util.*;

class Solution {
    public int majority(int[] nums) {
        int best = nums[0], bestCount = 0;
        for (int x : nums) {
            int times = 0;
            for (int y : nums) if (x == y) times++;
            if (times > bestCount) { bestCount = times; best = x; }
        }
        return best;
    }
}
