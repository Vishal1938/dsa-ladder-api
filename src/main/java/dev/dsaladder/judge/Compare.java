package dev.dsaladder.judge;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/** How a problem compares the user's answer with the expected one. */
public enum Compare {
    /** Same JSON value. Integers and longs compare numerically. */
    EXACT,
    /** The outer list may be in any order. */
    UNORDERED,
    /** Inner lists and the outer list may be in any order (subsets, groups, combinations). */
    UNORDERED_DEEP,
    /** Numbers within 1e-5 absolute or relative error. */
    FLOAT;

    public static Compare of(String s) {
        return s == null ? EXACT : Compare.valueOf(s.toUpperCase().replace('-', '_'));
    }

    public boolean equal(Object expected, Object actual) {
        return switch (this) {
            case EXACT -> eq(expected, actual, false);
            case FLOAT -> eq(expected, actual, true);
            case UNORDERED -> expected instanceof List<?> e && actual instanceof List<?> a && eq(sorted(e), sorted(a), false);
            case UNORDERED_DEEP -> expected instanceof List<?> e && actual instanceof List<?> a && eq(deepSorted(e), deepSorted(a), false);
        };
    }

    private static boolean eq(Object e, Object a, boolean tol) {
        if (e == null || a == null) return e == a;
        if (e instanceof Number x && a instanceof Number y) {
            if (tol || x instanceof Double || y instanceof Double) {
                double d1 = x.doubleValue(), d2 = y.doubleValue();
                double diff = Math.abs(d1 - d2);
                return diff <= 1e-5 || diff <= 1e-5 * Math.max(Math.abs(d1), Math.abs(d2));
            }
            return x.longValue() == y.longValue();
        }
        if (e instanceof List<?> x && a instanceof List<?> y) {
            if (x.size() != y.size()) return false;
            for (int i = 0; i < x.size(); i++) if (!eq(x.get(i), y.get(i), tol)) return false;
            return true;
        }
        return Objects.equals(e, a);
    }

    private static List<Object> sorted(List<?> l) {
        List<Object> c = new ArrayList<>(l);
        c.sort((p, q) -> Json.stringify(p).compareTo(Json.stringify(q)));
        return c;
    }

    private static Object deepSorted(Object o) {
        if (!(o instanceof List<?> l)) return o;
        List<Object> c = new ArrayList<>();
        for (Object x : l) c.add(deepSorted(x));
        c.sort((p, q) -> Json.stringify(p).compareTo(Json.stringify(q)));
        return c;
    }
}
