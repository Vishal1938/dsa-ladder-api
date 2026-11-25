import java.util.*;

class Solution {
    public int firstMissingPositive(int[] nums) {
        for (int v = 1; ; v++) {
            boolean found = false;
            for (int x : nums) if (x == v) found = true;
            if (!found) return v;
        }
    }
}
