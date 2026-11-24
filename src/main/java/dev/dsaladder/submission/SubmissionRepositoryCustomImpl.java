package dev.dsaladder.submission;

import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;

import java.util.List;

/**
 * The two "select distinct problemSlug" lookups, as a MongoDB distinct command.
 * Both are served by the {@code (userId, problemSlug)} compound index on {@link Submission}.
 */
class SubmissionRepositoryCustomImpl implements SubmissionRepositoryCustom {
    private static final String SLUG = "problemSlug";

    private final MongoTemplate mongo;

    SubmissionRepositoryCustomImpl(MongoTemplate mongo) { this.mongo = mongo; }

    @Override
    public List<String> solvedSlugs(String userId) {
        Query q = Query.query(Criteria.where("userId").is(userId).and("status").is("ACCEPTED"));
        return mongo.findDistinct(q, SLUG, Submission.class, String.class);
    }

    @Override
    public List<String> attemptedSlugs(String userId) {
        Query q = Query.query(Criteria.where("userId").is(userId));
        return mongo.findDistinct(q, SLUG, Submission.class, String.class);
    }
}
