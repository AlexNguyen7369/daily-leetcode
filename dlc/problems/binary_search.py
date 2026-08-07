"""Binary search over indices and over answers."""

PROBLEMS = [
    {
        "slug": "binary-search",
        "title": "Binary Search",
        "difficulty": "Easy",
        "topics": ["Array", "Binary Search"],
        "url": "https://leetcode.com/problems/binary-search/",
        "func": "search",
        "signature": "def search(nums: List[int], target: int) -> int:",
        "description": (
            "`nums` is sorted in ascending order with distinct values. Return the index of "
            "`target`, or -1 if it is absent. Your algorithm must run in O(log n) time."
        ),
        "examples": [
            "nums = [-1,0,3,5,9,12], target = 9  ->  4",
            "nums = [-1,0,3,5,9,12], target = 2  ->  -1",
        ],
        "constraints": ["1 <= len(nums) <= 10^4", "all values are unique and sorted ascending"],
        "hints": [
            "Keep an inclusive window [lo, hi] that must contain the target if it exists.",
            "Compare the midpoint and discard the half that cannot contain it.",
            "Use `lo + (hi - lo) // 2` and loop while lo <= hi.",
        ],
        "target": {"time": "O(log n)", "space": "O(1)"},
        "argspec": ["raw", "raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[-1, 0, 3, 5, 9, 12], 9], "expect": 4},
            {"args": [[-1, 0, 3, 5, 9, 12], 2], "expect": -1},
            {"args": [[5], 5], "expect": 0},
            {"args": [[5], -5], "expect": -1},
            {"args": [[2, 5], 5], "expect": 1},
            {"args": [[1, 2, 3, 4, 5, 6, 7, 8], 1], "expect": 0},
        ],
        "stress": {"args": lambda: [list(range(1_000_000)), 999_999], "budget": 1.0},
        "pitfalls": [
            "`while lo < hi` with an inclusive hi misses the last candidate.",
            "Forgetting mid +/- 1 when narrowing gives an infinite loop.",
        ],
        "solution": """
def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
""",
    },
    {
        "slug": "search-insert-position",
        "title": "Search Insert Position",
        "difficulty": "Easy",
        "topics": ["Array", "Binary Search"],
        "url": "https://leetcode.com/problems/search-insert-position/",
        "func": "search_insert",
        "signature": "def search_insert(nums: List[int], target: int) -> int:",
        "description": (
            "Given a sorted array of distinct integers, return the index of `target`. If it is "
            "not present, return the index where it would be inserted to keep the array sorted. "
            "O(log n) required."
        ),
        "examples": [
            "nums = [1,3,5,6], target = 5  ->  2",
            "nums = [1,3,5,6], target = 2  ->  1",
            "nums = [1,3,5,6], target = 7  ->  4",
        ],
        "constraints": ["1 <= len(nums) <= 10^4", "nums is sorted with distinct values"],
        "hints": [
            "You are looking for the first index whose value is >= target.",
            "That is a lower-bound search: keep a half-open window [lo, hi).",
            "When the loop ends, lo is the insertion point — no special case needed for 'absent'.",
        ],
        "target": {"time": "O(log n)", "space": "O(1)"},
        "argspec": ["raw", "raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[1, 3, 5, 6], 5], "expect": 2},
            {"args": [[1, 3, 5, 6], 2], "expect": 1},
            {"args": [[1, 3, 5, 6], 7], "expect": 4},
            {"args": [[1, 3, 5, 6], 0], "expect": 0},
            {"args": [[1], 1], "expect": 0},
        ],
        "stress": {"args": lambda: [list(range(0, 2_000_000, 2)), 1_999_999], "budget": 1.0},
        "pitfalls": ["Inserting past the end (index len(nums)) is a valid answer."],
        "solution": """
def search_insert(nums, target):
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
""",
    },
    {
        "slug": "search-a-2d-matrix",
        "title": "Search a 2D Matrix",
        "difficulty": "Medium",
        "topics": ["Array", "Binary Search", "Matrix"],
        "url": "https://leetcode.com/problems/search-a-2d-matrix/",
        "func": "search_matrix",
        "signature": "def search_matrix(matrix: List[List[int]], target: int) -> bool:",
        "description": (
            "Each row of `matrix` is sorted ascending, and the first value of each row is greater "
            "than the last value of the previous row. Return whether `target` is present, in "
            "O(log(m*n)) time."
        ),
        "examples": [
            "matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3   ->  True",
            "matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13  ->  False",
        ],
        "constraints": ["1 <= m, n <= 100", "-10^4 <= matrix[i][j], target <= 10^4"],
        "hints": [
            "The stated ordering means the whole matrix is one sorted sequence.",
            "Binary search indices 0 .. m*n-1 and map index -> (index // n, index % n).",
            "Alternatively binary search for the row first, then inside it.",
        ],
        "target": {"time": "O(log(m*n))", "space": "O(1)"},
        "argspec": ["raw", "raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3], "expect": True},
            {"args": [[[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13], "expect": False},
            {"args": [[[1]], 1], "expect": True},
            {"args": [[[1]], 2], "expect": False},
            {"args": [[[1, 3]], 3], "expect": True},
            {"args": [[[1], [3], [5]], 5], "expect": True},
        ],
        "stress": {
            "args": lambda: [[[r * 100 + c for c in range(100)] for r in range(100)], 9_999],
            "budget": 1.0,
        },
        "pitfalls": ["Scanning row by row is O(m*n) and misses the point of the problem."],
        "solution": """
def search_matrix(matrix, target):
    rows, cols = len(matrix), len(matrix[0])
    lo, hi = 0, rows * cols - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        value = matrix[mid // cols][mid % cols]
        if value == target:
            return True
        if value < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False
""",
    },
    {
        "slug": "koko-eating-bananas",
        "title": "Koko Eating Bananas",
        "difficulty": "Medium",
        "topics": ["Array", "Binary Search"],
        "url": "https://leetcode.com/problems/koko-eating-bananas/",
        "func": "min_eating_speed",
        "signature": "def min_eating_speed(piles: List[int], h: int) -> int:",
        "description": (
            "Koko eats at k bananas per hour. Each hour she picks one pile and eats up to k from "
            "it; if the pile has fewer she stops eating for that hour. Return the smallest k that "
            "lets her finish all piles within `h` hours."
        ),
        "examples": [
            "piles = [3,6,7,11], h = 8       ->  4",
            "piles = [30,11,23,4,20], h = 5  ->  30",
            "piles = [30,11,23,4,20], h = 6  ->  23",
        ],
        "constraints": ["1 <= len(piles) <= 10^4", "len(piles) <= h <= 10^9", "1 <= piles[i] <= 10^9"],
        "hints": [
            "You are searching over the answer, not over the array.",
            "hours(k) = sum(ceil(pile / k)) is non-increasing in k, so the feasible k form a suffix.",
            "Binary search k in [1, max(piles)] for the smallest k with hours(k) <= h.",
        ],
        "target": {"time": "O(n log(max(piles)))", "space": "O(1)"},
        "argspec": ["raw", "raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[3, 6, 7, 11], 8], "expect": 4},
            {"args": [[30, 11, 23, 4, 20], 5], "expect": 30},
            {"args": [[30, 11, 23, 4, 20], 6], "expect": 23},
            {"args": [[1], 1], "expect": 1},
            {"args": [[312884470], 968709470], "expect": 1},
            {"args": [[1, 1, 1, 999999999], 10], "expect": 142857143},
        ],
        "stress": {
            "args": lambda: [[10**9 - i for i in range(10_000)], 10_000],
            "budget": 2.0,
        },
        "pitfalls": [
            "Use -(-pile // k) or math.ceil with care — float division loses precision at 10^9.",
            "k must be at least 1, and never needs to exceed max(piles).",
        ],
        "solution": """
def min_eating_speed(piles, h):
    lo, hi = 1, max(piles)
    while lo < hi:
        k = (lo + hi) // 2
        hours = sum(-(-pile // k) for pile in piles)
        if hours <= h:
            hi = k
        else:
            lo = k + 1
    return lo
""",
    },
    {
        "slug": "find-minimum-in-rotated-sorted-array",
        "title": "Find Minimum in Rotated Sorted Array",
        "difficulty": "Medium",
        "topics": ["Array", "Binary Search"],
        "url": "https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/",
        "func": "find_min",
        "signature": "def find_min(nums: List[int]) -> int:",
        "description": (
            "`nums` is an ascending array of unique values that has been rotated between 1 and n "
            "times. Return its minimum element in O(log n) time."
        ),
        "examples": [
            "nums = [3,4,5,1,2]      ->  1",
            "nums = [4,5,6,7,0,1,2]  ->  0",
            "nums = [11,13,15,17]    ->  11",
        ],
        "constraints": ["1 <= len(nums) <= 5000", "all values unique", "the array is rotated"],
        "hints": [
            "Compare the midpoint with the *right* end, not the left.",
            "If nums[mid] > nums[hi] the minimum is strictly right of mid.",
            "Otherwise mid could itself be the minimum, so set hi = mid (not mid - 1).",
        ],
        "target": {"time": "O(log n)", "space": "O(1)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[3, 4, 5, 1, 2]], "expect": 1},
            {"args": [[4, 5, 6, 7, 0, 1, 2]], "expect": 0},
            {"args": [[11, 13, 15, 17]], "expect": 11},
            {"args": [[2, 1]], "expect": 1},
            {"args": [[1]], "expect": 1},
            {"args": [[5, 1, 2, 3, 4]], "expect": 1},
        ],
        "stress": {
            "args": lambda: [list(range(2_500, 5_000)) + list(range(2_500))],
            "budget": 1.0,
        },
        "pitfalls": [
            "Comparing against nums[lo] needs an extra case for the already-sorted array.",
            "min(nums) is O(n) — technically correct, but not what the problem asks.",
        ],
        "solution": """
def find_min(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    return nums[lo]
""",
    },
    {
        "slug": "search-in-rotated-sorted-array",
        "title": "Search in Rotated Sorted Array",
        "difficulty": "Medium",
        "topics": ["Array", "Binary Search"],
        "url": "https://leetcode.com/problems/search-in-rotated-sorted-array/",
        "func": "search_rotated",
        "signature": "def search_rotated(nums: List[int], target: int) -> int:",
        "description": (
            "`nums` was sorted ascending with distinct values, then rotated at some pivot. "
            "Return the index of `target` or -1, in O(log n) time."
        ),
        "examples": [
            "nums = [4,5,6,7,0,1,2], target = 0  ->  4",
            "nums = [4,5,6,7,0,1,2], target = 3  ->  -1",
            "nums = [1], target = 0              ->  -1",
        ],
        "constraints": ["1 <= len(nums) <= 5000", "all values unique"],
        "hints": [
            "At every step at least one of the two halves is properly sorted.",
            "Compare nums[lo] with nums[mid] to find out which half that is.",
            "If the target lies inside the sorted half's range, search there; otherwise search the other.",
        ],
        "target": {"time": "O(log n)", "space": "O(1)"},
        "argspec": ["raw", "raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[4, 5, 6, 7, 0, 1, 2], 0], "expect": 4},
            {"args": [[4, 5, 6, 7, 0, 1, 2], 3], "expect": -1},
            {"args": [[1], 0], "expect": -1},
            {"args": [[1], 1], "expect": 0},
            {"args": [[3, 1], 1], "expect": 1},
            {"args": [[5, 1, 3], 3], "expect": 2},
            {"args": [[1, 2, 3, 4, 5], 4], "expect": 3},
        ],
        "stress": {
            "args": lambda: [list(range(3_000, 5_000)) + list(range(3_000)), 2_999],
            "budget": 1.0,
        },
        "pitfalls": [
            "Use <= when testing whether the target is in the sorted half — the endpoints count.",
            "A non-rotated array must still work.",
        ],
        "solution": """
def search_rotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
""",
    },
]
