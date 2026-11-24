package dev.dsaladder.submission;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Index;
import jakarta.persistence.Table;

import java.time.Instant;

@Entity
@Table(name = "submission", indexes = {
        @Index(name = "idx_submission_user_problem", columnList = "user_id,problem_slug"),
        @Index(name = "idx_submission_user_created", columnList = "user_id,created_at")})
public class Submission {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private Long userId;

    @Column(nullable = false, length = 80)
    private String problemSlug;

    @Column(nullable = false, length = 40)
    private String topic;

    @Column(nullable = false, length = 30)
    private String status;

    private int passed;
    private int total;
    private long runtimeMs;

    @Column(nullable = false, columnDefinition = "TEXT")
    private String code;

    @Column(nullable = false)
    private Instant createdAt = Instant.now();

    protected Submission() {}

    public Submission(Long userId, String problemSlug, String topic, String status, int passed, int total, long runtimeMs, String code) {
        this.userId = userId;
        this.problemSlug = problemSlug;
        this.topic = topic;
        this.status = status;
        this.passed = passed;
        this.total = total;
        this.runtimeMs = runtimeMs;
        this.code = code;
    }

    public Long getId() { return id; }
    public Long getUserId() { return userId; }
    public String getProblemSlug() { return problemSlug; }
    public String getTopic() { return topic; }
    public String getStatus() { return status; }
    public int getPassed() { return passed; }
    public int getTotal() { return total; }
    public long getRuntimeMs() { return runtimeMs; }
    public String getCode() { return code; }
    public Instant getCreatedAt() { return createdAt; }
}
