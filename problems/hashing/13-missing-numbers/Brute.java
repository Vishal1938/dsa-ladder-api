import java.util.*;

class Solution {
    public List<Integer> findMissing(int[] nums) {
        List<Integer> missing = new ArrayList<>();
        for (int v = 1; v <= nums.length; v++) {
            boolean found = false;
            for (int x : nums) if (x == v) found = true;
            if (!found) missing.add(v);
        }
        return missing;
    }
}
