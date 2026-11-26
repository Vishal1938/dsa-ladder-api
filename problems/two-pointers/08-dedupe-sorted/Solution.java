import java.util.*;

class Solution {
    public int[] dedupeSorted(int[] sorted) {
        int write = 0;
        for (int read = 0; read < sorted.length; read++)
            if (write == 0 || sorted[read] != sorted[write - 1]) sorted[write++] = sorted[read];
        return Arrays.copyOf(sorted, write);
    }
}
