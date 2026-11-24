package dev.dsaladder.submission;

import java.util.List;

/** The distinct-slug lookups behind progress tracking; see {@link SubmissionRepositoryCustomImpl}. */
public interface SubmissionRepositoryCustom {

    /** Slugs the user has an ACCEPTED submission for. */
    List<String> solvedSlugs(String userId);

    /** Slugs the user has submitted at all. */
    List<String> attemptedSlugs(String userId);
}
