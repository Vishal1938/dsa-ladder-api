import java.util.*;

class Solution {
    public long fourSumCount(int[] a, int[] b, int[] c, int[] d) {
        long tuples = 0;
        for (int w : a)
            for (int x : b)
                for (int y : c)
                    for (int z : d)
                        if ((long) w + x + y + z == 0) tuples++;
        return tuples;
    }
}
