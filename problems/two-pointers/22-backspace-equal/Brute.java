import java.util.*;

class Solution {
    public boolean backspaceEqual(String a, String b) {
        return typed(a).equals(typed(b));
    }

    private String typed(String s) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '#') { if (sb.length() > 0) sb.deleteCharAt(sb.length() - 1); }
            else sb.append(c);
        }
        return sb.toString();
    }
}
