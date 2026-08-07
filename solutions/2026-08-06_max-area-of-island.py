"""
Max Area of Island  -  Medium
Array, DFS, BFS, Matrix
https://leetcode.com/problems/max-area-of-island/

Assigned: 2026-08-06

The grid holds 0s and 1s. An island is a group of 1s connected in the four cardinal directions. Return the area (number of cells) of the largest island, or 0 if there is none.

Examples
--------
  grid = [[1,1,0],[1,0,0],[0,0,1]]  ->  3
  grid = [[0,0],[0,0]]              ->  0

Constraints
-----------
  - 1 <= m, n <= 50
  - grid[i][j] is 0 or 1

Target complexity: O(m*n) time, O(m*n) space

  Check it        python leet.py check
  Nudge           python leet.py hint
  Reference       python leet.py solution
  Browser UI      python leet.py serve
"""

from typing import List, Optional


# ==========================================================================
#  YOUR SOLUTION
# ==========================================================================
def max_area_of_island(grid: List[List[int]]) -> int:
    pass


# ==========================================================================
#  SCRATCH TESTS - yours to play with.
#  `python leet.py check` runs the full hidden suite; this block is just for
#  poking at the function while you work.  Run it with:  python "2026-08-06_max-area-of-island.py"
# ==========================================================================
if __name__ == "__main__":
    print(max_area_of_island([[1, 1, 0], [1, 0, 0], [0, 0, 1]]))
    #  expected: 3
    print(max_area_of_island([[0, 0], [0, 0]]))
    #  expected: 0
    print(max_area_of_island([[1]]))
    #  expected: 1
