package dev.dsaladder.problems;

import dev.dsaladder.judge.Compare;
import dev.dsaladder.judge.FunctionSpec;
import dev.dsaladder.judge.Judge;

import java.util.List;

/** Plain data loaded from the problems/ directory. No framework types, so the CLI can use it too. */
public final class ProblemModel {
    private ProblemModel() {}

    public record Topic(String id, String name, String idea, List<String> triggers, List<Stage> stages, boolean hasBook) {}

    public record Stage(int index, String name, String summary, List<ExamProblem> exam) {}

    /** A LeetCode problem used as a stage's final exam. */
    public record ExamProblem(int id, String title, String slug, String note, int rating) {
        public String url() { return "https://leetcode.com/problems/" + slug + "/"; }
    }

    public record Example(String input, String output, String explanation) {}

    public record Problem(
            String slug, String topic, int stage, int order, String title, String difficulty,
            String whatsNew, String statement, List<Example> examples, List<String> hints, String trigger,
            FunctionSpec function, Compare compare, long timeLimitMs,
            String referenceSolution, List<Judge.TestCase> sampleTests, List<Judge.TestCase> allTests) {}
}
