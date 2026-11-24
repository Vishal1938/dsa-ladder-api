# Writing a problem book

A problem lives in `problems/<topic>/<NN>-<slug>/`:

| File | Contents |
|---|---|
| `problem.json` | slug, title, stage (0-based index into the topic's stages in `topics.json`), order, difficulty, `whatsNew` (the one idea this rung adds), `function` (method signature), `timeLimitMs`, `hints` (questions, mildest first), `trigger` ("when I see X → think Y"), optional `compare` |
| `statement.md` | The statement and constraints (Markdown). Write your own; don't copy LeetCode text. |
| `Solution.java` | Reference solution (`class Solution`). Never sent to users. |
| `Brute.java` | Independent slow solution, used only by `crosscheck`. |
| `tests.json` | `examples` (shown, with expected output and optional explanation), `tests` (hidden; output optional), `generated` (specs for big hidden tests), `crosscheck` (specs for small random inputs) |

Supported parameter/return types: `int long double boolean char String`, their arrays, `int[][] long[][] char[][] String[][]`,
`List<Integer> List<Long> List<String> List<List<Integer>> List<List<String>>`, `ListNode`, `TreeNode` (level-order arrays with `null`).
For in-place problems use `"returns": "void", "outputArg": <index>`.

Generator kinds (`TestGen`): `int`, `const`, `intArray`, `bits`, `intMatrix`, `string`, `ranges` (of an array/string argument),
`rects` (of a matrix argument), `updates`, `intervals`, `trips`. `ranges`/`rects`/`updates` accept `"wide": true` for
near-full ranges, which is what makes naive per-query loops time out.

## Rules of thumb for a good ladder

* Each rung changes **one** thing from the previous rung, and `whatsNew` says what.
* Start embarrassingly easy. The first two or three rungs build the mechanics; intuition comes from the middle rungs.
* Hints are questions that point at the bottleneck, not the answer.
* Big generated tests must make the brute force time out: check with
  `java -cp build/cli dev.dsaladder.cli.JudgeCli judge problems <slug> submit < problems/.../Brute.java`.

## Verify

```bash
mkdir -p build/cli
javac -d build/cli $(find src/main/java/dev/dsaladder/{judge,problems,cli} -name '*.java')
cp -r src/main/resources/judge build/cli/
java -cp build/cli dev.dsaladder.cli.JudgeCli check problems
java -cp build/cli dev.dsaladder.cli.JudgeCli crosscheck problems
```
