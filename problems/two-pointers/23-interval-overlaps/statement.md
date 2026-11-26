Two colleagues each hand in a list of the periods they are free, sorted and with no overlaps inside either list. You want every period when **both** of them are free.

Each interval `[start, end]` includes both ends, so two periods that merely touch at one instant overlap in that single instant, which counts as `[x, x]`. Return the overlapping periods in order.

**Constraints**
- `1 <= a.length, b.length <= 10^5`
- `0 <= start <= end <= 10^9`
- `each list is sorted by start and its own intervals never overlap`
