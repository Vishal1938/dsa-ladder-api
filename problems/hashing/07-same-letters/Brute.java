import java.util.*;

class Solution {
    public boolean sameLetters(String a, String b) {
        if (a.length() != b.length()) return false;
        char[] left = b.toCharArray();
        for (int i = 0; i < a.length(); i++) {
            int at = -1;
            for (int j = 0; j < left.length; j++) if (left[j] == a.charAt(i)) { at = j; break; }
            if (at < 0) return false;
            left[at] = ' ';                // cross this letter off
        }
        return true;
    }
}
