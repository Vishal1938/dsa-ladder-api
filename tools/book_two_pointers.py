"""Authoring source for the Two Pointers problem book.
Run:  python3 tools/book_two_pointers.py   -> writes problems/two-pointers/NN-slug/{problem.json,statement.md,Solution.java,Brute.java,tests.json}
Every problem has a reference solution AND a brute-force solution; `JudgeCli crosscheck` compares them on random inputs,
and `JudgeCli judge <slug> submit < Brute.java` must *reject* the brute force, so the intended idea is really required.
"""
import json, os, textwrap

ROOT = os.path.join(os.path.dirname(__file__), "..", "problems", "two-pointers")
P = []

def prob(**k):
    P.append(k)

def fn(name, returns, *params, out=None):
    f = {"name": name, "returns": returns, "params": [{"name": n, "type": t} for t, n in params]}
    if out is not None:
        f["outputArg"] = out
    return f

def arr(n, lo, hi, **opt):
    return {"kind": "intArray", "n": n, "min": lo, "max": hi, **opt}

def arrr(nmin, nmax, lo, hi, **opt):
    return {"kind": "intArray", "nMin": nmin, "nMax": nmax, "min": lo, "max": hi, **opt}

def I(lo, hi):
    return {"kind": "int", "min": lo, "max": hi}

def K(v):
    return {"kind": "const", "value": v}

def S(n, alpha):
    return {"kind": "string", "n": n, "alphabet": alpha}

def Sr(nmin, nmax, alpha):
    return {"kind": "string", "nMin": nmin, "nMax": nmax, "alphabet": alpha}

def near_pal(n, alpha, flips=0, noise=""):
    s = {"kind": "nearPalindrome", "n": n, "alphabet": alpha, "flips": flips}
    if noise:
        s["noise"] = noise
    return s

def near_pal_r(nmin, nmax, alpha, flips=0, noise=""):
    s = {"kind": "nearPalindrome", "nMin": nmin, "nMax": nmax, "alphabet": alpha, "flips": flips}
    if noise:
        s["noise"] = noise
    return s

def buffer_of(m, n, lo, hi):
    return {"kind": "sortedWithBuffer", "m": m, "n": n, "min": lo, "max": hi}

def choice(n, values):
    return {"kind": "choiceArray", "n": n, "values": values}

def choice_r(nmin, nmax, values):
    return {"kind": "choiceArray", "nMin": nmin, "nMax": nmax, "values": values}

def subseq(of, length, flip, alpha="abcdefghijklmnopqrstuvwxyz"):
    return {"kind": "subsequenceOf", "of": of, "len": length, "flip": flip, "alphabet": alpha}

def typed_again(of, count, flip, alpha):
    return {"kind": "insertBackspacePairs", "of": of, "count": count, "flip": flip, "alphabet": alpha}

def intervals(n, maxgap, maxlen):
    return {"kind": "disjointIntervals", "n": n, "maxGap": maxgap, "maxLen": maxlen}

# ============================== Stage 1: opposite ends ==============================
prob(slug="reverse-in-place", stage=0, title="Reverse in Place", difficulty="Easy",
 whats="The template for the whole stage: one pointer at each end, swap them, and step both inwards.",
 f=fn("reverseChars", "void", ("char[]", "s"), out=0),
 statement="""
A sign maker has the letters of a word sitting in a rail of slots, one letter per slot, and needs the word the other way round.

Reverse `s` **in place**: the only thing you may do is move letters between slots. Your method returns nothing; the rail itself is the answer.
""", constraints=["1 <= s.length <= 10^5", "s[i] is a lowercase English letter"],
 hints=["Which slot does the first letter have to end up in? And the second?",
        "If you swap those two letters straight away, which part of the rail is still unfinished?",
        "How do you know when the two slots you are swapping have met?"],
 trigger="“Reverse / mirror a sequence in place” → a pointer at each end, swap and step inwards.",
 examples=[([["h","e","l","l","o"]],["o","l","l","e","h"],"The first and last letters trade places, then the second and second-to-last."),
           ([["a","b"]],["b","a"],""),
           ([["x"]],["x"],"A single letter is already reversed.")],
 tests=[[["a","a"]],[["a","b","c"]],[["a","b","c","d"]],[["z","z","z","z","z"]],[["q","w","e","r","t","y"]]],
 gen=[{"seed":1101,"count":5,"args":[S(100000,"abcdefghijklmnopqrstuvwxyz")]},
      {"seed":1102,"count":2,"args":[S(100000,"ab")]}],
 cross=[{"seed":101,"count":250,"args":[Sr(1,10,"abc")]},
        {"seed":102,"count":150,"args":[Sr(1,4,"ab")]}],
 ref="""
    public void reverseChars(char[] s) {
        int left = 0, right = s.length - 1;
        while (left < right) {
            char t = s[left];
            s[left++] = s[right];
            s[right--] = t;
        }
    }""",
 brute="""
    public void reverseChars(char[] s) {
        List<Character> reversed = new ArrayList<>();
        for (char c : s) reversed.add(0, c);          // each new letter goes in front of the ones before it
        for (int i = 0; i < s.length; i++) s[i] = reversed.get(i);
    }""")

prob(slug="clean-palindrome", stage=0, title="Palindrome After Cleaning", difficulty="Easy",
 whats="The pointers no longer move on every step: each one first walks past the characters that do not count.",
 f=fn("isCleanPalindrome", "boolean", ("String", "s")),
 statement="""
A puzzle magazine checks whether a phrase reads the same backwards once you ignore everything that is not a letter or a digit, and treat capitals and small letters as the same.

Return `true` if `s` reads the same in both directions under those rules.
""", constraints=["1 <= s.length <= 10^5", "s consists of printable ASCII characters (letters, digits, spaces and punctuation)"],
 hints=["If you only had letters and digits, where would the two pointers start?",
        "What should a pointer do when it lands on a space or a comma — compare it, or something else?",
        "Could the two pointers cross while they are skipping junk, and what does that mean for the answer?"],
 trigger="“Palindrome ignoring some characters” → a pointer at each end, each skipping what does not count.",
 examples=[(["Step on no pets!"],True,"Cleaned up it reads stepnonopets backwards and forwards."),
           (["Judge a book"],False,""),
           (["12 a 21"],True,"Digits count too: the cleaned phrase is 12a21.")],
 tests=[[","],["a"],["ab"],["Aa"],["0P"],["aBcCbA"]],
 gen=[{"seed":1201,"count":4,"args":[near_pal(100000,"abcdefghijklmnopqrstuvwxyz",0,noise=" ,.!")]},
      {"seed":1202,"count":1,"args":[near_pal(100000,"abcde",2,noise=" ,.!")]},
      {"seed":1203,"count":1,"args":[near_pal(100000,"aAbB09",0,noise=" ,.!?;:")]}],
 cross=[{"seed":111,"count":200,"args":[near_pal_r(1,12,"abc",1,noise=" ,.")]},
        {"seed":112,"count":150,"args":[Sr(1,10,"aAbB, .")]},
        {"seed":113,"count":100,"args":[near_pal_r(1,8,"aA0",0,noise="!.")]}],
 ref="""
    public boolean isCleanPalindrome(String s) {
        int left = 0, right = s.length() - 1;
        while (left < right) {
            while (left < right && !Character.isLetterOrDigit(s.charAt(left))) left++;
            while (left < right && !Character.isLetterOrDigit(s.charAt(right))) right--;
            if (Character.toLowerCase(s.charAt(left)) != Character.toLowerCase(s.charAt(right))) return false;
            left++;
            right--;
        }
        return true;
    }""",
 brute="""
    public boolean isCleanPalindrome(String s) {
        String clean = "";
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (Character.isLetterOrDigit(c)) clean += Character.toLowerCase(c);
        }
        for (int i = 0; i < clean.length() / 2; i++)
            if (clean.charAt(i) != clean.charAt(clean.length() - 1 - i)) return false;
        return true;
    }""")

prob(slug="sorted-squares", stage=0, title="Squares of a Sorted List", difficulty="Easy",
 whats="The largest square is always at one of the two ends, so you can fill the answer from the back.",
 f=fn("sortedSquares", "int[]", ("int[]", "nums")),
 statement="""
A thermometer logs temperatures through the day, already in increasing order, and some of them are below zero. The lab needs the **squares** of those readings, also in increasing order.

Return the squares of `nums` sorted from smallest to largest. `nums` itself is already sorted.
""", constraints=["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4", "nums is sorted in non-decreasing order"],
 hints=["Squaring destroys the order, but not completely. Which reading has the largest square, and where in the list is it?",
        "If you know the largest square, which slot of the answer does it belong in?",
        "After taking a value from one end, what is left to consider?"],
 trigger="“Sorted input, but the measure peaks at the ends” → compare the two ends and fill the answer backwards.",
 examples=[([[-5,-2,0,1,4]],[0,1,4,16,25],"The squares are 25, 4, 0, 1 and 16; sorted they are 0, 1, 4, 16, 25."),
           ([[-7,-3]],[9,49],"Both are negative, so the squares come out in the opposite order."),
           ([[1,2,3]],[1,4,9],"")],
 tests=[[[0]],[[-1]],[[-3,-3]],[[-2,2]],[[-10000,10000]],[[0,0,0]]],
 gen=[{"seed":1301,"count":2,"args":[arr(100000,-10000,10000,sorted=True)]},
      {"seed":1302,"count":1,"args":[arr(100000,-10000,-1,sorted=True)]},
      {"seed":1303,"count":1,"args":[arr(100000,0,10000,sorted=True)]}],
 cross=[{"seed":121,"count":250,"args":[arrr(1,10,-9,9,sorted=True)]},
        {"seed":122,"count":150,"args":[arrr(1,6,-3,3,sorted=True)]}],
 ref="""
    public int[] sortedSquares(int[] nums) {
        int n = nums.length;
        int[] out = new int[n];
        int left = 0, right = n - 1;
        for (int slot = n - 1; slot >= 0; slot--) {
            int lo = nums[left] * nums[left], hi = nums[right] * nums[right];
            if (lo > hi) { out[slot] = lo; left++; }
            else { out[slot] = hi; right--; }
        }
        return out;
    }""",
 brute="""
    public int[] sortedSquares(int[] nums) {
        int n = nums.length;
        int[] squares = new int[n];
        for (int i = 0; i < n; i++) squares[i] = nums[i] * nums[i];
        boolean[] used = new boolean[n];
        int[] out = new int[n];
        for (int slot = 0; slot < n; slot++) {        // selection sort: smallest unused square each time
            int best = -1;
            for (int i = 0; i < n; i++) if (!used[i] && (best < 0 || squares[i] < squares[best])) best = i;
            used[best] = true;
            out[slot] = squares[best];
        }
        return out;
    }""")

prob(slug="pair-in-sorted", stage=0, title="Pair With a Given Sum, Sorted", difficulty="Easy",
 whats="Because the input is sorted, one comparison rules out a whole row of pairs at once.",
 f=fn("hasPairWithSum", "boolean", ("int[]", "sorted"), ("int", "target")),
 statement="""
A charity has a price list in increasing order and a donor who wants to buy exactly two items for a given total.

Return `true` if two **different** entries of `sorted` add up to `target`. `sorted` is already in non-decreasing order.
""", constraints=["1 <= sorted.length <= 10^5", "-10^9 <= sorted[i] <= 10^9", "-2 * 10^9 <= target <= 2 * 10^9",
                  "sorted is in non-decreasing order"],
 hints=["Start with the cheapest and the dearest item. What does their total tell you?",
        "If that total is too small, which of the two items can you rule out completely — and why is that safe?",
        "How many steps does each pointer take in total?"],
 trigger="“Sorted array, find a pair with a given sum” → one pointer at each end; too small moves left up, too big moves right down.",
 examples=[([[1,3,4,7,11],8],True,"1 + 7 = 8."),
           ([[2,4,6],11],False,"Every total of two entries is even."),
           ([[-4,-1,0,5],-5],True,"−4 + (−1) = −5.")],
 tests=[[[1],2],[[1,1],2],[[0,0],0],[[-5,5],0],[[1,2,3],7],[[-1000000000,1000000000],0]],
 gen=[{"seed":1401,"count":3,"args":[arr(100000,1,1000000000,sorted=True),K(-5)]},
      {"seed":1402,"count":1,"args":[arr(100000,-1000000000,1000000000,sorted=True),I(-2000000,2000000)]},
      {"seed":1403,"count":1,"args":[arr(100000,1,200,sorted=True),K(401)]}],
 cross=[{"seed":131,"count":250,"args":[arrr(1,10,-8,8,sorted=True),I(-10,10)]},
        {"seed":132,"count":150,"args":[arrr(2,8,-3,3,sorted=True),I(-4,4)]}],
 ref="""
    public boolean hasPairWithSum(int[] sorted, int target) {
        int left = 0, right = sorted.length - 1;
        while (left < right) {
            long sum = (long) sorted[left] + sorted[right];
            if (sum == target) return true;
            if (sum < target) left++;
            else right--;
        }
        return false;
    }""",
 brute="""
    public boolean hasPairWithSum(int[] sorted, int target) {
        boolean found = false;
        for (int i = 0; i < sorted.length; i++)
            for (int j = i + 1; j < sorted.length; j++)
                if ((long) sorted[i] + sorted[j] == target) found = true;
        return found;
    }""")

prob(slug="one-delete-palindrome", stage=0, title="Palindrome After One Deletion", difficulty="Medium",
 whats="At the first mismatch you do not give up: you try skipping the left character, and then the right one.",
 f=fn("almostPalindrome", "boolean", ("String", "s")),
 statement="""
A proof-reader will accept a phrase as a palindrome if it already reads the same both ways, **or** if deleting a single character makes it so.

Return `true` if `s` can be made into a palindrome by removing at most one character.
""", constraints=["1 <= s.length <= 10^5", "s consists of lowercase English letters"],
 hints=["Walk two pointers inwards as usual. What have you learnt the moment they disagree?",
        "At that point exactly one of the two characters has to go. How many possibilities is that?",
        "Each possibility leaves a plain “is this stretch a palindrome?” question. How expensive is answering it?"],
 trigger="“Palindrome allowing one edit” → two pointers, and at the first mismatch test both skips.",
 examples=[(["level"],True,"It is already a palindrome, so nothing has to be deleted."),
           (["levell"],True,"Deleting one of the final l's leaves level."),
           (["abcdef"],False,"")],
 tests=[["a"],["ab"],["abc"],["abca"],["aabb"],["abcdba"]],
 gen=[{"seed":1501,"count":2,"args":[near_pal(100000,"abcde",1)]},
      {"seed":1502,"count":1,"args":[near_pal(100000,"ab",2)]},
      {"seed":1503,"count":1,"args":[near_pal(100000,"abcdefghijklmnopqrstuvwxyz",0)]}],
 cross=[{"seed":141,"count":250,"args":[near_pal_r(1,12,"ab",1)]},
        {"seed":142,"count":150,"args":[Sr(1,9,"abc")]}],
 ref="""
    public boolean almostPalindrome(String s) {
        int left = 0, right = s.length() - 1;
        while (left < right) {
            if (s.charAt(left) != s.charAt(right))
                return isPalindrome(s, left + 1, right) || isPalindrome(s, left, right - 1);
            left++;
            right--;
        }
        return true;
    }

    private boolean isPalindrome(String s, int left, int right) {
        while (left < right) {
            if (s.charAt(left++) != s.charAt(right--)) return false;
        }
        return true;
    }""",
 brute="""
    public boolean almostPalindrome(String s) {
        if (plain(s)) return true;
        for (int drop = 0; drop < s.length(); drop++) {
            StringBuilder sb = new StringBuilder(s);
            sb.deleteCharAt(drop);
            if (plain(sb.toString())) return true;
        }
        return false;
    }

    private boolean plain(String t) {
        for (int i = 0; i < t.length() / 2; i++)
            if (t.charAt(i) != t.charAt(t.length() - 1 - i)) return false;
        return true;
    }""")

prob(slug="count-pairs-below", stage=0, title="Count Pairs Below a Total", difficulty="Medium",
 whats="When a pair fits, every pair between the two pointers fits as well, so you count r − l of them in one step.",
 f=fn("countPairsBelow", "long", ("int[]", "sorted"), ("int", "target")),
 statement="""
A delivery van has a weight allowance. Given the parcel weights in increasing order, the depot wants to know how many pairs of parcels it could send together.

Count the index pairs `i < j` with `sorted[i] + sorted[j]` **strictly less than** `target`. `sorted` is already in non-decreasing order.
""", constraints=["1 <= sorted.length <= 10^5", "-10^9 <= sorted[i] <= 10^9", "-2 * 10^9 <= target <= 2 * 10^9",
                  "sorted is in non-decreasing order"],
 hints=["Put a pointer at each end. If the lightest and the heaviest parcel fit together, what do you know about the lightest paired with anything in between?",
        "So how many pairs can you tick off without checking them one at a time?",
        "And if that pair does not fit, which parcel can never be part of a pair with anything that is left?"],
 trigger="“Count pairs under a limit in a sorted array” → two pointers, and add r − l whenever the pair fits.",
 examples=[([[1,2,3,4],6],4,"The pairs 1+2, 1+3, 1+4 and 2+3 stay under 6; 2+4 and 3+4 do not."),
           ([[-2,0,3],1],1,"Only −2 + 0 is under 1."),
           ([[5,6],3],0,"")],
 tests=[[[1],5],[[1,1],3],[[0,0,0],1],[[-5,-5],-9],[[1,2,3],100],[[2,2],4]],
 gen=[{"seed":1601,"count":2,"args":[arr(100000,-1000000000,1000000000,sorted=True),K(2000000000)]},
      {"seed":1602,"count":1,"args":[arr(100000,1,1000000,sorted=True),I(500000,1500000)]},
      {"seed":1603,"count":1,"args":[arr(100000,1,1000000000,sorted=True),K(-5)]}],
 cross=[{"seed":151,"count":250,"args":[arrr(1,10,-8,8,sorted=True),I(-10,10)]},
        {"seed":152,"count":150,"args":[arrr(1,8,-3,3,sorted=True),I(-4,4)]}],
 ref="""
    public long countPairsBelow(int[] sorted, int target) {
        long pairs = 0;
        int left = 0, right = sorted.length - 1;
        while (left < right) {
            if ((long) sorted[left] + sorted[right] < target) {
                pairs += right - left;                // left pairs with everything up to right
                left++;
            } else right--;
        }
        return pairs;
    }""",
 brute="""
    public long countPairsBelow(int[] sorted, int target) {
        long pairs = 0;
        for (int i = 0; i < sorted.length; i++)
            for (int j = i + 1; j < sorted.length; j++)
                if ((long) sorted[i] + sorted[j] < target) pairs++;
        return pairs;
    }""")

# ============================== Stage 2: reader & writer (same direction) ==============================
prob(slug="remove-value", stage=1, title="Remove a Value", difficulty="Easy",
 whats="Both pointers now walk the same way: a reader that visits everything and a writer that only advances on a keeper.",
 f=fn("removeValue", "int[]", ("int[]", "nums"), ("int", "val")),
 statement="""
A warehouse list contains some entries for a product that has been discontinued. They have to come out, and the remaining entries must keep their order.

Return the kept entries: everything in `nums` that is not equal to `val`, in the original order. Do the compacting inside `nums` with a writer index rather than building a second list.
""", constraints=["1 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9", "-10^9 <= val <= 10^9"],
 hints=["Deleting an entry and shifting the rest left costs a whole pass each time. Could you instead decide, for each entry, where it finally belongs?",
        "Keep a count of how many entries you have kept so far. What is that count also telling you?",
        "Why is it safe to write to a slot you have not read yet — or have you always read it already?"],
 trigger="“Remove / compact / filter in place, order preserved” → a reader index and a writer index moving the same way.",
 examples=[([[3,1,3,4],3],[1,4],"The two 3s go, and 1 and 4 keep their order."),
           ([[2,2],2],[],"Everything matches, so nothing is left."),
           ([[5],1],[5],"")],
 tests=[[[1],1],[[0,0,0],0],[[1,2,1,2],2],[[7,7,7,1],7],[[1,2,3],9],[[4,4,5,4],4]],
 gen=[{"seed":1701,"count":4,"args":[arr(100000,1,3),K(2)]},
      {"seed":1702,"count":1,"args":[arr(100000,1,1),K(1)]},
      {"seed":1703,"count":1,"args":[arr(100000,-1000000000,1000000000),K(7)]}],
 cross=[{"seed":161,"count":250,"args":[arrr(1,10,1,4),I(1,4)]},
        {"seed":162,"count":150,"args":[choice_r(1,8,[0,1,-1,2]),I(-1,2)]}],
 ref="""
    public int[] removeValue(int[] nums, int val) {
        int write = 0;
        for (int read = 0; read < nums.length; read++)
            if (nums[read] != val) nums[write++] = nums[read];
        return Arrays.copyOf(nums, write);
    }""",
 brute="""
    public int[] removeValue(int[] nums, int val) {
        int n = nums.length, i = 0;
        while (i < n) {
            if (nums[i] == val) {
                for (int j = i; j < n - 1; j++) nums[j] = nums[j + 1];   // delete it and close the gap
                n--;
            } else i++;
        }
        return Arrays.copyOf(nums, n);
    }""")

prob(slug="dedupe-sorted", stage=1, title="Dedupe a Sorted List", difficulty="Easy",
 whats="The writer's rule becomes a comparison with what it wrote last, instead of with a fixed value.",
 f=fn("dedupeSorted", "int[]", ("int[]", "sorted")),
 statement="""
A sorted guest list has some names recorded twice. The registrar wants one entry per guest, still in order.

Return the entries of `sorted` with repeats removed, keeping one copy of each. `sorted` is already in non-decreasing order.
""", constraints=["1 <= sorted.length <= 10^5", "-10^9 <= sorted[i] <= 10^9", "sorted is in non-decreasing order"],
 hints=["Because the list is sorted, where are all the copies of one value?",
        "The writer index points just past the entries you have decided to keep. Which single one of them do you need to look at?",
        "What should the writer do with the very first entry?"],
 trigger="“Drop duplicates from sorted data, in place” → writer index, keep a value only if it differs from the last kept one.",
 examples=[([[1,1,2,3,3]],[1,2,3],"One copy each of 1, 2 and 3."),
           ([[4]],[4],""),
           ([[2,2,2]],[2],"")],
 tests=[[[1,2]],[[0,0]],[[-1,-1,0]],[[5,5,5,5,5]],[[1,2,3,4]],[[-2,-2,-1,-1]]],
 gen=[{"seed":1801,"count":2,"args":[arr(100000,1,100,sorted=True)]},
      {"seed":1802,"count":1,"args":[arr(100000,1,1,sorted=True)]},
      {"seed":1803,"count":1,"args":[arr(100000,-1000000000,1000000000,sorted=True)]}],
 cross=[{"seed":171,"count":250,"args":[arrr(1,10,1,4,sorted=True)]},
        {"seed":172,"count":150,"args":[arrr(1,8,-2,2,sorted=True)]}],
 ref="""
    public int[] dedupeSorted(int[] sorted) {
        int write = 0;
        for (int read = 0; read < sorted.length; read++)
            if (write == 0 || sorted[read] != sorted[write - 1]) sorted[write++] = sorted[read];
        return Arrays.copyOf(sorted, write);
    }""",
 brute="""
    public int[] dedupeSorted(int[] sorted) {
        int n = sorted.length, i = 1;
        while (i < n) {
            if (sorted[i] == sorted[i - 1]) {
                for (int j = i; j < n - 1; j++) sorted[j] = sorted[j + 1];   // delete the repeat, close the gap
                n--;
            } else i++;
        }
        return Arrays.copyOf(sorted, n);
    }""")

prob(slug="dedupe-at-most-two", stage=1, title="Keep at Most Two of Each", difficulty="Medium",
 whats="Look two slots back in the kept part instead of one, and the same loop keeps two copies instead of one.",
 f=fn("dedupeAtMostTwo", "int[]", ("int[]", "sorted")),
 statement="""
A raffle allows each number to be entered at most twice. The sorted list of submitted entries has to be trimmed so that no number appears more than two times, keeping the order.

Return the trimmed entries of `sorted`. `sorted` is already in non-decreasing order.
""", constraints=["1 <= sorted.length <= 10^5", "-10^9 <= sorted[i] <= 10^9", "sorted is in non-decreasing order"],
 hints=["In the previous problem the writer compared with the last entry it kept. What question is it really asking?",
        "If you are allowed two copies, how far back in the kept part do you have to look to know you already have two?",
        "Why does that one comparison work without counting anything?"],
 trigger="“Keep at most k copies of each value in sorted data” → writer index, compare with the value k slots back.",
 examples=[([[1,1,1,2,2,3]],[1,1,2,2,3],"The third 1 is dropped; everything else is within the limit."),
           ([[5,5]],[5,5],"Two copies are allowed."),
           ([[1,2,3]],[1,2,3],"")],
 tests=[[[1]],[[0,0,0,0]],[[-1,-1,-1,2]],[[7,7,8,8,8]],[[1,1]],[[2,2,2,2,3]]],
 gen=[{"seed":1901,"count":2,"args":[arr(100000,1,50000,sorted=True)]},
      {"seed":1902,"count":1,"args":[arr(100000,1,3,sorted=True)]},
      {"seed":1903,"count":1,"args":[arr(100000,-1000000000,1000000000,sorted=True)]}],
 cross=[{"seed":181,"count":250,"args":[arrr(1,10,1,4,sorted=True)]},
        {"seed":182,"count":150,"args":[arrr(1,9,-2,2,sorted=True)]}],
 ref="""
    public int[] dedupeAtMostTwo(int[] sorted) {
        int write = 0;
        for (int read = 0; read < sorted.length; read++)
            if (write < 2 || sorted[read] != sorted[write - 2]) sorted[write++] = sorted[read];
        return Arrays.copyOf(sorted, write);
    }""",
 brute="""
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
    }""")

prob(slug="zeros-to-end", stage=1, title="Zeros to the End", difficulty="Easy",
 whats="Same writer index, except now you have to go back and fill the slots it left behind.",
 f=fn("moveZeros", "void", ("int[]", "nums"), out=0),
 statement="""
A spreadsheet column has gaps recorded as zeros. The analyst wants every real reading first, in its original order, and all the gaps pushed to the bottom.

Rearrange `nums` **in place** so that the non-zero values keep their relative order and every zero sits after them. Your method returns nothing; the array itself is the answer.
""", constraints=["1 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9"],
 hints=["Pretend for a moment that you only had to collect the non-zero values at the front. Which problem is that?",
        "After the writer has placed every non-zero value, what do you know about the rest of the array?",
        "How many zeros should there be, and do you need to have counted them?"],
 trigger="“Push some values to one end, keeping the others in order” → collect the keepers with a writer, then fill the tail.",
 examples=[([[0,1,0,3,12]],[1,3,12,0,0],"1, 3 and 12 keep their order and the two zeros move to the back."),
           ([[1,0,2]],[1,2,0],""),
           ([[0]],[0],"A single zero is already in the right place.")],
 tests=[[[0,0]],[[1,2]],[[0,0,1]],[[1,0,0,2,0]],[[-1,0,-2]],[[0,-5]]],
 gen=[{"seed":2001,"count":2,"args":[arr(100000,0,1)]},
      {"seed":2002,"count":1,"args":[arr(100000,0,0)]},
      {"seed":2003,"count":1,"args":[choice(100000,[0,0,0,1,-1,5])]}],
 cross=[{"seed":191,"count":250,"args":[choice_r(1,10,[0,0,1,-1,2])]},
        {"seed":192,"count":150,"args":[arrr(1,8,0,1)]}],
 ref="""
    public void moveZeros(int[] nums) {
        int write = 0;
        for (int read = 0; read < nums.length; read++)
            if (nums[read] != 0) nums[write++] = nums[read];
        while (write < nums.length) nums[write++] = 0;
    }""",
 brute="""
    public void moveZeros(int[] nums) {
        int n = nums.length, parked = 0, i = 0;
        while (i < n - parked) {
            if (nums[i] == 0) {
                for (int j = i; j < n - 1; j++) nums[j] = nums[j + 1];   // slide the zero all the way down
                nums[n - 1] = 0;
                parked++;
            } else i++;
        }
    }""")

prob(slug="merge-into-buffer", stage=1, title="Merge Into the Free Space", difficulty="Easy",
 whats="Writing from the back instead of the front, so the writer never lands on a value you still have to read.",
 f=fn("mergeInto", "void", ("int[]", "a"), ("int", "m"), ("int[]", "b"), out=0),
 statement="""
Two sorted sensor logs have to become one. The first log `a` has room for both: its first `m` slots hold its own readings and the rest are empty, written as zeros.

Merge `b` into `a` **in place**, so that `a` ends up holding all `m + b.length` readings in non-decreasing order. Your method returns nothing; `a` itself is the answer.
""", constraints=["0 <= m <= 10^5", "0 <= b.length <= 10^5", "a.length == m + b.length", "1 <= a.length",
                  "-10^9 <= values <= 10^9", "the first m entries of a and all of b are in non-decreasing order"],
 hints=["Merging from the front means writing into slot 0, which still holds a reading you need. Where else could the first write go?",
        "Which of the two logs holds the largest remaining reading, and which slot does it belong in?",
        "When one log runs out, is there anything left to do for the other?"],
 trigger="“Merge into an array that already holds one of the inputs” → walk and write from the back.",
 examples=[([[1,4,7,0,0],3,[2,5]],[1,2,4,5,7],"7 is the largest, so it goes into the last slot; then 5, then 4, and so on."),
           ([[3,0],1,[1]],[1,3],""),
           ([[0],0,[9]],[9],"The first log is empty, so only b's reading is left.")],
 tests=[[[2,0],1,[1]],[[1,2,0,0],2,[0,0]],[[5,0,0],1,[1,9]],[[0,0],0,[1,2]],[[-1,0],1,[-2]],[[4],1,[]]],
 gen=[{"seed":2101,"count":3,"args":[buffer_of(100000,100000,-1000000000,1000000000),K(100000),arr(100000,-1000000000,1000000000,sorted=True)]},
      {"seed":2102,"count":1,"args":[buffer_of(1,100000,-1000,1000),K(1),arr(100000,-1000,1000,sorted=True)]},
      {"seed":2103,"count":1,"args":[buffer_of(100000,1,-1000,1000),K(100000),arr(1,-1000,1000,sorted=True)]}],
 cross=[{"seed":201,"count":100,"args":[buffer_of(3,2,-9,9),K(3),arrr(2,2,-9,9,sorted=True)]},
        {"seed":202,"count":100,"args":[buffer_of(1,4,-5,5),K(1),arrr(4,4,-5,5,sorted=True)]},
        {"seed":203,"count":100,"args":[buffer_of(0,3,-5,5),K(0),arrr(3,3,-5,5,sorted=True)]},
        {"seed":204,"count":100,"args":[buffer_of(5,1,-4,4),K(5),arrr(1,1,-4,4,sorted=True)]}],
 ref="""
    public void mergeInto(int[] a, int m, int[] b) {
        int i = m - 1, j = b.length - 1, write = a.length - 1;
        while (j >= 0) {
            if (i >= 0 && a[i] > b[j]) a[write--] = a[i--];
            else a[write--] = b[j--];
        }
    }""",
 brute="""
    public void mergeInto(int[] a, int m, int[] b) {
        int filled = m;
        for (int x : b) {
            int at = filled;
            while (at > 0 && a[at - 1] > x) {         // make room by shifting the bigger values up
                a[at] = a[at - 1];
                at--;
            }
            a[at] = x;
            filled++;
        }
    }""")


prob(slug="appears-in-order", stage=1, title="Does the Word Appear in Order?", difficulty="Easy",
 whats="Two sequences, one pointer each: advance the word's pointer only on a match.",
 f=fn("appearsInOrder", "boolean", ("String", "text"), ("String", "word")),
 statement="""
A spam filter looks for a banned word hidden inside a message. The letters do not have to be next to each other, but they must appear **in order**.

Return `true` if every letter of `word` can be found inside `text`, left to right, each letter used at most once. An empty `word` always appears.
""", constraints=["1 <= text.length <= 10^5", "0 <= word.length <= 10^5",
                  "text and word consist of lowercase English letters"],
 hints=["Walk through the text one letter at a time. What is the only thing you need to remember about the word?",
        "When the current text letter is the one you are looking for, what changes? And when it is not?",
        "Is it ever worth skipping a letter of the text that does match what you need?"],
 trigger="“Is one sequence hidden inside another, in order?” → a pointer in each, and only the small one waits for a match.",
 examples=[(["abracadabra","aaa"],True,"The text has five a's, so three of them can be picked out in order."),
           (["abcdef","afc"],False,"After the f there is no c left."),
           (["banana",""],True,"")],
 tests=[["a","a"],["a","b"],["ab","abc"],["aaa","aaaa"],["abc",""],["aabbcc","abc"]],
 gen=[{"seed":2201,"count":2,"args":[S(100000,"abc"),subseq(0,50000,0.5,"abc")]},
      {"seed":2202,"count":1,"args":[S(100000,"ab"),subseq(0,99000,0.5,"ab")]},
      {"seed":2203,"count":1,"args":[S(100000,"abcdefghijklmnopqrstuvwxyz"),subseq(0,100000,0.0)]}],
 cross=[{"seed":211,"count":250,"args":[Sr(1,12,"ab"),subseq(0,4,0.5,"ab")]},
        {"seed":212,"count":150,"args":[Sr(1,8,"abc"),Sr(0,6,"abc")]}],
 ref="""
    public boolean appearsInOrder(String text, String word) {
        int want = 0;
        for (int i = 0; i < text.length() && want < word.length(); i++)
            if (text.charAt(i) == word.charAt(want)) want++;
        return want == word.length();
    }""",
 brute="""
    public boolean appearsInOrder(String text, String word) {
        int at = -1;
        for (int k = 0; k < word.length(); k++) {
            at = text.indexOf(word.charAt(k), at + 1);   // leftmost match after the previous one
            if (at < 0) return false;
        }
        return true;
    }""")

# ============================== Stage 3: sort first, then pointers ==============================
prob(slug="three-sum-zero", stage=2, title="Triples That Cancel Out", difficulty="Medium",
 whats="Sort, fix one number, and run the sorted pair search on the rest; skipping equal neighbours at both levels keeps the triples distinct.",
 f=fn("threeSumZero", "List<List<Integer>>", ("int[]", "nums")),
 compare="UNORDERED_DEEP",
 statement="""
An accountant wants to cancel entries against each other three at a time: three entries whose amounts add up to exactly zero.

Return every **distinct** triple of values from `nums` that sums to `0`. Two triples count as the same if they use the same three values, so each set of values must appear once. The triples, and the numbers inside each triple, may be returned in any order.
""", constraints=["3 <= nums.length <= 3000", "-10^5 <= nums[i] <= 10^5"],
 hints=["Checking every triple is three nested loops. If the list were sorted, which earlier problem could handle the inner two?",
        "After fixing the first number, what exactly are you looking for in the rest of the list?",
        "Equal values next to each other would produce the same triple twice. Where do you have to guard against that?"],
 trigger="“Find triples with a given sum” → sort, fix one, two pointers on the rest, and skip equal neighbours.",
 examples=[([[-3,1,2,0,3,-1]],[[-3,1,2],[-3,0,3],[-1,0,1]],"Three sets of values cancel out; any order of the triples is fine."),
           ([[0,0,0,0]],[[0,0,0]],"There is only one distinct triple even though there are four zeros."),
           ([[1,2,3]],[],"")],
 tests=[[[0,0,0]],[[1,1,1]],[[-1,-1,2]],[[-2,0,1,1]],[[100000,-100000,0]],[[-1,0,1,0]]],
 gen=[{"seed":2301,"count":1,"args":[arr(3000,-100000,100000)]},
      {"seed":2302,"count":1,"args":[arr(3000,-50,50)]},
      {"seed":2303,"count":1,"args":[choice(3000,[0,0,0,0,1,-1,2,-2])]},
      {"seed":2304,"count":1,"args":[arr(3000,-3,3)]}],
 cross=[{"seed":221,"count":250,"args":[arrr(3,10,-5,5)]},
        {"seed":222,"count":150,"args":[choice_r(3,8,[0,1,-1,2,-2])]}],
 ref="""
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
    }""",
 brute="""
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
    }""")

prob(slug="three-sum-closest", stage=2, title="Triple Closest to a Target", difficulty="Medium",
 whats="The same sorted loop, but instead of looking for an exact hit you keep the closest sum you have seen.",
 f=fn("threeSumClosest", "int", ("int[]", "nums"), ("int", "target")),
 statement="""
A courier can load exactly three parcels and wants the total weight as close as possible to a target weight.

Return the sum of three entries of `nums` whose total is nearest to `target`. If two different totals are **equally** near, return the **smaller** of the two.
""", constraints=["3 <= nums.length <= 1000", "-10^5 <= nums[i] <= 10^5", "-10^5 <= target <= 10^5"],
 hints=["Sorting lets you walk two pointers inwards. What tells you which pointer to move when the sum is too small?",
        "You are no longer looking for one particular sum. What do you have to carry along as you walk?",
        "Two totals can be the same distance from the target on opposite sides. Which one does the statement ask for?"],
 trigger="“Closest sum rather than an exact sum” → the same sorted two-pointer sweep, tracking the best distance.",
 examples=[([[-2,1,3,5],4],4,"−2 + 1 + 5 is exactly 4."),
           ([[1,1,1,5],5],3,"The only totals are 3 and 7, both two away from 5, so the smaller one wins."),
           ([[2,3,8],1],13,"There is only one triple.")],
 tests=[[[0,0,0],0],[[1,2,3],100],[[-1,-1,-1],0],[[100000,100000,100000],0],[[1,1,1,2,2],5],[[0,0,1,2],2]],
 gen=[{"seed":2401,"count":6,"args":[arr(1000,-100000,100000),I(-100000,100000)]},
      {"seed":2402,"count":4,"args":[arr(1000,-50,50),I(-20,20)]},
      {"seed":2403,"count":2,"args":[arr(1000,-2,2),K(1)]}],
 cross=[{"seed":231,"count":250,"args":[arrr(3,9,-9,9),I(-12,12)]},
        {"seed":232,"count":150,"args":[arrr(3,6,-3,3),I(-4,4)]}],
 ref="""
    public int threeSumClosest(int[] nums, int target) {
        int[] a = nums.clone();
        Arrays.sort(a);
        int bestSum = a[0] + a[1] + a[2];
        long bestGap = Math.abs((long) bestSum - target);
        for (int i = 0; i < a.length - 2; i++) {
            int left = i + 1, right = a.length - 1;
            while (left < right) {
                int sum = a[i] + a[left] + a[right];
                long gap = Math.abs((long) sum - target);
                if (gap < bestGap || (gap == bestGap && sum < bestSum)) {
                    bestGap = gap;
                    bestSum = sum;
                }
                if (sum == target) return sum;                   // nothing can be closer
                if (sum < target) left++;
                else right--;
            }
        }
        return bestSum;
    }""",
 brute="""
    public int threeSumClosest(int[] nums, int target) {
        int n = nums.length;
        int bestSum = nums[0] + nums[1] + nums[2];
        long bestGap = Math.abs((long) bestSum - target);
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++)
                for (int k = j + 1; k < n; k++) {
                    int sum = nums[i] + nums[j] + nums[k];
                    long gap = Math.abs((long) sum - target);
                    if (gap < bestGap || (gap == bestGap && sum < bestSum)) {
                        bestGap = gap;
                        bestSum = sum;
                    }
                }
        return bestSum;
    }""")

prob(slug="count-triangles", stage=2, title="Count Possible Triangles", difficulty="Medium",
 whats="Fix the largest side instead of the smallest, and a pair that works tells you r − l pairs work at once.",
 f=fn("countTriangles", "long", ("int[]", "sides")),
 statement="""
A workshop has a pile of sticks and wants to know how many different sets of three sticks could be laid out as a triangle with no gaps and no overlap.

Count the triples of positions in `sides` whose three lengths can form a triangle. Three lengths work exactly when each one is shorter than the other two added together. Some sticks have length `0`.
""", constraints=["1 <= sides.length <= 3000", "0 <= sides[i] <= 10^6"],
 hints=["Sort the sticks. If you already know which stick is the longest of the three, how many of the three conditions still need checking?",
        "With the longest stick fixed, you need two shorter ones that together beat it. Where do you put the two pointers?",
        "When the pair at l and r is long enough, what can you say about l paired with everything between l and r?"],
 trigger="“Count triples satisfying an inequality” → sort, fix the largest, then count pairs with two pointers.",
 examples=[([[2,2,3,4]],3,"The 2-2-3 set works, and so does 2-3-4 with either of the two 2s; 2-2-4 does not."),
           ([[1,1,3]],0,"1 + 1 is not longer than 3."),
           ([[0,1,1]],0,"A stick of length 0 can never be part of a triangle.")],
 tests=[[[1,1,1]],[[0,0,0]],[[5,5,5,5]],[[1,2,3]],[[1000000,1000000,1000000]],[[0,0,1,1]]],
 gen=[{"seed":2501,"count":1,"args":[arr(3000,1,1000000)]},
      {"seed":2502,"count":1,"args":[arr(3000,1,5)]},
      {"seed":2503,"count":1,"args":[choice(3000,[0,0,1,2,3,5,8,13])]},
      {"seed":2504,"count":1,"args":[arr(3000,1000,1001)]}],
 cross=[{"seed":241,"count":250,"args":[arrr(1,10,0,9)]},
        {"seed":242,"count":150,"args":[arrr(3,8,0,3)]}],
 ref="""
    public long countTriangles(int[] sides) {
        int[] a = sides.clone();
        Arrays.sort(a);
        long count = 0;
        for (int longest = a.length - 1; longest >= 2; longest--) {
            int left = 0, right = longest - 1;
            while (left < right) {
                if ((long) a[left] + a[right] > a[longest]) {
                    count += right - left;               // a[left] works with everything up to a[right]
                    right--;
                } else left++;
            }
        }
        return count;
    }""",
 brute="""
    public long countTriangles(int[] sides) {
        long count = 0;
        int n = sides.length;
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++)
                for (int k = j + 1; k < n; k++) {
                    long x = sides[i], y = sides[j], z = sides[k];
                    if (x + y > z && x + z > y && y + z > x) count++;
                }
        return count;
    }""")

prob(slug="min-boats", stage=2, title="Fewest Boats", difficulty="Medium",
 whats="A greedy rule after sorting: the heaviest passenger shares with the lightest if they fit, and otherwise rides alone.",
 f=fn("minBoats", "int", ("int[]", "weights"), ("int", "limit")),
 statement="""
A ferry runs boats that hold **at most two** people and can carry at most `limit` kilograms in total. Everybody weighs no more than `limit`, so everyone can be carried somehow.

Return the smallest number of boats needed to take everybody across.
""", constraints=["1 <= weights.length <= 10^5", "1 <= weights[i] <= limit <= 10^9"],
 hints=["Think about the heaviest passenger. Who is the best possible companion for them?",
        "If even the lightest passenger cannot share with the heaviest one, what does that settle?",
        "Once you have dealt with the heaviest passenger, what does the rest of the problem look like?"],
 trigger="“Pair items up under a limit, fewest groups” → sort, then pair the two ends greedily.",
 examples=[([[1,2],3],1,"Together they weigh exactly the limit."),
           ([[3,2,2,1],3],3,"1 shares with 2; the other 2 and the 3 each need their own boat."),
           ([[3,5,3,4],5],4,"No two of them fit together.")],
 tests=[[[1],1],[[1,1],2],[[2,2],2],[[1,1,1],2],[[5,1,4,2],6],[[1,2,3,4,5],5]],
 gen=[{"seed":2601,"count":2,"args":[arr(100000,1,1000),K(1000)]},
      {"seed":2602,"count":1,"args":[arr(100000,1,500),K(1000)]},
      {"seed":2603,"count":1,"args":[arr(100000,500,1000),K(1000)]}],
 cross=[{"seed":251,"count":250,"args":[arrr(1,10,1,6),I(6,12)]},
        {"seed":252,"count":150,"args":[arrr(1,8,1,3),I(3,6)]}],
 ref="""
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
    }""",
 brute="""
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
    }""")

prob(slug="max-pair-removals", stage=2, title="Most Pairs Removed", difficulty="Medium",
 whats="A match now consumes both pointers at once, because each value can only be spent one time.",
 f=fn("maxPairRemovals", "int", ("int[]", "nums"), ("int", "k")),
 statement="""
A card game lets you discard two cards whenever their values add up to exactly `k`. Each card can only be discarded once.

Return the largest number of discards you can make.
""", constraints=["1 <= nums.length <= 10^5", "1 <= nums[i] <= 10^9", "2 <= k <= 2 * 10^9"],
 hints=["Sort the cards. Starting from the two ends, what does a total that is too small tell you?",
        "What has to happen to both pointers when you do find a total of exactly k?",
        "Why can you never regret discarding a pair as soon as you find one?"],
 trigger="“Remove pairs with an exact sum, as many as possible” → sort, then two pointers that both step in on a match.",
 examples=[([[1,2,3,4],5],2,"1 with 4, and 2 with 3."),
           ([[3,1,3,4,3],6],1,"Only one pair of 3s can be made from the three of them."),
           ([[1,1],3],0,"")],
 tests=[[[1],1],[[1,1],2],[[1,2],3],[[5,5,5],10],[[2,2,2,2],4],[[1,9,2,8,3],10]],
 gen=[{"seed":2701,"count":2,"args":[arr(100000,1,1000),K(1001)]},
      {"seed":2702,"count":1,"args":[arr(100000,1,1),K(2)]},
      {"seed":2703,"count":1,"args":[arr(100000,1,1000000000),K(1000000000)]}],
 cross=[{"seed":261,"count":250,"args":[arrr(1,10,1,6),I(2,12)]},
        {"seed":262,"count":150,"args":[arrr(1,8,1,3),I(2,6)]}],
 ref="""
    public int maxPairRemovals(int[] nums, int k) {
        int[] a = nums.clone();
        Arrays.sort(a);
        int left = 0, right = a.length - 1, discards = 0;
        while (left < right) {
            long sum = (long) a[left] + a[right];
            if (sum == k) {
                discards++;
                left++;
                right--;
            } else if (sum < k) left++;
            else right--;
        }
        return discards;
    }""",
 brute="""
    public int maxPairRemovals(int[] nums, int k) {
        int n = nums.length, discards = 0;
        boolean[] gone = new boolean[n];
        while (true) {
            int a = -1, b = -1;
            for (int i = 0; i < n && a < 0; i++) {
                if (gone[i]) continue;
                for (int j = i + 1; j < n; j++)
                    if (!gone[j] && (long) nums[i] + nums[j] == k) { a = i; b = j; break; }
            }
            if (a < 0) return discards;                  // no pair left anywhere
            gone[a] = true;
            gone[b] = true;
            discards++;
        }
    }""")

# ============================== Stage 4: moving by a greedy rule ==============================
prob(slug="widest-container", stage=3, title="Widest Container", difficulty="Medium",
 whats="Start at the widest pair and always move the shorter wall: the taller one cannot help while the short one caps the height.",
 f=fn("maxWater", "long", ("int[]", "heights")),
 statement="""
A row of vertical walls stands on a flat floor, `heights[i]` tall at position `i`. Picking two walls and flooding the space between them holds water up to the height of the **shorter** wall, over a width equal to the distance between them.

Return the largest amount of water any two walls can hold.
""", constraints=["2 <= heights.length <= 10^5", "0 <= heights[i] <= 10^9"],
 hints=["Start with the two outermost walls. What is the only way to make the width bigger?",
        "Since width can only shrink, the height has to grow to compensate. Which of the two walls is holding the height back?",
        "Why is it safe to discard the shorter wall and never look at it again?"],
 trigger="“Best pair where the value depends on the weaker end” → start at both ends and always move the weaker one.",
 examples=[([[2,1,5,6,2,3]],10,"The first and last walls are 5 apart, and the shorter of them is 2."),
           ([[4,0,4]],8,"The two walls of height 4 are 2 apart."),
           ([[1,1]],1,"")],
 tests=[[[0,0]],[[1,2]],[[5,5,5]],[[1,1000000000]],[[1000000000,1000000000]],[[3,1,1,1,3]]],
 gen=[{"seed":2801,"count":2,"args":[arr(100000,0,1000000000)]},
      {"seed":2802,"count":1,"args":[arr(100000,0,10)]},
      {"seed":2803,"count":1,"args":[arr(100000,1000000000,1000000000)]}],
 cross=[{"seed":271,"count":250,"args":[arrr(2,10,0,9)]},
        {"seed":272,"count":150,"args":[arrr(2,6,0,3)]}],
 ref="""
    public long maxWater(int[] heights) {
        int left = 0, right = heights.length - 1;
        long best = 0;
        while (left < right) {
            long height = Math.min(heights[left], heights[right]);
            best = Math.max(best, height * (right - left));
            if (heights[left] < heights[right]) left++;
            else right--;
        }
        return best;
    }""",
 brute="""
    public long maxWater(int[] heights) {
        long best = 0;
        for (int i = 0; i < heights.length; i++)
            for (int j = i + 1; j < heights.length; j++)
                best = Math.max(best, (long) Math.min(heights[i], heights[j]) * (j - i));
        return best;
    }""")

prob(slug="trapped-rain", stage=3, title="Trapped Rain", difficulty="Hard",
 whats="The water over one position depends on the tallest wall on each side, and the side with the smaller running maximum is already decided.",
 f=fn("trappedRain", "long", ("int[]", "heights")),
 statement="""
Rain falls on a row of blocks of different heights and collects in the dips. Above position `i` the water rises to the level of the lower of the two tallest blocks on either side of it, and whatever is below the block itself does not count.

Return the total amount of water that stays behind after the rain.
""", constraints=["1 <= heights.length <= 10^5", "0 <= heights[i] <= 10^5"],
 hints=["Write down, for one position, exactly which two numbers decide how deep the water is there.",
        "Walking in from both ends, you know the tallest block seen so far on each side. Which of those two is certainly the true maximum for its side?",
        "So which pointer is safe to settle and move on?"],
 trigger="“Each position depends on a maximum from both sides” → two pointers carrying a running maximum each.",
 examples=[([[3,0,2,0,4]],7,"Three units of water in each dip beside the 2, and one unit on top of it."),
           ([[2,1,2]],1,""),
           ([[1,2,3]],0,"Water runs straight off a slope.")],
 tests=[[[0]],[[5]],[[1,0,1]],[[0,0,0]],[[5,0,0,0,5]],[[3,2,1,2,3]]],
 gen=[{"seed":2901,"count":2,"args":[arr(100000,0,100000)]},
      {"seed":2902,"count":1,"args":[arr(100000,0,3)]},
      {"seed":2903,"count":1,"args":[{"kind":"bits","n":100000}]}],
 cross=[{"seed":281,"count":250,"args":[arrr(1,10,0,6)]},
        {"seed":282,"count":150,"args":[arrr(1,8,0,2)]}],
 ref="""
    public long trappedRain(int[] heights) {
        int left = 0, right = heights.length - 1, maxLeft = 0, maxRight = 0;
        long water = 0;
        while (left < right) {
            if (heights[left] < heights[right]) {
                maxLeft = Math.max(maxLeft, heights[left]);
                water += maxLeft - heights[left];
                left++;
            } else {
                maxRight = Math.max(maxRight, heights[right]);
                water += maxRight - heights[right];
                right--;
            }
        }
        return water;
    }""",
 brute="""
    public long trappedRain(int[] heights) {
        long water = 0;
        for (int i = 0; i < heights.length; i++) {
            int tallestLeft = 0, tallestRight = 0;
            for (int j = 0; j <= i; j++) tallestLeft = Math.max(tallestLeft, heights[j]);
            for (int j = i; j < heights.length; j++) tallestRight = Math.max(tallestRight, heights[j]);
            water += Math.min(tallestLeft, tallestRight) - heights[i];
        }
        return water;
    }""")

prob(slug="three-colors", stage=3, title="Three Colours in One Pass", difficulty="Medium",
 whats="Three pointers split the array into settled 0s, settled 1s, an unknown middle and settled 2s, so one pass sorts it with no counting.",
 f=fn("sortColors", "void", ("int[]", "nums"), out=0),
 statement="""
A conveyor carries parts marked `0`, `1` or `2`, and they have to come out grouped in that order.

Sort `nums` **in place**. Do it in a single pass over the array and with only a few variables: no counting how many of each there are, and no library sort. Your method returns nothing; the array itself is the answer.
""", constraints=["1 <= nums.length <= 10^5", "nums[i] is 0, 1 or 2"],
 hints=["Imagine the array split into four zones: finished 0s, finished 1s, parts you have not looked at, and finished 2s. Where are the boundaries?",
        "You pick up the first unknown part. What do you do with it if it is a 0? A 1? A 2?",
        "One of those three cases must not advance your reading position. Which one, and why?"],
 trigger="“Sort values from a tiny fixed set in one in-place pass” → a pointer per boundary (the Dutch flag split).",
 examples=[([[1,2,0,1]],[0,1,1,2],"The 0 moves to the front and the 2 to the back."),
           ([[2,0]],[0,2],""),
           ([[1,1,1]],[1,1,1],"Already grouped.")],
 tests=[[[0]],[[2,1,0]],[[0,0,2,2,1,1]],[[2,2,2,0]],[[1,0]],[[2,0,1]]],
 gen=[{"seed":3001,"count":2,"args":[choice(100000,[0,1,2])]},
      {"seed":3002,"count":1,"args":[choice(100000,[0,0,1,2,2])]},
      {"seed":3003,"count":1,"args":[choice(100000,[2,2,2,1,0])]}],
 cross=[{"seed":291,"count":250,"args":[choice_r(1,10,[0,1,2])]},
        {"seed":292,"count":150,"args":[choice_r(1,6,[0,2])]}],
 ref="""
    public void sortColors(int[] nums) {
        int low = 0, at = 0, high = nums.length - 1;
        while (at <= high) {
            if (nums[at] == 0) {
                int t = nums[low];
                nums[low++] = nums[at];
                nums[at++] = t;
            } else if (nums[at] == 2) {
                int t = nums[high];
                nums[high--] = nums[at];
                nums[at] = t;                            // the swapped-in part is still unknown
            } else at++;
        }
    }""",
 brute="""
    public void sortColors(int[] nums) {
        int[] howMany = new int[3];
        for (int x : nums) howMany[x]++;
        int at = 0;
        for (int colour = 0; colour < 3; colour++)
            for (int t = 0; t < howMany[colour]; t++) nums[at++] = colour;
    }""")

prob(slug="next-arrangement", stage=3, title="Next Arrangement", difficulty="Medium",
 whats="Scanning from the right finds the one position worth changing, and the tail after it is already descending, so reversing it is enough.",
 f=fn("nextPermutation", "void", ("int[]", "nums"), out=0),
 statement="""
A combination lock shows a row of digits. Pressing “next” moves it to the very next arrangement of the **same** numbers in increasing order, as if all the arrangements were listed smallest to largest. From the largest arrangement it wraps round to the smallest.

Rearrange `nums` **in place** into that next arrangement. Values may repeat. Your method returns nothing; the array itself is the answer.
""", constraints=["1 <= nums.length <= 10^5", "0 <= nums[i] <= 10^9"],
 hints=["If the numbers decrease all the way from left to right, there is nothing bigger to go to. What is the answer then?",
        "Otherwise, scanning from the right, you reach a position that is smaller than its neighbour. Why is that the leftmost position that has to change?",
        "Once that position holds its new value, the rest must be as small as possible. What do you already know about the order of the rest?"],
 trigger="“Next arrangement in order” → from the right find the dip, swap with its next larger value, reverse the tail.",
 examples=[([[1,2,3]],[1,3,2],"Swapping the last two gives the next arrangement."),
           ([[3,2,1]],[1,2,3],"This is the largest arrangement, so it wraps round to the smallest."),
           ([[1,1,5]],[1,5,1],"")],
 tests=[[[1]],[[1,2]],[[2,1]],[[1,5,1]],[[1,3,2]],[[2,2,2]]],
 gen=[{"seed":3101,"count":2,"args":[arr(100000,0,1000000000)]},
      {"seed":3102,"count":1,"args":[{"kind":"bits","n":100000}]},
      {"seed":3103,"count":1,"args":[arr(100000,0,1000000,sorted=True)]}],
 cross=[{"seed":301,"count":250,"args":[arrr(1,8,0,3)]},
        {"seed":302,"count":150,"args":[arrr(1,6,0,1)]}],
 ref="""
    public void nextPermutation(int[] nums) {
        int n = nums.length, dip = n - 2;
        while (dip >= 0 && nums[dip] >= nums[dip + 1]) dip--;
        if (dip >= 0) {
            int swapWith = n - 1;                        // rightmost value bigger than nums[dip]
            while (nums[swapWith] <= nums[dip]) swapWith--;
            int t = nums[dip];
            nums[dip] = nums[swapWith];
            nums[swapWith] = t;
        }
        for (int left = dip + 1, right = n - 1; left < right; left++, right--) {
            int t = nums[left];
            nums[left] = nums[right];
            nums[right] = t;
        }
    }""",
 brute="""
    public void nextPermutation(int[] nums) {
        int n = nums.length, dip = -1;
        for (int i = n - 2; i >= 0; i--) if (nums[i] < nums[i + 1]) { dip = i; break; }
        if (dip < 0) {                                   // already the largest: wrap to the smallest
            Arrays.sort(nums);
            return;
        }
        int pick = -1;                                   // smallest value after dip that still beats it
        for (int j = dip + 1; j < n; j++)
            if (nums[j] > nums[dip] && (pick < 0 || nums[j] <= nums[pick])) pick = j;
        int t = nums[dip];
        nums[dip] = nums[pick];
        nums[pick] = t;
        Arrays.sort(nums, dip + 1, n);                   // make the tail as small as possible
    }""")

# ============================== Stage 5: two sequences ==============================
prob(slug="backspace-equal", stage=4, title="Same After Backspaces", difficulty="Easy",
 whats="Walking both strings from the back lets a counter absorb the backspaces, so you compare one real character at a time with no extra memory.",
 f=fn("backspaceEqual", "boolean", ("String", "a"), ("String", "b")),
 statement="""
Two people type a word into the same broken form, where `#` is the backspace key: it deletes the character just typed, or does nothing if there is nothing left.

Return `true` if both of them end up with the same text.
""", constraints=["1 <= a.length, b.length <= 10^5",
                  "a and b consist of lowercase English letters and the character '#'"],
 hints=["Reading forwards, you cannot tell whether a character survives until you have seen what comes after it. Which direction removes that problem?",
        "Going backwards, what should you do when you meet a backspace, and what when you meet a letter while backspaces are still owed?",
        "What has to be true when one string runs out before the other?"],
 trigger="“Compare two sequences with deletions” → walk both from the back, carrying a skip count.",
 examples=[(["chat##s","chs"],True,"The two backspaces delete t and a, leaving chs."),
           (["cat","car"],False,""),
           (["a##b","b"],True,"The first backspace deletes a and the second has nothing to delete.")],
 tests=[["#","#"],["a#","b#"],["a","a#"],["##a","a"],["ab#","a"],["a#b","b"]],
 gen=[{"seed":3201,"count":2,"args":[S(100000,"abc###"),typed_again(0,2000,0.5,"abc")]},
      {"seed":3202,"count":1,"args":[S(100000,"ab#"),typed_again(0,5000,0.0,"ab")]},
      {"seed":3203,"count":1,"args":[S(100000,"a#"),typed_again(0,100,1.0,"ab")]}],
 cross=[{"seed":311,"count":250,"args":[Sr(1,10,"ab##"),typed_again(0,2,0.6,"ab")]},
        {"seed":312,"count":150,"args":[Sr(1,8,"ab#"),Sr(1,8,"ab#")]}],
 ref="""
    public boolean backspaceEqual(String a, String b) {
        int i = a.length() - 1, j = b.length() - 1;
        while (true) {
            i = settle(a, i);
            j = settle(b, j);
            if (i < 0 || j < 0) return i < 0 && j < 0;
            if (a.charAt(i) != b.charAt(j)) return false;
            i--;
            j--;
        }
    }

    /** Walks back to the next character that actually survives, or past the start. */
    private int settle(String s, int at) {
        int owed = 0;
        while (at >= 0) {
            if (s.charAt(at) == '#') { owed++; at--; }
            else if (owed > 0) { owed--; at--; }
            else break;
        }
        return at;
    }""",
 brute="""
    public boolean backspaceEqual(String a, String b) {
        return typed(a).equals(typed(b));
    }

    private String typed(String s) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '#') { if (sb.length() > 0) sb.deleteCharAt(sb.length() - 1); }
            else sb.append(c);
        }
        return sb.toString();
    }""")

prob(slug="interval-overlaps", stage=4, title="Where Two Timetables Overlap", difficulty="Medium",
 whats="One pointer per list: intersect the pair you are looking at, then advance whichever interval finishes first.",
 f=fn("intervalIntersections", "int[][]", ("int[][]", "a"), ("int[][]", "b")),
 statement="""
Two colleagues each hand in a list of the periods they are free, sorted and with no overlaps inside either list. You want every period when **both** of them are free.

Each interval `[start, end]` includes both ends, so two periods that merely touch at one instant overlap in that single instant, which counts as `[x, x]`. Return the overlapping periods in order.
""", constraints=["1 <= a.length, b.length <= 10^5", "0 <= start <= end <= 10^9",
                  "each list is sorted by start and its own intervals never overlap"],
 hints=["Take the first interval of each list. What are the start and the end of the period they share, if any?",
        "If they do not overlap at all, which of the two can you throw away?",
        "After dealing with a pair, one of the two intervals might still overlap the next interval of the other list. Which one?"],
 trigger="“Intersect two sorted interval lists” → a pointer in each, advancing the one that ends first.",
 examples=[([[[1,4],[7,9]],[[2,3],[5,8]]],[[2,3],[7,8]],"They share 2 to 3 and 7 to 8."),
           ([[[1,3]],[[3,5]]],[[3,3]],"The periods only touch, at the single instant 3."),
           ([[[1,2]],[[5,6]]],[],"")],
 tests=[[[[0,0]],[[0,0]]],[[[1,10]],[[2,3],[5,6]]],[[[1,2],[3,4]],[[2,3]]],[[[1,2]],[[3,4]]],[[[5,9]],[[1,3]]],[[[0,1000000000]],[[7,7]]]],
 gen=[{"seed":3301,"count":2,"args":[intervals(100000,5,4),intervals(100000,5,4)]},
      {"seed":3302,"count":1,"args":[intervals(100000,1,1),intervals(100000,3,6)]},
      {"seed":3303,"count":1,"args":[intervals(100000,20,2),intervals(100000,2,20)]}],
 cross=[{"seed":321,"count":250,"args":[intervals(4,3,3),intervals(4,3,3)]},
        {"seed":322,"count":150,"args":[intervals(3,1,2),intervals(5,2,1)]}],
 ref="""
    public int[][] intervalIntersections(int[][] a, int[][] b) {
        List<int[]> out = new ArrayList<>();
        int i = 0, j = 0;
        while (i < a.length && j < b.length) {
            int start = Math.max(a[i][0], b[j][0]), end = Math.min(a[i][1], b[j][1]);
            if (start <= end) out.add(new int[]{start, end});
            if (a[i][1] < b[j][1]) i++;
            else j++;
        }
        return out.toArray(new int[0][]);
    }""",
 brute="""
    public int[][] intervalIntersections(int[][] a, int[][] b) {
        List<int[]> out = new ArrayList<>();
        for (int[] x : a)
            for (int[] y : b) {
                int start = Math.max(x[0], y[0]), end = Math.min(x[1], y[1]);
                if (start <= end) out.add(new int[]{start, end});
            }
        return out.toArray(new int[0][]);
    }""")

prob(slug="closest-pair-two-lists", stage=4, title="Closest Pair From Two Lists", difficulty="Medium",
 whats="With both lists sorted, moving the pointer at the smaller value is the only move that can close the gap.",
 f=fn("minAbsDifference", "long", ("int[]", "a"), ("int[]", "b")),
 statement="""
Two laboratories each report a batch of measurements. You want the closest agreement between them: one reading from each batch whose values differ as little as possible.

Return the smallest possible `|x − y|` over all choices of `x` from `a` and `y` from `b`.
""", constraints=["1 <= a.length, b.length <= 10^5", "-10^9 <= a[i], b[i] <= 10^9"],
 hints=["Comparing every reading with every other one is a pair of nested loops. What would sorting both lists buy you?",
        "You are looking at one reading from each list and the smaller one is from a. Could any later reading of b ever be closer to it?",
        "So which pointer should move, and what happens to the gap if you move the other one instead?"],
 trigger="“Closest pair across two lists” → sort both, then advance whichever side is currently smaller.",
 examples=[([[4,1,9],[12,6]],2,"4 and 6 are the closest pair."),
           ([[5],[5]],0,"The two batches agree exactly."),
           ([[-1000000000],[1000000000]],2000000000,"The gap does not fit in 32 bits.")],
 tests=[[[1],[2]],[[0],[0]],[[-5,-1],[-3]],[[1,2,3],[3,2,1]],[[1000000000],[-1000000000]],[[7,7],[7]]],
 gen=[{"seed":3401,"count":2,"args":[arr(100000,-1000000000,1000000000),arr(100000,-1000000000,1000000000)]},
      {"seed":3402,"count":1,"args":[arr(100000,1,1000),arr(100000,1000000,1001000)]},
      {"seed":3403,"count":1,"args":[arr(100000,0,0),arr(100000,1,1000000000)]}],
 cross=[{"seed":331,"count":250,"args":[arrr(1,10,-9,9),arrr(1,10,-9,9)]},
        {"seed":332,"count":150,"args":[arrr(1,6,-3,3),arrr(1,6,-3,3)]}],
 ref="""
    public long minAbsDifference(int[] a, int[] b) {
        int[] x = a.clone(), y = b.clone();
        Arrays.sort(x);
        Arrays.sort(y);
        int i = 0, j = 0;
        long best = Long.MAX_VALUE;
        while (i < x.length && j < y.length) {
            best = Math.min(best, Math.abs((long) x[i] - y[j]));
            if (x[i] < y[j]) i++;
            else j++;
        }
        return best;
    }""",
 brute="""
    public long minAbsDifference(int[] a, int[] b) {
        long best = Long.MAX_VALUE;
        for (int x : a)
            for (int y : b)
                best = Math.min(best, Math.abs((long) x - y));
        return best;
    }""")


def main():
    os.makedirs(ROOT, exist_ok=True)
    for i, p in enumerate(P, 1):
        d = os.path.join(ROOT, f"{i:02d}-{p['slug']}")
        os.makedirs(d, exist_ok=True)
        meta = {"slug": p["slug"], "topic": "two-pointers", "stage": p["stage"], "order": i, "title": p["title"],
                "difficulty": p["difficulty"], "whatsNew": p["whats"], "function": p["f"],
                "timeLimitMs": p.get("tl", 1000), "hints": p["hints"], "trigger": p["trigger"]}
        if p.get("compare"): meta["compare"] = p["compare"]
        with open(os.path.join(d, "problem.json"), "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=1)
        st = textwrap.dedent(p["statement"]).strip() + "\n\n**Constraints**\n" + "\n".join(f"- `{c}`" for c in p["constraints"]) + "\n"
        with open(os.path.join(d, "statement.md"), "w", encoding="utf-8") as f:
            f.write(st)
        for name, body in (("Solution.java", p["ref"]), ("Brute.java", p["brute"])):
            with open(os.path.join(d, name), "w", encoding="utf-8") as f:
                f.write("import java.util.*;\n\nclass Solution {" + body + "\n}\n")
        tests = {"examples": [{"input": a, "output": o, **({"explanation": e} if e else {})} for a, o, e in p["examples"]],
                 "tests": [{"input": t} for t in p["tests"]],
                 "generated": p["gen"], "crosscheck": p["cross"]}
        with open(os.path.join(d, "tests.json"), "w", encoding="utf-8") as f:
            json.dump(tests, f, ensure_ascii=False, separators=(",", ":"))
    print(len(P), "problems written")

if __name__ == "__main__":
    main()
