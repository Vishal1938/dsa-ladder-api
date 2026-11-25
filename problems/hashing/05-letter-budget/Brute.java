import java.util.*;

class Solution {
    public boolean canBuild(String note, String letters) {
        char[] bag = letters.toCharArray();
        for (int i = 0; i < note.length(); i++) {
            int at = -1;
            for (int j = 0; j < bag.length; j++) if (bag[j] == note.charAt(i)) { at = j; break; }
            if (at < 0) return false;
            bag[at] = ' ';                 // this magnet is used up
        }
        return true;
    }
}
