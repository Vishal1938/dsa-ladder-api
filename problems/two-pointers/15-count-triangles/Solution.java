import java.util.*;

class Solution {
    public long countTriangles(int[] sides) {
        int[] a = sides.clone();
        Arrays.sort(a);
        long count = 0;
        for (int longest = a.length - 1; longest >= 2; longest--) {
            int left = 0, right = longest - 1;
            while (left < right) {
                if ((long) a[left] + a[right] > a[longest]) {
                    count += right - left;               // a[left] works with everything up to a[right]
                    right--;
                } else left++;
            }
        }
        return count;
    }
}
