import java.util.*;

class Solution {
    public int[] rangeXor(int[] nums, int[][] queries) {
        int[] px = new int[nums.length + 1];
        for (int i = 0; i < nums.length; i++) px[i + 1] = px[i] ^ nums[i];
        int[] ans = new int[queries.length];
        for (int j = 0; j < queries.length; j++) ans[j] = px[queries[j][1] + 1] ^ px[queries[j][0]];
        return ans;
    }
}
