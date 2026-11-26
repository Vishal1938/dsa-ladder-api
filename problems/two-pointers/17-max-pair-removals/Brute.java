import java.util.*;

class Solution {
    public int maxPairRemovals(int[] nums, int k) {
        int n = nums.length, discards = 0;
        boolean[] gone = new boolean[n];
        while (true) {
            int a = -1, b = -1;
            for (int i = 0; i < n && a < 0; i++) {
                if (gone[i]) continue;
                for (int j = i + 1; j < n; j++)
                    if (!gone[j] && (long) nums[i] + nums[j] == k) { a = i; b = j; break; }
            }
            if (a < 0) return discards;                  // no pair left anywhere
            gone[a] = true;
            gone[b] = true;
            discards++;
        }
    }
}
