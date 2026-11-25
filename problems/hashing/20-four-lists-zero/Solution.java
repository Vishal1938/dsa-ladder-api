import java.util.*;

class Solution {
    public long fourSumCount(int[] a, int[] b, int[] c, int[] d) {
        Map<Integer, Integer> firstHalf = new HashMap<>();
        for (int x : a) for (int y : b) firstHalf.merge(x + y, 1, Integer::sum);
        long tuples = 0;
        for (int x : c) for (int y : d) tuples += firstHalf.getOrDefault(-(x + y), 0);
        return tuples;
    }
}
