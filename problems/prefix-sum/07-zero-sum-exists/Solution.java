import java.util.*;

class Solution {
    public boolean hasZeroSum(int[] nums) {
        Set<Long> seen = new HashSet<>();
        seen.add(0L);
        long prefix = 0;
        for (int x : nums) {
            prefix += x;
            if (!seen.add(prefix)) return true;
        }
        return false;
    }
}
