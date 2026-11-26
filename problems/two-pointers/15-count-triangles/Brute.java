import java.util.*;

class Solution {
    public long countTriangles(int[] sides) {
        long count = 0;
        int n = sides.length;
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++)
                for (int k = j + 1; k < n; k++) {
                    long x = sides[i], y = sides[j], z = sides[k];
                    if (x + y > z && x + z > y && y + z > x) count++;
                }
        return count;
    }
}
