import java.util.*;

class Solution {
    public void reverseChars(char[] s) {
        List<Character> reversed = new ArrayList<>();
        for (char c : s) reversed.add(0, c);          // each new letter goes in front of the ones before it
        for (int i = 0; i < s.length; i++) s[i] = reversed.get(i);
    }
}
