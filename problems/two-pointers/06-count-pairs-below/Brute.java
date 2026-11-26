import java.util.*;

class Solution {
    public long countPairsBelow(int[] sorted, int target) {
        long pairs = 0;
        for (int i = 0; i < sorted.length; i++)
            for (int j = i + 1; j < sorted.length; j++)
                if ((long) sorted[i] + sorted[j] < target) pairs++;
        return pairs;
    }
}
