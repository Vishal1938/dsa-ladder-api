import java.util.*;

class Solution {
    public int longestEvenVowels(String s) {
        int b = 0;
        for (int i = 0; i < s.length(); i++) { int m = 0; for (int j = i; j < s.length(); j++) { int v = "aeiou".indexOf(s.charAt(j)); if (v >= 0) m ^= 1 << v; if (m == 0) b = Math.max(b, j - i + 1); } }
        return b;
    }
}
