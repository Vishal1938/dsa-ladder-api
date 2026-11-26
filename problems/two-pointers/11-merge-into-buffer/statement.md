Two sorted sensor logs have to become one. The first log `a` has room for both: its first `m` slots hold its own readings and the rest are empty, written as zeros.

Merge `b` into `a` **in place**, so that `a` ends up holding all `m + b.length` readings in non-decreasing order. Your method returns nothing; `a` itself is the answer.

**Constraints**
- `0 <= m <= 10^5`
- `0 <= b.length <= 10^5`
- `a.length == m + b.length`
- `1 <= a.length`
- `-10^9 <= values <= 10^9`
- `the first m entries of a and all of b are in non-decreasing order`
