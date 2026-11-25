import java.util.*;

class Solution {
    public boolean sameLetters(String a, String b) {
        if (a.length() != b.length()) return false;
        int[] diff = new int[26];
        for (int i = 0; i < a.length(); i++) {
            diff[a.charAt(i) - 'a']++;
            diff[b.charAt(i) - 'a']--;
        }
        for (int d : diff) if (d != 0) return false;
        return true;
    }
}
