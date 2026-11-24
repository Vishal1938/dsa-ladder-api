import java.util.*;

class Solution {
    public int[] vowelCounts(String s, int[][] queries) {
        int[] a = new int[queries.length];
        for (int j = 0; j < queries.length; j++) for (int i = queries[j][0]; i <= queries[j][1]; i++) if ("aeiou".indexOf(s.charAt(i)) >= 0) a[j]++;
        return a;
    }
}
