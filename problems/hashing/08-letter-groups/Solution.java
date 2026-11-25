import java.util.*;

class Solution {
    public List<List<String>> groupAnagrams(String[] words) {
        Map<String, List<String>> groups = new HashMap<>();
        for (String w : words) {
            char[] letters = w.toCharArray();
            Arrays.sort(letters);
            groups.computeIfAbsent(new String(letters), k -> new ArrayList<>()).add(w);
        }
        return new ArrayList<>(groups.values());
    }
}
