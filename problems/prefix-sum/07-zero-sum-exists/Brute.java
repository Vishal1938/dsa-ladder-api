import java.util.*;

class Solution {
    public boolean hasZeroSum(int[] nums) {
        for (int i = 0; i < nums.length; i++) { long s = 0; for (int j = i; j < nums.length; j++) { s += nums[j]; if (s == 0) return true; } }
        return false;
    }
}
