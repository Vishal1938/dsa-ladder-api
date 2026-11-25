import java.util.*;

class Solution {
    public String frequencySort(String s) {
        char[] cs = s.toCharArray();
        int[] freq = new int[cs.length];
        for (int i = 0; i < cs.length; i++)
            for (int j = 0; j < cs.length; j++)
                if (cs[i] == cs[j]) freq[i]++;
        StringBuilder sb = new StringBuilder();
        Set<Character> done = new HashSet<>();
        while (true) {
            int best = -1;
            for (int i = 0; i < cs.length; i++) {
                if (done.contains(cs[i])) continue;
                if (best < 0 || freq[i] > freq[best] || (freq[i] == freq[best] && cs[i] < cs[best])) best = i;
            }
            if (best < 0) break;
            for (int t = 0; t < freq[best]; t++) sb.append(cs[best]);
            done.add(cs[best]);
        }
        return sb.toString();
    }
}
