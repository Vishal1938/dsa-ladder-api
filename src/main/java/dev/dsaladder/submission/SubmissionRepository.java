package dev.dsaladder.submission;

import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface SubmissionRepository extends JpaRepository<Submission, Long> {

    List<Submission> findByUserIdAndProblemSlugOrderByCreatedAtDesc(Long userId, String problemSlug, Pageable page);

    List<Submission> findByUserIdOrderByCreatedAtDesc(Long userId, Pageable page);

    @Query("select distinct s.problemSlug from Submission s where s.userId = :userId and s.status = 'ACCEPTED'")
    List<String> solvedSlugs(@Param("userId") Long userId);

    @Query("select distinct s.problemSlug from Submission s where s.userId = :userId")
    List<String> attemptedSlugs(@Param("userId") Long userId);
}
