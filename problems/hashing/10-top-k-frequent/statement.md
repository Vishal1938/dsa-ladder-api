A streaming service logs the id of every track that was played today. The editors want today's `k` most played tracks.

Return the `k` ids with the highest play counts, most played first. When two ids were played equally often, the **smaller id** comes first. `k` is never larger than the number of different ids in `nums`.

**Constraints**
- `1 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`
- `1 <= k <= the number of distinct values in nums`
