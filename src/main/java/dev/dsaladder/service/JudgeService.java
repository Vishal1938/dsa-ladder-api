package dev.dsaladder.service;

import dev.dsaladder.api.ApiException;
import dev.dsaladder.config.AppProperties;
import dev.dsaladder.judge.FunctionSpec;
import dev.dsaladder.judge.Json;
import dev.dsaladder.judge.Judge;
import dev.dsaladder.judge.Types;
import dev.dsaladder.judge.Verdict;
import dev.dsaladder.problems.ProblemModel.Problem;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Semaphore;
import java.util.concurrent.TimeUnit;

/**
 * Spring-facing wrapper around {@link Judge}: limits how many JVMs run at once, rate-limits each caller,
 * and computes expected answers for custom test inputs with the problem's reference solution.
 */
@Service
public class JudgeService {
    public static final int MAX_CUSTOM_CASES = 8;
    public static final int MAX_CUSTOM_CHARS = 50_000;

    private final Judge judge;
    private final Semaphore slots;
    private final int waitSeconds;
    private final int runsPerMinute, submitsPerMinute;
    private final Map<String, Deque<Long>> recent = new ConcurrentHashMap<>();
    private final Map<String, Judge.Compiled> referenceCache = new ConcurrentHashMap<>();

    public JudgeService(Judge judge, AppProperties props) {
        this.judge = judge;
        this.slots = new Semaphore(Math.max(1, props.judge().maxConcurrent()), true);
        this.waitSeconds = props.judge().queueWaitSeconds();
        this.runsPerMinute = props.judge().runsPerMinute();
        this.submitsPerMinute = props.judge().submitsPerMinute();
    }

    /** "Run": the sample cases, or the user's own inputs (expected answers come from the reference solution). */
    public Verdict run(Problem p, String code, List<List<String>> customInputs, String callerKey) {
        rateLimit("run:" + callerKey, runsPerMinute);
        List<Judge.TestCase> cases = customInputs == null || customInputs.isEmpty() ? p.sampleTests() : customCases(p, customInputs);
        return withSlot(() -> judge.judge(p.function(), code, cases, p.compare(), p.timeLimitMs(), false));
    }

    /** "Submit": every test, stopping at the first failure. */
    public Verdict submit(Problem p, String code, String callerKey) {
        rateLimit("submit:" + callerKey, submitsPerMinute);
        return withSlot(() -> judge.judge(p.function(), code, p.allTests(), p.compare(), p.timeLimitMs(), true));
    }

    private List<Judge.TestCase> customCases(Problem p, List<List<String>> inputs) {
        if (inputs.size() > MAX_CUSTOM_CASES) throw new ApiException(HttpStatus.BAD_REQUEST, "At most " + MAX_CUSTOM_CASES + " custom test cases.");
        int chars = inputs.stream().flatMap(List::stream).mapToInt(s -> s == null ? 0 : s.length()).sum();
        if (chars > MAX_CUSTOM_CHARS) throw new ApiException(HttpStatus.BAD_REQUEST, "Custom input is too large.");
        int nParams = p.function().params().size();
        List<List<Object>> args = new ArrayList<>();
        for (int c = 0; c < inputs.size(); c++) {
            List<String> raw = inputs.get(c);
            if (raw == null || raw.size() != nParams) throw new ApiException(HttpStatus.BAD_REQUEST, "Case " + (c + 1) + " needs " + nParams + " values, one per parameter.");
            List<Object> a = new ArrayList<>();
            for (int i = 0; i < nParams; i++) {
                FunctionSpec.Param prm = p.function().params().get(i);
                Object v;
                try {
                    v = Json.parse(raw.get(i).trim());
                } catch (RuntimeException e) {
                    throw new ApiException(HttpStatus.BAD_REQUEST, "Case " + (c + 1) + ", " + prm.name() + ": not valid JSON (" + e.getMessage() + ")");
                }
                if (!Types.matches(prm.type(), v)) throw new ApiException(HttpStatus.BAD_REQUEST, "Case " + (c + 1) + ", " + prm.name() + ": expected " + prm.type());
                a.add(v);
            }
            args.add(a);
        }
        Judge.Compiled ref = referenceCache.computeIfAbsent(p.slug(), s -> judge.compile(p.function(), p.referenceSolution()));
        Judge.RunOutput out = withSlot(() -> judge.run(ref, args, Math.max(5000, p.timeLimitMs() * 3)));
        if (out.results().size() != args.size()) {
            int bad = out.results().size() + 1;
            throw new ApiException(HttpStatus.BAD_REQUEST, "Case " + bad + " isn't a valid input for this problem (check the constraints).");
        }
        List<Judge.TestCase> cases = new ArrayList<>();
        for (int i = 0; i < args.size(); i++) cases.add(new Judge.TestCase(args.get(i), out.results().get(i), false));
        return cases;
    }

    private <T> T withSlot(java.util.function.Supplier<T> work) {
        boolean got;
        try {
            got = slots.tryAcquire(waitSeconds, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new ApiException(HttpStatus.SERVICE_UNAVAILABLE, "Interrupted");
        }
        if (!got) throw new ApiException(HttpStatus.SERVICE_UNAVAILABLE, "The judge is busy. Try again in a few seconds.");
        try {
            return work.get();
        } finally {
            slots.release();
        }
    }

    private void rateLimit(String key, int perMinute) {
        long now = System.currentTimeMillis();
        Deque<Long> q = recent.computeIfAbsent(key, k -> new ArrayDeque<>());
        synchronized (q) {
            while (!q.isEmpty() && now - q.peekFirst() > 60_000) q.pollFirst();
            if (q.size() >= perMinute) throw new ApiException(HttpStatus.TOO_MANY_REQUESTS, "Too many runs. Wait a minute and try again.");
            q.addLast(now);
        }
    }
}
