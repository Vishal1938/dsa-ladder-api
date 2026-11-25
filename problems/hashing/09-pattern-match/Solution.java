import java.util.*;

class Solution {
    public boolean followsPattern(String pattern, String sentence) {
        String[] words = sentence.split(" ");
        if (words.length != pattern.length()) return false;
        Map<Character, String> forLetter = new HashMap<>();
        Map<String, Character> forWord = new HashMap<>();
        for (int i = 0; i < words.length; i++) {
            char c = pattern.charAt(i);
            String w = words[i];
            String boundWord = forLetter.putIfAbsent(c, w);
            if (boundWord != null && !boundWord.equals(w)) return false;
            Character boundLetter = forWord.putIfAbsent(w, c);
            if (boundLetter != null && boundLetter != c) return false;
        }
        return true;
    }
}
