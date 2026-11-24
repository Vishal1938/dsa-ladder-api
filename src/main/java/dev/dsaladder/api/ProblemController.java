package dev.dsaladder.api;

import dev.dsaladder.api.Dtos.ExampleDto;
import dev.dsaladder.api.Dtos.ParamDto;
import dev.dsaladder.api.Dtos.ProblemDetail;
import dev.dsaladder.api.Dtos.RunRequest;
import dev.dsaladder.api.Dtos.SubmissionDto;
import dev.dsaladder.api.Dtos.SubmitRequest;
import dev.dsaladder.api.Dtos.VerdictDto;
import dev.dsaladder.judge.Json;
import dev.dsaladder.judge.Judge;
import dev.dsaladder.judge.Verdict;
import dev.dsaladder.problems.ProblemModel.Problem;
import dev.dsaladder.problems.ProblemModel.Topic;
import dev.dsaladder.problems.ProblemStore;
import dev.dsaladder.security.AuthUser;
import dev.dsaladder.service.JudgeService;
import dev.dsaladder.service.ProgressService;
import dev.dsaladder.submission.Submission;
import dev.dsaladder.submission.SubmissionRepository;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.data.domain.PageRequest;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/api/problems")
public class ProblemController {
    private final ProblemStore store;
    private final JudgeService judge;
    private final SubmissionRepository submissions;
    private final ProgressService progress;

    public ProblemController(ProblemStore store, JudgeService judge, SubmissionRepository submissions, ProgressService progress) {
        this.store = store;
        this.judge = judge;
        this.submissions = submissions;
        this.progress = progress;
    }

    private Problem find(String slug) {
        Problem p = store.problem(slug);
        if (p == null) throw ApiException.notFound("Problem");
        return p;
    }

    @GetMapping("/{slug}")
    public ProblemDetail get(@PathVariable String slug) {
        Problem p = find(slug);
        Topic t = store.topic(p.topic());
        List<Problem> book = store.problems(p.topic());
        int i = book.indexOf(p);
        List<List<String>> samples = new ArrayList<>();
        for (Judge.TestCase tc : p.sampleTests()) samples.add(tc.args().stream().map(Json::stringify).toList());
        return new ProblemDetail(p.slug(), p.title(), p.topic(), t.name(), p.stage(), t.stages().get(p.stage()).name(),
                p.difficulty(), p.whatsNew(), p.statement(),
                p.examples().stream().map(e -> new ExampleDto(e.input(), e.output(), e.explanation())).toList(),
                p.hints(), p.trigger(), p.function().starterCode(), p.function().signature(),
                p.function().params().stream().map(x -> new ParamDto(x.name(), x.type())).toList(),
                samples, p.timeLimitMs(),
                i > 0 ? book.get(i - 1).slug() : null, i >= 0 && i < book.size() - 1 ? book.get(i + 1).slug() : null,
                progress.current().solved().contains(p.slug()));
    }

    @PostMapping("/{slug}/run")
    public VerdictDto run(@PathVariable String slug, @RequestBody RunRequest req, HttpServletRequest http) {
        Problem p = find(slug);
        if (req.code() == null) throw new ApiException(HttpStatus.BAD_REQUEST, "code is required");
        return VerdictDto.of(judge.run(p, req.code(), req.inputs(), callerKey(http)), null, false);
    }

    @PostMapping("/{slug}/submit")
    public VerdictDto submit(@PathVariable String slug, @RequestBody SubmitRequest req, HttpServletRequest http) {
        Problem p = find(slug);
        if (req.code() == null) throw new ApiException(HttpStatus.BAD_REQUEST, "code is required");
        Verdict v = judge.submit(p, req.code(), callerKey(http));
        var user = AuthUser.current();
        if (user.isEmpty() || v.status() == Verdict.Status.INTERNAL_ERROR) return VerdictDto.of(v, null, false);
        Submission s = submissions.save(new Submission(user.get().id(), p.slug(), p.topic(), v.status().name(), v.passed(), v.total(), v.runtimeMs(), req.code()));
        return VerdictDto.of(v, s.getId(), true);
    }

    @GetMapping("/{slug}/submissions")
    public List<SubmissionDto> mine(@PathVariable String slug) {
        AuthUser u = AuthUser.current().orElseThrow(() -> new ApiException(HttpStatus.UNAUTHORIZED, "Sign in to see your submissions"));
        find(slug);
        return submissions.findByUserIdAndProblemSlugOrderByCreatedAtDesc(u.id(), slug, PageRequest.of(0, 30)).stream()
                .map(s -> new SubmissionDto(s.getId(), s.getProblemSlug(), s.getStatus(), s.getPassed(), s.getTotal(), s.getRuntimeMs(), s.getCreatedAt(), s.getCode()))
                .toList();
    }

    private static String callerKey(HttpServletRequest http) {
        return AuthUser.current().map(u -> "u" + u.id()).orElseGet(() -> {
            String fwd = http.getHeader("X-Forwarded-For");
            return "ip" + (fwd != null && !fwd.isBlank() ? fwd.split(",")[0].trim() : http.getRemoteAddr());
        });
    }
}
