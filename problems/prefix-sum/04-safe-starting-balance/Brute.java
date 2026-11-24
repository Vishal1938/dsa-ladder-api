import java.util.*;

class Solution {
    public long minStart(int[] changes) {
        for (long x = 1; ; x++) {
            long b = x; boolean ok = true;
            for (int c : changes) { b += c; if (b < 1) { ok = false; break; } }
            if (ok) return x;
        }
    }
}
