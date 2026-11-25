import java.util.*;

class Solution {
    public int maxPairSameDigitSum(int[] nums) {
        int[] best = new int[82];                       // 99999999 has the largest digit sum, 72
        Arrays.fill(best, -1);
        int prize = -1;
        for (int x : nums) {
            int s = 0;
            for (int t = x; t > 0; t /= 10) s += t % 10;
            if (best[s] >= 0) prize = Math.max(prize, best[s] + x);
            best[s] = Math.max(best[s], x);
        }
        return prize;
    }
}
