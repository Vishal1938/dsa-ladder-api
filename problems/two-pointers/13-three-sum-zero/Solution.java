import java.util.*;

class Solution {
    public List<List<Integer>> threeSumZero(int[] nums) {
        int[] a = nums.clone();
        Arrays.sort(a);
        List<List<Integer>> out = new ArrayList<>();
        for (int i = 0; i < a.length - 2; i++) {
            if (i > 0 && a[i] == a[i - 1]) continue;              // same first number as last time
            int left = i + 1, right = a.length - 1;
            while (left < right) {
                int sum = a[i] + a[left] + a[right];
                if (sum < 0) left++;
                else if (sum > 0) right--;
                else {
                    out.add(List.of(a[i], a[left], a[right]));
                    left++;
                    right--;
                    while (left < right && a[left] == a[left - 1]) left++;
                    while (left < right && a[right] == a[right + 1]) right--;
                }
            }
        }
        return out;
    }
}
