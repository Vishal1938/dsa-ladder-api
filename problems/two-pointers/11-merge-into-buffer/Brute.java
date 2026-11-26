import java.util.*;

class Solution {
    public void mergeInto(int[] a, int m, int[] b) {
        int filled = m;
        for (int x : b) {
            int at = filled;
            while (at > 0 && a[at - 1] > x) {         // make room by shifting the bigger values up
                a[at] = a[at - 1];
                at--;
            }
            a[at] = x;
            filled++;
        }
    }
}
