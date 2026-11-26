A delivery van has a weight allowance. Given the parcel weights in increasing order, the depot wants to know how many pairs of parcels it could send together.

Count the index pairs `i < j` with `sorted[i] + sorted[j]` **strictly less than** `target`. `sorted` is already in non-decreasing order.

**Constraints**
- `1 <= sorted.length <= 10^5`
- `-10^9 <= sorted[i] <= 10^9`
- `-2 * 10^9 <= target <= 2 * 10^9`
- `sorted is in non-decreasing order`
