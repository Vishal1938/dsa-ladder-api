import java.util.*;

class Solution {
    public int[] vowelCounts(String s, int[][] queries) {
        int[] count = new int[s.length() + 1];
        for (int i = 0; i < s.length(); i++) count[i + 1] = count[i] + ("aeiou".indexOf(s.charAt(i)) >= 0 ? 1 : 0);
        int[] ans = new int[queries.length];
        for (int j = 0; j < queries.length; j++) ans[j] = count[queries[j][1] + 1] - count[queries[j][0]];
        return ans;
    }
}
