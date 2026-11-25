import java.util.*;

class Solution {
    public String frequencySort(String s) {
        int[] count = new int[26];
        for (int i = 0; i < s.length(); i++) count[s.charAt(i) - 'a']++;
        Integer[] letters = new Integer[26];
        for (int c = 0; c < 26; c++) letters[c] = c;
        Arrays.sort(letters, (p, q) -> count[p] != count[q] ? count[q] - count[p] : p - q);
        StringBuilder sb = new StringBuilder(s.length());
        for (int c : letters) for (int t = 0; t < count[c]; t++) sb.append((char) ('a' + c));
        return sb.toString();
    }
}
