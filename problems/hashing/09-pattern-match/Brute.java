import java.util.*;

class Solution {
    public boolean followsPattern(String pattern, String sentence) {
        String[] words = sentence.split(" ");
        boolean ok = words.length == pattern.length();
        if (ok)
            for (int i = 0; i < pattern.length(); i++)
                for (int j = i + 1; j < pattern.length(); j++)
                    // same letter <=> same word, checked for every pair of positions
                    if ((pattern.charAt(i) == pattern.charAt(j)) != words[i].equals(words[j])) ok = false;
        return ok;
    }
}
