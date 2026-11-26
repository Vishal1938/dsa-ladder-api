import java.util.*;

class Solution {
    public boolean appearsInOrder(String text, String word) {
        int at = -1;
        for (int k = 0; k < word.length(); k++) {
            at = text.indexOf(word.charAt(k), at + 1);   // leftmost match after the previous one
            if (at < 0) return false;
        }
        return true;
    }
}
