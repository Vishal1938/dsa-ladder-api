import java.util.*;

class Solution {
    public void mergeInto(int[] a, int m, int[] b) {
        int i = m - 1, j = b.length - 1, write = a.length - 1;
        while (j >= 0) {
            if (i >= 0 && a[i] > b[j]) a[write--] = a[i--];
            else a[write--] = b[j--];
        }
    }
}
