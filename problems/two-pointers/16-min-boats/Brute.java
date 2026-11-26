import java.util.*;

class Solution {
    public int minBoats(int[] weights, int limit) {
        int n = weights.length, boats = 0, waiting = n;
        boolean[] gone = new boolean[n];
        while (waiting > 0) {
            int heaviest = -1;
            for (int i = 0; i < n; i++)
                if (!gone[i] && (heaviest < 0 || weights[i] > weights[heaviest])) heaviest = i;
            gone[heaviest] = true;
            waiting--;
            int mate = -1;                               // the lightest person who still fits
            for (int i = 0; i < n; i++)
                if (!gone[i] && weights[i] + weights[heaviest] <= limit
                        && (mate < 0 || weights[i] < weights[mate])) mate = i;
            if (mate >= 0) {
                gone[mate] = true;
                waiting--;
            }
            boats++;
        }
        return boats;
    }
}
