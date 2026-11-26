A workshop has a pile of sticks and wants to know how many different sets of three sticks could be laid out as a triangle with no gaps and no overlap.

Count the triples of positions in `sides` whose three lengths can form a triangle. Three lengths work exactly when each one is shorter than the other two added together. Some sticks have length `0`.

**Constraints**
- `1 <= sides.length <= 3000`
- `0 <= sides[i] <= 10^6`
