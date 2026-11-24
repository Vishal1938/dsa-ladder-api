import java.util.*;

class Solution {
    public int longestEvenVowels(String s) {
        int[] first = new int[32];
        Arrays.fill(first, -2);
        first[0] = -1;
        int mask = 0, best = 0;
        for (int i = 0; i < s.length(); i++) {
            int v = "aeiou".indexOf(s.charAt(i));
            if (v >= 0) mask ^= 1 << v;
            if (first[mask] == -2) first[mask] = i;
            else best = Math.max(best, i - first[mask]);
        }
        return best;
    }
}
