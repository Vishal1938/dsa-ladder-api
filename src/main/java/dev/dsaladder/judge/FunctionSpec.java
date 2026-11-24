package dev.dsaladder.judge;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * The method a problem asks the user to implement, e.g. {@code long[] rangeSums(int[] nums, int[][] queries)}.
 * Types are Java source types; each must be listed in {@link #CONVERTERS}.
 */
public record FunctionSpec(String name, String returns, List<Param> params, Integer outputArg) {

    public record Param(String name, String type) {}

    /** Java type → name of the converter in the harness class {@code J}. */
    static final Map<String, String> CONVERTERS = Map.ofEntries(
            Map.entry("int", "toInt"), Map.entry("long", "toLong"), Map.entry("double", "toDouble"),
            Map.entry("boolean", "toBoolean"), Map.entry("char", "toChar"), Map.entry("String", "toString"),
            Map.entry("int[]", "toIntArr"), Map.entry("long[]", "toLongArr"), Map.entry("double[]", "toDoubleArr"),
            Map.entry("boolean[]", "toBooleanArr"), Map.entry("char[]", "toCharArr"), Map.entry("String[]", "toStringArr"),
            Map.entry("int[][]", "toIntArr2"), Map.entry("long[][]", "toLongArr2"), Map.entry("char[][]", "toCharArr2"),
            Map.entry("String[][]", "toStringArr2"),
            Map.entry("List<Integer>", "toListInt"), Map.entry("List<Long>", "toListLong"), Map.entry("List<String>", "toListString"),
            Map.entry("List<List<Integer>>", "toListListInt"), Map.entry("List<List<String>>", "toListListString"),
            Map.entry("ListNode", "toListNode"), Map.entry("TreeNode", "toTreeNode"));

    public static FunctionSpec fromJson(Map<String, Object> m) {
        List<Param> ps = new ArrayList<>();
        for (Object o : Json.arr(m.get("params"))) {
            Map<String, Object> p = Json.obj(o);
            String type = (String) p.get("type");
            if (!CONVERTERS.containsKey(type)) throw new IllegalArgumentException("Unsupported parameter type: " + type);
            ps.add(new Param((String) p.get("name"), type));
        }
        Object oa = m.get("outputArg");
        String ret = (String) m.get("returns");
        if (!"void".equals(ret) && !CONVERTERS.containsKey(ret)) throw new IllegalArgumentException("Unsupported return type: " + ret);
        if ("void".equals(ret) && oa == null) throw new IllegalArgumentException("void functions need outputArg");
        return new FunctionSpec((String) m.get("name"), ret, ps, oa == null ? null : ((Number) oa).intValue());
    }

    /** Java code for the harness's {@code call} method. */
    String callSource() {
        StringBuilder sb = new StringBuilder("static Object call(List<Object> a) throws Throwable {\n        Solution s = new Solution();\n");
        for (int i = 0; i < params.size(); i++) {
            Param p = params.get(i);
            sb.append("        ").append(p.type()).append(" p").append(i).append(" = J.")
              .append(CONVERTERS.get(p.type())).append("(a.get(").append(i).append("));\n");
        }
        StringBuilder args = new StringBuilder();
        for (int i = 0; i < params.size(); i++) args.append(i > 0 ? ", " : "").append('p').append(i);
        if ("void".equals(returns)) {
            sb.append("        s.").append(name).append('(').append(args).append(");\n        return p").append(outputArg).append(";\n");
        } else {
            sb.append("        return s.").append(name).append('(').append(args).append(");\n");
        }
        return sb.append("    }").toString();
    }

    /** The code shown in the editor when a user opens the problem. */
    public String starterCode() {
        StringBuilder sb = new StringBuilder("import java.util.*;\n\n");
        boolean list = params.stream().anyMatch(p -> p.type().equals("ListNode")) || "ListNode".equals(returns);
        boolean tree = params.stream().anyMatch(p -> p.type().equals("TreeNode")) || "TreeNode".equals(returns);
        if (list) sb.append("/* Provided for you:\n * class ListNode { int val; ListNode next; ListNode(int val) { this.val = val; } }\n */\n");
        if (tree) sb.append("/* Provided for you:\n * class TreeNode { int val; TreeNode left, right; TreeNode(int val) { this.val = val; } }\n */\n");
        sb.append("class Solution {\n    public ").append(returns).append(' ').append(name).append('(');
        for (int i = 0; i < params.size(); i++) sb.append(i > 0 ? ", " : "").append(params.get(i).type()).append(' ').append(params.get(i).name());
        sb.append(") {\n        \n    }\n}\n");
        return sb.toString();
    }

    public String signature() {
        StringBuilder sb = new StringBuilder(returns).append(' ').append(name).append('(');
        for (int i = 0; i < params.size(); i++) sb.append(i > 0 ? ", " : "").append(params.get(i).type()).append(' ').append(params.get(i).name());
        return sb.append(')').toString();
    }
}
