import java.util.*;

class Solution {
    public int[] sortedSquares(int[] nums) {
        int n = nums.length;
        int[] squares = new int[n];
        for (int i = 0; i < n; i++) squares[i] = nums[i] * nums[i];
        boolean[] used = new boolean[n];
        int[] out = new int[n];
        for (int slot = 0; slot < n; slot++) {        // selection sort: smallest unused square each time
            int best = -1;
            for (int i = 0; i < n; i++) if (!used[i] && (best < 0 || squares[i] < squares[best])) best = i;
            used[best] = true;
            out[slot] = squares[best];
        }
        return out;
    }
}
