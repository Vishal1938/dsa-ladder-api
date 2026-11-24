package dev.dsaladder.judge;

import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class JudgeTest {
    private final Judge judge = new Judge(JudgeConfig.defaults());
    private final FunctionSpec sum = FunctionSpec.fromJson(Json.obj(Json.parse(
            "{\"name\":\"total\",\"returns\":\"long\",\"params\":[{\"name\":\"nums\",\"type\":\"int[]\"}]}")));
    private final List<Judge.TestCase> cases = List.of(
            new Judge.TestCase(List.of(List.of(1L, 2L, 3L)), 6L, false),
            new Judge.TestCase(List.of(List.of(-5L)), -5L, true));

    private Verdict judge(String body) {
        return judge.judge(sum, "class Solution { public long total(int[] nums) { " + body + " } }", cases, Compare.EXACT, 1000, true);
    }

    @Test
    void accepted() {
        Verdict v = judge("long s = 0; for (int x : nums) s += x; return s;");
        assertEquals(Verdict.Status.ACCEPTED, v.status());
        assertEquals(2, v.passed());
    }

    @Test
    void wrongAnswerShowsFailingHiddenCase() {
        Verdict v = judge("long s = 0; for (int x : nums) s += Math.abs(x); return s;");
        assertEquals(Verdict.Status.WRONG_ANSWER, v.status());
        Verdict.CaseResult last = v.cases().get(v.cases().size() - 1);
        assertEquals("[[-5]]", last.input());
        assertEquals("5", last.actual());
    }

    @Test
    void compileErrorPointsAtLine() {
        Verdict v = judge("return y;");
        assertEquals(Verdict.Status.COMPILE_ERROR, v.status());
        assertTrue(v.compileOutput().startsWith("Line 1:"), v.compileOutput());
    }

    @Test
    void runtimeError() {
        Verdict v = judge("return nums[10];");
        assertEquals(Verdict.Status.RUNTIME_ERROR, v.status());
        assertTrue(v.error().contains("ArrayIndexOutOfBoundsException"), v.error());
    }

    @Test
    void timeLimit() {
        Verdict v = judge("while (true) {}");
        assertEquals(Verdict.Status.TIME_LIMIT_EXCEEDED, v.status());
    }

    @Test
    void capturesStdout() {
        Verdict v = judge("System.out.println(\"hi\"); long s = 0; for (int x : nums) s += x; return s;");
        assertEquals("hi\n", v.cases().get(0).stdout());
    }

    @Test
    void unorderedDeepCompare() {
        assertTrue(Compare.UNORDERED_DEEP.equal(Json.parse("[[1,2],[3]]"), Json.parse("[[3],[2,1]]")));
    }

    @Test
    void generatorIsDeterministic() {
        Map<String, Object> spec = Json.obj(Json.parse("{\"seed\":5,\"count\":1,\"args\":[{\"kind\":\"intArray\",\"n\":50,\"min\":-9,\"max\":9}]}"));
        assertEquals(TestGen.expand(spec), TestGen.expand(spec));
    }
}
