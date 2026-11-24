A shuttle drives in one direction past stops `0, 1, 2, …`. Each trip `[count, from, to]` is a group of `count` people who board at stop `from` and get off at stop `to` (their seats are free again at stop `to`).

Return `true` if the shuttle never carries more than `capacity` people at once.

**Constraints**
- `1 <= trips.length <= 10^5`
- `1 <= count <= 100`
- `0 <= from < to <= 10^5`
- `1 <= capacity <= 10^7`
