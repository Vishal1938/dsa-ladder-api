import java.util.*;

class Solution {
    public List<List<Integer>> threeSumZero(int[] nums) {
        Set<List<Integer>> found = new LinkedHashSet<>();
        int n = nums.length;
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++)
                for (int k = j + 1; k < n; k++)
                    if (nums[i] + nums[j] + nums[k] == 0) {
                        List<Integer> triple = new ArrayList<>(List.of(nums[i], nums[j], nums[k]));
                        Collections.sort(triple);
                        found.add(triple);
                    }
        return new ArrayList<>(found);
    }
}
