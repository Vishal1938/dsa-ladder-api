import java.util.*;

class Solution {
    public int firstRepeat(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        for (int x : nums) if (!seen.add(x)) return x;
        return -1;
    }
}
