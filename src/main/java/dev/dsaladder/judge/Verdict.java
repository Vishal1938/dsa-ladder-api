package dev.dsaladder.judge;

import java.util.List;

/** Result of judging one submission (or one "Run" against sample cases). */
public record Verdict(
        Status status,
        int passed,
        int total,
        long runtimeMs,
        String compileOutput,
        String error,
        List<CaseResult> cases) {

    public enum Status { ACCEPTED, WRONG_ANSWER, COMPILE_ERROR, RUNTIME_ERROR, TIME_LIMIT_EXCEEDED, OUTPUT_LIMIT_EXCEEDED, INTERNAL_ERROR }

    /**
     * One test case. {@code hidden} cases only expose their input/expected/actual when they are the failing case.
     * Values are JSON strings so the API can pass them through untouched.
     */
    public record CaseResult(int index, boolean passed, boolean hidden, String input, String expected, String actual,
                             String stdout, Long runtimeMicros) {}
}
