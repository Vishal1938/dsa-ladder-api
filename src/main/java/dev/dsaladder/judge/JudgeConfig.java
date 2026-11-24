package dev.dsaladder.judge;

import java.nio.file.Path;
import java.util.List;

/**
 * @param javaBin            the java executable used to run submissions
 * @param memoryMb           max heap for a submission
 * @param startupAllowanceMs wall-clock time added to a problem's time limit for JVM start-up
 * @param maxOutputBytes     stdout cap for a whole run
 * @param maxSourceChars     max length of a submission
 * @param sandboxPrefix      command prepended to every run, e.g. ["prlimit","--nproc=64","--fsize=1048576","--"]
 */
public record JudgeConfig(String javaBin, int memoryMb, long startupAllowanceMs, int maxOutputBytes, int maxSourceChars,
                          List<String> sandboxPrefix) {

    public static JudgeConfig defaults() {
        return new JudgeConfig(Path.of(System.getProperty("java.home"), "bin", "java").toString(),
                256, 2500, 16 << 20, 64_000, List.of());
    }
}
