Four machines each produce a list of measured deviations. A calibration is *valid* when you can pick one deviation from each list and the four of them cancel out exactly.

Count the tuples `(i, j, k, l)` with `a[i] + b[j] + c[k] + d[l] == 0`. Two tuples are different if any index differs, even when the values are the same.

**Constraints**
- `1 <= a.length, b.length, c.length, d.length <= 1000`
- `-10^8 <= values <= 10^8`
