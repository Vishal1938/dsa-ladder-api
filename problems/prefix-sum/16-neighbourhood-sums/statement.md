For every cell `(r, c)` compute the sum of all cells `(i, j)` with `|i − r| <= k` and `|j − c| <= k` that lie inside the grid.

Return a grid of the same size with these sums.

**Constraints**
- `1 <= rows, cols <= 200`
- `0 <= k <= 200`
- `0 <= grid[r][c] <= 1000`
