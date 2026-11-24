package dev.dsaladder.api;

import dev.dsaladder.judge.Verdict;

import java.time.Instant;
import java.util.List;
import java.util.Map;

/** JSON shapes of the public API. The frontend's src/api/types.ts mirrors these. */
public final class Dtos {
    private Dtos() {}

    public record TopicSummary(String id, String name, String idea, boolean hasBook, int stageCount, int problemCount, int solvedCount) {}

    public record ExamDto(int id, String title, String url, String note, int rating) {}

    public record ProblemRow(String slug, String title, String difficulty, String whatsNew, int order, boolean solved, boolean attempted) {}

    public record StageDto(int index, String name, List<ProblemRow> problems, List<ExamDto> exam) {}

    public record TopicDetail(String id, String name, String idea, List<String> triggers, boolean hasBook, List<StageDto> stages) {}

    public record ExampleDto(String input, String output, String explanation) {}

    public record ParamDto(String name, String type) {}

    public record ProblemDetail(String slug, String title, String topic, String topicName, int stage, String stageName,
                                String difficulty, String whatsNew, String statement, List<ExampleDto> examples,
                                List<String> hints, String trigger, String starterCode, String signature, List<ParamDto> params,
                                List<List<String>> sampleInputs, long timeLimitMs, String prev, String next, boolean solved) {}

    public record RunRequest(String code, List<List<String>> inputs) {}

    public record SubmitRequest(String code) {}

    public record CaseDto(int index, boolean passed, boolean hidden, String input, String expected, String actual,
                          String stdout, Long runtimeMicros) {}

    public record VerdictDto(String status, int passed, int total, long runtimeMs, String compileOutput, String error,
                             List<CaseDto> cases, Long submissionId, boolean saved) {
        public static VerdictDto of(Verdict v, Long submissionId, boolean saved) {
            return new VerdictDto(v.status().name(), v.passed(), v.total(), v.runtimeMs(), v.compileOutput(), v.error(),
                    v.cases().stream().map(c -> new CaseDto(c.index(), c.passed(), c.hidden(), c.input(), c.expected(),
                            c.actual(), c.stdout(), c.runtimeMicros())).toList(), submissionId, saved);
        }
    }

    public record SubmissionDto(Long id, String problemSlug, String status, int passed, int total, long runtimeMs,
                                Instant createdAt, String code) {}

    public record Stats(int solved, int attempted, int totalProblems, Map<String, Integer> solvedByTopic, List<SubmissionDto> recent) {}
}
