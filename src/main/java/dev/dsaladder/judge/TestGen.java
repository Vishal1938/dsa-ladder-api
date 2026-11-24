package dev.dsaladder.judge;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
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
                int lo = kind.equals("bits") ? 0 : i(m, "min", 0), hi = kind.equals("bits") ? 1 : i(m, "max", 0);
                List<Object> l = new ArrayList<>(n);
                for (int k = 0; k < n; k++) l.add(between(r, lo, hi));
                return l;
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
