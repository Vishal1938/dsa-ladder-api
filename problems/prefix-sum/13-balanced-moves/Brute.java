import java.util.*;

class Solution {
    public int longestBalanced(String moves) {
        int b = 0;
        for (int i = 0; i < moves.length(); i++) { int s = 0; for (int j = i; j < moves.length(); j++) { s += moves.charAt(j) == 'R' ? 1 : -1; if (s == 0) b = Math.max(b, j - i + 1); } }
        return b;
    }
}
