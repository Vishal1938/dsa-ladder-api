package dev.dsaladder.submission;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.Instant;

@Document("submissions")
@CompoundIndex(def = "{'userId':1,'problemSlug':1}")
@CompoundIndex(def = "{'userId':1,'createdAt':-1}")
public class Submission {
    /** MongoDB ObjectId, as its 24-character hex string. */
    @Id
    private String id;

    private String userId;

    private String problemSlug;

    private String topic;

    private String status;

    private int passed;
    private int total;
    private long runtimeMs;

    private String code;

    private Instant createdAt = Instant.now();

    protected Submission() {}

    public Submission(String userId, String problemSlug, String topic, String status, int passed, int total, long runtimeMs, String code) {
        this.userId = userId;
        this.problemSlug = problemSlug;
        this.topic = topic;
        this.status = status;
        this.passed = passed;
        this.total = total;
        this.runtimeMs = runtimeMs;
        this.code = code;
    }

    public String getId() { return id; }
    public String getUserId() { return userId; }
    public String getProblemSlug() { return problemSlug; }
    public String getTopic() { return topic; }
    public String getStatus() { return status; }
    public int getPassed() { return passed; }
    public int getTotal() { return total; }
    public long getRuntimeMs() { return runtimeMs; }
    public String getCode() { return code; }
    public Instant getCreatedAt() { return createdAt; }
}
