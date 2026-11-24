package dev.dsaladder.judge;

import javax.tools.Diagnostic;
import javax.tools.DiagnosticCollector;
import javax.tools.JavaCompiler;
import javax.tools.JavaFileObject;
import javax.tools.StandardJavaFileManager;
import javax.tools.ToolProvider;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;
import java.util.Objects;
import java.util.concurrent.TimeUnit;
import java.util.stream.Stream;

/**
 * Compiles a user's {@code Solution} together with a generated harness and runs it in a separate JVM
 * with memory, time and output limits. Dependency-free so it can be tested and used from a CLI.
 *
 * <p>Isolation: each run is a fresh JVM in its own temp directory with an empty environment. In production the
 * process is additionally wrapped by {@link JudgeConfig#sandboxPrefix()} (e.g. {@code prlimit}, {@code nsjail})
 * and the whole backend runs in a non-root container. See docs/ARCHITECTURE.md → "Security model".
 */
public final class Judge {

    public record TestCase(List<Object> args, Object expected, boolean hidden) {}

    public record Compiled(boolean ok, Path dir, String output) {}

    /** Raw outcome of executing compiled code on a list of inputs. */
    public record RunOutput(List<Object> results, List<Long> nanos, List<String> stdout, Integer errorAt, String error,
                            boolean timedOut, boolean outputLimit, String internal) {}

    private static final String HARNESS = loadHarness();
    private static final String TYPES = """
            class ListNode { int val; ListNode next; ListNode() {} ListNode(int val) { this.val = val; } ListNode(int val, ListNode next) { this.val = val; this.next = next; } }
            class TreeNode { int val; TreeNode left, right; TreeNode() {} TreeNode(int val) { this.val = val; } TreeNode(int val, TreeNode left, TreeNode right) { this.val = val; this.left = left; this.right = right; } }
            """;

    private final JudgeConfig cfg;

    public Judge(JudgeConfig cfg) { this.cfg = cfg; }

    private static String loadHarness() {
        try (InputStream in = Judge.class.getResourceAsStream("/judge/JudgeMain.java.txt")) {
            return new String(Objects.requireNonNull(in, "harness template missing").readAllBytes(), StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new IllegalStateException(e);
        }
    }

    // ------------------------------------------------------------------ compile

    public Compiled compile(FunctionSpec spec, String userCode) {
        if (userCode == null || userCode.isBlank()) return new Compiled(false, null, "Your code is empty.");
        if (userCode.length() > cfg.maxSourceChars()) return new Compiled(false, null, "Your code is too long (max " + cfg.maxSourceChars() + " characters).");
        String code = userCode.replaceFirst("(?m)^\\s*package\\s+[\\w.]+\\s*;", "");
        JavaCompiler javac = ToolProvider.getSystemJavaCompiler();
        if (javac == null) return new Compiled(false, null, "INTERNAL: no Java compiler available (run the backend on a JDK, not a JRE).");
        Path dir;
        try {
            dir = Files.createTempDirectory("judge-");
            Files.writeString(dir.resolve("Solution.java"), code);
            String harness = HARNESS.replace("/*__CALL__*/", spec.callSource()).replace("/*__TYPES__*/", TYPES);
            Files.writeString(dir.resolve("JudgeMain.java"), harness);
        } catch (IOException e) {
            return new Compiled(false, null, "INTERNAL: " + e.getMessage());
        }
        DiagnosticCollector<JavaFileObject> diags = new DiagnosticCollector<>();
        try (StandardJavaFileManager fm = javac.getStandardFileManager(diags, Locale.ENGLISH, StandardCharsets.UTF_8)) {
            var units = fm.getJavaFileObjects(dir.resolve("Solution.java").toFile(), dir.resolve("JudgeMain.java").toFile());
            List<String> opts = List.of("-d", dir.toString(), "-encoding", "UTF-8", "-nowarn", "-proc:none", "-g");
            boolean ok = javac.getTask(null, fm, diags, opts, null, units).call();
            if (ok) return new Compiled(true, dir, "");
            return new Compiled(false, dir, formatDiagnostics(diags, spec));
        } catch (IOException e) {
            return new Compiled(false, dir, "INTERNAL: " + e.getMessage());
        }
    }

    private static String formatDiagnostics(DiagnosticCollector<JavaFileObject> diags, FunctionSpec spec) {
        StringBuilder user = new StringBuilder();
        boolean harnessError = false;
        for (Diagnostic<? extends JavaFileObject> d : diags.getDiagnostics()) {
            if (d.getKind() != Diagnostic.Kind.ERROR) continue;
            String file = d.getSource() == null ? "" : Path.of(d.getSource().toUri()).getFileName().toString();
            if (file.equals("Solution.java")) {
                user.append("Line ").append(d.getLineNumber()).append(": ").append(d.getMessage(Locale.ENGLISH)).append('\n');
            } else harnessError = true;
        }
        if (user.length() == 0 && harnessError) {
            return "Your class must be named Solution and contain the method\n    public " + spec.signature()
                    + "\nwith exactly this name, parameter types and return type.";
        }
        return user.toString().strip();
    }

    // ------------------------------------------------------------------ run

    public RunOutput run(Compiled c, List<List<Object>> inputs, long timeLimitMs) {
        StringBuilder in = new StringBuilder().append(inputs.size()).append('\n');
        for (List<Object> a : inputs) in.append(Json.stringify(a)).append('\n');
        byte[] stdin = in.toString().getBytes(StandardCharsets.UTF_8);

        List<String> cmd = new ArrayList<>(cfg.sandboxPrefix());
        cmd.add(cfg.javaBin());
        cmd.add("-Xmx" + cfg.memoryMb() + "m");
        cmd.add("-Xss16m");
        cmd.add("-XX:+UseSerialGC");
        cmd.add("-XX:ActiveProcessorCount=1");
        cmd.add("-Xshare:auto");
        cmd.add("-Djava.awt.headless=true");
        cmd.add("-cp");
        cmd.add(c.dir().toString());
        cmd.add("JudgeMain");

        ProcessBuilder pb = new ProcessBuilder(cmd).directory(c.dir().toFile());
        pb.environment().clear();
        pb.environment().put("LANG", "C.UTF-8");
        Process p;
        try {
            p = pb.start();
        } catch (IOException e) {
            return new RunOutput(List.of(), List.of(), List.of(), null, null, false, false, "Could not start the JVM: " + e.getMessage());
        }
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        ByteArrayOutputStream err = new ByteArrayOutputStream();
        Thread tin = Thread.ofVirtual().start(() -> {
            try (OutputStream os = p.getOutputStream()) { os.write(stdin); } catch (IOException ignored) { }
        });
        boolean[] overflow = {false};
        Thread tout = Thread.ofVirtual().start(() -> pump(p.getInputStream(), out, cfg.maxOutputBytes(), overflow, p));
        Thread terr = Thread.ofVirtual().start(() -> pump(p.getErrorStream(), err, 64 * 1024, new boolean[1], null));
        boolean finished;
        try {
            finished = p.waitFor(cfg.startupAllowanceMs() + timeLimitMs, TimeUnit.MILLISECONDS);
            if (!finished) p.destroyForcibly().waitFor(2, TimeUnit.SECONDS);
            tin.join(1000); tout.join(2000); terr.join(1000);
        } catch (InterruptedException e) {
            p.destroyForcibly();
            Thread.currentThread().interrupt();
            return new RunOutput(List.of(), List.of(), List.of(), null, null, false, false, "Interrupted");
        }
        RunOutput parsed = parse(out.toString(StandardCharsets.UTF_8), inputs.size(), !finished, overflow[0]);
        if (finished && parsed.results().size() < inputs.size() && parsed.errorAt() == null && !overflow[0]) {
            String e = err.toString(StandardCharsets.UTF_8);
            String msg = e.contains("OutOfMemoryError") ? "java.lang.OutOfMemoryError: Java heap space (memory limit " + cfg.memoryMb() + " MB)"
                    : e.isBlank() ? "The program exited early (exit code " + p.exitValue() + ")" : e.strip();
            return new RunOutput(parsed.results(), parsed.nanos(), parsed.stdout(), parsed.results().size(), msg, false, false, null);
        }
        return parsed;
    }

    private static void pump(InputStream in, ByteArrayOutputStream sink, int max, boolean[] overflow, Process killOnOverflow) {
        byte[] buf = new byte[8192];
        try (in) {
            int n;
            while ((n = in.read(buf)) > 0) {
                if (sink.size() + n > max) {
                    sink.write(buf, 0, Math.max(0, max - sink.size()));
                    overflow[0] = true;
                    if (killOnOverflow != null) killOnOverflow.destroyForcibly();
                    return;
                }
                sink.write(buf, 0, n);
            }
        } catch (IOException ignored) { }
    }

    private static RunOutput parse(String text, int n, boolean timedOut, boolean overflow) {
        List<Object> results = new ArrayList<>();
        List<Long> nanos = new ArrayList<>();
        List<String> stdout = new ArrayList<>();
        for (int i = 0; i < n; i++) stdout.add("");
        Integer errorAt = null;
        String error = null;
        String[] lines = text.split("\n", -1);
        for (int i = 0; i + 1 < lines.length; i++) {
            String h = lines[i];
            if (!h.startsWith("@@")) continue;
            String[] parts = h.split(" ");
            String body = lines[i + 1];
            try {
                int t = Integer.parseInt(parts[1]);
                switch (parts[0]) {
                    case "@@R" -> { results.add(Json.parse(body)); nanos.add(Long.parseLong(parts[2])); }
                    case "@@O" -> { if (t >= 0 && t < n) stdout.set(t, (String) Json.parse(body)); }
                    case "@@E" -> { errorAt = Math.max(t, results.size()); error = (String) Json.parse(body); }
                    default -> { }
                }
                i++;
            } catch (RuntimeException ignored) { /* truncated line (time/output limit) */ }
        }
        return new RunOutput(results, nanos, stdout, errorAt, error, timedOut, overflow, null);
    }

    // ------------------------------------------------------------------ judge

    /**
     * Judges {@code code} on {@code cases}. Stops at the first failing case (like LeetCode) when {@code stopOnFail}.
     */
    public Verdict judge(FunctionSpec spec, String code, List<TestCase> cases, Compare compare, long timeLimitMs, boolean stopOnFail) {
        Compiled c = compile(spec, code);
        try {
            if (!c.ok()) {
                Verdict.Status st = c.output().startsWith("INTERNAL") ? Verdict.Status.INTERNAL_ERROR : Verdict.Status.COMPILE_ERROR;
                return new Verdict(st, 0, cases.size(), 0, c.output(), null, List.of());
            }
            List<List<Object>> inputs = cases.stream().map(TestCase::args).toList();
            RunOutput r = run(c, inputs, timeLimitMs);
            return grade(r, cases, compare, timeLimitMs, stopOnFail);
        } finally {
            cleanup(c.dir());
        }
    }

    Verdict grade(RunOutput r, List<TestCase> cases, Compare compare, long timeLimitMs, boolean stopOnFail) {
        if (r.internal() != null) return new Verdict(Verdict.Status.INTERNAL_ERROR, 0, cases.size(), 0, null, r.internal(), List.of());
        List<Verdict.CaseResult> out = new ArrayList<>();
        int passed = 0;
        long totalNanos = 0;
        Verdict.Status status = Verdict.Status.ACCEPTED;
        String error = null;
        for (int i = 0; i < cases.size(); i++) {
            TestCase tc = cases.get(i);
            String in = Json.stringify(tc.args());
            String exp = tc.expected() == null ? null : Json.stringify(tc.expected());
            if (i < r.results().size()) {
                Object actual = r.results().get(i);
                long ns = r.nanos().get(i);
                totalNanos += ns;
                boolean ok = tc.expected() == null || compare.equal(tc.expected(), actual);
                if (ok) passed++;
                boolean show = !tc.hidden() || !ok;
                out.add(new Verdict.CaseResult(i, ok, tc.hidden(), show ? in : null, show ? exp : null,
                        show ? Json.stringify(actual) : null, show ? r.stdout().get(i) : null, ns / 1000));
                if (!ok && status == Verdict.Status.ACCEPTED) status = Verdict.Status.WRONG_ANSWER;
                if (!ok && stopOnFail) break;
            } else {
                if (r.errorAt() != null && r.errorAt() == i) {
                    status = Verdict.Status.RUNTIME_ERROR;
                    error = r.error();
                } else if (r.outputLimit()) {
                    status = Verdict.Status.OUTPUT_LIMIT_EXCEEDED;
                    error = "Your output was too large.";
                } else if (r.timedOut()) {
                    status = Verdict.Status.TIME_LIMIT_EXCEEDED;
                    error = "Time limit exceeded (" + timeLimitMs + " ms for all tests). Look for a faster approach.";
                } else {
                    status = Verdict.Status.RUNTIME_ERROR;
                    error = r.error() == null ? "The program stopped before finishing all tests." : r.error();
                }
                out.add(new Verdict.CaseResult(i, false, tc.hidden(), in, exp, null, r.stdout().size() > i ? r.stdout().get(i) : null, null));
                break;
            }
        }
        if (status == Verdict.Status.ACCEPTED && totalNanos / 1_000_000 > timeLimitMs) {
            status = Verdict.Status.TIME_LIMIT_EXCEEDED;
            error = "All answers were right, but the total time " + totalNanos / 1_000_000 + " ms is over the " + timeLimitMs + " ms limit.";
        }
        return new Verdict(status, passed, cases.size(), totalNanos / 1_000_000, null, error, out);
    }

    static void cleanup(Path dir) {
        if (dir == null) return;
        try (Stream<Path> s = Files.walk(dir)) {
            s.sorted(Comparator.reverseOrder()).forEach(p -> { try { Files.deleteIfExists(p); } catch (IOException ignored) { } });
        } catch (IOException ignored) { }
    }

    public JudgeConfig config() { return cfg; }
}
