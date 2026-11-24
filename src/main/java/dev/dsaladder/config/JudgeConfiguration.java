package dev.dsaladder.config;

import dev.dsaladder.judge.Judge;
import dev.dsaladder.judge.JudgeConfig;
import dev.dsaladder.problems.ProblemStore;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.io.IOException;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.List;

@Configuration
public class JudgeConfiguration {
    private static final Logger log = LoggerFactory.getLogger(JudgeConfiguration.class);

    @Bean
    public Judge judge(AppProperties props) {
        JudgeConfig d = JudgeConfig.defaults();
        String prefix = props.judge().sandboxPrefix();
        List<String> sandbox = prefix == null || prefix.isBlank() ? List.of() : Arrays.asList(prefix.trim().split("\\s+"));
        return new Judge(new JudgeConfig(d.javaBin(), props.judge().memoryMb(), d.startupAllowanceMs(), d.maxOutputBytes(),
                d.maxSourceChars(), sandbox));
    }

    /** Loads every problem book at start-up and verifies it against its reference solution. Fails fast on bad content. */
    @Bean
    public ProblemStore problemStore(AppProperties props, Judge judge) throws IOException {
        long t0 = System.currentTimeMillis();
        Path dir = Path.of(props.problemsDir()).toAbsolutePath().normalize();
        ProblemStore store = ProblemStore.load(dir, judge, Math.max(2, Runtime.getRuntime().availableProcessors()));
        if (!store.errors().isEmpty()) {
            store.errors().forEach(e -> log.error("Problem error: {}", e));
            throw new IllegalStateException(store.errors().size() + " problem(s) failed verification; see the log above.");
        }
        log.info("Loaded {} topics and {} problems from {} in {} ms", store.topics().size(), store.problems().size(), dir,
                System.currentTimeMillis() - t0);
        return store;
    }
}
