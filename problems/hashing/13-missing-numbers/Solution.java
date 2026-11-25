import java.util.*;

class Solution {
    public List<Integer> findMissing(int[] nums) {
        for (int x : nums) {
            int slot = Math.abs(x) - 1;                 // the array itself records "value slot+1 showed up"
            if (nums[slot] > 0) nums[slot] = -nums[slot];
        }
        List<Integer> missing = new ArrayList<>();
        for (int i = 0; i < nums.length; i++) if (nums[i] > 0) missing.add(i + 1);
        return missing;
    }
}
