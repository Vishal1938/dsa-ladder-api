import java.util.*;

class Solution {
    public void rotateImage(int[][] matrix) {
        int n = matrix.length;
        for (int r = 0; r < n; r++)                     // mirror along the main diagonal
            for (int c = r + 1; c < n; c++) {
                int t = matrix[r][c];
                matrix[r][c] = matrix[c][r];
                matrix[c][r] = t;
            }
        for (int[] row : matrix)                        // then reverse every row
            for (int from = 0, to = n - 1; from < to; from++, to--) {
                int t = row[from];
                row[from] = row[to];
                row[to] = t;
            }
    }
}
