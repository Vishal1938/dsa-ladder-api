# Architecture

```
 Browser (dsa-ladder-web)  ──HTTPS /api──▶  Spring Boot API (this repo)  ──▶  MongoDB (users, submissions)
                                                  │
                                                  ├── ProblemStore   (problems/ loaded + verified at start-up)
                                                  └── Judge          (javac in-process, run in a separate JVM per submission)
```

## Repository layout

| Path | What it is |
|---|---|
| `problems/` | Content. `topics.json` (ladders, stages, LeetCode final exams) and one folder per problem book. |
| `src/main/java/dev/dsaladder/judge` | The judge. **No Spring, no dependencies**, so it is unit-testable and usable from the CLI. |
| `src/main/java/dev/dsaladder/problems` | Loads and verifies problem books (also dependency-free). |
| `src/main/java/dev/dsaladder/cli` | `JudgeCli`: `check`, `crosscheck`, `judge`, `export`, `serve`. Used by CI and problem authors. |
| `src/main/java/dev/dsaladder/{api,service,security,user,submission,config}` | The Spring Boot application. |
| `tools/book_*.py` | Authoring source for each problem book (generates the problem folders). |

## How judging works

1. **Harness generation.** Each problem declares the method to implement (`problem.json → function`), e.g.
   `long[] rangeSums(int[] nums, int[][] queries)`. `FunctionSpec` generates a `call()` method that converts JSON test
   arguments into those Java types and calls `new Solution().rangeSums(...)`. The template is
   `resources/judge/JudgeMain.java.txt`; it contains its own tiny JSON parser, so the generated program needs nothing
   but the JDK.
2. **Compile.** The user's `Solution.java` and the harness are compiled **in-process** with `javax.tools.JavaCompiler`
   into a fresh temp directory. Errors in the user's file are reported with line numbers; an error inside the harness
   means the method signature doesn't match, which is reported as such.
3. **Run.** A separate JVM (`-Xmx256m`, serial GC, one CPU) runs all test cases in one process, reading them from
   stdin. User output (`System.out`) is captured per test. The process gets an empty environment and a wall-clock limit
   (problem time limit + JVM start-up allowance); it is killed on timeout or when stdout exceeds 16 MB.
4. **Grade.** Results are compared with `Compare` (`EXACT`, `UNORDERED`, `UNORDERED_DEEP`, `FLOAT`). Submissions stop at
   the first failing case and reveal it, even if hidden (like LeetCode). If every answer is right but the summed
   per-test time is over the limit, the verdict is Time Limit Exceeded.

`JudgeService` (Spring) adds a semaphore so only `app.judge.max-concurrent` JVMs run at once, a per-user/IP rate limit,
and **custom test inputs**: inputs typed in the Testcase tab are type-checked against the method signature and their
expected answers are produced by running the problem's reference solution.

### Live compile checks

`POST /api/problems/{slug}/check` is step 2 on its own: `Judge.diagnose` compiles the code and returns each compiler
message with 1-based start/end line and column (end exclusive), so the editor can underline errors while the user
types. **No process is started and no user code runs** — the only risk is compile time, so the endpoint gets its own
rate limit (`app.judge.checks-per-minute`, default 120) and its own two-permit pool rather than competing with runs
for the judge's JVM slots. A check takes roughly 0.2–0.5 s. A `package` declaration is blanked out with spaces instead
of being deleted, so the positions still line up with what the user sees. When only the generated harness fails to
compile, the method signature doesn't match, and that is reported as one error on the `class Solution` line.

## Problem verification

At start-up (and in CI via `JudgeCli check`), every problem is loaded and its reference solution is run on every test:

* hand-written expected answers must match the reference (catches typos in examples),
* large tests are **generated deterministically** from a short spec (`tests.json → generated`) and their answers come
  from the reference, so the repo stays small,
* the reference must finish well inside the time limit.

`JudgeCli crosscheck` additionally compares the reference with an independent brute-force solution (`Brute.java`) on
hundreds of small random inputs per problem. The big generated tests are sized so that an O(n²) solution gets Time Limit
Exceeded, so learners have to use the intended idea.

## Security model

Running untrusted code is the risky part of this app. Layers, from inside out:

1. **Per-run JVM**: separate process, heap cap, wall-clock kill, output cap, empty environment, its own temp directory
   that is deleted afterwards.
2. **Resource limits**: in production every run is prefixed with `prlimit` (file size, open files, no core dumps);
   the prefix is configurable (`JUDGE_SANDBOX_PREFIX`) so it can be swapped for `nsjail` or `bwrap`.
3. **Container**: the API runs as a non-root user in a read-only container with all Linux capabilities dropped,
   `no-new-privileges`, a PID limit and a memory limit (see `docker-compose.yml`; apply the same settings on your host
   where it allows). Writable space is only a size-limited `/tmp`.

What this does **not** give you: network isolation per run, or protection from a submission reading files that the
backend user can read inside the container (there are no secrets on disk; secrets come from environment variables,
which runs don't inherit). For a public deployment with untrusted users, run the backend on a separate small VM, or
use `nsjail` as the sandbox prefix (network namespace + seccomp). See *Roadmap* in the README.

## Data model

Two MongoDB collections. `_id` is an `ObjectId`, exposed in the API as its 24-character hex string.

**`users`**

| Field | Notes |
|---|---|
| `_id` | `ObjectId`; the JWT subject |
| `email` | lower-cased on register; **unique index** |
| `passwordHash` | BCrypt |
| `displayName`, `createdAt` | |

**`submissions`**

| Field | Notes |
|---|---|
| `_id` | `ObjectId` |
| `userId` | the user's id as a string (no join; documents are read per user) |
| `problemSlug`, `topic` | |
| `status` | `ACCEPTED`, `WRONG_ANSWER`, … |
| `passed`, `total`, `runtimeMs`, `code`, `createdAt` | |

Compound indexes: `{userId, problemSlug}` serves the per-problem history and the distinct-slug progress
queries; `{userId, createdAt: -1}` serves the recent-submissions list. Both are declared on the document class
and created at start-up (`spring.data.mongodb.auto-index-creation=true`).

Progress ("solved") is derived from submissions: a problem is solved when the user has an `ACCEPTED` submission.
`SubmissionRepositoryCustomImpl` runs the two `distinct` commands behind this. Problems themselves are files, not
database documents, so content changes are reviewed like code.

## API

| Method | Path | Auth | Purpose |
|---|---|---|---|
| GET | `/api/topics` | optional | Ladders with problem/solved counts |
| GET | `/api/topics/{id}` | optional | Stages, problems (with solved flags) and final-exam lists |
| GET | `/api/problems/{slug}` | optional | Statement, examples, hints, starter code, sample inputs |
| POST | `/api/problems/{slug}/run` | optional | `{code, inputs?}` → verdict on examples or custom inputs |
| POST | `/api/problems/{slug}/submit` | optional | `{code}` → verdict on all tests; saved when signed in |
| POST | `/api/problems/{slug}/check` | optional | `{code}` → `{diagnostics}`: compile errors with positions; compiles only |
| GET | `/api/problems/{slug}/submissions` | required | Your last 30 submissions for the problem |
| POST | `/api/auth/register`, `/api/auth/login` | – | → `{token, user}` (JWT, HS256) |
| GET | `/api/auth/me`, `/api/me/stats` | required | Current user, progress summary |
