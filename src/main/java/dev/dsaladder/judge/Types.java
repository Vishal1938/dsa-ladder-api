package dev.dsaladder.judge;

import java.util.List;

/** Checks that a parsed JSON value has the shape of a Java parameter type, so custom inputs fail with a clear message. */
public final class Types {
    private Types() {}

    public static boolean matches(String type, Object v) {
        switch (type) {
            case "int": return v instanceof Long l && l >= Integer.MIN_VALUE && l <= Integer.MAX_VALUE;
            case "long": return v instanceof Long;
            case "double": return v instanceof Number;
            case "boolean": return v instanceof Boolean;
            case "char": return v instanceof String s && s.length() == 1;
            case "String": return v instanceof String;
            default: break;
        }
        if (type.endsWith("[]")) {
            String inner = type.substring(0, type.length() - 2);
            if (inner.equals("char") && v instanceof String) return true;
            return v instanceof List<?> l && l.stream().allMatch(x -> matches(inner, x));
        }
        if (type.startsWith("List<") && type.endsWith(">")) {
            String inner = type.substring(5, type.length() - 1);
            String javaInner = switch (inner) { case "Integer" -> "int"; case "Long" -> "long"; default -> inner; };
            return v instanceof List<?> l && l.stream().allMatch(x -> matches(javaInner, x));
        }
        if (type.equals("ListNode")) return v instanceof List<?> l && l.stream().allMatch(x -> matches("int", x));
        if (type.equals("TreeNode")) return v instanceof List<?> l && l.stream().allMatch(x -> x == null || matches("int", x));
        return false;
    }
}
