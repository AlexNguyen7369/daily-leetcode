"""Intervals, sorting and heaps."""

import random

PROBLEMS = [
    {
        "slug": "last-stone-weight",
        "title": "Last Stone Weight",
        "difficulty": "Easy",
        "topics": ["Array", "Heap"],
        "url": "https://leetcode.com/problems/last-stone-weight/",
        "func": "last_stone_weight",
        "signature": "def last_stone_weight(stones: List[int]) -> int:",
        "description": (
            "Repeatedly smash the two heaviest stones together. If they are equal both are "
            "destroyed; otherwise the heavier one is left with the weight difference. Return the "
            "weight of the last remaining stone, or 0 if none remain."
        ),
        "examples": ["stones = [2,7,4,1,8,1]  ->  1", "stones = [1]  ->  1", "stones = [2,2]  ->  0"],
        "constraints": ["1 <= len(stones) <= 30", "1 <= stones[i] <= 1000"],
        "hints": [
            "You always need the two largest values — that is a max-heap.",
            "Python's heapq is a min-heap; push negatives to invert it.",
            "Push the difference back only when it is non-zero.",
        ],
        "target": {"time": "O(n log n)", "space": "O(n)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[2, 7, 4, 1, 8, 1]], "expect": 1},
            {"args": [[1]], "expect": 1},
            {"args": [[2, 2]], "expect": 0},
            {"args": [[3, 7, 2]], "expect": 2},
            {"args": [[10, 4, 2, 10]], "expect": 2},
        ],
        "stress": {
            "args": lambda: [random.Random(71).choices(range(1, 1001), k=30)],
            "budget": 1.0,
        },
        "pitfalls": ["Re-sorting the whole list every round is O(n^2 log n) — fine at n=30, but the heap is the point."],
        "solution": """
def last_stone_weight(stones):
    import heapq
    heap = [-s for s in stones]
    heapq.heapify(heap)
    while len(heap) > 1:
        first = -heapq.heappop(heap)
        second = -heapq.heappop(heap)
        if first != second:
            heapq.heappush(heap, -(first - second))
    return -heap[0] if heap else 0
""",
    },
    {
        "slug": "kth-largest-element-in-an-array",
        "title": "Kth Largest Element in an Array",
        "difficulty": "Medium",
        "topics": ["Array", "Heap", "Quickselect", "Sorting"],
        "url": "https://leetcode.com/problems/kth-largest-element-in-an-array/",
        "func": "find_kth_largest",
        "signature": "def find_kth_largest(nums: List[int], k: int) -> int:",
        "description": (
            "Return the k-th largest element in `nums` — the k-th in sorted-descending order, "
            "not the k-th distinct value."
        ),
        "examples": [
            "nums = [3,2,1,5,6,4], k = 2         ->  5",
            "nums = [3,2,3,1,2,4,5,5,6], k = 4   ->  4",
        ],
        "constraints": ["1 <= k <= len(nums) <= 10^5", "-10^4 <= nums[i] <= 10^4"],
        "hints": [
            "Sorting is O(n log n) and completely acceptable as a first answer.",
            "A min-heap capped at size k is O(n log k).",
            "Quickselect partitions around a pivot and recurses into one side only — O(n) average.",
        ],
        "target": {"time": "O(n) average (quickselect) or O(n log k)", "space": "O(k)"},
        "argspec": ["raw", "raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[3, 2, 1, 5, 6, 4], 2], "expect": 5},
            {"args": [[3, 2, 3, 1, 2, 4, 5, 5, 6], 4], "expect": 4},
            {"args": [[1], 1], "expect": 1},
            {"args": [[2, 1], 2], "expect": 1},
            {"args": [[7, 7, 7], 2], "expect": 7},
        ],
        "stress": {
            "args": lambda: [random.Random(81).choices(range(-10_000, 10_000), k=200_000), 500],
            "budget": 2.0,
        },
        "pitfalls": ["Duplicates count — the 2nd largest of [7,7,7] is 7."],
        "solution": """
def find_kth_largest(nums, k):
    import heapq
    heap = []
    for x in nums:
        if len(heap) < k:
            heapq.heappush(heap, x)
        elif x > heap[0]:
            heapq.heapreplace(heap, x)
    return heap[0]
""",
    },
    {
        "slug": "merge-intervals",
        "title": "Merge Intervals",
        "difficulty": "Medium",
        "topics": ["Array", "Sorting"],
        "url": "https://leetcode.com/problems/merge-intervals/",
        "func": "merge_intervals",
        "signature": "def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:",
        "description": (
            "Merge all overlapping intervals and return the non-overlapping intervals that cover "
            "the same span, sorted by start."
        ),
        "examples": [
            "intervals = [[1,3],[2,6],[8,10],[15,18]]  ->  [[1,6],[8,10],[15,18]]",
            "intervals = [[1,4],[4,5]]                 ->  [[1,5]]",
        ],
        "constraints": ["1 <= len(intervals) <= 10^4", "0 <= start <= end <= 10^4"],
        "hints": [
            "Sort by start time first — then any overlap is with the interval you just emitted.",
            "Two intervals overlap when the next start is <= the current end.",
            "Merging means extending the current end to max(current end, next end).",
        ],
        "target": {"time": "O(n log n)", "space": "O(n)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[[1, 3], [2, 6], [8, 10], [15, 18]]], "expect": [[1, 6], [8, 10], [15, 18]]},
            {"args": [[[1, 4], [4, 5]]], "expect": [[1, 5]]},
            {"args": [[[1, 4], [0, 4]]], "expect": [[0, 4]]},
            {"args": [[[1, 4], [2, 3]]], "expect": [[1, 4]]},
            {"args": [[[1, 4]]], "expect": [[1, 4]]},
            {"args": [[[2, 3], [4, 5], [6, 7], [8, 9], [1, 10]]], "expect": [[1, 10]]},
        ],
        "stress": {
            "args": lambda: [[[i, i + 1] for i in range(0, 20_000, 2)]],
            "budget": 2.0,
        },
        "pitfalls": [
            "Touching intervals like [1,4] and [4,5] do count as overlapping.",
            "[[1,4],[2,3]] — the nested interval must not shrink the merged end.",
        ],
        "solution": """
def merge_intervals(intervals):
    out = []
    for start, end in sorted(intervals):
        if out and start <= out[-1][1]:
            out[-1][1] = max(out[-1][1], end)
        else:
            out.append([start, end])
    return out
""",
    },
    {
        "slug": "insert-interval",
        "title": "Insert Interval",
        "difficulty": "Medium",
        "topics": ["Array"],
        "url": "https://leetcode.com/problems/insert-interval/",
        "func": "insert_interval",
        "signature": "def insert_interval(intervals: List[List[int]], new_interval: List[int]) -> List[List[int]]:",
        "description": (
            "`intervals` is sorted by start and has no overlaps. Insert `new_interval`, merging "
            "where necessary, and return the result still sorted and non-overlapping."
        ),
        "examples": [
            "intervals = [[1,3],[6,9]], newInterval = [2,5]  ->  [[1,5],[6,9]]",
            "intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]  ->  [[1,2],[3,10],[12,16]]",
        ],
        "constraints": ["0 <= len(intervals) <= 10^4", "intervals is sorted by start"],
        "hints": [
            "The input is already sorted, so you can do this in one O(n) pass without re-sorting.",
            "Three phases: intervals entirely before the new one, the overlapping run, then the rest.",
            "While overlapping, absorb into the new interval: start = min(...), end = max(...).",
        ],
        "target": {"time": "O(n)", "space": "O(n)"},
        "argspec": ["raw", "raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[[1, 3], [6, 9]], [2, 5]], "expect": [[1, 5], [6, 9]]},
            {
                "args": [[[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]],
                "expect": [[1, 2], [3, 10], [12, 16]],
            },
            {"args": [[], [5, 7]], "expect": [[5, 7]]},
            {"args": [[[1, 5]], [2, 3]], "expect": [[1, 5]]},
            {"args": [[[1, 5]], [6, 8]], "expect": [[1, 5], [6, 8]]},
            {"args": [[[1, 5]], [0, 0]], "expect": [[0, 0], [1, 5]]},
        ],
        "stress": {
            "args": lambda: [[[i, i + 1] for i in range(0, 40_000, 4)], [10, 30_000]],
            "budget": 2.0,
        },
        "pitfalls": [
            "An empty input list still has to produce [new_interval].",
            "Inserting before everything and after everything are both real cases.",
        ],
        "solution": """
def insert_interval(intervals, new_interval):
    start, end = new_interval
    out = []
    i = 0
    n = len(intervals)
    while i < n and intervals[i][1] < start:
        out.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= end:
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    out.append([start, end])
    while i < n:
        out.append(intervals[i])
        i += 1
    return out
""",
    },
]
