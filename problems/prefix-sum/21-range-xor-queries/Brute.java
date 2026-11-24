import java.util.*;

class Solution {
    public int[] rangeXor(int[] nums, int[][] queries) {
        int[] a = new int[queries.length];
        for (int j = 0; j < queries.length; j++) for (int i = queries[j][0]; i <= queries[j][1]; i++) a[j] ^= nums[i];
        return a;
    }
}
