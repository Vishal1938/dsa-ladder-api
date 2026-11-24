import java.util.*;

class Solution {
    public int longestBalanced(String moves) {
        Map<Integer, Integer> first = new HashMap<>();
        first.put(0, -1);
        int pos = 0, best = 0;
        for (int i = 0; i < moves.length(); i++) {
            pos += moves.charAt(i) == 'R' ? 1 : -1;
            Integer j = first.get(pos);
            if (j != null) best = Math.max(best, i - j);
            else first.put(pos, i);
        }
        return best;
    }
}
