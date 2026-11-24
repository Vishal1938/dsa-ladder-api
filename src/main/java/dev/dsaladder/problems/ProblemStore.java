package dev.dsaladder.problems;

import dev.dsaladder.judge.Compare;
import dev.dsaladder.judge.FunctionSpec;
import dev.dsaladder.judge.Json;
import dev.dsaladder.judge.Judge;
import dev.dsaladder.judge.TestGen;
import dev.dsaladder.problems.ProblemModel.Example;
import dev.dsaladder.problems.ProblemModel.ExamProblem;
import dev.dsaladder.problems.ProblemModel.Problem;
import dev.dsaladder.problems.ProblemModel.Stage;
import dev.dsaladder.problems.ProblemModel.Topic;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.stream.Stream;

/**
 * Loads topics and problem books from disk:
 * <pre>
 * problems/topics.json
 * problems/&lt;topic&gt;/&lt;NN-slug&gt;/problem.json | statement.md | Solution.java (reference) | tests.json
 * </pre>
 * Generated tests are expanded and their expected answers computed by running the reference solution, which also
 * verifies every hand-written expected answer. Any mismatch is reported as a load error.
 */
public final class ProblemStore {

    private final List<Topic> topics = new ArrayList<>();
    private final Map<String, Problem> bySlug = new LinkedHashMap<>();
    private final List<String> errors = Collections.synchronizedList(new ArrayList<>());

    public static ProblemStore load(Path root, Judge judge, int threads) throws IOException {
        ProblemStore s = new ProblemStore();
        s.loadTopics(root);
        List<Path> dirs = new ArrayList<>();
        for (Topic t : s.topics) {
            Path td = root.resolve(t.id());
            if (!Files.isDirectory(td)) continue;
            try (Stream<Path> st = Files.list(td)) {
                st.filter(p -> Files.isRegularFile(p.resolve("problem.json"))).sorted().forEach(dirs::add);
            }
        }
        ExecutorService pool = Executors.newFixedThreadPool(Math.max(1, threads));
        List<Future<Problem>> fs = new ArrayList<>();
        for (Path d : dirs) fs.add(pool.submit(() -> s.loadProblem(d, judge)));
        for (Future<Problem> f : fs) {
            try {
                Problem p = f.get();
                if (p != null) s.bySlug.put(p.slug(), p);
            } catch (Exception e) {
                s.errors.add(String.valueOf(e.getCause() == null ? e : e.getCause()));
            }
        }
        pool.shutdown();
        // keep a stable order: topic, stage, order
        List<Problem> sorted = new ArrayList<>(s.bySlug.values());
        List<String> topicOrder = s.topics.stream().map(Topic::id).toList();
        sorted.sort(Comparator.comparing((Problem p) -> topicOrder.indexOf(p.topic())).thenComparing(Problem::stage).thenComparing(Problem::order));
        s.bySlug.clear();
        sorted.forEach(p -> s.bySlug.put(p.slug(), p));
        List<Topic> withFlags = new ArrayList<>();
        for (Topic t : s.topics) {
            boolean has = sorted.stream().anyMatch(p -> p.topic().equals(t.id()));
            withFlags.add(new Topic(t.id(), t.name(), t.idea(), t.triggers(), t.stages(), has));
        }
        s.topics.clear();
        s.topics.addAll(withFlags);
        return s;
    }

    private void loadTopics(Path root) throws IOException {
        Object parsed = Json.parse(Files.readString(root.resolve("topics.json")));
        for (Object o : Json.arr(parsed)) {
            Map<String, Object> t = Json.obj(o);
            List<Stage> stages = new ArrayList<>();
            int si = 0;
            for (Object so : Json.arr(t.get("stages"))) {
                Map<String, Object> sm = Json.obj(so);
                List<ExamProblem> exam = new ArrayList<>();
                for (Object eo : Json.arr(sm.getOrDefault("exam", List.of()))) {
                    Map<String, Object> em = Json.obj(eo);
                    exam.add(new ExamProblem(((Number) em.get("id")).intValue(), (String) em.get("title"), (String) em.get("slug"),
                            (String) em.getOrDefault("note", ""), ((Number) em.getOrDefault("rating", 0L)).intValue()));
                }
                stages.add(new Stage(si++, (String) sm.get("name"), (String) sm.getOrDefault("summary", ""), exam));
            }
            List<String> triggers = new ArrayList<>();
            for (Object x : Json.arr(t.getOrDefault("triggers", List.of()))) triggers.add((String) x);
            topics.add(new Topic((String) t.get("id"), (String) t.get("name"), (String) t.get("idea"), triggers, stages, false));
        }
    }

    private Problem loadProblem(Path dir, Judge judge) throws IOException {
        Map<String, Object> meta = Json.obj(Json.parse(Files.readString(dir.resolve("problem.json"))));
        String slug = (String) meta.get("slug");
        FunctionSpec fn = FunctionSpec.fromJson(Json.obj(meta.get("function")));
        Compare cmp = Compare.of((String) meta.get("compare"));
        long tl = ((Number) meta.getOrDefault("timeLimitMs", 2000L)).longValue();
        String ref = Files.readString(dir.resolve("Solution.java"));
        Map<String, Object> tests = Json.obj(Json.parse(Files.readString(dir.resolve("tests.json"))));

        List<Map<String, Object>> raw = new ArrayList<>(); // {args, expected?, hidden, explanation?}
        for (Object o : Json.arr(tests.getOrDefault("examples", List.of()))) {
            Map<String, Object> m = Json.obj(o);
            raw.add(Map.of("args", m.get("input"), "hidden", false, "expected", m.getOrDefault("output", Missing.M),
                    "explanation", m.getOrDefault("explanation", "")));
        }
        for (Object o : Json.arr(tests.getOrDefault("tests", List.of()))) {
            Map<String, Object> m = Json.obj(o);
            raw.add(Map.of("args", m.get("input"), "hidden", true, "expected", m.getOrDefault("output", Missing.M), "explanation", ""));
        }
        for (Object o : Json.arr(tests.getOrDefault("generated", List.of()))) {
            for (List<Object> args : TestGen.expand(Json.obj(o))) raw.add(Map.of("args", args, "hidden", true, "expected", Missing.M, "explanation", ""));
        }
        // Run the reference solution on everything: fills generated answers and verifies hand-written ones.
        Judge.Compiled c = judge.compile(fn, ref);
        if (!c.ok()) throw new IllegalStateException(slug + ": reference solution does not compile:\n" + c.output());
        List<List<Object>> inputs = new ArrayList<>();
        for (Map<String, Object> r : raw) inputs.add(Json.arr(r.get("args")));
        Judge.RunOutput out = judge.run(c, inputs, Math.max(20_000, tl * 10));
        try { java.nio.file.Files.walk(c.dir()).sorted(Comparator.reverseOrder()).forEach(p -> p.toFile().delete()); } catch (IOException ignored) { }
        if (out.results().size() != inputs.size()) {
            throw new IllegalStateException(slug + ": reference solution failed on test " + out.results().size() + ": "
                    + (out.error() != null ? out.error() : out.timedOut() ? "timed out" : out.internal()));
        }
        List<Judge.TestCase> samples = new ArrayList<>(), all = new ArrayList<>();
        List<Example> examples = new ArrayList<>();
        for (int i = 0; i < raw.size(); i++) {
            Map<String, Object> r = raw.get(i);
            Object exp = r.get("expected");
            Object refAns = out.results().get(i);
            if (exp != Missing.M && !cmp.equal(exp, refAns)) {
                errors.add(slug + ": test " + i + " expects " + Json.stringify(exp) + " but the reference returns " + Json.stringify(refAns));
            }
            Object use = exp == Missing.M ? refAns : exp;
            Judge.TestCase tc = new Judge.TestCase(Json.arr(r.get("args")), use, (Boolean) r.get("hidden"));
            all.add(tc);
            if (!(Boolean) r.get("hidden")) {
                samples.add(tc);
                examples.add(new Example(describeArgs(fn, tc.args()), Json.stringify(use), (String) r.get("explanation")));
            }
        }
        List<String> hints = new ArrayList<>();
        for (Object h : Json.arr(meta.getOrDefault("hints", List.of()))) hints.add((String) h);
        return new Problem(slug, (String) meta.get("topic"), ((Number) meta.get("stage")).intValue(),
                ((Number) meta.get("order")).intValue(), (String) meta.get("title"), (String) meta.getOrDefault("difficulty", "Easy"),
                (String) meta.getOrDefault("whatsNew", ""), Files.readString(dir.resolve("statement.md")), examples, hints,
                (String) meta.getOrDefault("trigger", ""), fn, cmp, tl, ref, samples, all);
    }

    /** "nums = [1,2,3], k = 2" */
    public static String describeArgs(FunctionSpec fn, List<Object> args) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < args.size(); i++) {
            if (i > 0) sb.append(", ");
            String name = i < fn.params().size() ? fn.params().get(i).name() : "arg" + i;
            sb.append(name).append(" = ").append(Json.stringify(args.get(i)));
        }
        return sb.toString();
    }

    private enum Missing { M }

    public List<Topic> topics() { return topics; }
    public Topic topic(String id) { return topics.stream().filter(t -> t.id().equals(id)).findFirst().orElse(null); }
    public Problem problem(String slug) { return bySlug.get(slug); }
    public List<Problem> problems() { return List.copyOf(bySlug.values()); }
    public List<Problem> problems(String topic) { return bySlug.values().stream().filter(p -> p.topic().equals(topic)).toList(); }
    public List<String> errors() { return errors; }
}
