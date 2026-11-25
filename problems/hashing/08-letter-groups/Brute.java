import java.util.*;

class Solution {
    public List<List<String>> groupAnagrams(String[] words) {
        List<List<String>> groups = new ArrayList<>();
        for (String w : words) {
            boolean placed = false;
            for (List<String> g : groups)
                if (same(g.get(0), w)) { g.add(w); placed = true; break; }
            if (!placed) {
                List<String> g = new ArrayList<>();
                g.add(w);
                groups.add(g);
            }
        }
        return groups;
    }

    private boolean same(String a, String b) {
        if (a.length() != b.length()) return false;
        char[] left = b.toCharArray();
        for (int i = 0; i < a.length(); i++) {
            int at = -1;
            for (int j = 0; j < left.length; j++) if (left[j] == a.charAt(i)) { at = j; break; }
            if (at < 0) return false;
            left[at] = ' ';
        }
        return true;
    }
}
