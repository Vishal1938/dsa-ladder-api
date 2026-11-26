import java.util.*;

class Solution {
    public boolean backspaceEqual(String a, String b) {
        int i = a.length() - 1, j = b.length() - 1;
        while (true) {
            i = settle(a, i);
            j = settle(b, j);
            if (i < 0 || j < 0) return i < 0 && j < 0;
            if (a.charAt(i) != b.charAt(j)) return false;
            i--;
            j--;
        }
    }

    /** Walks back to the next character that actually survives, or past the start. */
    private int settle(String s, int at) {
        int owed = 0;
        while (at >= 0) {
            if (s.charAt(at) == '#') { owed++; at--; }
            else if (owed > 0) { owed--; at--; }
            else break;
        }
        return at;
    }
}
