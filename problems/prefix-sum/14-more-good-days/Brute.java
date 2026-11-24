import java.util.*;

class Solution {
    public int longestPositive(int[] scores) {
        int b = 0;
        for (int i = 0; i < scores.length; i++) { int s = 0; for (int j = i; j < scores.length; j++) { s += scores[j] >= 7 ? 1 : -1; if (s > 0) b = Math.max(b, j - i + 1); } }
        return b;
    }
}
