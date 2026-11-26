package dev.dsaladder.judge;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.SplittableRandom;

/**
 * Deterministic generators for large test inputs, so the repository stores a short spec instead of megabytes of JSON.
 * Example spec: {@code {"seed":7,"count":2,"args":[{"kind":"intArray","n":100000,"min":-1000,"max":1000},{"kind":"int","min":-50,"max":50}]}}
 */
public final class TestGen {
    private TestGen() {}

    public static List<List<Object>> expand(Map<String, Object> spec) {
        long seed = ((Number) spec.getOrDefault("seed", 1L)).longValue();
        int count = ((Number) spec.getOrDefault("count", 1L)).intValue();
        SplittableRandom rnd = new SplittableRandom(seed);
        List<List<Object>> out = new ArrayList<>();
        for (int c = 0; c < count; c++) {
            List<Object> args = new ArrayList<>();
            for (Object o : Json.arr(spec.get("args"))) args.add(gen(Json.obj(o), args, rnd));
            out.add(args);
        }
        return out;
    }

    private static int i(Map<String, Object> m, String k, int def) {
        Object v = m.get(k);
        return v == null ? def : ((Number) v).intValue();
    }

    private static int size(Map<String, Object> m, SplittableRandom r) {
        if (m.containsKey("n")) return i(m, "n", 1);
        int lo = i(m, "nMin", 1), hi = i(m, "nMax", lo);
        return r.nextInt(lo, hi + 1);
    }

    private static long between(SplittableRandom r, int lo, int hi) { return r.nextLong(lo, (long) hi + 1); }

    private static double probability(Map<String, Object> m, String k) {
        Object v = m.get(k);
        return v == null ? 0 : ((Number) v).doubleValue();
    }

    private static void sortAscending(List<Object> l) {
        l.sort((p, q) -> Long.compare((Long) p, (Long) q));
    }

    private static String word(String alphabet, int len, SplittableRandom r) {
        StringBuilder sb = new StringBuilder(len);
        for (int k = 0; k < len; k++) sb.append(alphabet.charAt(r.nextInt(alphabet.length())));
        return sb.toString();
    }

    /** Fisher-Yates, so a shuffled copy keeps exactly the same multiset. */
    private static void shuffle(List<Object> l, SplittableRandom r) {
        for (int k = l.size() - 1; k > 0; k--) {
            int j = r.nextInt(k + 1);
            Object t = l.get(k);
            l.set(k, l.get(j));
            l.set(j, t);
        }
    }

    private static int lengthOf(Object arg) {
        if (arg instanceof String s) return s.length();
        if (arg instanceof List<?> l) return l.size();
        return ((Number) arg).intValue();
    }

    private static Object gen(Map<String, Object> m, List<Object> prev, SplittableRandom r) {
        String kind = (String) m.get("kind");
        switch (kind) {
            case "const": return m.get("value");
            case "int": return between(r, i(m, "min", 0), i(m, "max", 0));
            case "intArray": case "bits": {
                int n = size(m, r);
                int lo = kind.equals("bits") ? 0 : i(m, "min", 0);
                // "maxIsN": true keeps the values inside 1..n (+ maxOffset), which is what the "array as hash table" problems need.
                int hi = kind.equals("bits") ? 1
                        : Boolean.TRUE.equals(m.get("maxIsN")) ? n + i(m, "maxOffset", 0)
                        : i(m, "max", 0);
                List<Object> l = new ArrayList<>(n);
                if (Boolean.TRUE.equals(m.get("distinct"))) {
                    if ((long) hi - lo + 1 < n) throw new IllegalArgumentException("intArray: \"distinct\" needs max - min + 1 >= n");
                    Set<Long> used = new HashSet<>();
                    while (l.size() < n) {
                        long v = between(r, lo, hi);
                        if (used.add(v)) l.add(v);
                    }
                } else {
                    for (int k = 0; k < n; k++) l.add(between(r, lo, hi));
                }
                if (Boolean.TRUE.equals(m.get("sorted"))) sortAscending(l);
                return l;
            }
            case "sortedWithBuffer": {
                // m sorted values followed by n zeros: the shape of "merge b into the free space at the end of a".
                int head = i(m, "m", 0), tail = i(m, "n", 0);
                List<Object> l = new ArrayList<>(head + tail);
                for (int k = 0; k < head; k++) l.add(between(r, i(m, "min", 0), i(m, "max", 0)));
                sortAscending(l);
                for (int k = 0; k < tail; k++) l.add(0L);
                return l;
            }
            case "disjointIntervals": {
                int n = i(m, "n", 1), maxGap = i(m, "maxGap", 10), maxLen = i(m, "maxLen", 10);
                List<Object> l = new ArrayList<>(n);
                long at = 0;
                for (int k = 0; k < n; k++) {
                    at += r.nextInt(maxGap + 1);
                    long end = at + r.nextInt(maxLen + 1);
                    l.add(List.of(at, end));
                    at = end + 1;                       // never overlap the interval just emitted
                }
                return l;
            }
            case "nearPalindrome": {
                // A palindrome, then `flips` positions changed, then optional junk characters sprinkled in.
                int n = size(m, r);
                String alpha = (String) m.getOrDefault("alphabet", "abcdefghijklmnopqrstuvwxyz");
                char[] cs = new char[n];
                for (int k = 0; k < (n + 1) / 2; k++) {
                    char c = alpha.charAt(r.nextInt(alpha.length()));
                    cs[k] = c;
                    cs[n - 1 - k] = c;
                }
                for (int f = i(m, "flips", 0); f > 0 && n > 0; f--) cs[r.nextInt(n)] = alpha.charAt(r.nextInt(alpha.length()));
                String noise = (String) m.getOrDefault("noise", "");
                if (noise.isEmpty()) return new String(cs);
                StringBuilder sb = new StringBuilder(2 * n + 1);
                for (int k = 0; k <= n; k++) {
                    if (r.nextInt(3) == 0) sb.append(noise.charAt(r.nextInt(noise.length())));
                    if (k < n) sb.append(cs[k]);
                }
                return sb.toString();
            }
            case "subsequenceOf": {
                String src = (String) prev.get(i(m, "of", 0));
                int need = Math.min(i(m, "len", 0), src.length());
                StringBuilder sb = new StringBuilder(need);
                for (int k = 0; k < src.length() && need > 0; k++) {
                    if (r.nextInt(src.length() - k) < need) {    // uniform subset, left to right
                        sb.append(src.charAt(k));
                        need--;
                    }
                }
                if (sb.length() > 0 && r.nextDouble() < probability(m, "flip")) {
                    String alpha = (String) m.getOrDefault("alphabet", "abcdefghijklmnopqrstuvwxyz");
                    sb.setCharAt(r.nextInt(sb.length()), alpha.charAt(r.nextInt(alpha.length())));
                }
                return sb.toString();
            }
            case "insertBackspacePairs": {
                // "x#" means "type x, then backspace", so inserting such pairs leaves the typed result unchanged.
                // The positions are chosen in the original string, so no pair is ever inserted inside another one.
                String src = (String) prev.get(i(m, "of", 0));
                int count = i(m, "count", 0);
                String alpha = (String) m.getOrDefault("alphabet", "abcdefghijklmnopqrstuvwxyz");
                int[] at = new int[count];
                for (int k = 0; k < count; k++) at[k] = r.nextInt(src.length() + 1);
                Arrays.sort(at);
                StringBuilder sb = new StringBuilder(src.length() + 2 * count);
                int next = 0;
                for (int k = 0; k <= src.length(); k++) {
                    while (next < count && at[next] == k) {
                        sb.append(alpha.charAt(r.nextInt(alpha.length()))).append('#');
                        next++;
                    }
                    if (k < src.length()) sb.append(src.charAt(k));
                }
                if (sb.length() > 0 && r.nextDouble() < probability(m, "flip")) {
                    sb.setCharAt(r.nextInt(sb.length()), alpha.charAt(r.nextInt(alpha.length())));
                }
                return sb.toString();
            }
            case "choiceArray": {
                int n = size(m, r);
                List<Object> values = Json.arr(m.get("values"));
                List<Object> l = new ArrayList<>(n);
                for (int k = 0; k < n; k++) l.add(((Number) values.get(r.nextInt(values.size()))).longValue());
                return l;
            }
            case "wordArray": {
                int n = size(m, r);
                int lo = i(m, "minLen", 1), hi = i(m, "maxLen", lo);
                String alpha = (String) m.getOrDefault("alphabet", "abcdefghijklmnopqrstuvwxyz");
                List<Object> l = new ArrayList<>(n);
                for (int k = 0; k < n; k++) l.add(word(alpha, r.nextInt(lo, hi + 1), r));
                return l;
            }
            case "shuffleOf": {
                // A rearrangement of an earlier string argument, so anagram checks cannot shortcut on the length.
                List<Object> cs = new ArrayList<>();
                String src = (String) prev.get(i(m, "of", 0));
                for (int k = 0; k < src.length(); k++) cs.add(src.charAt(k));
                shuffle(cs, r);
                StringBuilder sb = new StringBuilder(cs.size());
                for (Object c : cs) sb.append((char) (Character) c);
                if (sb.length() > 0 && r.nextDouble() < probability(m, "flip")) {
                    String alpha = (String) m.getOrDefault("alphabet", "abcdefghijklmnopqrstuvwxyz");
                    sb.setCharAt(r.nextInt(sb.length()), alpha.charAt(r.nextInt(alpha.length())));
                }
                return sb.toString();
            }
            case "sentenceFor": {
                // One distinct word per distinct letter of an earlier pattern argument, so the pattern is followed exactly.
                String pattern = (String) prev.get(i(m, "of", 0));
                List<Object> words = new ArrayList<>(Json.arr(m.get("words")));
                shuffle(words, r);
                Map<Character, String> word = new HashMap<>();
                List<String> out = new ArrayList<>(pattern.length());
                for (int k = 0; k < pattern.length(); k++) {
                    char c = pattern.charAt(k);
                    String w = word.get(c);
                    if (w == null) {
                        if (word.size() >= words.size()) throw new IllegalArgumentException("sentenceFor: fewer words than letters in the pattern");
                        word.put(c, w = (String) words.get(word.size()));
                    }
                    out.add(w);
                }
                if (!out.isEmpty() && r.nextDouble() < probability(m, "flip")) {
                    out.set(r.nextInt(out.size()), (String) words.get(r.nextInt(words.size())));
                }
                return String.join(" ", out);
            }
            case "gridWithEqualLines": {
                // An n x n grid in which `copies` columns are copies of a row, so row/column matches actually exist.
                int n = i(m, "n", 1), copies = i(m, "copies", 0);
                List<List<Object>> g = new ArrayList<>(n);
                for (int a = 0; a < n; a++) {
                    List<Object> row = new ArrayList<>(n);
                    for (int b = 0; b < n; b++) row.add(between(r, i(m, "min", 0), i(m, "max", 0)));
                    g.add(row);
                }
                for (int k = 0; k < copies; k++) {
                    List<Object> source = List.copyOf(g.get(r.nextInt(n)));
                    int c = r.nextInt(n);
                    for (int a = 0; a < n; a++) g.get(a).set(c, source.get(a));
                }
                return new ArrayList<Object>(g);
            }
            case "intMatrix": {
                int rows = i(m, "rows", 1), cols = i(m, "cols", 1);
                List<Object> g = new ArrayList<>(rows);
                for (int a = 0; a < rows; a++) {
                    List<Object> row = new ArrayList<>(cols);
                    for (int b = 0; b < cols; b++) row.add(between(r, i(m, "min", 0), i(m, "max", 0)));
                    g.add(row);
                }
                return g;
            }
            case "string": {
                int n = size(m, r);
                String alpha = (String) m.getOrDefault("alphabet", "abcdefghijklmnopqrstuvwxyz");
                StringBuilder sb = new StringBuilder(n);
                for (int k = 0; k < n; k++) sb.append(alpha.charAt(r.nextInt(alpha.length())));
                return sb.toString();
            }
            case "ranges": {
                int len = lengthOf(prev.get(i(m, "of", 0))), q = i(m, "q", 1);
                List<Object> l = new ArrayList<>(q);
                boolean wide = Boolean.TRUE.equals(m.get("wide"));
                for (int k = 0; k < q; k++) {
                    int a = wide ? r.nextInt(Math.max(1, len / 10)) : r.nextInt(len);
                    int b = wide ? len - 1 - r.nextInt(Math.max(1, len / 10)) : r.nextInt(len);
                    l.add(List.of((long) Math.min(a, b), (long) Math.max(a, b)));
                }
                return l;
            }
            case "rects": {
                List<?> grid = (List<?>) prev.get(i(m, "of", 0));
                int rows = grid.size(), cols = ((List<?>) grid.get(0)).size(), q = i(m, "q", 1);
                List<Object> l = new ArrayList<>(q);
                boolean wide = Boolean.TRUE.equals(m.get("wide"));
                for (int k = 0; k < q; k++) {
                    int r1 = wide ? r.nextInt(Math.max(1, rows / 10)) : r.nextInt(rows), r2 = wide ? rows - 1 - r.nextInt(Math.max(1, rows / 10)) : r.nextInt(rows);
                    int c1 = wide ? r.nextInt(Math.max(1, cols / 10)) : r.nextInt(cols), c2 = wide ? cols - 1 - r.nextInt(Math.max(1, cols / 10)) : r.nextInt(cols);
                    l.add(List.of((long) Math.min(r1, r2), (long) Math.min(c1, c2), (long) Math.max(r1, r2), (long) Math.max(c1, c2)));
                }
                return l;
            }
            case "updates": {
                int n = lengthOf(prev.get(i(m, "of", 0))), q = i(m, "q", 1);
                List<Object> l = new ArrayList<>(q);
                boolean wide = Boolean.TRUE.equals(m.get("wide"));
                for (int k = 0; k < q; k++) {
                    int a = wide ? r.nextInt(Math.max(1, n / 10)) : r.nextInt(n), b = wide ? n - 1 - r.nextInt(Math.max(1, n / 10)) : r.nextInt(n);
                    l.add(List.of((long) Math.min(a, b), (long) Math.max(a, b), between(r, i(m, "min", 0), i(m, "max", 0))));
                }
                return l;
            }
            case "intervals": {
                int q = i(m, "q", 1), maxT = i(m, "maxTime", 100);
                List<Object> l = new ArrayList<>(q);
                for (int k = 0; k < q; k++) {
                    int a = r.nextInt(maxT), len = 1 + r.nextInt(Math.max(1, i(m, "maxLen", maxT)));
                    l.add(List.of((long) a, (long) Math.min(maxT, a + len)));
                }
                return l;
            }
            case "trips": {
                int q = i(m, "q", 1), maxLoc = i(m, "maxLoc", 100), maxC = i(m, "maxCount", 10);
                List<Object> l = new ArrayList<>(q);
                for (int k = 0; k < q; k++) {
                    int a = r.nextInt(maxLoc), b = a + 1 + r.nextInt(Math.max(1, maxLoc - a));
                    l.add(List.of(between(r, 1, maxC), (long) a, (long) Math.min(b, maxLoc)));
                }
                return l;
            }
            default: throw new IllegalArgumentException("Unknown generator kind: " + kind);
        }
    }
}
