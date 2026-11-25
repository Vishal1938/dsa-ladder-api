A sensor reports one reading per second: `nums[i]` is the reading at second `i`. A pair of seconds `i < j` is **steady** if the reading grew by exactly one per second in between, that is `nums[j] - nums[i] == j - i`.

Return the number of steady pairs.

**Constraints**
- `1 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`
