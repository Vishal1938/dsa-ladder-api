import java.util.*;

class Solution {
    public int minBoats(int[] weights, int limit) {
        int[] a = weights.clone();
        Arrays.sort(a);
        int left = 0, right = a.length - 1, boats = 0;
        while (left <= right) {
            if (a[left] + a[right] <= limit) left++;      // the lightest rides along
            right--;
            boats++;
        }
        return boats;
    }
}
