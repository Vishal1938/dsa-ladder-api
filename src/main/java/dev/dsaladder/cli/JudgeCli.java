package dev.dsaladder.cli;

import dev.dsaladder.judge.Json;
import dev.dsaladder.judge.Judge;
import dev.dsaladder.judge.JudgeConfig;
import dev.dsaladder.judge.Verdict;
import dev.dsaladder.problems.ProblemModel.Problem;
import dev.dsaladder.problems.ProblemStore;

import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Command-line entry point for problem authors and CI.
 * <pre>
 *   check  &lt;problemsDir&gt;                       load every problem, verify references and tests
 *   judge  &lt;problemsDir&gt; &lt;slug&gt; run|submit      judge code read from stdin, print the verdict as JSON
 * </pre>
 */
public final class JudgeCli {
    public static void main(String[] args) throws Exception {
        if (args.length < 2) {
            System.err.println("usage: check <problemsDir> | judge <problemsDir> <slug> run|submit < code");
            System.exit(2);
        }
        Judge judge = new Judge(JudgeConfig.defaults());
        long t0 = System.currentTimeMillis();
        ProblemStore store = ProblemStore.load(Path.of(args[1]), judge, Runtime.getRuntime().availableProcessors());
        if (args[0].equals("check")) {
            for (Problem p : store.problems()) {
                Verdict v = judge.judge(p.function(), p.referenceSolution(), p.allTests(), p.compare(), p.timeLimitMs(), true);
                System.out.printf("  %-30s stage %d  %3d tests (%d samples)  reference %s in %d ms (limit %d)%n", p.slug(), p.stage() + 1, p.allTests().size(), p.sampleTests().size(), v.status(), v.runtimeMs(), p.timeLimitMs());
                if (v.status() != Verdict.Status.ACCEPTED) store.errors().add(p.slug() + ": reference gets " + v.status() + " under the time limit (" + v.runtimeMs() + " ms)");
                Verdict s = judge.judge(p.function(), p.function().starterCode(), p.sampleTests(), p.compare(), p.timeLimitMs(), true);
                if (s.status() != Verdict.Status.COMPILE_ERROR) store.errors().add(p.slug() + ": starter code unexpectedly compiles");
            }
            System.out.printf("%d problems loaded in %d ms%n", store.problems().size(), System.currentTimeMillis() - t0);
            if (!store.errors().isEmpty()) {
                store.errors().forEach(e -> System.out.println("ERROR " + e));
                System.exit(1);
            }
            System.out.println("All problems OK");
            return;
        }
        if (args[0].equals("crosscheck")) {
            int bad = 0, total = 0;
            for (Problem p : store.problems()) {
                Path dir;
                try (var st = java.nio.file.Files.list(Path.of(args[1], p.topic()))) {
                    dir = st.filter(d -> d.getFileName().toString().endsWith("-" + p.slug())).findFirst().orElseThrow();
                }
                Path brute = dir.resolve("Brute.java");
                if (!java.nio.file.Files.exists(brute)) continue;
                Map<String, Object> tests = Json.obj(Json.parse(java.nio.file.Files.readString(dir.resolve("tests.json"))));
                List<Judge.TestCase> cases = new ArrayList<>();
                Judge.Compiled ref = judge.compile(p.function(), p.referenceSolution());
                for (Object spec : Json.arr(tests.getOrDefault("crosscheck", List.of()))) {
                    List<List<Object>> inputs = dev.dsaladder.judge.TestGen.expand(Json.obj(spec));
                    Judge.RunOutput r = judge.run(ref, inputs, 20000);
                    for (int i = 0; i < inputs.size(); i++) cases.add(new Judge.TestCase(inputs.get(i), r.results().get(i), false));
                }
                Verdict v = judge.judge(p.function(), java.nio.file.Files.readString(brute), cases, p.compare(), 60000, true);
                total += cases.size();
                String msg = v.status() == Verdict.Status.ACCEPTED ? "agree on " + cases.size() + " random inputs"
                        : "DISAGREE " + v.status() + " " + (v.cases().isEmpty() ? v.compileOutput() + " " + v.error() : v.cases().get(v.cases().size() - 1));
                if (v.status() != Verdict.Status.ACCEPTED) bad++;
                System.out.printf("  %-30s %s%n", p.slug(), msg);
            }
            System.out.println(bad == 0 ? "Reference and brute force agree on all " + total + " inputs" : bad + " problems disagree");
            System.exit(bad == 0 ? 0 : 1);
        }
        if (args[0].equals("export")) {
            // Writes the read-only API responses (same shapes as the Spring DTOs) for the frontend's dev server.
            Path out = Path.of(args[2]);
            java.nio.file.Files.createDirectories(out);
            List<Object> topics = new ArrayList<>();
            for (var t : store.topics()) {
                List<Problem> ps = store.problems(t.id());
                Map<String, Object> m = new LinkedHashMap<>();
                m.put("id", t.id()); m.put("name", t.name()); m.put("idea", t.idea()); m.put("hasBook", t.hasBook());
                m.put("stageCount", t.stages().size()); m.put("problemCount", ps.size()); m.put("solvedCount", 0);
                topics.add(m);
                Map<String, Object> d = new LinkedHashMap<>();
                d.put("id", t.id()); d.put("name", t.name()); d.put("idea", t.idea()); d.put("triggers", t.triggers()); d.put("hasBook", t.hasBook());
                List<Object> stages = new ArrayList<>();
                for (var s : t.stages()) {
                    Map<String, Object> sm = new LinkedHashMap<>();
                    sm.put("index", s.index()); sm.put("name", s.name());
                    List<Object> rows = new ArrayList<>();
                    for (Problem p : ps) if (p.stage() == s.index()) {
                        Map<String, Object> r = new LinkedHashMap<>();
                        r.put("slug", p.slug()); r.put("title", p.title()); r.put("difficulty", p.difficulty()); r.put("whatsNew", p.whatsNew());
                        r.put("order", p.order()); r.put("solved", false); r.put("attempted", false);
                        rows.add(r);
                    }
                    sm.put("problems", rows);
                    List<Object> exam = new ArrayList<>();
                    for (var e : s.exam()) { Map<String, Object> em = new LinkedHashMap<>(); em.put("id", e.id()); em.put("title", e.title()); em.put("url", e.url()); em.put("note", e.note()); em.put("rating", e.rating()); exam.add(em); }
                    sm.put("exam", exam);
                    stages.add(sm);
                }
                d.put("stages", stages);
                java.nio.file.Files.writeString(out.resolve("topic-" + t.id() + ".json"), Json.stringify(d));
                for (int i = 0; i < ps.size(); i++) {
                    Problem p = ps.get(i);
                    Map<String, Object> pm = new LinkedHashMap<>();
                    pm.put("slug", p.slug()); pm.put("title", p.title()); pm.put("topic", p.topic()); pm.put("topicName", t.name());
                    pm.put("stage", p.stage()); pm.put("stageName", t.stages().get(p.stage()).name()); pm.put("difficulty", p.difficulty());
                    pm.put("whatsNew", p.whatsNew()); pm.put("statement", p.statement());
                    List<Object> ex = new ArrayList<>();
                    for (var e : p.examples()) { Map<String, Object> em = new LinkedHashMap<>(); em.put("input", e.input()); em.put("output", e.output()); em.put("explanation", e.explanation()); ex.add(em); }
                    pm.put("examples", ex); pm.put("hints", p.hints()); pm.put("trigger", p.trigger());
                    pm.put("starterCode", p.function().starterCode()); pm.put("signature", p.function().signature());
                    List<Object> params = new ArrayList<>();
                    for (var prm : p.function().params()) { Map<String, Object> x = new LinkedHashMap<>(); x.put("name", prm.name()); x.put("type", prm.type()); params.add(x); }
                    pm.put("params", params);
                    List<Object> samples = new ArrayList<>();
                    for (Judge.TestCase tc : p.sampleTests()) samples.add(tc.args().stream().map(Json::stringify).toList());
                    pm.put("sampleInputs", samples); pm.put("timeLimitMs", p.timeLimitMs());
                    pm.put("prev", i > 0 ? ps.get(i - 1).slug() : null); pm.put("next", i < ps.size() - 1 ? ps.get(i + 1).slug() : null);
                    pm.put("solved", false);
                    java.nio.file.Files.writeString(out.resolve("problem-" + p.slug() + ".json"), Json.stringify(pm));
                }
            }
            java.nio.file.Files.writeString(out.resolve("topics.json"), Json.stringify(topics));
            System.out.println("exported to " + out);
            return;
        }
        if (args[0].equals("serve")) {
            // Line-based judge server for the dev API: one JSON request per line → one verdict JSON per line.
            System.out.println("READY");
            java.io.BufferedReader br = new java.io.BufferedReader(new java.io.InputStreamReader(System.in, StandardCharsets.UTF_8));
            String line;
            while ((line = br.readLine()) != null) {
                Map<String, Object> req = Json.obj(Json.parse(line));
                Problem p = store.problem((String) req.get("slug"));
                String code = (String) req.get("code");
                if ("check".equals(req.get("mode"))) {
                    List<Object> ds = new ArrayList<>();
                    for (Judge.CompileIssue d : judge.diagnose(p.function(), code)) {
                        Map<String, Object> dm = new LinkedHashMap<>();
                        dm.put("startLine", d.startLine()); dm.put("startColumn", d.startColumn());
                        dm.put("endLine", d.endLine()); dm.put("endColumn", d.endColumn());
                        dm.put("severity", d.severity()); dm.put("message", d.message());
                        ds.add(dm);
                    }
                    System.out.println(Json.stringify(Map.of("diagnostics", ds)));
                    System.out.flush();
                    continue;
                }
                Verdict v = "submit".equals(req.get("mode"))
                        ? judge.judge(p.function(), code, p.allTests(), p.compare(), p.timeLimitMs(), true)
                        : judge.judge(p.function(), code, p.sampleTests(), p.compare(), p.timeLimitMs(), false);
                System.out.println(Json.stringify(toMap(v)));
                System.out.flush();
            }
            return;
        }
        if (args[0].equals("judge")) {
            Problem p = store.problem(args[2]);
            String code = new String(System.in.readAllBytes(), StandardCharsets.UTF_8);
            boolean submit = args.length > 3 && args[3].equals("submit");
            Verdict v = judge.judge(p.function(), code, submit ? p.allTests() : p.sampleTests(), p.compare(), p.timeLimitMs(), submit);
            System.out.println(Json.stringify(toMap(v)));
        }
    }

    static Map<String, Object> toMap(Verdict v) {
        Map<String, Object> m = new LinkedHashMap<>();
        m.put("status", v.status().name());
        m.put("passed", v.passed());
        m.put("total", v.total());
        m.put("runtimeMs", v.runtimeMs());
        m.put("compileOutput", v.compileOutput());
        m.put("error", v.error());
        List<Object> cs = new ArrayList<>();
        for (Verdict.CaseResult c : v.cases()) {
            Map<String, Object> cm = new LinkedHashMap<>();
            cm.put("index", c.index()); cm.put("passed", c.passed()); cm.put("hidden", c.hidden());
            cm.put("input", c.input()); cm.put("expected", c.expected()); cm.put("actual", c.actual());
            cm.put("stdout", c.stdout()); cm.put("runtimeMicros", c.runtimeMicros());
            cs.add(cm);
        }
        m.put("cases", cs);
        return m;
    }
}
