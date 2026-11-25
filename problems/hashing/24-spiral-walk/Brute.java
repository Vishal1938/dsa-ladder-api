import java.util.*;

class Solution {
    public List<Integer> spiralOrder(int[][] matrix) {
        List<List<Integer>> rest = new ArrayList<>();
        for (int[] row : matrix) {
            List<Integer> r = new ArrayList<>();
            for (int x : row) r.add(x);
            rest.add(r);
        }
        List<Integer> out = new ArrayList<>();
        while (!rest.isEmpty() && !rest.get(0).isEmpty()) {
            out.addAll(rest.remove(0));                 // the top row is next, left to right
            int rows = rest.size(), cols = rows == 0 ? 0 : rest.get(0).size();
            List<List<Integer>> turned = new ArrayList<>();
            for (int c = cols - 1; c >= 0; c--) {       // turn what is left, so the next side is on top
                List<Integer> r = new ArrayList<>();
                for (int i = 0; i < rows; i++) r.add(rest.get(i).get(c));
                turned.add(r);
            }
            rest = turned;
        }
        return out;
    }
}
