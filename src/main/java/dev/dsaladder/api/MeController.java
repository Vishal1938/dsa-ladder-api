package dev.dsaladder.api;

import dev.dsaladder.api.Dtos.Stats;
import dev.dsaladder.api.Dtos.SubmissionDto;
import dev.dsaladder.problems.ProblemModel.Problem;
import dev.dsaladder.problems.ProblemStore;
import dev.dsaladder.security.AuthUser;
import dev.dsaladder.submission.SubmissionRepository;
import org.springframework.data.domain.PageRequest;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/me")
public class MeController {
    private final SubmissionRepository submissions;
    private final ProblemStore store;

    public MeController(SubmissionRepository submissions, ProblemStore store) {
        this.submissions = submissions;
        this.store = store;
    }

    @GetMapping("/stats")
    public Stats stats() {
        AuthUser u = AuthUser.current().orElseThrow(() -> new ApiException(HttpStatus.UNAUTHORIZED, "Not signed in"));
        List<String> solved = submissions.solvedSlugs(u.id());
        List<String> attempted = submissions.attemptedSlugs(u.id());
        Map<String, Integer> byTopic = new LinkedHashMap<>();
        for (String slug : solved) {
            Problem p = store.problem(slug);
            if (p != null) byTopic.merge(p.topic(), 1, Integer::sum);
        }
        List<SubmissionDto> recent = submissions.findByUserIdOrderByCreatedAtDesc(u.id(), PageRequest.of(0, 15)).stream()
                .map(s -> new SubmissionDto(s.getId(), s.getProblemSlug(), s.getStatus(), s.getPassed(), s.getTotal(), s.getRuntimeMs(), s.getCreatedAt(), null))
                .toList();
        return new Stats(solved.size(), attempted.size(), store.problems().size(), byTopic, recent);
    }
}
