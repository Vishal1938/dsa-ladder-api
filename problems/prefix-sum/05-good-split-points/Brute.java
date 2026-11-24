import java.util.*;

class Solution {
    public int countSplits(int[] nums) {
        int g = 0;
        for (int i = 0; i < nums.length - 1; i++) {
            long l = 0, r = 0;
            for (int j = 0; j <= i; j++) l += nums[j];
            for (int j = i + 1; j < nums.length; j++) r += nums[j];
            if (l >= r) g++;
        }
        return g;
    }
}
