import java.util.*;

class Solution {
    public int[] dedupeSorted(int[] sorted) {
        int n = sorted.length, i = 1;
        while (i < n) {
            if (sorted[i] == sorted[i - 1]) {
                for (int j = i; j < n - 1; j++) sorted[j] = sorted[j + 1];   // delete the repeat, close the gap
                n--;
            } else i++;
        }
        return Arrays.copyOf(sorted, n);
    }
}
