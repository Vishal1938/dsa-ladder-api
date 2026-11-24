"""Authoring source for the Prefix Sums problem book.
Run:  python3 tools/book_prefix_sum.py   → writes problems/prefix-sum/NN-slug/{problem.json,statement.md,Solution.java,Brute.java,tests.json}
Every problem has a reference solution AND a brute-force solution; `JudgeCli crosscheck` compares them on random inputs.
"""
import json, os, textwrap

ROOT = os.path.join(os.path.dirname(__file__), "..", "problems", "prefix-sum")
P = []

def prob(**k):
    P.append(k)

def fn(name, returns, *params):
    return {"name": name, "returns": returns, "params": [{"name": n, "type": t} for t, n in params]}

def arr(n, lo, hi, kind="intArray"):
    return {"kind": kind, "n": n, "min": lo, "max": hi}

def arrr(nmin, nmax, lo, hi):
    return {"kind": "intArray", "nMin": nmin, "nMax": nmax, "min": lo, "max": hi}

def I(lo, hi):
    return {"kind": "int", "min": lo, "max": hi}

# ============================== Stage 1: prefix arrays ==============================
prob(slug="running-total", stage=0, title="Running Total", difficulty="Easy",
 whats="The base idea: each total is the previous total plus one number.",
 f=fn("runningTotal", "long[]", ("int[]", "nums")),
 statement="""
A shop records its sales for each day in `nums`. The manager wants a **running total**: for every day `i`, the total of all sales from day `0` up to and including day `i`.

Return an array `total` where `total[i] = nums[0] + nums[1] + … + nums[i]`.
""", constraints=["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4"],
 hints=["If you already know the total of the first i numbers, how much work is the total of the first i + 1?",
        "total[i] = total[i − 1] + nums[i]. Use a long so large sums can't overflow."],
 trigger="“Total so far” at every position → one pass, carry the running sum.",
 examples=[([[3,1,4,1,5]],[3,4,8,9,14],"3, then 3+1, then 3+1+4, and so on."),([[5,-2,-3]],[5,3,0],"")],
 tests=[[[7]],[[-1,-1,-1,-1]],[[10000,10000,10000]]],
 gen=[{"seed":11,"count":4,"args":[arr(100000,-10000,10000)]}],
 cross=[{"seed":1,"count":200,"args":[arrr(1,12,-20,20)]}],
 ref="""
    public long[] runningTotal(int[] nums) {
        long[] total = new long[nums.length];
        long sum = 0;
        for (int i = 0; i < nums.length; i++) {
            sum += nums[i];
            total[i] = sum;
        }
        return total;
    }""",
 brute="""
    public long[] runningTotal(int[] nums) {
        long[] t = new long[nums.length];
        for (int i = 0; i < nums.length; i++) for (int j = 0; j <= i; j++) t[i] += nums[j];
        return t;
    }""")

prob(slug="range-sum-queries", stage=0, title="Range Sum Queries", difficulty="Easy",
 whats="Many questions about the same array: pay once to build prefix sums, then answer each question in O(1).",
 f=fn("rangeSums", "long[]", ("int[]", "nums"), ("int[][]", "queries")),
 statement="""
You are given an array `nums` and a list of questions. Each question `queries[j] = [l, r]` asks for the sum of `nums[l] + nums[l+1] + … + nums[r]` (both ends included).

Return an array `answer` where `answer[j]` is the answer to question `j`.

There can be as many questions as numbers, so adding up each range one by one is too slow.
""", constraints=["1 <= nums.length <= 10^5", "1 <= queries.length <= 10^5", "-10^4 <= nums[i] <= 10^4", "0 <= l <= r < nums.length"],
 hints=["Adding each range costs up to n steps per question. What could you compute once, before reading any question?",
        "If prefix[i] is the sum of the first i numbers, how do you get the sum of nums[l..r] from two prefix values?",
        "Make prefix one longer than nums with prefix[0] = 0. Then sum(l..r) = prefix[r + 1] − prefix[l]."],
 trigger="Many range-sum questions on a fixed array → build prefix sums once.",
 examples=[([[2,-1,3,5,-2],[[0,2],[1,3],[4,4]]],[4,7,-2],"2 + (−1) + 3 = 4; (−1) + 3 + 5 = 7; just nums[4] = −2."),
           ([[10,20],[[0,1]]],[30],"")],
 tests=[[[5],[[0,0]]],[[1,2,3,4],[[0,3],[3,3],[1,2],[0,0]]]],
 gen=[{"seed":21,"count":1,"args":[arr(100000,-10000,10000),{"kind":"ranges","q":100000,"of":0}]},{"seed":22,"count":2,"args":[arr(100000,-10000,10000),{"kind":"ranges","q":100000,"of":0,"wide":True}]}],
 cross=[{"seed":2,"count":200,"args":[arrr(1,10,-9,9),{"kind":"ranges","q":5,"of":0}]}],
 ref="""
    public long[] rangeSums(int[] nums, int[][] queries) {
        long[] prefix = new long[nums.length + 1];
        for (int i = 0; i < nums.length; i++) prefix[i + 1] = prefix[i] + nums[i];
        long[] answer = new long[queries.length];
        for (int j = 0; j < queries.length; j++) answer[j] = prefix[queries[j][1] + 1] - prefix[queries[j][0]];
        return answer;
    }""",
 brute="""
    public long[] rangeSums(int[] nums, int[][] queries) {
        long[] a = new long[queries.length];
        for (int j = 0; j < queries.length; j++) for (int i = queries[j][0]; i <= queries[j][1]; i++) a[j] += nums[i];
        return a;
    }""")

prob(slug="balance-point", stage=0, title="Balance Point", difficulty="Easy",
 whats="Left sum comes from the running prefix; right sum = total − left − current. No second pass needed.",
 f=fn("balancePoint", "int", ("int[]", "nums")),
 statement="""
A plank has weights `nums` placed along it. Index `i` is a **balance point** if the sum of all weights strictly to the left of `i` equals the sum of all weights strictly to the right of `i`. (An empty side has sum 0.)

Return the **smallest** balance point, or `-1` if there is none.
""", constraints=["1 <= nums.length <= 10^5", "-1000 <= nums[i] <= 1000"],
 hints=["For each i you need two numbers: the sum on the left and the sum on the right. Which one can you keep updating as you walk?",
        "If you know the total of the whole array, can you get the right side from the left side?",
        "right = total − left − nums[i]. Check left == right, then add nums[i] to left."],
 trigger="Compare left part with right part at every index → total + running prefix.",
 examples=[([[2,3,-1,8,4]],3,"Left of index 3: 2 + 3 − 1 = 4. Right: 4."),([[1,2,3]],-1,""),([[2,1,-1]],0,"Left of index 0 is empty (0); right is 1 + (−1) = 0.")],
 tests=[[[0]],[[5]],[[0,0,0]],[[-1,-1,0,1,1,0]]],
 gen=[{"seed":31,"count":2,"args":[arr(100000,-3,3)]},{"seed":33,"count":3,"args":[arr(100000,1,1000)]},{"seed":32,"count":1,"args":[arr(100000,-1000,1000)]}],
 cross=[{"seed":3,"count":300,"args":[arrr(1,8,-3,3)]}],
 ref="""
    public int balancePoint(int[] nums) {
        long total = 0;
        for (int x : nums) total += x;
        long left = 0;
        for (int i = 0; i < nums.length; i++) {
            if (left == total - left - nums[i]) return i;
            left += nums[i];
        }
        return -1;
    }""",
 brute="""
    public int balancePoint(int[] nums) {
        for (int i = 0; i < nums.length; i++) {
            long l = 0, r = 0;
            for (int j = 0; j < i; j++) l += nums[j];
            for (int j = i + 1; j < nums.length; j++) r += nums[j];
            if (l == r) return i;
        }
        return -1;
    }""")

prob(slug="safe-starting-balance", stage=0, title="Safe Starting Balance", difficulty="Easy",
 whats="The answer depends only on the lowest point the running sum ever reaches.",
 f=fn("minStart", "long", ("int[]", "changes")),
 statement="""
You start with `x` coins, where `x` is a positive whole number. Then `changes[0], changes[1], …` are applied one after another (positive means you gain coins, negative means you lose them).

After **every** change your balance must be at least `1`.

Return the smallest starting amount `x >= 1` that keeps you safe the whole way.
""", constraints=["1 <= changes.length <= 10^5", "-10^4 <= changes[i] <= 10^4"],
 hints=["After k changes your balance is x + (sum of the first k changes). When is that most at risk?",
        "Only the minimum running sum matters. Call it m. What does x need to be so that x + m >= 1?",
        "x = max(1, 1 − m), where m is the smallest running sum (if every running sum is positive, x = 1)."],
 trigger="“Never drop below a level” → look at the minimum of the running sum.",
 examples=[([[-2,4,-5,1]],4,"Running sums: −2, 2, −3, −2. The lowest is −3, so you need 4 to stay at 1 or above."),([[1,2]],1,""),([[1,-2,-3]],5,"")],
 tests=[[[5]],[[-1]],[[-10000,-10000,-10000]]],
 gen=[{"seed":41,"count":2,"args":[arr(100000,-10000,10000)]}],
 cross=[{"seed":4,"count":300,"args":[arrr(1,8,-6,6)]}],
 ref="""
    public long minStart(int[] changes) {
        long sum = 0, lowest = 0;
        for (int c : changes) {
            sum += c;
            lowest = Math.min(lowest, sum);
        }
        return 1 - lowest;
    }""",
 brute="""
    public long minStart(int[] changes) {
        for (long x = 1; ; x++) {
            long b = x; boolean ok = true;
            for (int c : changes) { b += c; if (b < 1) { ok = false; break; } }
            if (ok) return x;
        }
    }""")

prob(slug="good-split-points", stage=0, title="Good Split Points", difficulty="Easy",
 whats="Every split needs a left sum and a right sum; both come from one running prefix and the total.",
 f=fn("countSplits", "int", ("int[]", "nums")),
 statement="""
You may cut `nums` into a non-empty left part `nums[0..i]` and a non-empty right part `nums[i+1..n-1]`.

A cut is **good** if the sum of the left part is **greater than or equal to** the sum of the right part.

Return how many of the `n − 1` possible cuts are good.
""", constraints=["2 <= nums.length <= 10^5", "-10^5 <= nums[i] <= 10^5"],
 hints=["There are n − 1 cuts. For each you need the left sum and the right sum. Can you avoid re-adding everything for every cut?",
        "Walk left to right keeping left = sum of nums[0..i]. The right sum is total − left.",
        "Sums can reach 10^10, so use long."],
 trigger="Compare prefix vs suffix at every cut → running prefix + total.",
 examples=[([[1,4,-2,6]],1,"Only the cut after index 1 works: 1 + 4 = 5 ≥ −2 + 6 = 4."),([[2,3,1,0]],2,"")],
 tests=[[[1,1]],[[0,0]],[[-5,5]],[[100000,100000,-100000]]],
 gen=[{"seed":51,"count":5,"args":[arr(100000,-100000,100000)]}],
 cross=[{"seed":5,"count":300,"args":[arrr(2,9,-5,5)]}],
 ref="""
    public int countSplits(int[] nums) {
        long total = 0;
        for (int x : nums) total += x;
        long left = 0;
        int good = 0;
        for (int i = 0; i < nums.length - 1; i++) {
            left += nums[i];
            if (left >= total - left) good++;
        }
        return good;
    }""",
 brute="""
    public int countSplits(int[] nums) {
        int g = 0;
        for (int i = 0; i < nums.length - 1; i++) {
            long l = 0, r = 0;
            for (int j = 0; j <= i; j++) l += nums[j];
            for (int j = i + 1; j < nums.length; j++) r += nums[j];
            if (l >= r) g++;
        }
        return g;
    }""")

prob(slug="best-k-window", stage=0, title="Best Window of Length k", difficulty="Easy",
 whats="A window sum is just prefix[i + k] − prefix[i], the range-sum trick applied to every window.",
 f=fn("bestWindow", "long", ("int[]", "nums"), ("int", "k")),
 statement="""
Return the largest possible sum of `k` **consecutive** elements of `nums`.
""", constraints=["1 <= k <= nums.length <= 2 * 10^5", "-10^4 <= nums[i] <= 10^4"],
 hints=["Every window is a range [i, i + k − 1]. Which formula from Range Sum Queries gives a range sum in O(1)?",
        "With prefix sums the window starting at i has sum prefix[i + k] − prefix[i]. Try every i."],
 trigger="Sums of all windows of a fixed length → prefix differences (or slide the window).",
 examples=[([[4,-1,3,-7,8,2],3],6,"4 − 1 + 3 = 6."),([[-3,-1,-2],2],-3,"Every window is negative; the best is −1 + (−2) = −3.")],
 tests=[[[5],1],[[1,2,3],3],[[-1,-1,-1,-1],1]],
 gen=[{"seed":61,"count":1,"args":[arr(100000,-10000,10000),I(1,100000)]},{"seed":62,"count":4,"args":[arr(200000,-10000,10000),I(80000,120000)]}],
 cross=[{"seed":6,"count":300,"args":[arrr(6,10,-9,9),I(1,6)]}],
 ref="""
    public long bestWindow(int[] nums, int k) {
        long[] prefix = new long[nums.length + 1];
        for (int i = 0; i < nums.length; i++) prefix[i + 1] = prefix[i] + nums[i];
        long best = Long.MIN_VALUE;
        for (int i = 0; i + k <= nums.length; i++) best = Math.max(best, prefix[i + k] - prefix[i]);
        return best;
    }""",
 brute="""
    public long bestWindow(int[] nums, int k) {
        long best = Long.MIN_VALUE;
        for (int i = 0; i + k <= nums.length; i++) { long s = 0; for (int j = i; j < i + k; j++) s += nums[j]; best = Math.max(best, s); }
        return best;
    }""")

# ============================== Stage 2: prefix + hashmap ==============================
prob(slug="zero-sum-exists", stage=1, title="Does a Zero-Sum Stretch Exist?", difficulty="Easy",
 whats="New idea: two equal prefix sums mean the numbers between them add up to 0. A set remembers the prefixes you've seen.",
 f=fn("hasZeroSum", "boolean", ("int[]", "nums")),
 statement="""
Return `true` if some **non-empty contiguous** part of `nums` adds up to exactly `0`, otherwise `false`.
""", constraints=["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4"],
 hints=["Write prefix sums for [4, 2, −3, 1, 6]: 0, 4, 6, 3, 4, 10. Do you notice a repeated value? What does the repeat mean?",
        "If prefix[i] == prefix[j] (i < j), then nums[i..j−1] sums to 0.",
        "Keep a HashSet of prefix sums seen so far, starting with 0. A repeat means yes."],
 trigger="“Some subarray sums to 0” → a repeated prefix sum (HashSet).",
 examples=[([[4,2,-3,1,6]],True,"2 + (−3) + 1 = 0."),([[1,2,3]],False,""),([[0]],True,"The single element 0 counts.")],
 tests=[[[5]],[[-5,5]],[[1,-1,1]],[[3,4,-7,1]]],
 gen=[{"seed":71,"count":3,"args":[arr(100000,1,10000)]},{"seed":72,"count":2,"args":[arr(100000,-10000,10000)]}],
 cross=[{"seed":7,"count":400,"args":[arrr(1,7,-4,4)]}],
 ref="""
    public boolean hasZeroSum(int[] nums) {
        Set<Long> seen = new HashSet<>();
        seen.add(0L);
        long prefix = 0;
        for (int x : nums) {
            prefix += x;
            if (!seen.add(prefix)) return true;
        }
        return false;
    }""",
 brute="""
    public boolean hasZeroSum(int[] nums) {
        for (int i = 0; i < nums.length; i++) { long s = 0; for (int j = i; j < nums.length; j++) { s += nums[j]; if (s == 0) return true; } }
        return false;
    }""")

prob(slug="count-zero-sum", stage=1, title="Count Zero-Sum Stretches", difficulty="Medium",
 whats="From “does one exist?” to “how many?”: replace the set with a map of counts.",
 f=fn("countZeroSum", "long", ("int[]", "nums")),
 statement="""
Return the **number** of non-empty contiguous subarrays of `nums` whose sum is exactly `0`.
""", constraints=["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4"],
 hints=["In the previous problem one repeat was enough. Now, if the current prefix value has appeared 3 times before, how many zero-sum subarrays end here?",
        "Keep a HashMap from prefix value to how many times you've seen it. Start with {0: 1}.",
        "For each new prefix p: add count[p] to the answer, then increment count[p]. Use long for the answer."],
 trigger="Count subarrays with sum 0 → HashMap of prefix counts, seed {0:1}.",
 examples=[([[1,-1,1,-1]],4,"[1,−1], [−1,1], [1,−1] (second one) and the whole array."),([[0,0,0]],6,"Every non-empty subarray sums to 0: 3 + 2 + 1.")],
 tests=[[[5]],[[0]],[[2,-2,2,-2,2]]],
 gen=[{"seed":81,"count":1,"args":[arr(100000,-2,2)]},{"seed":82,"count":1,"args":[arr(100000,0,0)]},{"seed":83,"count":1,"args":[arr(100000,-10000,10000)]}],
 cross=[{"seed":8,"count":400,"args":[arrr(1,9,-3,3)]}],
 ref="""
    public long countZeroSum(int[] nums) {
        Map<Long, Integer> count = new HashMap<>();
        count.put(0L, 1);
        long prefix = 0, answer = 0;
        for (int x : nums) {
            prefix += x;
            int c = count.getOrDefault(prefix, 0);
            answer += c;
            count.put(prefix, c + 1);
        }
        return answer;
    }""",
 brute="""
    public long countZeroSum(int[] nums) {
        long c = 0;
        for (int i = 0; i < nums.length; i++) { long s = 0; for (int j = i; j < nums.length; j++) { s += nums[j]; if (s == 0) c++; } }
        return c;
    }""")

prob(slug="count-sum-k", stage=1, title="Count Subarrays With Sum k", difficulty="Medium",
 whats="Sum 0 was “find the same prefix”. Sum k is “find prefix − k”.",
 f=fn("countSumK", "long", ("int[]", "nums"), ("int", "k")),
 statement="""
Return the number of non-empty contiguous subarrays of `nums` whose sum equals `k`. The array may contain negative numbers.
""", constraints=["1 <= nums.length <= 10^5", "-1000 <= nums[i] <= 1000", "-10^6 <= k <= 10^6"],
 hints=["A subarray ending at j has sum prefix[j+1] − prefix[i]. When does that equal k?",
        "You need earlier prefixes equal to (current prefix − k). How do you count those quickly?",
        "Map of prefix counts seeded with {0:1}. For each prefix p: answer += count[p − k]; then count[p]++."],
 trigger="Count subarrays with sum k, negatives allowed → prefix + HashMap (look up prefix − k).",
 examples=[([[1,2,3,-3,3],3],5,"[1,2], [3], [1,2,3,−3], [3,−3,3] and the last [3]."),([[2,-1,1,2],2],4,"")],
 tests=[[[5],5],[[5],-5],[[0,0,0],0],[[-1,-1,1],0]],
 gen=[{"seed":91,"count":1,"args":[arr(100000,-1000,1000),I(-2000,2000)]},{"seed":92,"count":1,"args":[arr(100000,-1,1),I(-2,2)]}],
 cross=[{"seed":9,"count":400,"args":[arrr(1,9,-3,3),I(-4,4)]}],
 ref="""
    public long countSumK(int[] nums, int k) {
        Map<Long, Integer> count = new HashMap<>();
        count.put(0L, 1);
        long prefix = 0, answer = 0;
        for (int x : nums) {
            prefix += x;
            answer += count.getOrDefault(prefix - k, 0);
            count.merge(prefix, 1, Integer::sum);
        }
        return answer;
    }""",
 brute="""
    public long countSumK(int[] nums, int k) {
        long c = 0;
        for (int i = 0; i < nums.length; i++) { long s = 0; for (int j = i; j < nums.length; j++) { s += nums[j]; if (s == k) c++; } }
        return c;
    }""")

prob(slug="longest-sum-k", stage=1, title="Longest Subarray With Sum k", difficulty="Medium",
 whats="Counting needed how many times a prefix appeared. Longest needs where it appeared first.",
 f=fn("longestSumK", "int", ("int[]", "nums"), ("int", "k")),
 statement="""
Return the length of the **longest** contiguous subarray of `nums` whose sum equals `k`, or `0` if there is none.
""", constraints=["1 <= nums.length <= 10^5", "-1000 <= nums[i] <= 1000", "-10^6 <= k <= 10^6"],
 hints=["For a subarray ending at j to be as long as possible, which earlier prefix with value (prefix − k) do you want: the first one or the last one?",
        "Store the FIRST index at which each prefix value appears. Never overwrite it.",
        "Seed the map with {0: −1} so subarrays starting at index 0 work."],
 trigger="Longest subarray with sum k → map prefix → first index.",
 examples=[([[2,-1,2,1,-4,3],2],4,"[2, 1, −4, 3] sums to 2."),([[-1,3,-2],1],2,"[3, −2]."),([[1,2],5],0,"")],
 tests=[[[3],3],[[0,0,0],0],[[1,1,1],2],[[2,-2,2,-2],0]],
 gen=[{"seed":101,"count":1,"args":[arr(100000,-1000,1000),I(-1000,1000)]},{"seed":102,"count":1,"args":[arr(100000,-1,1),I(-3,3)]}],
 cross=[{"seed":10,"count":400,"args":[arrr(1,9,-3,3),I(-4,4)]}],
 ref="""
    public int longestSumK(int[] nums, int k) {
        Map<Long, Integer> first = new HashMap<>();
        first.put(0L, -1);
        long prefix = 0;
        int best = 0;
        for (int i = 0; i < nums.length; i++) {
            prefix += nums[i];
            Integer j = first.get(prefix - k);
            if (j != null) best = Math.max(best, i - j);
            first.putIfAbsent(prefix, i);
        }
        return best;
    }""",
 brute="""
    public int longestSumK(int[] nums, int k) {
        int b = 0;
        for (int i = 0; i < nums.length; i++) { long s = 0; for (int j = i; j < nums.length; j++) { s += nums[j]; if (s == k) b = Math.max(b, j - i + 1); } }
        return b;
    }""")

prob(slug="even-sum-subarrays", stage=1, title="Even-Sum Subarrays", difficulty="Medium",
 whats="You don't need the exact prefix, only its parity. Two prefixes with the same parity give an even sum.",
 f=fn("countEvenSum", "long", ("int[]", "nums")),
 statement="""
Return the number of non-empty contiguous subarrays of `nums` whose sum is **even**.
""", constraints=["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4"],
 hints=["sum(i..j) = prefix[j+1] − prefix[i]. When is a difference of two numbers even?",
        "Only the parity of each prefix matters. Count how many prefixes so far were even and how many odd.",
        "Start with evenCount = 1 (the empty prefix). For each new prefix, add the count of earlier prefixes with the same parity."],
 trigger="Subarray sum divisible by 2 → count prefix parities.",
 examples=[([[1,2,3]],2,"[2] and [1,2,3] (sum 6)."),([[2,4]],3,"")],
 tests=[[[1]],[[2]],[[-1,-1]],[[1,1,1,1]]],
 gen=[{"seed":111,"count":2,"args":[arr(100000,-10000,10000)]}],
 cross=[{"seed":11,"count":300,"args":[arrr(1,9,-5,5)]}],
 ref="""
    public long countEvenSum(int[] nums) {
        long[] seen = {1, 0};          // seen[parity] = prefixes so far with that parity
        long prefix = 0, answer = 0;
        for (int x : nums) {
            prefix += x;
            int p = (int) Math.floorMod(prefix, 2L);
            answer += seen[p];
            seen[p]++;
        }
        return answer;
    }""",
 brute="""
    public long countEvenSum(int[] nums) {
        long c = 0;
        for (int i = 0; i < nums.length; i++) { long s = 0; for (int j = i; j < nums.length; j++) { s += nums[j]; if (s % 2 == 0) c++; } }
        return c;
    }""")

prob(slug="divisible-subarrays", stage=1, title="Subarrays Divisible by k", difficulty="Medium",
 whats="Parity was “mod 2”. Generalise to mod k, and handle negative remainders.",
 f=fn("countDivisible", "long", ("int[]", "nums"), ("int", "k")),
 statement="""
Return the number of non-empty contiguous subarrays of `nums` whose sum is divisible by `k`.
""", constraints=["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4", "2 <= k <= 10^4"],
 hints=["In Even-Sum Subarrays you matched prefixes with the same remainder mod 2. What changes for mod k?",
        "Two prefixes with the same remainder mod k give a sum divisible by k. Count remainders in an array of size k.",
        "In Java, −7 % 5 is −2. Use Math.floorMod(prefix, k) (or ((p % k) + k) % k) so negative prefixes land in 0..k−1."],
 trigger="Subarray sum divisible by k → count equal prefix remainders (fix negative mods).",
 examples=[([[3,2,-5,5,1],5],6,"For example [3,2], [−5], [5] and [3,2,−5,5]."),([[5],9],0,"")],
 tests=[[[-5],5],[[-1,2,9],2],[[0,0],3]],
 gen=[{"seed":121,"count":1,"args":[arr(100000,-10000,10000),I(2,10000)]},{"seed":122,"count":1,"args":[arr(100000,-10000,10000),I(2,7)]}],
 cross=[{"seed":12,"count":400,"args":[arrr(1,9,-9,9),I(2,6)]}],
 ref="""
    public long countDivisible(int[] nums, int k) {
        long[] seen = new long[k];
        seen[0] = 1;
        long prefix = 0, answer = 0;
        for (int x : nums) {
            prefix += x;
            int r = (int) Math.floorMod(prefix, (long) k);
            answer += seen[r];
            seen[r]++;
        }
        return answer;
    }""",
 brute="""
    public long countDivisible(int[] nums, int k) {
        long c = 0;
        for (int i = 0; i < nums.length; i++) { long s = 0; for (int j = i; j < nums.length; j++) { s += nums[j]; if (s % k == 0) c++; } }
        return c;
    }""")

prob(slug="balanced-moves", stage=1, title="Longest Balanced Walk", difficulty="Medium",
 whats="Transform first: turn L into −1 and R into +1. “Equal counts” becomes “sum 0”.",
 f=fn("longestBalanced", "int", ("String", "moves")),
 statement="""
A robot's moves are given as a string of `'L'` (left) and `'R'` (right) steps.

Find the longest contiguous stretch of moves after which the robot is back where that stretch began, that is, the stretch has **equally many** `'L'` and `'R'`. Return its length (`0` if none).
""", constraints=["1 <= moves.length <= 10^5", "moves consists only of 'L' and 'R'"],
 hints=["Can you turn “same number of L and R” into a statement about a sum?",
        "Let L = −1 and R = +1. A balanced stretch is a subarray with sum 0, which is Longest Subarray With Sum k with k = 0.",
        "Store the first index of each running position, seeded with {0: −1}."],
 trigger="Equal counts of two kinds → map them to −1/+1, look for sum 0.",
 examples=[(["RLRRLL"],6,"The whole walk ends where it started."),(["RRL"],2,"“RL”."),(["RRR"],0,"")],
 tests=[["L"],["LR"],["LLRRLR"],["RRRLLLL"]],
 gen=[{"seed":131,"count":2,"args":[{"kind":"string","n":100000,"alphabet":"LR"}]},{"seed":132,"count":1,"args":[{"kind":"string","n":100000,"alphabet":"LLLR"}]}],
 cross=[{"seed":13,"count":400,"args":[{"kind":"string","nMin":1,"nMax":10,"alphabet":"LR"}]}],
 ref="""
    public int longestBalanced(String moves) {
        Map<Integer, Integer> first = new HashMap<>();
        first.put(0, -1);
        int pos = 0, best = 0;
        for (int i = 0; i < moves.length(); i++) {
            pos += moves.charAt(i) == 'R' ? 1 : -1;
            Integer j = first.get(pos);
            if (j != null) best = Math.max(best, i - j);
            else first.put(pos, i);
        }
        return best;
    }""",
 brute="""
    public int longestBalanced(String moves) {
        int b = 0;
        for (int i = 0; i < moves.length(); i++) { int s = 0; for (int j = i; j < moves.length(); j++) { s += moves.charAt(j) == 'R' ? 1 : -1; if (s == 0) b = Math.max(b, j - i + 1); } }
        return b;
    }""")

prob(slug="more-good-days", stage=1, title="More Good Days Than Bad", difficulty="Hard",
 whats="Same ±1 transform, but now the sum must be positive. You only need to look one step down: prefix − 1.",
 f=fn("longestPositive", "int", ("int[]", "scores")),
 statement="""
`scores[i]` is your daily score from 0 to 10. A day is **good** if its score is `7` or more, otherwise it is **bad**.

Return the length of the longest stretch of consecutive days with **strictly more** good days than bad days (`0` if none).
""", constraints=["1 <= scores.length <= 10^5", "0 <= scores[i] <= 10"],
 hints=["Map good days to +1 and bad days to −1. What does “more good than bad” mean for the sum of a stretch?",
        "If the running sum p is positive, the whole prefix works. Otherwise, a stretch ending here works when an earlier prefix is smaller than p.",
        "Because the sum moves by ±1, the earliest prefix smaller than p is the first time it was p − 1. Store first indexes."],
 trigger="Longest subarray with positive ±1 sum → first index of prefix − 1.",
 examples=[([[8,2,9,9,1,0,7]],7,"The whole week: 4 good days, 3 bad."),([[6,6,6]],0,""),([[7,1,7]],3,"")],
 tests=[[[10]],[[0]],[[7,0]],[[0,7,7]],[[0,0,7,7,7,0,0,0,7]]],
 gen=[{"seed":141,"count":2,"args":[arr(100000,0,10)]},{"seed":142,"count":1,"args":[arr(100000,4,9)]}],
 cross=[{"seed":14,"count":400,"args":[arrr(1,10,3,10)]}],
 ref="""
    public int longestPositive(int[] scores) {
        Map<Integer, Integer> first = new HashMap<>();
        int sum = 0, best = 0;
        for (int i = 0; i < scores.length; i++) {
            sum += scores[i] >= 7 ? 1 : -1;
            if (sum > 0) best = i + 1;
            else {
                Integer j = first.get(sum - 1);
                if (j != null) best = Math.max(best, i - j);
            }
            first.putIfAbsent(sum, i);
        }
        return best;
    }""",
 brute="""
    public int longestPositive(int[] scores) {
        int b = 0;
        for (int i = 0; i < scores.length; i++) { int s = 0; for (int j = i; j < scores.length; j++) { s += scores[j] >= 7 ? 1 : -1; if (s > 0) b = Math.max(b, j - i + 1); } }
        return b;
    }""")

# ============================== Stage 3: 2D prefix ==============================
prob(slug="grid-region-sums", stage=2, title="Grid Region Sums", difficulty="Medium",
 whats="Range sums in 2D: P[r][c] covers the rectangle from the top-left corner. Combine four corners.",
 f=fn("regionSums", "long[]", ("int[][]", "grid"), ("int[][]", "queries")),
 statement="""
`grid` is a field of numbers. Each query `[r1, c1, r2, c2]` asks for the sum of the rectangle with top-left corner `(r1, c1)` and bottom-right corner `(r2, c2)`, both included.

Return the answers in order.
""", constraints=["1 <= rows, cols <= 300", "-1000 <= grid[r][c] <= 1000", "1 <= queries.length <= 10^5", "0 <= r1 <= r2 < rows, 0 <= c1 <= c2 < cols"],
 hints=["Let P[r][c] be the sum of everything above and to the left: rows 0..r−1 and columns 0..c−1. How do you build P from its neighbours?",
        "P[r+1][c+1] = grid[r][c] + P[r][c+1] + P[r+1][c] − P[r][c] (the overlap was added twice).",
        "Rectangle = P[r2+1][c2+1] − P[r1][c2+1] − P[r2+1][c1] + P[r1][c1]."],
 trigger="Many sub-rectangle sums → 2D prefix sums with inclusion–exclusion.",
 examples=[([[[1,2,3],[4,5,6],[7,8,9]],[[0,0,1,1],[1,1,2,2],[0,2,2,2]]],[12,28,18],"1+2+4+5 = 12; 5+6+8+9 = 28; 3+6+9 = 18.")],
 tests=[[[[5]],[[0,0,0,0]]],[[[1,-1],[-1,1]],[[0,0,1,1],[0,1,1,1],[1,0,1,0]]]],
 gen=[{"seed":151,"count":1,"args":[{"kind":"intMatrix","rows":300,"cols":300,"min":-1000,"max":1000},{"kind":"rects","q":100000,"of":0}]},{"seed":152,"count":2,"args":[{"kind":"intMatrix","rows":300,"cols":300,"min":-1000,"max":1000},{"kind":"rects","q":100000,"of":0,"wide":True}]}],
 cross=[{"seed":15,"count":200,"args":[{"kind":"intMatrix","rows":4,"cols":5,"min":-9,"max":9},{"kind":"rects","q":6,"of":0}]}],
 ref="""
    public long[] regionSums(int[][] grid, int[][] queries) {
        int R = grid.length, C = grid[0].length;
        long[][] P = new long[R + 1][C + 1];
        for (int r = 0; r < R; r++)
            for (int c = 0; c < C; c++)
                P[r + 1][c + 1] = grid[r][c] + P[r][c + 1] + P[r + 1][c] - P[r][c];
        long[] ans = new long[queries.length];
        for (int i = 0; i < queries.length; i++) {
            int r1 = queries[i][0], c1 = queries[i][1], r2 = queries[i][2], c2 = queries[i][3];
            ans[i] = P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1];
        }
        return ans;
    }""",
 brute="""
    public long[] regionSums(int[][] grid, int[][] queries) {
        long[] a = new long[queries.length];
        for (int i = 0; i < queries.length; i++) for (int r = queries[i][0]; r <= queries[i][2]; r++) for (int c = queries[i][1]; c <= queries[i][3]; c++) a[i] += grid[r][c];
        return a;
    }""")

prob(slug="neighbourhood-sums", stage=2, title="Neighbourhood Sums", difficulty="Medium",
 whats="Every cell asks one rectangle question. Clamp the rectangle to the grid, then reuse Grid Region Sums.",
 f=fn("neighbourhoodSum", "long[][]", ("int[][]", "grid"), ("int", "k")),
 statement="""
For every cell `(r, c)` compute the sum of all cells `(i, j)` with `|i − r| <= k` and `|j − c| <= k` that lie inside the grid.

Return a grid of the same size with these sums.
""", constraints=["1 <= rows, cols <= 200", "0 <= k <= 200", "0 <= grid[r][c] <= 1000"],
 hints=["Each output cell is a rectangle sum. Which rectangle, and what happens at the borders?",
        "Rows max(0, r − k)..min(rows − 1, r + k), same for columns. Then one 2D prefix lookup per cell."],
 trigger="A sum around every cell → 2D prefix + clamped rectangles.",
 examples=[([[[2,0,1],[1,3,0],[0,1,2]],1],[[6,7,4],[7,10,7],[5,7,6]],"The centre sees the whole grid: 10."),([[[1,2],[3,4]],0],[[1,2],[3,4]],"")],
 tests=[[[[7]],3],[[[1,1,1,1]],1],[[[1],[2],[3]],5]],
 gen=[{"seed":161,"count":3,"args":[{"kind":"intMatrix","rows":200,"cols":200,"min":0,"max":1000},I(1,20)]}],
 cross=[{"seed":16,"count":200,"args":[{"kind":"intMatrix","rows":4,"cols":3,"min":0,"max":9},I(0,3)]}],
 ref="""
    public long[][] neighbourhoodSum(int[][] grid, int k) {
        int R = grid.length, C = grid[0].length;
        long[][] P = new long[R + 1][C + 1];
        for (int r = 0; r < R; r++)
            for (int c = 0; c < C; c++)
                P[r + 1][c + 1] = grid[r][c] + P[r][c + 1] + P[r + 1][c] - P[r][c];
        long[][] out = new long[R][C];
        for (int r = 0; r < R; r++)
            for (int c = 0; c < C; c++) {
                int r1 = Math.max(0, r - k), c1 = Math.max(0, c - k), r2 = Math.min(R - 1, r + k), c2 = Math.min(C - 1, c + k);
                out[r][c] = P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1];
            }
        return out;
    }""",
 brute="""
    public long[][] neighbourhoodSum(int[][] grid, int k) {
        int R = grid.length, C = grid[0].length; long[][] o = new long[R][C];
        for (int r = 0; r < R; r++) for (int c = 0; c < C; c++) for (int i = 0; i < R; i++) for (int j = 0; j < C; j++) if (Math.abs(i - r) <= k && Math.abs(j - c) <= k) o[r][c] += grid[i][j];
        return o;
    }""")

prob(slug="largest-square-budget", stage=2, title="Largest Square Within Budget", difficulty="Hard",
 whats="Combine 2D prefix sums with a search: for each size, every square's sum is one O(1) lookup.",
 f=fn("largestSquare", "int", ("int[][]", "grid"), ("int", "budget")),
 statement="""
`grid[r][c]` is the cost of a plot of land (all costs are non-negative). Return the side length of the **largest square** of plots whose total cost is at most `budget`, or `0` if even a single plot is too expensive.
""", constraints=["1 <= rows, cols <= 200", "0 <= grid[r][c] <= 10^4", "0 <= budget <= 10^9"],
 hints=["With 2D prefix sums, what does it cost to get the sum of one k × k square?",
        "Costs are non-negative: if some square of side k fits the budget, does some square of side k − 1 fit too?",
        "So the answer is monotone. Either binary search k, or grow k while some square of the next size fits."],
 trigger="Largest square/rectangle under a sum limit → 2D prefix + monotone search over the size.",
 examples=[([[[1,1,3,2],[1,1,3,2],[1,1,3,2]],4],2,"The 2 × 2 square of 1s costs 4."),([[[5,5],[5,5]],4],0,"")],
 tests=[[[[0]],0],[[[3]],3],[[[1,1],[1,1]],100]],
 gen=[{"seed":171,"count":1,"args":[{"kind":"intMatrix","rows":200,"cols":200,"min":0,"max":10000},I(1000000,50000000)]},{"seed":172,"count":1,"args":[{"kind":"intMatrix","rows":200,"cols":150,"min":0,"max":100},I(0,2000000)]}],
 cross=[{"seed":17,"count":300,"args":[{"kind":"intMatrix","rows":4,"cols":5,"min":0,"max":9},I(0,60)]}],
 ref="""
    public int largestSquare(int[][] grid, int budget) {
        int R = grid.length, C = grid[0].length;
        long[][] P = new long[R + 1][C + 1];
        for (int r = 0; r < R; r++)
            for (int c = 0; c < C; c++)
                P[r + 1][c + 1] = grid[r][c] + P[r][c + 1] + P[r + 1][c] - P[r][c];
        int best = 0;
        for (int r = 0; r < R; r++)
            for (int c = 0; c < C; c++) {
                // try to beat the current best by one: answers only grow, so this is O(R*C)
                int k = best + 1;
                while (r + k <= R && c + k <= C && P[r + k][c + k] - P[r][c + k] - P[r + k][c] + P[r][c] <= budget) {
                    best = k;
                    k++;
                }
            }
        return best;
    }""",
 brute="""
    public int largestSquare(int[][] grid, int budget) {
        int R = grid.length, C = grid[0].length, b = 0;
        for (int r = 0; r < R; r++) for (int c = 0; c < C; c++) for (int k = 1; r + k <= R && c + k <= C; k++) { long s = 0; for (int i = r; i < r + k; i++) for (int j = c; j < c + k; j++) s += grid[i][j]; if (s <= budget) b = Math.max(b, k); }
        return b;
    }""")

# ============================== Stage 4: difference arrays ==============================
prob(slug="range-add-updates", stage=3, title="Range Add Updates", difficulty="Medium",
 whats="Reverse the idea: instead of reading ranges, write them. Mark the start and one-past-the-end, then take a prefix sum.",
 f=fn("applyUpdates", "long[]", ("int", "n"), ("int[][]", "updates")),
 statement="""
Start with an array of `n` zeros. Each update `[l, r, v]` adds `v` to every position from `l` to `r` (both included).

Return the array after all updates.
""", constraints=["1 <= n <= 10^5", "1 <= updates.length <= 10^5", "0 <= l <= r < n", "-10^4 <= v <= 10^4"],
 hints=["Adding v to a whole range costs up to n steps per update. Could you record each update in O(1) and fix everything at the end?",
        "Write +v at index l and −v at index r + 1 of a helper array. What does a running sum of that helper array give you?",
        "diff has length n + 1. The answer is the running sum of diff[0..n−1]."],
 trigger="Many range updates, one read at the end → difference array + prefix sum.",
 examples=[([5,[[1,3,2],[2,4,3],[0,2,-2]]],[-2,0,3,5,3],"After all three updates."),([3,[[0,2,1]]],[1,1,1],"")],
 tests=[[1,[[0,0,5]]],[4,[[0,3,1],[0,3,-1]]],[6,[[5,5,7],[0,0,-7]]]],
 gen=[{"seed":181,"count":1,"args":[I(100000,100000),{"kind":"updates","q":100000,"of":0,"min":-10000,"max":10000}]},{"seed":182,"count":2,"args":[I(100000,100000),{"kind":"updates","q":100000,"of":0,"min":-10000,"max":10000,"wide":True}]}],
 cross=[{"seed":18,"count":300,"args":[I(1,9),{"kind":"updates","q":5,"of":0,"min":-5,"max":5}]}],
 ref="""
    public long[] applyUpdates(int n, int[][] updates) {
        long[] diff = new long[n + 1];
        for (int[] u : updates) {
            diff[u[0]] += u[2];
            diff[u[1] + 1] -= u[2];
        }
        long[] out = new long[n];
        long run = 0;
        for (int i = 0; i < n; i++) {
            run += diff[i];
            out[i] = run;
        }
        return out;
    }""",
 brute="""
    public long[] applyUpdates(int n, int[][] updates) {
        long[] o = new long[n];
        for (int[] u : updates) for (int i = u[0]; i <= u[1]; i++) o[i] += u[2];
        return o;
    }""")

prob(slug="peak-visitors", stage=3, title="Peak Visitors", difficulty="Medium",
 whats="Each visit is a range update of +1. The busiest moment is the maximum of the running sum.",
 f=fn("peakVisitors", "int", ("int[][]", "visits")),
 statement="""
A museum logs each visit as `[arrive, leave]`: the visitor is inside at every whole minute `t` with `arrive <= t < leave` (they are gone at minute `leave`).

Return the largest number of visitors inside at the same minute.
""", constraints=["1 <= visits.length <= 10^5", "0 <= arrive < leave <= 10^5"],
 hints=["Each visitor adds 1 to a range of minutes. Which technique applies many range additions cheaply?",
        "+1 at arrive, −1 at leave (not leave + 1, because the range is half-open). The running sum is the head-count."],
 trigger="Max overlap of many intervals → difference array (or sorted start/end events).",
 examples=[([[[1,4],[2,5],[4,6]]],2,"At minute 4 the first visitor has left, so it's never 3 at once."),([[[0,1],[1,2]]],1,"")],
 tests=[[[[0,100000]]],[[[5,6],[5,6],[5,6]]],[[[0,2],[1,3],[2,4],[3,5]]]],
 gen=[{"seed":191,"count":1,"args":[{"kind":"intervals","q":100000,"maxTime":100000,"maxLen":2000}]},{"seed":192,"count":3,"args":[{"kind":"intervals","q":100000,"maxTime":100000}]}],
 cross=[{"seed":19,"count":300,"args":[{"kind":"intervals","q":5,"maxTime":12,"maxLen":5}]}],
 ref="""
    public int peakVisitors(int[][] visits) {
        int maxT = 0;
        for (int[] v : visits) maxT = Math.max(maxT, v[1]);
        int[] diff = new int[maxT + 1];
        for (int[] v : visits) {
            diff[v[0]]++;
            diff[v[1]]--;
        }
        int run = 0, best = 0;
        for (int t = 0; t <= maxT; t++) {
            run += diff[t];
            best = Math.max(best, run);
        }
        return best;
    }""",
 brute="""
    public int peakVisitors(int[][] visits) {
        int b = 0;
        for (int t = 0; t <= 20; t++) { int c = 0; for (int[] v : visits) if (v[0] <= t && t < v[1]) c++; b = Math.max(b, c); }
        return b;
    }""")

prob(slug="shuttle-capacity", stage=3, title="Shuttle Capacity", difficulty="Medium",
 whats="Same difference-array idea with weights: groups board at one stop and leave at another.",
 f=fn("canCarry", "boolean", ("int[][]", "trips"), ("int", "capacity")),
 statement="""
A shuttle drives in one direction past stops `0, 1, 2, …`. Each trip `[count, from, to]` is a group of `count` people who board at stop `from` and get off at stop `to` (their seats are free again at stop `to`).

Return `true` if the shuttle never carries more than `capacity` people at once.
""", constraints=["1 <= trips.length <= 10^5", "1 <= count <= 100", "0 <= from < to <= 10^5", "1 <= capacity <= 10^7"],
 hints=["How many people are on board between stop s and s + 1? Think of each trip as a range update.",
        "+count at from, −count at to. Walk the stops with a running sum and compare with capacity."],
 trigger="Load over time from many start/end events → difference array.",
 examples=[([[[3,0,4],[2,2,6]],4],False,"Between stops 2 and 4 there are 5 people."),([[[3,0,4],[2,4,6]],3],True,"The first group leaves exactly when the second boards.")],
 tests=[[[[1,0,1]],1],[[[100,0,100000]],99],[[[3,2,7],[3,7,9],[8,3,9]],11]],
 gen=[{"seed":201,"count":3,"args":[{"kind":"trips","q":100000,"maxLoc":100000,"maxCount":100},I(2000000,3000000)]},{"seed":202,"count":1,"args":[{"kind":"trips","q":100000,"maxLoc":1000,"maxCount":100},I(2400000,2600000)]}],
 cross=[{"seed":20,"count":400,"args":[{"kind":"trips","q":4,"maxLoc":10,"maxCount":5},I(1,12)]}],
 ref="""
    public boolean canCarry(int[][] trips, int capacity) {
        int maxStop = 0;
        for (int[] t : trips) maxStop = Math.max(maxStop, t[2]);
        long[] diff = new long[maxStop + 1];
        for (int[] t : trips) {
            diff[t[1]] += t[0];
            diff[t[2]] -= t[0];
        }
        long onBoard = 0;
        for (int s = 0; s <= maxStop; s++) {
            onBoard += diff[s];
            if (onBoard > capacity) return false;
        }
        return true;
    }""",
 brute="""
    public boolean canCarry(int[][] trips, int capacity) {
        for (int s = 0; s <= 10; s++) { long c = 0; for (int[] t : trips) if (t[1] <= s && s < t[2]) c += t[0]; if (c > capacity) return false; }
        return true;
    }""")

# ============================== Stage 5: prefix of other operations ==============================
prob(slug="range-xor-queries", stage=4, title="Range XOR Queries", difficulty="Easy",
 whats="Prefix sums work for any operation you can undo. XOR undoes itself: x ^ x = 0.",
 f=fn("rangeXor", "int[]", ("int[]", "nums"), ("int[][]", "queries")),
 statement="""
For each query `[l, r]` return `nums[l] ^ nums[l+1] ^ … ^ nums[r]` (`^` is bitwise XOR).
""", constraints=["1 <= nums.length, queries.length <= 10^5", "0 <= nums[i] <= 10^9", "0 <= l <= r < nums.length"],
 hints=["For sums you subtracted two prefixes. What operation undoes an XOR?",
        "px[i + 1] = px[i] ^ nums[i]; the answer is px[r + 1] ^ px[l], because the shared part cancels."],
 trigger="Range queries of an invertible operation (sum, XOR) → prefix + inverse.",
 examples=[([[6,1,7,2],[[0,1],[1,2],[0,3],[2,2]]],[7,6,2,7],"6^1 = 7, 1^7 = 6, 6^1^7^2 = 2.")],
 tests=[[[0],[[0,0]]],[[5,5,5],[[0,1],[0,2]]]],
 gen=[{"seed":211,"count":1,"args":[arr(100000,0,1000000000),{"kind":"ranges","q":100000,"of":0}]},{"seed":212,"count":2,"args":[arr(100000,0,1000000000),{"kind":"ranges","q":100000,"of":0,"wide":True}]}],
 cross=[{"seed":21,"count":300,"args":[arrr(1,8,0,31),{"kind":"ranges","q":5,"of":0}]}],
 ref="""
    public int[] rangeXor(int[] nums, int[][] queries) {
        int[] px = new int[nums.length + 1];
        for (int i = 0; i < nums.length; i++) px[i + 1] = px[i] ^ nums[i];
        int[] ans = new int[queries.length];
        for (int j = 0; j < queries.length; j++) ans[j] = px[queries[j][1] + 1] ^ px[queries[j][0]];
        return ans;
    }""",
 brute="""
    public int[] rangeXor(int[] nums, int[][] queries) {
        int[] a = new int[queries.length];
        for (int j = 0; j < queries.length; j++) for (int i = queries[j][0]; i <= queries[j][1]; i++) a[j] ^= nums[i];
        return a;
    }""")

prob(slug="vowel-count-queries", stage=4, title="Vowel Count Queries", difficulty="Easy",
 whats="Prefix sums of a yes/no property: count how many positions so far satisfy it.",
 f=fn("vowelCounts", "int[]", ("String", "s"), ("int[][]", "queries")),
 statement="""
For each query `[l, r]`, return how many vowels (`a, e, i, o, u`) appear in `s[l..r]` (both ends included).
""", constraints=["1 <= s.length, queries.length <= 10^5", "s consists of lowercase English letters", "0 <= l <= r < s.length"],
 hints=["Turn s into an array of 1s (vowel) and 0s (not). What are the queries now?",
        "count[i + 1] = count[i] + (s[i] is a vowel ? 1 : 0). Answer = count[r + 1] − count[l]."],
 trigger="“How many positions in a range satisfy X?” → prefix count of X.",
 examples=[(["prefixsum",[[0,3],[2,8],[5,5]]],[1,3,0],"“pref” has 1 vowel; “efixsum” has e, i, u.")],
 tests=[["a",[[0,0]]],["bcd",[[0,2]]],["aeiou",[[1,3],[0,4]]]],
 gen=[{"seed":221,"count":1,"args":[{"kind":"string","n":100000,"alphabet":"abcdefghijklmnopqrstuvwxyz"},{"kind":"ranges","q":100000,"of":0}]},{"seed":222,"count":2,"args":[{"kind":"string","n":100000,"alphabet":"abcdefghijklmnopqrstuvwxyz"},{"kind":"ranges","q":100000,"of":0,"wide":True}]}],
 cross=[{"seed":22,"count":300,"args":[{"kind":"string","nMin":1,"nMax":10,"alphabet":"abeiou"},{"kind":"ranges","q":4,"of":0}]}],
 ref="""
    public int[] vowelCounts(String s, int[][] queries) {
        int[] count = new int[s.length() + 1];
        for (int i = 0; i < s.length(); i++) count[i + 1] = count[i] + ("aeiou".indexOf(s.charAt(i)) >= 0 ? 1 : 0);
        int[] ans = new int[queries.length];
        for (int j = 0; j < queries.length; j++) ans[j] = count[queries[j][1] + 1] - count[queries[j][0]];
        return ans;
    }""",
 brute="""
    public int[] vowelCounts(String s, int[][] queries) {
        int[] a = new int[queries.length];
        for (int j = 0; j < queries.length; j++) for (int i = queries[j][0]; i <= queries[j][1]; i++) if ("aeiou".indexOf(s.charAt(i)) >= 0) a[j]++;
        return a;
    }""")

prob(slug="even-vowels-longest", stage=4, title="Longest Substring With Even Vowels", difficulty="Hard",
 whats="Track five parities at once in a 5-bit mask. Equal masks mean every vowel appears an even number of times in between.",
 f=fn("longestEvenVowels", "int", ("String", "s")),
 statement="""
Return the length of the longest substring of `s` in which **each** vowel `a, e, i, o, u` appears an **even** number of times (zero counts as even).
""", constraints=["1 <= s.length <= 10^5", "s consists of lowercase English letters"],
 hints=["You only care whether each vowel count is even or odd so far. How many different “parity states” are there?",
        "Store the state as 5 bits; seeing a vowel flips its bit (XOR). When is the substring between two positions good?",
        "Same mask at i and j → every vowel count between them is even. Store the first index of each mask (seed mask 0 at −1)."],
 trigger="“Every X appears an even number of times” → XOR parity mask + first index of each mask.",
 examples=[(["helloworld"],8,"“lloworld” has two o’s and no other vowels."),(["bcbcbc"],6,""),(["aeiou"],0,"")],
 tests=[["a"],["b"],["aa"],["abcab"]],
 gen=[{"seed":231,"count":1,"args":[{"kind":"string","n":100000,"alphabet":"abcdefghijklmnopqrstuvwxyz"}]},{"seed":232,"count":1,"args":[{"kind":"string","n":100000,"alphabet":"aeioub"}]}],
 cross=[{"seed":23,"count":400,"args":[{"kind":"string","nMin":1,"nMax":10,"alphabet":"aeb"}]}],
 ref="""
    public int longestEvenVowels(String s) {
        int[] first = new int[32];
        Arrays.fill(first, -2);
        first[0] = -1;
        int mask = 0, best = 0;
        for (int i = 0; i < s.length(); i++) {
            int v = "aeiou".indexOf(s.charAt(i));
            if (v >= 0) mask ^= 1 << v;
            if (first[mask] == -2) first[mask] = i;
            else best = Math.max(best, i - first[mask]);
        }
        return best;
    }""",
 brute="""
    public int longestEvenVowels(String s) {
        int b = 0;
        for (int i = 0; i < s.length(); i++) { int m = 0; for (int j = i; j < s.length(); j++) { int v = "aeiou".indexOf(s.charAt(j)); if (v >= 0) m ^= 1 << v; if (m == 0) b = Math.max(b, j - i + 1); } }
        return b;
    }""")


def main():
    os.makedirs(ROOT, exist_ok=True)
    for f in os.listdir(ROOT):
        pass
    for i, p in enumerate(P, 1):
        d = os.path.join(ROOT, f"{i:02d}-{p['slug']}")
        os.makedirs(d, exist_ok=True)
        meta = {"slug": p["slug"], "topic": "prefix-sum", "stage": p["stage"], "order": i, "title": p["title"],
                "difficulty": p["difficulty"], "whatsNew": p["whats"], "function": p["f"],
                "timeLimitMs": p.get("tl", 1000), "hints": p["hints"], "trigger": p["trigger"]}
        if p.get("compare"): meta["compare"] = p["compare"]
        json.dump(meta, open(os.path.join(d, "problem.json"), "w"), ensure_ascii=False, indent=1)
        st = textwrap.dedent(p["statement"]).strip() + "\n\n**Constraints**\n" + "\n".join(f"- `{c}`" for c in p["constraints"]) + "\n"
        open(os.path.join(d, "statement.md"), "w").write(st)
        for name, body in (("Solution.java", p["ref"]), ("Brute.java", p["brute"])):
            open(os.path.join(d, name), "w").write("import java.util.*;\n\nclass Solution {" + body + "\n}\n")
        tests = {"examples": [{"input": a, "output": o, **({"explanation": e} if e else {})} for a, o, e in p["examples"]],
                 "tests": [{"input": t} for t in p["tests"]],
                 "generated": p["gen"], "crosscheck": p["cross"]}
        json.dump(tests, open(os.path.join(d, "tests.json"), "w"), ensure_ascii=False, separators=(",", ":"))
    print(len(P), "problems written")

if __name__ == "__main__":
    main()
