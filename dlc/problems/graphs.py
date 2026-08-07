"""Grid traversal and graph search."""


def _big_grid(rows, cols, pattern):
    return [[pattern(r, c) for c in range(cols)] for r in range(rows)]


PROBLEMS = [
    {
        "slug": "number-of-islands",
        "title": "Number of Islands",
        "difficulty": "Medium",
        "topics": ["Array", "DFS", "BFS", "Union Find", "Matrix"],
        "url": "https://leetcode.com/problems/number-of-islands/",
        "func": "num_islands",
        "signature": "def num_islands(grid: List[List[str]]) -> int:",
        "description": (
            "The grid holds '1' (land) and '0' (water). Count the islands — groups of land "
            "connected horizontally or vertically. The grid's edges are all surrounded by water."
        ),
        "examples": [
            'grid = [["1","1","0"],["1","0","0"],["0","0","1"]]  ->  2',
            'grid = [["0"]]  ->  0',
        ],
        "constraints": ["1 <= m, n <= 300", "grid[i][j] is '0' or '1'"],
        "hints": [
            "Every unvisited land cell you meet starts exactly one new island.",
            "Flood-fill from it (DFS or BFS) and mark everything reachable as visited.",
            "Marking in place (overwrite '1' with '0') avoids a separate visited set.",
        ],
        "target": {"time": "O(m*n)", "space": "O(m*n) worst case"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {
                "args": [[["1", "1", "1", "1", "0"], ["1", "1", "0", "1", "0"],
                          ["1", "1", "0", "0", "0"], ["0", "0", "0", "0", "0"]]],
                "expect": 1,
            },
            {
                "args": [[["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"],
                          ["0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]]],
                "expect": 3,
            },
            {"args": [[["0"]]], "expect": 0},
            {"args": [[["1"]]], "expect": 1},
            {"args": [[["1", "0", "1"], ["0", "1", "0"], ["1", "0", "1"]]], "expect": 5},
        ],
        "stress": {
            "args": lambda: [_big_grid(300, 300, lambda r, c: "1" if (r + c) % 2 == 0 else "0")],
            "budget": 3.0,
        },
        "pitfalls": [
            "Diagonals do not connect islands.",
            "Recursive DFS on a 300x300 all-land grid can exceed Python's recursion limit — "
            "an explicit stack or BFS is safer.",
        ],
        "solution": """
def num_islands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != '1':
                continue
            count += 1
            stack = [(r, c)]
            grid[r][c] = '0'
            while stack:
                y, x = stack.pop()
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] == '1':
                        grid[ny][nx] = '0'
                        stack.append((ny, nx))
    return count
""",
    },
    {
        "slug": "max-area-of-island",
        "title": "Max Area of Island",
        "difficulty": "Medium",
        "topics": ["Array", "DFS", "BFS", "Matrix"],
        "url": "https://leetcode.com/problems/max-area-of-island/",
        "func": "max_area_of_island",
        "signature": "def max_area_of_island(grid: List[List[int]]) -> int:",
        "description": (
            "The grid holds 0s and 1s. An island is a group of 1s connected in the four cardinal "
            "directions. Return the area (number of cells) of the largest island, or 0 if there is none."
        ),
        "examples": [
            "grid = [[1,1,0],[1,0,0],[0,0,1]]  ->  3",
            "grid = [[0,0],[0,0]]              ->  0",
        ],
        "constraints": ["1 <= m, n <= 50", "grid[i][j] is 0 or 1"],
        "hints": [
            "Same flood fill as counting islands, but each fill returns a size.",
            "Take the maximum over all fills.",
            "Mark cells as visited the moment you push them, not when you pop them.",
        ],
        "target": {"time": "O(m*n)", "space": "O(m*n)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[[1, 1, 0], [1, 0, 0], [0, 0, 1]]], "expect": 3},
            {"args": [[[0, 0], [0, 0]]], "expect": 0},
            {"args": [[[1]]], "expect": 1},
            {
                "args": [[[0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 1, 1, 0, 0],
                          [0, 1, 1, 0, 0], [0, 0, 0, 1, 1]]],
                "expect": 4,
            },
            {"args": [[[1, 1, 1], [1, 1, 1]]], "expect": 6},
        ],
        "stress": {
            "args": lambda: [_big_grid(50, 50, lambda r, c: 1)],
            "budget": 2.0,
        },
        "pitfalls": ["Counting a cell twice inflates the area — mark before you recurse."],
        "solution": """
def max_area_of_island(grid):
    rows, cols = len(grid), len(grid[0])
    best = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 1:
                continue
            area = 0
            stack = [(r, c)]
            grid[r][c] = 0
            while stack:
                y, x = stack.pop()
                area += 1
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] == 1:
                        grid[ny][nx] = 0
                        stack.append((ny, nx))
            best = max(best, area)
    return best
""",
    },
    {
        "slug": "course-schedule",
        "title": "Course Schedule",
        "difficulty": "Medium",
        "topics": ["DFS", "BFS", "Graph", "Topological Sort"],
        "url": "https://leetcode.com/problems/course-schedule/",
        "func": "can_finish",
        "signature": "def can_finish(num_courses: int, prerequisites: List[List[int]]) -> bool:",
        "description": (
            "`prerequisites[i] = [a, b]` means you must take course b before course a. "
            "Return True if you can finish all `num_courses` courses."
        ),
        "examples": [
            "numCourses = 2, prerequisites = [[1,0]]        ->  True",
            "numCourses = 2, prerequisites = [[1,0],[0,1]]  ->  False",
        ],
        "constraints": ["1 <= numCourses <= 2000", "0 <= len(prerequisites) <= 5000", "pairs are unique"],
        "hints": [
            "This asks whether a directed graph has a cycle.",
            "Kahn's algorithm: repeatedly remove a node with in-degree 0 and decrement its neighbours.",
            "If you manage to remove all n nodes there is no cycle. (DFS with three colours works too.)",
        ],
        "target": {"time": "O(V + E)", "space": "O(V + E)"},
        "argspec": ["raw", "raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [2, [[1, 0]]], "expect": True},
            {"args": [2, [[1, 0], [0, 1]]], "expect": False},
            {"args": [1, []], "expect": True},
            {"args": [5, [[1, 4], [2, 4], [3, 1], [3, 2]]], "expect": True},
            {"args": [3, [[0, 1], [1, 2], [2, 0]]], "expect": False},
            {"args": [4, [[2, 0], [1, 0], [3, 1], [3, 2], [1, 3]]], "expect": False},
        ],
        "stress": {
            "args": lambda: [2_000, [[i + 1, i] for i in range(1_999)]],
            "budget": 2.0,
        },
        "pitfalls": [
            "The graph may be disconnected — every component needs checking.",
            "A plain 'visited' set without tracking the current recursion path reports false cycles.",
        ],
        "solution": """
def can_finish(num_courses, prerequisites):
    from collections import deque
    graph = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        indegree[course] += 1
    queue = deque(i for i in range(num_courses) if indegree[i] == 0)
    seen = 0
    while queue:
        node = queue.popleft()
        seen += 1
        for nxt in graph[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return seen == num_courses
""",
    },
    {
        "slug": "rotting-oranges",
        "title": "Rotting Oranges",
        "difficulty": "Medium",
        "topics": ["Array", "BFS", "Matrix"],
        "url": "https://leetcode.com/problems/rotting-oranges/",
        "func": "oranges_rotting",
        "signature": "def oranges_rotting(grid: List[List[int]]) -> int:",
        "description": (
            "0 is empty, 1 is a fresh orange, 2 is rotten. Every minute, a fresh orange adjacent "
            "to a rotten one becomes rotten. Return the minutes until no fresh orange remains, "
            "or -1 if that never happens."
        ),
        "examples": [
            "grid = [[2,1,1],[1,1,0],[0,1,1]]  ->  4",
            "grid = [[2,1,1],[0,1,1],[1,0,1]]  ->  -1",
            "grid = [[0,2]]                    ->  0",
        ],
        "constraints": ["1 <= m, n <= 10", "grid[i][j] is 0, 1 or 2"],
        "hints": [
            "Rot spreads one ring at a time — that is level-by-level BFS.",
            "Seed the queue with *every* rotten orange at once (multi-source BFS).",
            "Count fresh oranges up front; if any remain when the queue drains, return -1.",
        ],
        "target": {"time": "O(m*n)", "space": "O(m*n)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[[2, 1, 1], [1, 1, 0], [0, 1, 1]]], "expect": 4},
            {"args": [[[2, 1, 1], [0, 1, 1], [1, 0, 1]]], "expect": -1},
            {"args": [[[0, 2]]], "expect": 0},
            {"args": [[[0]]], "expect": 0},
            {"args": [[[1]]], "expect": -1},
            {"args": [[[2, 2], [1, 1]]], "expect": 1},
        ],
        "stress": {
            "args": lambda: [[[2 if (r, c) == (0, 0) else 1 for c in range(10)] for r in range(10)]],
            "budget": 1.5,
        },
        "pitfalls": [
            "A grid with no fresh oranges answers 0, not -1.",
            "Rotting one orange at a time (single-source BFS per rotten cell) gives the wrong minute count.",
        ],
        "solution": """
def oranges_rotting(grid):
    from collections import deque
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1
    if fresh == 0:
        return 0
    minutes = 0
    while queue and fresh:
        minutes += 1
        for _ in range(len(queue)):
            y, x = queue.popleft()
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = y + dy, x + dx
                if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] == 1:
                    grid[ny][nx] = 2
                    fresh -= 1
                    queue.append((ny, nx))
    return -1 if fresh else minutes
""",
    },
]
