package dev.dsaladder.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

/** Everything under {@code app.*} in application.yml. */
@ConfigurationProperties(prefix = "app")
public record AppProperties(String problemsDir, String jwtSecret, int jwtTtlHours, String corsOrigins, JudgeProps judge) {

    public record JudgeProps(int memoryMb, int maxConcurrent, int queueWaitSeconds, String sandboxPrefix,
                             int runsPerMinute, int submitsPerMinute) {}
}
