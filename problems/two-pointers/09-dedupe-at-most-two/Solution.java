import java.util.*;

class Solution {
    public int[] dedupeAtMostTwo(int[] sorted) {
        int write = 0;
        for (int read = 0; read < sorted.length; read++)
            if (write < 2 || sorted[read] != sorted[write - 2]) sorted[write++] = sorted[read];
        return Arrays.copyOf(sorted, write);
    }
}
