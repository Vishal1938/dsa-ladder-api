A vending machine takes exactly two coins. Given the coin values `nums` and the price `target`, find two different coins whose values add up to the price.

Return `[i, j]` with `i < j` and `nums[i] + nums[j] == target`. If several pairs work, pick the one with the **smallest `j`**; if there is still a tie, pick the smallest `i`. Return `[-1, -1]` if no pair adds up to the price.

**Constraints**
- `1 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`
- `-10^9 <= target <= 10^9`
