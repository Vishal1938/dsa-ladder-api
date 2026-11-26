import java.util.*;

class Solution {
    public void sortColors(int[] nums) {
        int[] howMany = new int[3];
        for (int x : nums) howMany[x]++;
        int at = 0;
        for (int colour = 0; colour < 3; colour++)
            for (int t = 0; t < howMany[colour]; t++) nums[at++] = colour;
    }
}
