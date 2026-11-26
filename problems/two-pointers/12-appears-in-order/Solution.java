import java.util.*;

class Solution {
    public boolean appearsInOrder(String text, String word) {
        int want = 0;
        for (int i = 0; i < text.length() && want < word.length(); i++)
            if (text.charAt(i) == word.charAt(want)) want++;
        return want == word.length();
    }
}
