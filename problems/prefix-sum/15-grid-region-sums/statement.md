`grid` is a field of numbers. Each query `[r1, c1, r2, c2]` asks for the sum of the rectangle with top-left corner `(r1, c1)` and bottom-right corner `(r2, c2)`, both included.

Return the answers in order.

**Constraints**
- `1 <= rows, cols <= 300`
- `-1000 <= grid[r][c] <= 1000`
- `1 <= queries.length <= 10^5`
- `0 <= r1 <= r2 < rows, 0 <= c1 <= c2 < cols`
