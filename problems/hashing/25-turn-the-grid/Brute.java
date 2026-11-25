import java.util.*;

class Solution {
    public void rotateImage(int[][] matrix) {
        int n = matrix.length;
        int[][] cells = new int[n * n][];
        int k = 0;
        for (int r = 0; r < n; r++)
            for (int c = 0; c < n; c++) cells[k++] = new int[]{r, c, matrix[r][c]};
        for (int r = 0; r < n; r++)
            for (int c = 0; c < n; c++)
                // after a clockwise quarter turn, (r, c) holds whatever used to be at (n - 1 - c, r)
                for (int[] cell : cells)
                    if (cell[0] == n - 1 - c && cell[1] == r) { matrix[r][c] = cell[2]; break; }
    }
}
