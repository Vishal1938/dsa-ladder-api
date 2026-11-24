You start with `x` coins, where `x` is a positive whole number. Then `changes[0], changes[1], …` are applied one after another (positive means you gain coins, negative means you lose them).

After **every** change your balance must be at least `1`.

Return the smallest starting amount `x >= 1` that keeps you safe the whole way.

**Constraints**
- `1 <= changes.length <= 10^5`
- `-10^4 <= changes[i] <= 10^4`
