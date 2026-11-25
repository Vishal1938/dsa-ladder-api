import java.util.*;

class Solution {
    public int maxPairSameDigitSum(int[] nums) {
        int prize = -1;
        for (int i = 0; i < nums.length; i++)
            for (int j = i + 1; j < nums.length; j++)
                if (digitSum(nums[i]) == digitSum(nums[j])) prize = Math.max(prize, nums[i] + nums[j]);
        return prize;
    }

    private int digitSum(int x) {
        int s = 0;
        while (x > 0) { s += x % 10; x /= 10; }
        return s;
    }
}
