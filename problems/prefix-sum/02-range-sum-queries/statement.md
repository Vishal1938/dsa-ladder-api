You are given an array `nums` and a list of questions. Each question `queries[j] = [l, r]` asks for the sum of `nums[l] + nums[l+1] + … + nums[r]` (both ends included).

Return an array `answer` where `answer[j]` is the answer to question `j`.

There can be as many questions as numbers, so adding up each range one by one is too slow.

**Constraints**
- `1 <= nums.length <= 10^5`
- `1 <= queries.length <= 10^5`
- `-10^4 <= nums[i] <= 10^4`
- `0 <= l <= r < nums.length`
