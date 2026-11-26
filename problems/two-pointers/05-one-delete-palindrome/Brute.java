import java.util.*;

class Solution {
    public boolean almostPalindrome(String s) {
        if (plain(s)) return true;
        for (int drop = 0; drop < s.length(); drop++) {
            StringBuilder sb = new StringBuilder(s);
            sb.deleteCharAt(drop);
            if (plain(sb.toString())) return true;
        }
        return false;
    }

    private boolean plain(String t) {
        for (int i = 0; i < t.length() / 2; i++)
            if (t.charAt(i) != t.charAt(t.length() - 1 - i)) return false;
        return true;
    }
}
