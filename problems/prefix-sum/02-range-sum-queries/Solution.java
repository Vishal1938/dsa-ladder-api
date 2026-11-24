import java.util.*;

class Solution {
    public long[] rangeSums(int[] nums, int[][] queries) {
        long[] prefix = new long[nums.length + 1];
        for (int i = 0; i < nums.length; i++) prefix[i + 1] = prefix[i] + nums[i];
        long[] answer = new long[queries.length];
        for (int j = 0; j < queries.length; j++) answer[j] = prefix[queries[j][1] + 1] - prefix[queries[j][0]];
        return answer;
    }
}
