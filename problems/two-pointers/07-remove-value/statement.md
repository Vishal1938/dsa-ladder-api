A warehouse list contains some entries for a product that has been discontinued. They have to come out, and the remaining entries must keep their order.

Return the kept entries: everything in `nums` that is not equal to `val`, in the original order. Do the compacting inside `nums` with a writer index rather than building a second list.

**Constraints**
- `1 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`
- `-10^9 <= val <= 10^9`
