package dev.dsaladder.submission;

import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.List;

public interface SubmissionRepository extends MongoRepository<Submission, String>, SubmissionRepositoryCustom {

    List<Submission> findByUserIdAndProblemSlugOrderByCreatedAtDesc(String userId, String problemSlug, Pageable page);

    List<Submission> findByUserIdOrderByCreatedAtDesc(String userId, Pageable page);
}
