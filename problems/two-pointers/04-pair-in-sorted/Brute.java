import java.util.*;

class Solution {
    public boolean hasPairWithSum(int[] sorted, int target) {
        boolean found = false;
        for (int i = 0; i < sorted.length; i++)
            for (int j = i + 1; j < sorted.length; j++)
                if ((long) sorted[i] + sorted[j] == target) found = true;
        return found;
    }
}
