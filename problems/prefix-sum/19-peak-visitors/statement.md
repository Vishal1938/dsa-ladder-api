A museum logs each visit as `[arrive, leave]`: the visitor is inside at every whole minute `t` with `arrive <= t < leave` (they are gone at minute `leave`).

Return the largest number of visitors inside at the same minute.

**Constraints**
- `1 <= visits.length <= 10^5`
- `0 <= arrive < leave <= 10^5`
