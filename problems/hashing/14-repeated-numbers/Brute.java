import java.util.*;

class Solution {
    public List<Integer> findRepeated(int[] nums) {
        List<Integer> repeated = new ArrayList<>();
        for (int v = 1; v <= nums.length; v++) {
            int times = 0;
            for (int x : nums) if (x == v) times++;
            if (times > 1) repeated.add(v);
        }
        return repeated;
    }
}
