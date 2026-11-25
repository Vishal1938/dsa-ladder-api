A warehouse ships goods in boxes of `m` items. Two batches can be shipped together without a leftover exactly when the total number of items divides evenly by `m`.

Given the batch sizes `nums`, count the index pairs `i < j` for which `nums[i] + nums[j]` is divisible by `m`.

**Constraints**
- `1 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`
- `1 <= m <= 10^4`
