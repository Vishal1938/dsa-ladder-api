import java.util.*;

class Solution {
    public long[] rangeSums(int[] nums, int[][] queries) {
        long[] a = new long[queries.length];
        for (int j = 0; j < queries.length; j++) for (int i = queries[j][0]; i <= queries[j][1]; i++) a[j] += nums[i];
        return a;
    }
}
