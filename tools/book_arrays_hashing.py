"""Authoring source for the Arrays & Hashing problem book.
Run:  python3 tools/book_arrays_hashing.py   -> writes problems/hashing/NN-slug/{problem.json,statement.md,Solution.java,Brute.java,tests.json}
Every problem has a reference solution AND a brute-force solution; `JudgeCli crosscheck` compares them on random inputs,
and `JudgeCli judge <slug> submit < Brute.java` must *reject* the brute force, so the intended idea is really required.
"""
import json, os, textwrap

ROOT = os.path.join(os.path.dirname(__file__), "..", "problems", "hashing")
P = []

def prob(**k):
    P.append(k)

def fn(name, returns, *params, out=None):
    f = {"name": name, "returns": returns, "params": [{"name": n, "type": t} for t, n in params]}
    if out is not None:
        f["outputArg"] = out
    return f

def arr(n, lo, hi):
    return {"kind": "intArray", "n": n, "min": lo, "max": hi}

def arrr(nmin, nmax, lo, hi):
    return {"kind": "intArray", "nMin": nmin, "nMax": nmax, "min": lo, "max": hi}

def upto_n(n, offset=0):
    """Values in 1..n (+ offset) - the shape the "array is the hash table" problems need."""
    return {"kind": "intArray", "n": n, "min": 1, "maxIsN": True, "maxOffset": offset}

def upto_n_r(nmin, nmax):
    return {"kind": "intArray", "nMin": nmin, "nMax": nmax, "min": 1, "maxIsN": True}

def I(lo, hi):
    return {"kind": "int", "min": lo, "max": hi}

def K(v):
    return {"kind": "const", "value": v}

def S(n, alpha):
    return {"kind": "string", "n": n, "alphabet": alpha}

def Sr(nmin, nmax, alpha):
    return {"kind": "string", "nMin": nmin, "nMax": nmax, "alphabet": alpha}

def choice(n, values):
    return {"kind": "choiceArray", "n": n, "values": values}

def choice_r(nmin, nmax, values):
    return {"kind": "choiceArray", "nMin": nmin, "nMax": nmax, "values": values}

def words(n, minlen, maxlen, alpha):
    return {"kind": "wordArray", "n": n, "minLen": minlen, "maxLen": maxlen, "alphabet": alpha}

def words_r(nmin, nmax, minlen, maxlen, alpha):
    return {"kind": "wordArray", "nMin": nmin, "nMax": nmax, "minLen": minlen, "maxLen": maxlen, "alphabet": alpha}

def shuffled(of, flip, alpha):
    return {"kind": "shuffleOf", "of": of, "flip": flip, "alphabet": alpha}

def sentence(of, wordlist, flip):
    return {"kind": "sentenceFor", "of": of, "words": wordlist, "flip": flip}

def grid(rows, cols, lo, hi):
    return {"kind": "intMatrix", "rows": rows, "cols": cols, "min": lo, "max": hi}

def grid_lines(n, lo, hi, copies):
    return {"kind": "gridWithEqualLines", "n": n, "min": lo, "max": hi, "copies": copies}

NATO = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel", "india", "juliet"]

# ============================== Stage 1: remember what you've seen ==============================
prob(slug="seen-before", stage=0, title="Seen Before?", difficulty="Easy",
 whats="The base idea of the whole topic: a hash set answers “have I met this already?” in one step.",
 f=fn("hasDuplicate", "boolean", ("int[]", "nums")),
 statement="""
The turnstile at a conference records the badge number of everyone who walks in, in order. Nobody is supposed to enter twice.

Return `true` if some badge number appears more than once in `nums`, and `false` if they are all different.
""", constraints=["1 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9"],
 hints=["Comparing every badge with every other badge takes about n²/2 comparisons. What would you need to remember instead, so that one look is enough?",
        "What does a HashSet tell you when you try to add something that is already in it?"],
 trigger="“Have I seen this value before?” → a hash set you add to as you walk.",
 examples=[([[4,1,7,4]],True,"Badge 4 shows up twice."),([[3,1,2]],False,""),([[9]],False,"A single badge cannot clash with anything.")],
 tests=[[[1,1]],[[-5,5,-5]],[[0,0]],[[1,2,3,4,5,6]],[[-1000000000,1000000000]]],
 # seed 27 is a worst case on purpose: its four arrays repeat nothing until index 80662, 97868, never and 66668,
 # which is what forces the nested-loop version to do ~1.5 * 10^10 comparisons.
 gen=[{"seed":27,"count":4,"args":[arr(100000,-1000000000,1000000000)]},
      {"seed":41,"count":4,"args":[arr(100000,-1000000000,1000000000)]},
      {"seed":1102,"count":1,"args":[arr(100000,1,1000000000)]}],
 cross=[{"seed":101,"count":250,"args":[arrr(1,12,-6,6)]},
        {"seed":102,"count":150,"args":[arrr(1,10,-1000,1000)]}],
 ref="""
    public boolean hasDuplicate(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        for (int x : nums) if (!seen.add(x)) return true;
        return false;
    }""",
 brute="""
    public boolean hasDuplicate(int[] nums) {
        for (int i = 0; i < nums.length; i++)
            for (int j = i + 1; j < nums.length; j++)
                if (nums[i] == nums[j]) return true;
        return false;
    }""")

prob(slug="first-repeat", stage=0, title="First Repeat", difficulty="Easy",
 whats="Same set, but you now report which value repeats — the first one you bump into going left to right.",
 f=fn("firstRepeat", "int", ("int[]", "nums")),
 statement="""
A card game deals cards one by one. The round ends the moment a value is dealt that has already been dealt earlier in the round.

Find the smallest index `j` such that `nums[j]` also appears somewhere before `j`, and return `nums[j]`. If no value ever repeats, return `-1`.
""", constraints=["1 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9"],
 hints=["You want the earliest position at which a repeat finishes, not the smallest repeated value. In which order should you walk the array?",
        "While walking, what single question do you need answered about everything to the left of you?"],
 trigger="“The first value that repeats” → scan once, asking a set about each value before adding it.",
 examples=[([[5,2,7,2,5]],2,"At index 3 the value 2 has been seen before; that is the earliest such index."),
           ([[1,2,3]],-1,""),([[4,4]],4,"")],
 tests=[[[7]],[[0,0,0]],[[-3,1,-3]],[[1,2,3,4,5]],[[-1,-2,-3,-2,-1]]],
 gen=[{"seed":27,"count":4,"args":[arr(100000,-1000000000,1000000000)]},   # see Seen Before?: the first repeat comes very late
      {"seed":1202,"count":1,"args":[arr(100000,1,1000000000)]}],
 cross=[{"seed":111,"count":250,"args":[arrr(1,12,-6,6)]},
        {"seed":112,"count":150,"args":[arrr(1,10,-1000,1000)]}],
 ref="""
    public int firstRepeat(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        for (int x : nums) if (!seen.add(x)) return x;
        return -1;
    }""",
 brute="""
    public int firstRepeat(int[] nums) {
        for (int j = 0; j < nums.length; j++)
            for (int i = 0; i < j; i++)
                if (nums[i] == nums[j]) return nums[j];
        return -1;
    }""")

prob(slug="pair-with-sum", stage=0, title="Pair With a Given Sum", difficulty="Easy",
 whats="A set only remembers that you saw a value; a map also remembers where, which is what lets you return indexes.",
 f=fn("pairWithSum", "int[]", ("int[]", "nums"), ("int", "target")),
 statement="""
A vending machine takes exactly two coins. Given the coin values `nums` and the price `target`, find two different coins whose values add up to the price.

Return `[i, j]` with `i < j` and `nums[i] + nums[j] == target`. If several pairs work, pick the one with the **smallest `j`**; if there is still a tie, pick the smallest `i`. Return `[-1, -1]` if no pair adds up to the price.
""", constraints=["1 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9", "-10^9 <= target <= 10^9"],
 hints=["Fix the second index j. There is only one value that could sit at i — which one?",
        "So while walking j from left to right, what should you have stored about every index before j?",
        "If the same value occurs twice to the left of j, which of the two indexes do you want to keep in the map?"],
 trigger="“Find a pair adding up to T” → map value → first index, then look up target − x.",
 examples=[([[2,7,4,5],9],[0,1],"2 + 7 = 9, and no pair finishes earlier than index 1."),
           ([[3,3,1],6],[0,1],""),([[1,2],8],[-1,-1],"")],
 tests=[[[5],10],[[0,0],0],[[-4,4],0],[[1,1,1],2],[[4,2,3,1],4],[[-1000000000,1000000000],0]],
 # a negative target against all-positive prices: there is no pair at all, so a nested loop never gets to stop early
 gen=[{"seed":1301,"count":4,"args":[arr(100000,1,1000000000),K(-5)]},
      {"seed":1302,"count":1,"args":[arr(100000,-1000000000,1000000000),I(-2000000,2000000)]},
      {"seed":1303,"count":1,"args":[arr(100000,1,200),I(399,401)]}],
 cross=[{"seed":121,"count":250,"args":[arrr(1,10,-8,8),I(-10,10)]},
        {"seed":122,"count":150,"args":[arrr(2,8,-3,3),I(-4,4)]}],
 ref="""
    public int[] pairWithSum(int[] nums, int target) {
        Map<Integer, Integer> firstIndex = new HashMap<>();
        for (int j = 0; j < nums.length; j++) {
            Integer i = firstIndex.get(target - nums[j]);
            if (i != null) return new int[]{i, j};
            firstIndex.putIfAbsent(nums[j], j);
        }
        return new int[]{-1, -1};
    }""",
 brute="""
    public int[] pairWithSum(int[] nums, int target) {
        for (int j = 0; j < nums.length; j++)
            for (int i = 0; i < j; i++)
                if ((long) nums[i] + nums[j] == target) return new int[]{i, j};
        return new int[]{-1, -1};
    }""")

prob(slug="count-equal-pairs", stage=0, title="Count Equal Pairs", difficulty="Medium",
 whats="From “does it repeat?” to “how often?”: a map of counts, where each new copy pairs with every earlier copy.",
 f=fn("countEqualPairs", "long", ("int[]", "nums")),
 statement="""
Everyone at a party writes down their favourite number. Two people are *twins* if they wrote the same number.

Return the number of index pairs `i < j` with `nums[i] == nums[j]`.
""", constraints=["1 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9"],
 hints=["If a value has already been written down 3 times and a fourth person writes it, how many new twin pairs appear?",
        "Walking left to right, should you add to the answer before or after recording the current value?",
        "How large can the answer get when all 100,000 numbers are equal — does it still fit in an int?"],
 trigger="“Count pairs of equal elements” → frequency map, add the count so far before increasing it.",
 examples=[([[1,2,1,1]],3,"The three 1s give the pairs (0,2), (0,3) and (2,3)."),
           ([[5,6,7]],0,""),([[2,2]],1,"")],
 tests=[[[9]],[[0,0,0,0]],[[-1,-1,2,-1]],[[1,2,3,4]],[[-5,5,-5,5]]],
 gen=[{"seed":1401,"count":2,"args":[arr(100000,1,50)]},
      {"seed":1402,"count":1,"args":[arr(100000,-1000000000,1000000000)]},
      {"seed":1403,"count":1,"args":[arr(100000,7,7)]}],
 cross=[{"seed":131,"count":250,"args":[arrr(1,12,-3,3)]},
        {"seed":132,"count":150,"args":[arrr(1,10,-1000,1000)]}],
 ref="""
    public long countEqualPairs(int[] nums) {
        Map<Integer, Integer> count = new HashMap<>();
        long pairs = 0;
        for (int x : nums) {
            int seen = count.getOrDefault(x, 0);
            pairs += seen;                 // x pairs with every earlier copy of x
            count.put(x, seen + 1);
        }
        return pairs;
    }""",
 brute="""
    public long countEqualPairs(int[] nums) {
        long pairs = 0;
        for (int i = 0; i < nums.length; i++)
            for (int j = i + 1; j < nums.length; j++)
                if (nums[i] == nums[j]) pairs++;
        return pairs;
    }""")

prob(slug="letter-budget", stage=0, title="Letter Budget", difficulty="Easy",
 whats="Counting with a budget: tally up what you have, then spend it one letter at a time.",
 f=fn("canBuild", "boolean", ("String", "note"), ("String", "letters")),
 statement="""
You want to spell out `note` using a bag of fridge magnets. The bag holds the letters of `letters`, and each magnet in the bag can be used **at most once**.

Return `true` if `note` can be spelled from the bag, otherwise `false`.
""", constraints=["1 <= note.length <= 10^5", "1 <= letters.length <= 10^5", "note and letters consist of lowercase English letters"],
 hints=["Does the order of the magnets in the bag matter at all? What about the order of the letters in the note?",
        "There are only 26 different letters. What would you store for each of them?",
        "Which direction is easier: counting what you need and comparing, or counting what you have and spending it?"],
 trigger="“Can X be built from the letters of Y?” → one tally of 26 counts, decrement while you spend.",
 examples=[(["badge","gabdeez"],True,"The bag has a b, an a, a d, a g and an e, which is exactly what the note needs."),
           (["aa","ab"],False,"The note needs two a's but the bag holds one."),
           (["xyz","zyx"],True,"")],
 tests=[["a","a"],["a","b"],["aaa","aa"],["abc","aabbcc"],["zyxzyx","xxyyzz"],["ab","b"]],
 gen=[{"seed":1501,"count":2,"args":[S(100000,"ab"),S(100000,"ab")]},
      {"seed":1502,"count":1,"args":[S(50000,"abc"),S(100000,"abc")]},
      {"seed":1503,"count":1,"args":[S(100000,"abcdefghijklmnopqrstuvwxyz"),S(100000,"abcdefghijklmnopqrstuvwxyz")]}],
 cross=[{"seed":141,"count":250,"args":[Sr(1,8,"abc"),Sr(1,8,"abc")]},
        {"seed":142,"count":150,"args":[Sr(1,6,"ab"),Sr(1,10,"ab")]}],
 ref="""
    public boolean canBuild(String note, String letters) {
        int[] have = new int[26];
        for (int i = 0; i < letters.length(); i++) have[letters.charAt(i) - 'a']++;
        for (int i = 0; i < note.length(); i++) if (--have[note.charAt(i) - 'a'] < 0) return false;
        return true;
    }""",
 brute="""
    public boolean canBuild(String note, String letters) {
        char[] bag = letters.toCharArray();
        for (int i = 0; i < note.length(); i++) {
            int at = -1;
            for (int j = 0; j < bag.length; j++) if (bag[j] == note.charAt(i)) { at = j; break; }
            if (at < 0) return false;
            bag[at] = ' ';                 // this magnet is used up
        }
        return true;
    }""")

prob(slug="count-pairs-with-sum", stage=0, title="Count Pairs With a Given Sum", difficulty="Medium",
 whats="Finding one pair becomes counting them all: ask the map how many partners you have already passed, not just whether one exists.",
 f=fn("countPairsWithSum", "long", ("int[]", "nums"), ("int", "target")),
 statement="""
A shop runs a “buy two, pay exactly `target`” promotion. Given the prices `nums`, count how many different pairs of items the promotion applies to.

Return the number of index pairs `i < j` with `nums[i] + nums[j] == target`.
""", constraints=["1 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9", "-10^9 <= target <= 10^9"],
 hints=["In Pair With a Given Sum you stopped at the first partner. What do you need instead if you must not stop?",
        "For the element at j, how many valid partners sit to its left?",
        "Could the answer be bigger than an int when all 100,000 prices are equal?"],
 trigger="“Count pairs with sum T” → frequency map of what you passed, add count[target − x].",
 examples=[([[1,5,3,3,7],8],3,"1 + 7, and 5 + 3 twice (once for each 3)."),
           ([[2,2,2],4],3,"Any two of the three 2s."),([[1,2],7],0,"")],
 tests=[[[1],1],[[0,0,0],0],[[-2,2,-2,2],0],[[5,5,5,5],10],[[-1000000000,1000000000],0],[[3,3],7]],
 gen=[{"seed":1601,"count":2,"args":[arr(100000,1,50),K(51)]},
      {"seed":1602,"count":1,"args":[arr(100000,-1000,1000),I(-100,100)]},
      {"seed":1603,"count":1,"args":[arr(100000,-1000000000,1000000000),K(0)]}],
 cross=[{"seed":151,"count":250,"args":[arrr(1,12,-5,5),I(-8,8)]},
        {"seed":152,"count":150,"args":[arrr(1,10,-2,2),I(-3,3)]}],
 ref="""
    public long countPairsWithSum(int[] nums, int target) {
        Map<Integer, Integer> count = new HashMap<>();
        long pairs = 0;
        for (int x : nums) {
            pairs += count.getOrDefault(target - x, 0);
            count.merge(x, 1, Integer::sum);
        }
        return pairs;
    }""",
 brute="""
    public long countPairsWithSum(int[] nums, int target) {
        long pairs = 0;
        for (int i = 0; i < nums.length; i++)
            for (int j = i + 1; j < nums.length; j++)
                if ((long) nums[i] + nums[j] == target) pairs++;
        return pairs;
    }""")

# ============================== Stage 2: group by a key ==============================
prob(slug="same-letters", stage=1, title="Same Letters", difficulty="Easy",
 whats="A word's letter tally is a key: two words are rearrangements of each other exactly when their tallies match.",
 f=fn("sameLetters", "boolean", ("String", "a"), ("String", "b")),
 statement="""
A word game asks whether two words are made of exactly the same letters, just in a different order (“listen” and “silent”, for example).

Return `true` if `b` is a rearrangement of `a`, otherwise `false`.
""", constraints=["1 <= a.length, b.length <= 10^5", "a and b consist of lowercase English letters"],
 hints=["Which cheap check rules out most pairs before you look at a single letter?",
        "Crossing letters off one copy works, but searching for each letter costs a whole pass. What could you compare instead of the words themselves?",
        "There are 26 letters. How big does the summary of a word need to be?"],
 trigger="“Are these two words rearrangements?” → compare the 26 letter counts, not the letters.",
 examples=[(["listen","silent"],True,"Both use e, i, l, n, s and t once each."),
           (["apple","pale"],False,"Different lengths, so they cannot match."),
           (["aab","abb"],False,"")],
 tests=[["a","a"],["a","b"],["ab","ba"],["aabb","abab"],["abc","abcd"],["zz","zz"]],
 gen=[{"seed":1701,"count":2,"args":[S(100000,"abcde"),shuffled(0,0.5,"abcde")]},
      {"seed":1702,"count":1,"args":[S(100000,"ab"),shuffled(0,0.0,"ab")]},
      {"seed":1703,"count":1,"args":[S(100000,"abcdefghijklmnopqrstuvwxyz"),shuffled(0,1.0,"abcdefghijklmnopqrstuvwxyz")]}],
 cross=[{"seed":161,"count":250,"args":[Sr(1,8,"abc"),shuffled(0,0.6,"abc")]},
        {"seed":162,"count":150,"args":[Sr(1,6,"ab"),Sr(1,6,"ab")]}],
 ref="""
    public boolean sameLetters(String a, String b) {
        if (a.length() != b.length()) return false;
        int[] diff = new int[26];
        for (int i = 0; i < a.length(); i++) {
            diff[a.charAt(i) - 'a']++;
            diff[b.charAt(i) - 'a']--;
        }
        for (int d : diff) if (d != 0) return false;
        return true;
    }""",
 brute="""
    public boolean sameLetters(String a, String b) {
        if (a.length() != b.length()) return false;
        char[] left = b.toCharArray();
        for (int i = 0; i < a.length(); i++) {
            int at = -1;
            for (int j = 0; j < left.length; j++) if (left[j] == a.charAt(i)) { at = j; break; }
            if (at < 0) return false;
            left[at] = ' ';                // cross this letter off
        }
        return true;
    }""")

prob(slug="letter-groups", stage=1, title="Letter Groups", difficulty="Medium",
 whats="One comparison becomes one lookup: use the letter tally as a map key and equal keys land in the same bucket.",
 f=fn("groupAnagrams", "List<List<String>>", ("String[]", "words")),
 compare="UNORDERED_DEEP",
 statement="""
A crossword editor wants to bundle the words in a list so that words made of exactly the same letters sit together.

Return the groups. Each word belongs to exactly one group, and the groups (and the words inside them) may be returned in any order.
""", constraints=["1 <= words.length <= 2 * 10^4", "1 <= words[i].length <= 20", "words[i] consists of lowercase English letters"],
 hints=["Comparing every word with every other word is the obvious plan. What makes it slow when almost every word is in a group of its own?",
        "Same Letters compared two tallies. Could a tally itself be used to look a group up?",
        "What kind of value can be a HashMap key — and how would you turn a tally into one?"],
 trigger="“Group things that are equal up to rearrangement” → map a canonical key (sorted word / letter tally) to a bucket.",
 examples=[([["tab","bat","cat","act","tba"]],[["tab","bat","tba"],["cat","act"]],"tab, bat and tba use the same letters; so do cat and act."),
           ([["x"]],[["x"]],""),
           ([["ab","ba","abb"]],[["ab","ba"],["abb"]],"abb has three letters, so it cannot join the other two.")],
 tests=[[["a","a"]],[["zz","zz","zz"]],[["abc","bca","cab","acb","bac","cba"]],[["ab","cd"]],[["aab","aba","baa","bab"]]],
 # a wide alphabet means almost every word is in a group of its own, which is the worst case for scanning groups
 gen=[{"seed":1801,"count":1,"args":[words(20000,8,10,"abcdefghij")]},
      {"seed":1802,"count":1,"args":[words(20000,6,6,"ab")]},
      {"seed":1803,"count":1,"args":[words(20000,1,20,"abcdefgh")]}],
 cross=[{"seed":171,"count":250,"args":[words_r(1,8,1,4,"ab")]},
        {"seed":172,"count":150,"args":[words_r(1,6,1,5,"abc")]}],
 ref="""
    public List<List<String>> groupAnagrams(String[] words) {
        Map<String, List<String>> groups = new HashMap<>();
        for (String w : words) {
            char[] letters = w.toCharArray();
            Arrays.sort(letters);
            groups.computeIfAbsent(new String(letters), k -> new ArrayList<>()).add(w);
        }
        return new ArrayList<>(groups.values());
    }""",
 brute="""
    public List<List<String>> groupAnagrams(String[] words) {
        List<List<String>> groups = new ArrayList<>();
        for (String w : words) {
            boolean placed = false;
            for (List<String> g : groups)
                if (same(g.get(0), w)) { g.add(w); placed = true; break; }
            if (!placed) {
                List<String> g = new ArrayList<>();
                g.add(w);
                groups.add(g);
            }
        }
        return groups;
    }

    private boolean same(String a, String b) {
        if (a.length() != b.length()) return false;
        char[] left = b.toCharArray();
        for (int i = 0; i < a.length(); i++) {
            int at = -1;
            for (int j = 0; j < left.length; j++) if (left[j] == a.charAt(i)) { at = j; break; }
            if (at < 0) return false;
            left[at] = ' ';
        }
        return true;
    }""")

prob(slug="pattern-match", stage=1, title="Does the Sentence Follow the Pattern?", difficulty="Easy",
 whats="A key can map back: the pairing has to hold in both directions, or two letters could end up sharing one word.",
 f=fn("followsPattern", "boolean", ("String", "pattern"), ("String", "sentence")),
 statement="""
A puzzle gives you a pattern of letters such as `"abba"` and a sentence such as `"dog cat cat dog"`. The sentence follows the pattern if the words line up with the letters one for one: the same letter always stands for the same word, and two different letters never stand for the same word.

The sentence is a list of words separated by single spaces. Return `true` if it follows the pattern.
""", constraints=["1 <= pattern.length <= 3 * 10^4", "pattern consists of lowercase English letters",
                  "1 <= sentence.length <= 3 * 10^5", "sentence is lowercase words separated by single spaces, with no leading or trailing space"],
 hints=["First: how many words must the sentence have?",
        "Suppose you only record “letter a means dog”. Which wrong sentence would you then accept?",
        "How many lookup tables do you need so that no two letters can claim the same word?"],
 trigger="“One-to-one pairing between two sequences” → two maps, one each way.",
 examples=[(["abba","dog cat cat dog"],True,"a stands for dog and b for cat, consistently in both directions."),
           (["abba","dog cat cat fish"],False,"The last word should be dog."),
           (["aba","dog dog dog"],False,"Here a and b would both have to stand for dog.")],
 tests=[["a","hello"],["a","hello world"],["ab","x x"],["aa","x x"],["abab","q r q r"],["aa","x y"]],
 gen=[{"seed":1901,"count":3,"args":[S(30000,"abcdefgh"),sentence(0,NATO,0.3)]},
      {"seed":1902,"count":1,"args":[S(30000,"ab"),sentence(0,NATO,1.0)]}],
 cross=[{"seed":181,"count":250,"args":[Sr(1,7,"abc"),sentence(0,["red","blue","green","black"],0.5)]},
        {"seed":182,"count":150,"args":[Sr(1,5,"ab"),sentence(0,["red","blue","green"],1.0)]}],
 ref="""
    public boolean followsPattern(String pattern, String sentence) {
        String[] words = sentence.split(" ");
        if (words.length != pattern.length()) return false;
        Map<Character, String> forLetter = new HashMap<>();
        Map<String, Character> forWord = new HashMap<>();
        for (int i = 0; i < words.length; i++) {
            char c = pattern.charAt(i);
            String w = words[i];
            String boundWord = forLetter.putIfAbsent(c, w);
            if (boundWord != null && !boundWord.equals(w)) return false;
            Character boundLetter = forWord.putIfAbsent(w, c);
            if (boundLetter != null && boundLetter != c) return false;
        }
        return true;
    }""",
 brute="""
    public boolean followsPattern(String pattern, String sentence) {
        String[] words = sentence.split(" ");
        boolean ok = words.length == pattern.length();
        if (ok)
            for (int i = 0; i < pattern.length(); i++)
                for (int j = i + 1; j < pattern.length(); j++)
                    // same letter <=> same word, checked for every pair of positions
                    if ((pattern.charAt(i) == pattern.charAt(j)) != words[i].equals(words[j])) ok = false;
        return ok;
    }""")

prob(slug="top-k-frequent", stage=1, title="Top k Most Frequent", difficulty="Medium",
 whats="Counting first turns “most frequent” into plain ordering: group by value, then order the groups.",
 f=fn("topKFrequent", "int[]", ("int[]", "nums"), ("int", "k")),
 statement="""
A streaming service logs the id of every track that was played today. The editors want today's `k` most played tracks.

Return the `k` ids with the highest play counts, most played first. When two ids were played equally often, the **smaller id** comes first. `k` is never larger than the number of different ids in `nums`.
""", constraints=["1 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9", "1 <= k <= the number of distinct values in nums"],
 hints=["What is the first thing you need before you can talk about “most frequent” at all?",
        "Once you have the counts, how many things are left to put in order — n, or something usually much smaller?",
        "Two ids with the same count must come out in a fixed order. Where does that rule belong?"],
 trigger="“Top k by frequency” → frequency map first, then order the distinct values.",
 examples=[([[1,1,2,2,3,4],2],[1,2],"1 and 2 were played twice, 3 and 4 only once."),
           ([[5,5,5,7],1],[5],""),
           ([[4,6,4,6,9],2],[4,6],"Both were played twice, and 4 is the smaller id.")],
 tests=[[[9],1],[[1,1,2],2],[[-1,-1,-2,-2],2],[[3,3,3,1,1,2],3],[[0,0,0],1],[[7,8,9],3]],
 gen=[{"seed":2001,"count":2,"args":[arr(100000,1,1000),I(1,500)]},
      {"seed":2002,"count":1,"args":[arr(100000,1,20),K(20)]},
      {"seed":2003,"count":1,"args":[arr(100000,1,50000),I(1,1000)]}],
 cross=[{"seed":191,"count":250,"args":[upto_n_r(10,16),K(3)]},
        {"seed":192,"count":150,"args":[arrr(6,12,1,4),K(1)]}],
 ref="""
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> count = new HashMap<>();
        for (int x : nums) count.merge(x, 1, Integer::sum);
        List<Integer> values = new ArrayList<>(count.keySet());
        values.sort((p, q) -> {
            int byCount = Integer.compare(count.get(q), count.get(p));
            return byCount != 0 ? byCount : Integer.compare(p, q);
        });
        int[] top = new int[k];
        for (int i = 0; i < k; i++) top[i] = values.get(i);
        return top;
    }""",
 brute="""
    public int[] topKFrequent(int[] nums, int k) {
        int n = nums.length;
        int[] freq = new int[n];
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                if (nums[i] == nums[j]) freq[i]++;
        List<Integer> taken = new ArrayList<>();
        int[] top = new int[k];
        for (int r = 0; r < k; r++) {
            int best = -1;
            for (int i = 0; i < n; i++) {
                if (taken.contains(nums[i])) continue;
                if (best < 0 || freq[i] > freq[best] || (freq[i] == freq[best] && nums[i] < nums[best])) best = i;
            }
            top[r] = nums[best];
            taken.add(nums[best]);
        }
        return top;
    }""")

prob(slug="sort-by-frequency", stage=1, title="Sort Letters by Frequency", difficulty="Medium",
 whats="Same counting, but now the whole answer is the ordering: write each group out as a run of repeats.",
 f=fn("frequencySort", "String", ("String", "s")),
 statement="""
A typesetter wants to see which letters a text leans on. Rewrite `s` so that the letters appear grouped, the most frequent letter first.

All copies of a letter must stay together. A letter that occurs more often comes before one that occurs less often; when two letters occur equally often, the **alphabetically smaller** one comes first.
""", constraints=["1 <= s.length <= 10^5", "s consists of lowercase English letters"],
 hints=["The output has exactly the same letters as the input. So what is really being decided?",
        "How many different groups can there be, however long the text is?",
        "Two letters with the same count need a fixed order — where do you apply that rule?"],
 trigger="“Output ordered by how often things occur” → count, order the distinct keys, then expand.",
 examples=[(["treetop"],"eettopr","e and t appear twice each, and e is the smaller letter; o, p and r appear once."),
           (["aabbbc"],"bbbaac",""),
           (["xyz"],"xyz","All three appear once, so they come out in alphabetical order.")],
 tests=[["a"],["aa"],["zzaa"],["abcabc"],["zyx"],["aaabbc"]],
 gen=[{"seed":2101,"count":2,"args":[S(100000,"abcdefghijklmnopqrstuvwxyz")]},
      {"seed":2102,"count":1,"args":[S(100000,"ab")]},
      {"seed":2103,"count":1,"args":[S(100000,"z")]}],
 cross=[{"seed":201,"count":250,"args":[Sr(1,10,"abc")]},
        {"seed":202,"count":150,"args":[Sr(1,8,"abcdef")]}],
 ref="""
    public String frequencySort(String s) {
        int[] count = new int[26];
        for (int i = 0; i < s.length(); i++) count[s.charAt(i) - 'a']++;
        Integer[] letters = new Integer[26];
        for (int c = 0; c < 26; c++) letters[c] = c;
        Arrays.sort(letters, (p, q) -> count[p] != count[q] ? count[q] - count[p] : p - q);
        StringBuilder sb = new StringBuilder(s.length());
        for (int c : letters) for (int t = 0; t < count[c]; t++) sb.append((char) ('a' + c));
        return sb.toString();
    }""",
 brute="""
    public String frequencySort(String s) {
        char[] cs = s.toCharArray();
        int[] freq = new int[cs.length];
        for (int i = 0; i < cs.length; i++)
            for (int j = 0; j < cs.length; j++)
                if (cs[i] == cs[j]) freq[i]++;
        StringBuilder sb = new StringBuilder();
        Set<Character> done = new HashSet<>();
        while (true) {
            int best = -1;
            for (int i = 0; i < cs.length; i++) {
                if (done.contains(cs[i])) continue;
                if (best < 0 || freq[i] > freq[best] || (freq[i] == freq[best] && cs[i] < cs[best])) best = i;
            }
            if (best < 0) break;
            for (int t = 0; t < freq[best]; t++) sb.append(cs[best]);
            done.add(cs[best]);
        }
        return sb.toString();
    }""")

prob(slug="matching-row-column", stage=1, title="Matching Row and Column", difficulty="Medium",
 whats="A whole row can be the key: squash each row into one hashable value and look the columns up.",
 f=fn("equalPairs", "int", ("int[][]", "grid")),
 statement="""
A seating plan is an `n × n` grid of numbers. The organiser wants to know how often a row reads exactly the same, top to bottom, as a column reads left to right.

Count the pairs `(r, c)` such that row `r` and column `c` hold the same numbers in the same order.
""", constraints=["1 <= n <= 1000", "grid has n rows and n columns", "-10^9 <= grid[r][c] <= 10^9"],
 hints=["Comparing every row with every column costs n steps per pair. How many pairs are there?",
        "Letter Groups turned a word into a key. What is the key here?",
        "If two different rows read the same, how many column matches does each of them contribute?"],
 trigger="“Match whole rows against whole columns” → hash each row, then look up each column.",
 examples=[([[[1,2],[2,1]]],2,"Row 0 matches column 0, and row 1 matches column 1."),
           ([[[3,1,2],[1,3,2],[2,2,2]]],3,"The grid is mirror-symmetric, so every row matches the column with the same number."),
           ([[[1,1],[1,1]]],4,"Every row matches every column.")],
 tests=[[[[5]]],[[[1,2],[3,4]]],[[[7,7],[7,7]]],[[[1,2,3],[2,4,5],[3,5,6]]],[[[1,1,1],[1,1,1],[1,1,1]]],[[[1,2,3],[4,5,6],[7,8,9]]]],
 gen=[{"seed":2201,"count":1,"args":[grid_lines(1000,1,999,4)]},
      {"seed":2202,"count":1,"args":[grid_lines(700,1,3,3)]},
      {"seed":2203,"count":1,"args":[grid_lines(1000,1,99,2)]},
      {"seed":2204,"count":1,"args":[grid_lines(600,-1000000000,1000000000,2)]}],
 cross=[{"seed":211,"count":150,"args":[grid(4,4,1,2)]},
        {"seed":212,"count":150,"args":[grid_lines(5,1,3,2)]},
        {"seed":213,"count":100,"args":[grid_lines(3,1,2,1)]}],
 ref="""
    public int equalPairs(int[][] grid) {
        int n = grid.length;
        Map<String, Integer> rows = new HashMap<>();
        for (int[] row : grid) rows.merge(key(row), 1, Integer::sum);
        int pairs = 0;
        int[] column = new int[n];
        for (int c = 0; c < n; c++) {
            for (int r = 0; r < n; r++) column[r] = grid[r][c];
            pairs += rows.getOrDefault(key(column), 0);
        }
        return pairs;
    }

    private String key(int[] line) {
        StringBuilder sb = new StringBuilder();
        for (int x : line) sb.append(x).append(',');
        return sb.toString();
    }""",
 brute="""
    public int equalPairs(int[][] grid) {
        int n = grid.length, pairs = 0;
        for (int r = 0; r < n; r++)
            for (int c = 0; c < n; c++) {
                int[] column = new int[n];
                for (int i = 0; i < n; i++) column[i] = grid[i][c];
                if (Arrays.equals(grid[r], column)) pairs++;
            }
        return pairs;
    }""")

# ============================== Stage 3: the array is the hash table ==============================
prob(slug="missing-numbers", stage=2, title="Missing Numbers", difficulty="Easy",
 whats="When every value is between 1 and n, the array itself is the hash table: slot v − 1 belongs to value v.",
 f=fn("findMissing", "List<Integer>", ("int[]", "nums")),
 statement="""
A cloakroom has `n` numbered pegs, `1` to `n`, and `n` coats were handed in. Each coat's ticket shows a peg number, but some numbers were written twice and others never at all.

Given the `n` ticket numbers in `nums`, return the peg numbers that do not appear, in increasing order. Return an empty list if none are missing.
""", constraints=["1 <= nums.length <= 10^5", "1 <= nums[i] <= nums.length"],
 hints=["Searching the array for each of 1, 2, …, n costs a whole pass per number. Where could you leave a mark instead?",
        "Value v has a natural home in the array. Which index is it?",
        "You must mark a slot without losing the number stored in it — what can you change about a positive number and still read it back?"],
 trigger="Values are 1..n and you want the missing ones → mark slot v − 1 in place, for example by flipping its sign.",
 examples=[([[2,2,1,4]],[3],"There are 4 pegs; 3 was never written down."),
           ([[1,2,3]],[],"Nothing is missing."),([[2,2]],[1],"")],
 tests=[[[1]],[[2,2]],[[1,1,1,1]],[[4,3,2,1]],[[3,3,3]],[[1,1]]],
 gen=[{"seed":2301,"count":2,"args":[upto_n(100000)]},
      {"seed":2302,"count":1,"args":[upto_n(100000,-99990)]},
      {"seed":2303,"count":1,"args":[upto_n(100000,-99999)]}],
 cross=[{"seed":221,"count":250,"args":[upto_n_r(1,10)]},
        {"seed":222,"count":150,"args":[upto_n_r(1,4)]}],
 ref="""
    public List<Integer> findMissing(int[] nums) {
        for (int x : nums) {
            int slot = Math.abs(x) - 1;                 // the array itself records "value slot+1 showed up"
            if (nums[slot] > 0) nums[slot] = -nums[slot];
        }
        List<Integer> missing = new ArrayList<>();
        for (int i = 0; i < nums.length; i++) if (nums[i] > 0) missing.add(i + 1);
        return missing;
    }""",
 brute="""
    public List<Integer> findMissing(int[] nums) {
        List<Integer> missing = new ArrayList<>();
        for (int v = 1; v <= nums.length; v++) {
            boolean found = false;
            for (int x : nums) if (x == v) found = true;
            if (!found) missing.add(v);
        }
        return missing;
    }""")

prob(slug="repeated-numbers", stage=2, title="Repeated Numbers", difficulty="Medium",
 whats="The same marks read the other way round: arriving at a slot that is already marked means you have met this value before.",
 f=fn("findRepeated", "List<Integer>", ("int[]", "nums")),
 statement="""
The same cloakroom, the same `n` tickets with numbers between `1` and `n`.

This time return the peg numbers that were written down **more than once**, each listed once, in increasing order. Return an empty list if every number appears at most once.
""", constraints=["1 <= nums.length <= 10^5", "1 <= nums[i] <= nums.length"],
 hints=["Missing Numbers marked slot v − 1 the first time it met v. What does it mean if that slot is already marked?",
        "Can you record the repeats without a second array?",
        "A value that shows up three times will be noticed twice — how do you make sure it is reported only once?"],
 trigger="Values are 1..n and you want the repeats → mark slot v − 1; arriving at a marked slot means a repeat.",
 examples=[([[1,3,3,2,2]],[2,3],"3 and 2 were each written twice."),
           ([[1,2,3]],[],""),([[2,2,2]],[2],"2 is reported once even though it appears three times.")],
 tests=[[[1]],[[1,1]],[[3,3,3,3]],[[1,2,3,4]],[[4,4,2,2]],[[2,2,1]]],
 gen=[{"seed":2401,"count":2,"args":[upto_n(100000)]},
      {"seed":2402,"count":1,"args":[upto_n(100000,-50000)]},
      {"seed":2403,"count":1,"args":[upto_n(100000,-99999)]}],
 cross=[{"seed":231,"count":250,"args":[upto_n_r(1,10)]},
        {"seed":232,"count":150,"args":[upto_n_r(1,4)]}],
 ref="""
    public List<Integer> findRepeated(int[] nums) {
        List<Integer> hits = new ArrayList<>();
        for (int x : nums) {
            int v = Math.abs(x), slot = v - 1;
            if (nums[slot] < 0) hits.add(v);            // slot already marked: v is not new
            else nums[slot] = -nums[slot];
        }
        Collections.sort(hits);
        List<Integer> repeated = new ArrayList<>();
        for (int v : hits) if (repeated.isEmpty() || repeated.get(repeated.size() - 1) != v) repeated.add(v);
        return repeated;
    }""",
 brute="""
    public List<Integer> findRepeated(int[] nums) {
        List<Integer> repeated = new ArrayList<>();
        for (int v = 1; v <= nums.length; v++) {
            int times = 0;
            for (int x : nums) if (x == v) times++;
            if (times > 1) repeated.add(v);
        }
        return repeated;
    }""")

prob(slug="smallest-missing-positive", stage=2, title="Smallest Missing Positive", difficulty="Hard",
 whats="The values are no longer promised to be 1..n, so first move each useful value into its own slot, then read the slots in order.",
 f=fn("firstMissingPositive", "int", ("int[]", "nums")),
 statement="""
A ticketing system hands out positive, whole ticket numbers. You are given the numbers currently in use (in any order, possibly with repeats, possibly with junk like zero or negative numbers).

Return the smallest positive whole number that is **not** in use.
""", constraints=["1 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9"],
 hints=["With n numbers in hand, how large can the answer possibly be? Which values can you therefore ignore completely?",
        "Only values from 1 to n matter, and there are exactly n slots. Where would you like value v to sit?",
        "Swapping a value into its own slot hands you another value to place. How do you make sure that loop cannot run forever?"],
 trigger="Smallest missing positive with O(1) extra memory → swap each value v into slot v − 1, then find the first wrong slot.",
 examples=[([[3,4,-1,1]],2,"1, 3 and 4 are in use; 2 is the smallest positive number that is not."),
           ([[1,2,3]],4,"Every number from 1 to 3 is taken."),
           ([[7,8,9]],1,"")],
 tests=[[[1]],[[2]],[[-5,-4]],[[1,1]],[[1,2,2,4]],[[1000000000]]],
 # values in 1..10000 out of 10^5 slots: all of them are present, so the answer is 10001 and a "try 1, try 2, ..."
 # search has to scan the array ten thousand times. Seeds 16, 18 and 9 are the worst cases found.
 gen=[{"seed":16,"count":4,"args":[upto_n(100000,-90000)]},
      {"seed":18,"count":4,"args":[upto_n(100000,-90000)]},
      {"seed":9,"count":2,"args":[upto_n(100000,-90000)]},
      {"seed":2503,"count":1,"args":[arr(100000,-1000000000,1000000000)]},
      {"seed":2504,"count":1,"args":[upto_n(100000)]}],
 cross=[{"seed":241,"count":250,"args":[arrr(1,10,-5,12)]},
        {"seed":242,"count":150,"args":[upto_n_r(1,8)]}],
 ref="""
    public int firstMissingPositive(int[] nums) {
        int n = nums.length;
        for (int i = 0; i < n; i++) {
            // send nums[i] home, and keep going with whatever came back
            while (nums[i] >= 1 && nums[i] <= n && nums[nums[i] - 1] != nums[i]) {
                int home = nums[i] - 1;
                int t = nums[home];
                nums[home] = nums[i];
                nums[i] = t;
            }
        }
        for (int i = 0; i < n; i++) if (nums[i] != i + 1) return i + 1;
        return n + 1;
    }""",
 brute="""
    public int firstMissingPositive(int[] nums) {
        for (int v = 1; ; v++) {
            boolean found = false;
            for (int x : nums) if (x == v) found = true;
            if (!found) return v;
        }
    }""")

prob(slug="longest-run", stage=2, title="Longest Run of Consecutive Values", difficulty="Medium",
 whats="A set turns “is x − 1 here?” into a single question, so you can count each run only from its first value.",
 f=fn("longestConsecutive", "int", ("int[]", "nums")),
 statement="""
A warehouse scanner reports the shelf numbers that are currently occupied, in no particular order and possibly with repeats.

Return the length of the longest block of **consecutive** shelf numbers that are all occupied.
""", constraints=["1 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9"],
 hints=["Sorting works, but you are in the hashing chapter. What can a set tell you about a single value in one step?",
        "If you walk upwards from every value, you count the same run over and over. Which values are worth starting from?",
        "How do you recognise the first value of a run?"],
 trigger="“Longest stretch of consecutive values” → a set, and only count upwards from values whose predecessor is absent.",
 examples=[([[9,1,4,7,3,2,6,8]],4,"1, 2, 3, 4 are all occupied (and so are 6, 7, 8, 9)."),
           ([[5,5,5]],1,"Repeats do not make a run longer."),
           ([[10,20,30]],1,"")],
 tests=[[[1]],[[1,2]],[[2,1]],[[-1,0,1]],[[1000000000,999999999]],[[4,4,3,3,2]]],
 gen=[{"seed":2601,"count":2,"args":[arr(100000,1,150000)]},
      {"seed":2602,"count":1,"args":[upto_n(100000)]},
      {"seed":2603,"count":1,"args":[arr(100000,-1000000000,1000000000)]}],
 cross=[{"seed":251,"count":250,"args":[arrr(1,10,1,12)]},
        {"seed":252,"count":150,"args":[arrr(1,10,-4,4)]}],
 ref="""
    public int longestConsecutive(int[] nums) {
        Set<Integer> occupied = new HashSet<>();
        for (int x : nums) occupied.add(x);
        int best = 0;
        for (int x : occupied) {
            if (occupied.contains(x - 1)) continue;      // not the start of a run
            int length = 1;
            while (occupied.contains(x + length)) length++;
            best = Math.max(best, length);
        }
        return best;
    }""",
 brute="""
    public int longestConsecutive(int[] nums) {
        int best = 0;
        for (int x : nums) {
            int length = 1;
            while (holds(nums, x + length)) length++;
            best = Math.max(best, length);
        }
        return best;
    }

    private boolean holds(int[] nums, int v) {
        for (int x : nums) if (x == v) return true;
        return false;
    }""")

# ============================== Stage 4: transform, then count pairs ==============================
prob(slug="pairs-divisible", stage=3, title="Pairs With a Divisible Sum", difficulty="Medium",
 whats="Don't store the value, store what the question cares about: its remainder.",
 f=fn("pairsDivisible", "long", ("int[]", "nums"), ("int", "m")),
 statement="""
A warehouse ships goods in boxes of `m` items. Two batches can be shipped together without a leftover exactly when the total number of items divides evenly by `m`.

Given the batch sizes `nums`, count the index pairs `i < j` for which `nums[i] + nums[j]` is divisible by `m`.
""", constraints=["1 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9", "1 <= m <= 10^4"],
 hints=["Two numbers that differ by a multiple of m behave identically here. What is the only thing about a number that matters?",
        "If the element you are looking at leaves remainder r, what remainder must its partner leave?",
        "In Java, −7 % 5 is −2. How do you get remainders that land between 0 and m − 1?"],
 trigger="“Sum divisible by m” → count remainders and pair r with (m − r) % m.",
 examples=[([[3,1,2,6,9],3],4,"The three multiples of 3 give three pairs, and 1 + 2 = 3 gives a fourth."),
           ([[1,2],4],0,""),
           ([[-1,1,3],2],3,"Any two odd numbers add up to an even number.")],
 tests=[[[5],5],[[0,0,0],7],[[-4,4],8],[[1,1,1,1],2],[[1,2,3],1],[[-1000000000,-1000000000],4]],
 gen=[{"seed":2701,"count":2,"args":[arr(100000,-1000000000,1000000000),I(2,10000)]},
      {"seed":2702,"count":1,"args":[arr(100000,-1000000000,1000000000),K(2)]},
      {"seed":2703,"count":1,"args":[arr(100000,1,1000),K(1)]}],
 cross=[{"seed":261,"count":250,"args":[arrr(1,10,-9,9),I(1,6)]},
        {"seed":262,"count":150,"args":[arrr(1,8,-3,3),I(1,4)]}],
 ref="""
    public long pairsDivisible(int[] nums, int m) {
        long[] seen = new long[m];
        long pairs = 0;
        for (int x : nums) {
            int r = Math.floorMod(x, m);
            pairs += seen[(m - r) % m];
            seen[r]++;
        }
        return pairs;
    }""",
 brute="""
    public long pairsDivisible(int[] nums, int m) {
        long pairs = 0;
        for (int i = 0; i < nums.length; i++)
            for (int j = i + 1; j < nums.length; j++)
                if (((long) nums[i] + nums[j]) % m == 0) pairs++;
        return pairs;
    }""")

prob(slug="steady-pairs", stage=3, title="Steady Pairs", difficulty="Medium",
 whats="Rearrange the condition until each side mentions only one index — then it is just “count equal keys” again.",
 f=fn("countSteadyPairs", "long", ("int[]", "nums")),
 statement="""
A sensor reports one reading per second: `nums[i]` is the reading at second `i`. A pair of seconds `i < j` is **steady** if the reading grew by exactly one per second in between, that is `nums[j] - nums[i] == j - i`.

Return the number of steady pairs.
""", constraints=["1 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9"],
 hints=["The condition mixes both indexes. Can you move things around so that the left side only mentions i and the right side only mentions j?",
        "Once both sides are the same expression of a single index, what are you counting?",
        "Which earlier problem in this ladder has it just turned into?"],
 trigger="A condition tying i to j → rewrite it as f(i) = f(j), then count equal keys.",
 examples=[([[4,5,6,2]],3,"The first three readings rise by exactly one per second, giving three pairs."),
           ([[7,7]],0,""),
           ([[1,3,3,5]],2,"Seconds 0 and 2 (1 → 3 over two seconds), and seconds 1 and 3.")],
 tests=[[[5]],[[1,2,3,4,5]],[[0,0,0]],[[-1000000000,-999999999]],[[2,2,2,2]],[[1,2,3,4,5,6,7,8,9,10]]],
 gen=[{"seed":2801,"count":1,"args":[arr(100000,-1000000000,1000000000)]},
      {"seed":2802,"count":1,"args":[arr(100000,1,100)]},
      {"seed":2803,"count":1,"args":[arr(100000,1,100000)]},
      {"seed":2804,"count":1,"args":[arr(100000,5,5)]}],
 cross=[{"seed":271,"count":250,"args":[arrr(1,10,-3,3)]},
        {"seed":272,"count":150,"args":[arrr(1,12,1,4)]}],
 ref="""
    public long countSteadyPairs(int[] nums) {
        Map<Integer, Integer> count = new HashMap<>();
        long pairs = 0;
        for (int i = 0; i < nums.length; i++) {
            int key = nums[i] - i;                      // nums[j] - j == nums[i] - i
            int seen = count.getOrDefault(key, 0);
            pairs += seen;
            count.put(key, seen + 1);
        }
        return pairs;
    }""",
 brute="""
    public long countSteadyPairs(int[] nums) {
        long pairs = 0;
        for (int i = 0; i < nums.length; i++)
            for (int j = i + 1; j < nums.length; j++)
                if ((long) nums[j] - nums[i] == j - i) pairs++;
        return pairs;
    }""")

prob(slug="digit-sum-pair", stage=3, title="Best Pair With Equal Digit Sums", difficulty="Medium",
 whats="The key can be computed from the value, and each group only needs its best candidate kept.",
 f=fn("maxPairSameDigitSum", "int", ("int[]", "nums")),
 statement="""
A lottery pays out on two tickets whose numbers have the same digit sum (`18` and `36` both sum to `9`), and the prize is the sum of the two numbers.

Return the largest possible prize, or `-1` if no two tickets share a digit sum.
""", constraints=["2 <= nums.length <= 10^5", "1 <= nums[i] <= 10^8"],
 hints=["Tickets only compete with tickets that share their digit sum. How would you put them into groups?",
        "How many different digit sums are even possible here?",
        "Inside one group, how many tickets do you actually have to remember?"],
 trigger="“Best pair sharing a derived property” → group by the computed key, keep only the best per group.",
 examples=[([[18,43,36,13,7]],54,"18 and 36 both have digit sum 9, and 18 + 36 = 54."),
           ([[10,12,19,14]],-1,"The digit sums 1, 3, 10 and 5 are all different."),
           ([[51,71,17,42]],93,"51 and 42 both have digit sum 6.")],
 tests=[[[1,2]],[[1,1]],[[100000000,1]],[[9,18,27]],[[5,50,500]],[[11,2,20]]],
 gen=[{"seed":2901,"count":2,"args":[arr(100000,1,100000000)]},
      {"seed":2902,"count":1,"args":[arr(100000,1,1000)]},
      {"seed":2903,"count":1,"args":[arr(100000,100000000,100000000)]}],
 cross=[{"seed":281,"count":250,"args":[arrr(2,10,1,100)]},
        {"seed":282,"count":150,"args":[arrr(2,8,1,100000)]}],
 ref="""
    public int maxPairSameDigitSum(int[] nums) {
        int[] best = new int[82];                       // 99999999 has the largest digit sum, 72
        Arrays.fill(best, -1);
        int prize = -1;
        for (int x : nums) {
            int s = 0;
            for (int t = x; t > 0; t /= 10) s += t % 10;
            if (best[s] >= 0) prize = Math.max(prize, best[s] + x);
            best[s] = Math.max(best[s], x);
        }
        return prize;
    }""",
 brute="""
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
    }""")

prob(slug="four-lists-zero", stage=3, title="One From Each of Four Lists", difficulty="Medium",
 whats="Split the work in half: hash every sum the first two lists can make, then look its negative up from the other two.",
 f=fn("fourSumCount", "long", ("int[]", "a"), ("int[]", "b"), ("int[]", "c"), ("int[]", "d")),
 statement="""
Four machines each produce a list of measured deviations. A calibration is *valid* when you can pick one deviation from each list and the four of them cancel out exactly.

Count the tuples `(i, j, k, l)` with `a[i] + b[j] + c[k] + d[l] == 0`. Two tuples are different if any index differs, even when the values are the same.
""", constraints=["1 <= a.length, b.length, c.length, d.length <= 1000", "-10^8 <= values <= 10^8"],
 hints=["Trying every tuple means a loop per list. How many steps is that for lists of 1000?",
        "If you already knew the sum of the first two picks, what single number would you need to find in the other two lists?",
        "How many different sums can the first two lists make, and could you afford to store them all?"],
 trigger="“Pick one from each of four lists so the sum is T” → split 2 + 2 and hash the sums of one half.",
 examples=[([[1,2],[-2,-1],[0,0],[0,0]],8,"a + b has to be 0: either 1 + (−1) or 2 + (−2). Each of the two zeros in c and in d can be used, so 2 × 2 × 2 = 8."),
           ([[0],[0],[0],[0]],1,""),
           ([[1],[1],[1],[1]],0,"")],
 tests=[[[5],[-5],[0],[0]],[[1,1],[-1,-1],[0],[0]],[[100000000],[-100000000],[100000000],[-100000000]],
        [[1,2,3],[1,2,3],[-1,-2,-3],[-1,-2,-3]],[[0,0,0],[0,0,0],[0,0,0],[0,0,0]],[[7],[7],[7],[7]]],
 gen=[{"seed":3001,"count":1,"args":[arr(1000,-3,3),arr(1000,-3,3),arr(1000,-3,3),arr(1000,-3,3)]},
      {"seed":3002,"count":1,"args":[arr(800,-100000000,100000000),arr(800,-100000000,100000000),arr(800,-100000000,100000000),arr(800,-100000000,100000000)]},
      {"seed":3003,"count":1,"args":[arr(1000,-1000,1000),arr(1000,-1000,1000),arr(1000,-1000,1000),arr(1000,-1000,1000)]}],
 cross=[{"seed":291,"count":250,"args":[arrr(1,5,-3,3),arrr(1,5,-3,3),arrr(1,5,-3,3),arrr(1,5,-3,3)]},
        {"seed":292,"count":150,"args":[arrr(1,4,-1,1),arrr(1,4,-1,1),arrr(1,4,-1,1),arrr(1,4,-1,1)]}],
 ref="""
    public long fourSumCount(int[] a, int[] b, int[] c, int[] d) {
        Map<Integer, Integer> firstHalf = new HashMap<>();
        for (int x : a) for (int y : b) firstHalf.merge(x + y, 1, Integer::sum);
        long tuples = 0;
        for (int x : c) for (int y : d) tuples += firstHalf.getOrDefault(-(x + y), 0);
        return tuples;
    }""",
 brute="""
    public long fourSumCount(int[] a, int[] b, int[] c, int[] d) {
        long tuples = 0;
        for (int w : a)
            for (int x : b)
                for (int y : c)
                    for (int z : d)
                        if ((long) w + x + y + z == 0) tuples++;
        return tuples;
    }""")

# ============================== Stage 5: arrays in place ==============================
prob(slug="product-except-self", stage=4, title="Product of Everything Else", difficulty="Medium",
 whats="Two sweeps replace the map: everything to the left of i, times everything to its right.",
 f=fn("productExceptSelf", "long[]", ("int[]", "nums")),
 statement="""
A factory line has `n` stations, each with an efficiency factor. For every station you want to know the combined factor of **all the other** stations.

Return an array `out` where `out[i]` is the product of every `nums[j]` with `j != i`. Division is not allowed — one zero on the line would make it meaningless.

For a line with a single station the answer is `1`, the product of nothing at all.
""", constraints=["1 <= nums.length <= 10^5", "-30 <= nums[i] <= 30",
                  "every answer fits in a signed 64-bit integer"],
 hints=["The product of everything except station i splits naturally into two halves. Which two?",
        "Can you fill in all the left halves in one pass from the left?",
        "Do you need a second array for the right halves, or can you reuse the answer array?"],
 trigger="“Combine everything except me” → one prefix sweep and one suffix sweep.",
 examples=[([[1,2,3,4]],[24,12,8,6],"24 = 2·3·4, 12 = 1·3·4, 8 = 1·2·4, 6 = 1·2·3."),
           ([[2,0,3]],[0,6,0],"The middle answer is 2·3 = 6; the other two include the zero."),
           ([[5]],[1],"There is nothing else on the line, and the empty product is 1.")],
 tests=[[[0,0]],[[-1,1,-1]],[[1,1,1,1]],[[0,1,2,3]],[[-2,3]],[[7]]],
 gen=[{"seed":3101,"count":2,"args":[choice(100000,[1,-1])]},
      {"seed":3102,"count":1,"args":[choice(100000,[1,-1,0])]},
      {"seed":3103,"count":1,"args":[choice(100000,[1,1,1,-1])]}],
 cross=[{"seed":301,"count":250,"args":[choice_r(1,8,[-2,-1,0,1,2])]},
        {"seed":302,"count":150,"args":[choice_r(1,6,[1,-1,0,3])]}],
 ref="""
    public long[] productExceptSelf(int[] nums) {
        int n = nums.length;
        long[] out = new long[n];
        long run = 1;
        for (int i = 0; i < n; i++) { out[i] = run; run *= nums[i]; }      // everything to the left of i
        run = 1;
        for (int i = n - 1; i >= 0; i--) { out[i] *= run; run *= nums[i]; } // times everything to its right
        return out;
    }""",
 brute="""
    public long[] productExceptSelf(int[] nums) {
        long[] out = new long[nums.length];
        for (int i = 0; i < nums.length; i++) {
            long p = 1;
            for (int j = 0; j < nums.length; j++) if (j != i) p *= nums[j];
            out[i] = p;
        }
        return out;
    }""")

prob(slug="majority-vote", stage=4, title="Majority Vote", difficulty="Easy",
 whats="You can drop the map entirely: one candidate and one counter survive, because a real majority outlasts every cancellation.",
 f=fn("majority", "int", ("int[]", "nums")),
 statement="""
A committee votes by shouting out candidate ids, one after another. One candidate is known to have **strictly more than half** of all the votes.

Return that candidate's id. Try to do it with a couple of variables — no map, no sorting.
""", constraints=["1 <= nums.length <= 10^5", "-10^9 <= nums[i] <= 10^9",
                  "exactly one value occurs more than nums.length / 2 times"],
 hints=["Imagine pairing up two votes for different candidates and throwing both away. Who is left at the end?",
        "How much do you have to remember to run that pairing while walking the array once?",
        "What should happen to your counter when it reaches zero?"],
 trigger="“A value occurring more than half the time” → keep one candidate and one counter (Boyer–Moore voting).",
 examples=[([[3,3,1,3,2]],3,"3 got three of the five votes."),
           ([[8,8]],8,""),([[5]],5,"")],
 tests=[[[1,1,1]],[[-4,-4,2]],[[2,1,2,1,2]],[[7,7,7,1,2]],[[0,0,0,0,1,2,3]],[[-1000000000,-1000000000,5]]],
 gen=[{"seed":3201,"count":2,"args":[choice(100000,[7,7,7,7,1,2,3])]},
      {"seed":3202,"count":1,"args":[choice(100000,[-5,-5,-5,-5,-5,1,2,3,4])]},
      {"seed":3203,"count":1,"args":[choice(100000,[1000000000,1000000000,1000000000,-1,-2])]}],
 cross=[{"seed":311,"count":150,"args":[choice_r(13,21,[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,2])]},
        {"seed":312,"count":150,"args":[choice_r(13,21,[-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,0,9])]},
        {"seed":313,"count":150,"args":[choice_r(15,25,[11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,2,3])]}],
 ref="""
    public int majority(int[] nums) {
        int candidate = nums[0], votes = 0;
        for (int x : nums) {
            if (votes == 0) candidate = x;
            votes += x == candidate ? 1 : -1;
        }
        return candidate;
    }""",
 brute="""
    public int majority(int[] nums) {
        int best = nums[0], bestCount = 0;
        for (int x : nums) {
            int times = 0;
            for (int y : nums) if (x == y) times++;
            if (times > bestCount) { bestCount = times; best = x; }
        }
        return best;
    }""")

prob(slug="rotate-right", stage=4, title="Rotate Right", difficulty="Medium",
 whats="Two cheap observations do the whole job: k only matters modulo n, and a rotation is three reversals.",
 f=fn("rotate", "void", ("int[]", "nums"), ("int", "k"), out=0),
 statement="""
A playlist is shown in a window that scrolls. Shifting it right by one step moves every track one place to the right and brings the last track round to the front.

Shift `nums` right by `k` steps, **modifying the array in place**. Your method returns nothing; the array itself is the answer.
""", constraints=["1 <= nums.length <= 10^5", "0 <= k <= 10^9", "-10^9 <= nums[i] <= 10^9"],
 hints=["What does shifting by exactly one full length do? So how many genuinely different values of k are there?",
        "Write the array before and after a shift. Which two blocks of numbers swap places?",
        "Reversing the whole array puts the right block first, but backwards. What fixes that?"],
 trigger="“Rotate an array in place” → reduce k modulo n, then reverse the whole array and each of the two parts.",
 examples=[([[1,2,3,4,5],2],[4,5,1,2,3],"The last two tracks wrap round to the front."),
           ([[9,8],5],[8,9],"Two shifts bring you back to the start, so 5 shifts behave like 1."),
           ([[7],3],[7],"")],
 tests=[[[1,2],0],[[1,2,3],3],[[1,2,3],1],[[1,2,3,4],1000000000],[[5,6,7,8,9],7],[[1,2,3,4,5,6],1000000000]],
 gen=[{"seed":3301,"count":2,"args":[arr(100000,-1000000000,1000000000),I(999000000,1000000000)]},
      {"seed":3302,"count":1,"args":[arr(100000,-1000000000,1000000000),I(1,100000)]},
      {"seed":3303,"count":1,"args":[arr(100000,-1000000000,1000000000),K(100000)]}],
 cross=[{"seed":321,"count":250,"args":[arrr(1,9,-9,9),I(0,15)]},
        {"seed":322,"count":150,"args":[arrr(1,5,-3,3),I(0,30)]}],
 ref="""
    public void rotate(int[] nums, int k) {
        int n = nums.length;
        k %= n;
        reverse(nums, 0, n - 1);
        reverse(nums, 0, k - 1);
        reverse(nums, k, n - 1);
    }

    private void reverse(int[] nums, int from, int to) {
        while (from < to) {
            int t = nums[from];
            nums[from++] = nums[to];
            nums[to--] = t;
        }
    }""",
 brute="""
    public void rotate(int[] nums, int k) {
        for (int step = 0; step < k; step++) {
            int last = nums[nums.length - 1];
            for (int i = nums.length - 1; i > 0; i--) nums[i] = nums[i - 1];
            nums[0] = last;
        }
    }""")

prob(slug="spiral-walk", stage=4, title="Spiral Walk", difficulty="Medium",
 whats="Four boundaries are enough state: read the outer ring, shrink them, repeat.",
 f=fn("spiralOrder", "List<Integer>", ("int[][]", "matrix")),
 statement="""
A robot vacuum starts in the top-left corner of a rectangular room laid out as a grid, drives right along the first row, then down the last column, then left along the last row, then up — always turning when it meets a wall or a stripe it has already cleaned.

Return the grid values in the order the robot visits them.
""", constraints=["1 <= rows, cols <= 10^5", "rows * cols <= 4 * 10^5", "-10^9 <= matrix[r][c] <= 10^9"],
 hints=["After the first row is done, which rows are still in play? After the last column is done, which columns?",
        "How many numbers describe “what is left to clean” at any moment?",
        "A single leftover row or column is the case that trips most people up — what stops you from reading it twice?"],
 trigger="“Visit a matrix ring by ring” → keep top/bottom/left/right and move them inwards.",
 examples=[([[[1,2,3],[4,5,6],[7,8,9]]],[1,2,3,6,9,8,7,4,5],"Right along the top, down the right side, left along the bottom, up the left side, then the middle."),
           ([[[1,2],[3,4]]],[1,2,4,3],""),
           ([[[5]]],[5],"")],
 tests=[[[[1,2,3,4]]],[[[1],[2],[3]]],[[[1,2],[3,4],[5,6]]],[[[1,2,3],[4,5,6]]],[[[1,2,3,4],[5,6,7,8],[9,10,11,12]]],[[[1,1],[1,1]]]],
 gen=[{"seed":3401,"count":1,"args":[grid(600,600,-1000000000,1000000000)]},
      {"seed":3402,"count":1,"args":[grid(1,100000,-1000,1000)]},
      {"seed":3403,"count":1,"args":[grid(100000,1,-1000,1000)]},
      {"seed":3404,"count":1,"args":[grid(400,900,-1000,1000)]},
      {"seed":3405,"count":1,"args":[grid(600,600,-1000,1000)]}],
 cross=[{"seed":331,"count":150,"args":[grid(4,5,-9,9)]},
        {"seed":332,"count":100,"args":[grid(1,6,-9,9)]},
        {"seed":333,"count":100,"args":[grid(6,1,-9,9)]},
        {"seed":334,"count":100,"args":[grid(3,3,-9,9)]}],
 ref="""
    public List<Integer> spiralOrder(int[][] matrix) {
        List<Integer> out = new ArrayList<>();
        int top = 0, bottom = matrix.length - 1, left = 0, right = matrix[0].length - 1;
        while (top <= bottom && left <= right) {
            for (int c = left; c <= right; c++) out.add(matrix[top][c]);
            top++;
            for (int r = top; r <= bottom; r++) out.add(matrix[r][right]);
            right--;
            if (top <= bottom) {
                for (int c = right; c >= left; c--) out.add(matrix[bottom][c]);
                bottom--;
            }
            if (left <= right) {
                for (int r = bottom; r >= top; r--) out.add(matrix[r][left]);
                left++;
            }
        }
        return out;
    }""",
 brute="""
    public List<Integer> spiralOrder(int[][] matrix) {
        List<List<Integer>> rest = new ArrayList<>();
        for (int[] row : matrix) {
            List<Integer> r = new ArrayList<>();
            for (int x : row) r.add(x);
            rest.add(r);
        }
        List<Integer> out = new ArrayList<>();
        while (!rest.isEmpty() && !rest.get(0).isEmpty()) {
            out.addAll(rest.remove(0));                 // the top row is next, left to right
            int rows = rest.size(), cols = rows == 0 ? 0 : rest.get(0).size();
            List<List<Integer>> turned = new ArrayList<>();
            for (int c = cols - 1; c >= 0; c--) {       // turn what is left, so the next side is on top
                List<Integer> r = new ArrayList<>();
                for (int i = 0; i < rows; i++) r.add(rest.get(i).get(c));
                turned.add(r);
            }
            rest = turned;
        }
        return out;
    }""")

prob(slug="turn-the-grid", stage=4, title="Turn the Grid", difficulty="Medium",
 whats="A quarter turn in place is two easy moves you already know: mirror along the diagonal, then reverse each row.",
 f=fn("rotateImage", "void", ("int[][]", "matrix"), out=0),
 statement="""
A photo editor stores an image as a square grid of pixel values. Turn the image a quarter turn **clockwise**, changing the given grid itself. Your method returns nothing; the grid is the answer.

Do not build a second grid — the point is to move the pixels around inside the one you were given.
""", constraints=["1 <= n <= 1000", "matrix has n rows and n columns", "-10^9 <= matrix[r][c] <= 10^9"],
 hints=["Where does the value at row r, column c end up after a quarter turn clockwise?",
        "Mirroring the grid along its main diagonal is an easy in-place move. How close does that get you?",
        "After the mirror, compare each row with what you actually want — what single operation is left?"],
 trigger="“Rotate a square matrix 90° in place” → transpose, then reverse every row.",
 examples=[([[[1,2],[3,4]]],[[3,1],[4,2]],"The left column becomes the top row."),
           ([[[1,2,3],[4,5,6],[7,8,9]]],[[7,4,1],[8,5,2],[9,6,3]],""),
           ([[[5]]],[[5]],"A single pixel has nowhere to go.")],
 tests=[[[[7]]],[[[1,1],[1,1]]],[[[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]],[[[0,-1],[-2,3]]],[[[2,4],[6,8]]]],
 gen=[{"seed":3501,"count":1,"args":[grid(300,300,-1000000000,1000000000)]},
      {"seed":3502,"count":1,"args":[grid(500,500,-1000,1000)]},
      {"seed":3503,"count":1,"args":[grid(250,250,-5,5)]}],
 cross=[{"seed":341,"count":150,"args":[grid(4,4,-9,9)]},
        {"seed":342,"count":100,"args":[grid(1,1,-9,9)]},
        {"seed":343,"count":100,"args":[grid(5,5,-9,9)]},
        {"seed":344,"count":100,"args":[grid(2,2,-9,9)]}],
 ref="""
    public void rotateImage(int[][] matrix) {
        int n = matrix.length;
        for (int r = 0; r < n; r++)                     // mirror along the main diagonal
            for (int c = r + 1; c < n; c++) {
                int t = matrix[r][c];
                matrix[r][c] = matrix[c][r];
                matrix[c][r] = t;
            }
        for (int[] row : matrix)                        // then reverse every row
            for (int from = 0, to = n - 1; from < to; from++, to--) {
                int t = row[from];
                row[from] = row[to];
                row[to] = t;
            }
    }""",
 brute="""
    public void rotateImage(int[][] matrix) {
        int n = matrix.length;
        int[][] cells = new int[n * n][];
        int k = 0;
        for (int r = 0; r < n; r++)
            for (int c = 0; c < n; c++) cells[k++] = new int[]{r, c, matrix[r][c]};
        for (int r = 0; r < n; r++)
            for (int c = 0; c < n; c++)
                // after a clockwise quarter turn, (r, c) holds whatever used to be at (n - 1 - c, r)
                for (int[] cell : cells)
                    if (cell[0] == n - 1 - c && cell[1] == r) { matrix[r][c] = cell[2]; break; }
    }""")


def main():
    os.makedirs(ROOT, exist_ok=True)
    for i, p in enumerate(P, 1):
        d = os.path.join(ROOT, f"{i:02d}-{p['slug']}")
        os.makedirs(d, exist_ok=True)
        meta = {"slug": p["slug"], "topic": "hashing", "stage": p["stage"], "order": i, "title": p["title"],
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
