import java.util.*;

class Solution {
    public long minStart(int[] changes) {
        long sum = 0, lowest = 0;
        for (int c : changes) {
            sum += c;
            lowest = Math.min(lowest, sum);
        }
        return 1 - lowest;
    }
}
