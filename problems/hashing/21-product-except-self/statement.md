A factory line has `n` stations, each with an efficiency factor. For every station you want to know the combined factor of **all the other** stations.

Return an array `out` where `out[i]` is the product of every `nums[j]` with `j != i`. Division is not allowed — one zero on the line would make it meaningless.

For a line with a single station the answer is `1`, the product of nothing at all.

**Constraints**
- `1 <= nums.length <= 10^5`
- `-30 <= nums[i] <= 30`
- `every answer fits in a signed 64-bit integer`
