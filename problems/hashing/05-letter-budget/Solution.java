import java.util.*;

class Solution {
    public boolean canBuild(String note, String letters) {
        int[] have = new int[26];
        for (int i = 0; i < letters.length(); i++) have[letters.charAt(i) - 'a']++;
        for (int i = 0; i < note.length(); i++) if (--have[note.charAt(i) - 'a'] < 0) return false;
        return true;
    }
}
