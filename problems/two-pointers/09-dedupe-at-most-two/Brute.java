import java.util.*;

class Solution {
    public int[] dedupeAtMostTwo(int[] sorted) {
        List<Integer> kept = new ArrayList<>();
        for (int x : sorted) {
            int times = 0;
            for (int y : kept) if (y == x) times++;    // how many copies have I kept already?
            if (times < 2) kept.add(x);
        }
        int[] out = new int[kept.size()];
        for (int i = 0; i < out.length; i++) out[i] = kept.get(i);
        return out;
    }
}
