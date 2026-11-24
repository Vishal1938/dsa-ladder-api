package dev.dsaladder.service;

import dev.dsaladder.security.AuthUser;
import dev.dsaladder.submission.SubmissionRepository;
import org.springframework.stereotype.Service;

import java.util.HashSet;
import java.util.Set;

/** Which problems the current user has solved or attempted. Anonymous users have none. */
@Service
public class ProgressService {
    private final SubmissionRepository submissions;

    public ProgressService(SubmissionRepository submissions) { this.submissions = submissions; }

    public record Progress(Set<String> solved, Set<String> attempted) {
        public static final Progress NONE = new Progress(Set.of(), Set.of());
    }

    public Progress current() {
        return AuthUser.current()
                .map(u -> new Progress(new HashSet<>(submissions.solvedSlugs(u.id())), new HashSet<>(submissions.attemptedSlugs(u.id()))))
                .orElse(Progress.NONE);
    }
}
