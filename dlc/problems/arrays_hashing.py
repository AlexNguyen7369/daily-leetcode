"""Arrays, hashing and counting."""

import random

PROBLEMS = [
    {
        "slug": "two-sum",
        "title": "Two Sum",
        "difficulty": "Easy",
        "topics": ["Array", "Hash Table"],
        "url": "https://leetcode.com/problems/two-sum/",
        "func": "two_sum",
        "signature": "def two_sum(nums: List[int], target: int) -> List[int]:",
        "description": (
            "Given an array of integers `nums` and an integer `target`, return the "
            "indices of the two numbers that add up to `target`.\n"
            "Exactly one valid answer exists, and you may not use the same element twice. "
            "Return the indices in increasing order."
        ),
        "examples": [
            "nums = [2,7,11,15], target = 9  ->  [0,1]   (2 + 7 == 9)",
            "nums = [3,2,4],     target = 6  ->  [1,2]",
            "nums = [3,3],       target = 6  ->  [0,1]",
        ],
        "constraints": [
            "2 <= len(nums) <= 10^4",
            "-10^9 <= nums[i], target <= 10^9",
        ],
        "hints": [
            "The brute force is every pair. What information would let you skip the inner loop?",
            "While scanning left to right, for each x you need to know whether target - x was already seen.",
            "Keep a dict {value: index} of everything seen so far and look up target - x in O(1).",
        ],
        "target": {"time": "O(n)", "space": "O(n)"},
        "argspec": ["raw", "raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[2, 7, 11, 15], 9], "expect": [0, 1]},
            {"args": [[3, 2, 4], 6], "expect": [1, 2]},
            {"args": [[3, 3], 6], "expect": [0, 1]},
            {"args": [[-1, -2, -3, -4, -5], -8], "expect": [2, 4]},
            {"args": [[0, 4, 3, 0], 0], "expect": [0, 3]},
            {"args": [[5, 75, 25], 100], "expect": [1, 2]},
        ],
        "stress": {"args": lambda: [list(range(200_000)), 399_997], "budget": 1.5},
        "pitfalls": [
            "Adding a value to the dict before you look it up lets an element pair with itself.",
            "Duplicate values are legal — store the index you would return.",
        ],
        "solution": """
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []
""",
    },
    {
        "slug": "contains-duplicate",
        "title": "Contains Duplicate",
        "difficulty": "Easy",
        "topics": ["Array", "Hash Table", "Sorting"],
        "url": "https://leetcode.com/problems/contains-duplicate/",
        "func": "contains_duplicate",
        "signature": "def contains_duplicate(nums: List[int]) -> bool:",
        "description": (
            "Return True if any value appears at least twice in `nums`, and False if "
            "every element is distinct."
        ),
        "examples": [
            "nums = [1,2,3,1]       ->  True",
            "nums = [1,2,3,4]       ->  False",
            "nums = [1,1,1,3,3,4,2] ->  True",
        ],
        "constraints": ["1 <= len(nums) <= 10^5", "-10^9 <= nums[i] <= 10^9"],
        "hints": [
            "Sorting puts duplicates next to each other — that is O(n log n).",
            "A set answers 'have I seen this before?' in O(1).",
            "len(set(nums)) != len(nums) is the whole problem in one line.",
        ],
        "target": {"time": "O(n)", "space": "O(n)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[1, 2, 3, 1]], "expect": True},
            {"args": [[1, 2, 3, 4]], "expect": False},
            {"args": [[1, 1, 1, 3, 3, 4, 3, 2, 4, 2]], "expect": True},
            {"args": [[1]], "expect": False},
            {"args": [[-1, -1]], "expect": True},
        ],
        "stress": {"args": lambda: [list(range(300_000))], "budget": 1.5},
        "pitfalls": ["Returning early inside the loop matters for the all-distinct case only."],
        "solution": """
def contains_duplicate(nums):
    return len(set(nums)) != len(nums)
""",
    },
    {
        "slug": "valid-anagram",
        "title": "Valid Anagram",
        "difficulty": "Easy",
        "topics": ["Hash Table", "String", "Sorting"],
        "url": "https://leetcode.com/problems/valid-anagram/",
        "func": "is_anagram",
        "signature": "def is_anagram(s: str, t: str) -> bool:",
        "description": (
            "Given two strings `s` and `t`, return True if `t` is an anagram of `s` — "
            "the same letters with the same multiplicities, in any order."
        ),
        "examples": [
            's = "anagram", t = "nagaram"  ->  True',
            's = "rat",     t = "car"      ->  False',
        ],
        "constraints": ["1 <= len(s), len(t) <= 5 * 10^4", "s and t consist of lowercase letters"],
        "hints": [
            "Different lengths can never be anagrams — check that first.",
            "Sorting both strings works and is O(n log n).",
            "Counting characters into a dict (or collections.Counter) is O(n).",
        ],
        "target": {"time": "O(n)", "space": "O(1) — at most 26 counters"},
        "argspec": ["raw", "raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": ["anagram", "nagaram"], "expect": True},
            {"args": ["rat", "car"], "expect": False},
            {"args": ["a", "a"], "expect": True},
            {"args": ["ab", "a"], "expect": False},
            {"args": ["aacc", "ccac"], "expect": False},
        ],
        "stress": {
            "args": lambda: ["ab" * 100_000, "ba" * 100_000],
            "budget": 1.5,
        },
        "pitfalls": ["`s.count(c) for c in s` inside a loop is O(n^2) — it rescans the string."],
        "solution": """
def is_anagram(s, t):
    if len(s) != len(t):
        return False
    counts = {}
    for c in s:
        counts[c] = counts.get(c, 0) + 1
    for c in t:
        if counts.get(c, 0) == 0:
            return False
        counts[c] -= 1
    return True
""",
    },
    {
        "slug": "majority-element",
        "title": "Majority Element",
        "difficulty": "Easy",
        "topics": ["Array", "Hash Table", "Divide and Conquer"],
        "url": "https://leetcode.com/problems/majority-element/",
        "func": "majority_element",
        "signature": "def majority_element(nums: List[int]) -> int:",
        "description": (
            "Return the element that appears more than n/2 times in `nums`. "
            "You may assume the majority element always exists."
        ),
        "examples": ["nums = [3,2,3]           ->  3", "nums = [2,2,1,1,1,2,2]  ->  2"],
        "constraints": ["1 <= len(nums) <= 5 * 10^4", "-10^9 <= nums[i] <= 10^9"],
        "hints": [
            "Counting occurrences in a dict is O(n) time and O(n) space.",
            "Can you do it in O(1) space? Think about cancelling out pairs of different elements.",
            "Boyer-Moore voting: keep a candidate and a count; count++ on a match, count-- otherwise, "
            "and replace the candidate when count hits 0.",
        ],
        "target": {"time": "O(n)", "space": "O(1)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[3, 2, 3]], "expect": 3},
            {"args": [[2, 2, 1, 1, 1, 2, 2]], "expect": 2},
            {"args": [[1]], "expect": 1},
            {"args": [[6, 5, 5]], "expect": 5},
            {"args": [[-1, -1, 2]], "expect": -1},
        ],
        "stress": {"args": lambda: [[7] * 150_001 + list(range(150_000))], "budget": 1.5},
        "pitfalls": ["nums.count(x) inside a loop is O(n^2)."],
        "solution": """
def majority_element(nums):
    candidate, count = None, 0
    for x in nums:
        if count == 0:
            candidate = x
        count += 1 if x == candidate else -1
    return candidate
""",
    },
    {
        "slug": "single-number",
        "title": "Single Number",
        "difficulty": "Easy",
        "topics": ["Array", "Bit Manipulation"],
        "url": "https://leetcode.com/problems/single-number/",
        "func": "single_number",
        "signature": "def single_number(nums: List[int]) -> int:",
        "description": (
            "Every element in `nums` appears exactly twice except for one, which appears once. "
            "Return that single one, using O(n) time and O(1) extra space."
        ),
        "examples": ["nums = [2,2,1]      ->  1", "nums = [4,1,2,1,2]  ->  4"],
        "constraints": ["1 <= len(nums) <= 3 * 10^4", "each element appears twice except one"],
        "hints": [
            "A set where you add/remove works but uses O(n) space.",
            "Which operation cancels a value against itself?",
            "XOR: x ^ x == 0 and x ^ 0 == x, so XOR-ing everything leaves the loner.",
        ],
        "target": {"time": "O(n)", "space": "O(1)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[2, 2, 1]], "expect": 1},
            {"args": [[4, 1, 2, 1, 2]], "expect": 4},
            {"args": [[1]], "expect": 1},
            {"args": [[0, 1, 0]], "expect": 1},
            {"args": [[-3, 5, 5]], "expect": -3},
        ],
        "stress": {
            "args": lambda: [[i for i in range(100_000)] + [i for i in range(100_000) if i != 42]],
            "budget": 1.5,
        },
        "pitfalls": ["The O(1) space constraint rules out the dict/set solutions."],
        "solution": """
def single_number(nums):
    result = 0
    for x in nums:
        result ^= x
    return result
""",
    },
    {
        "slug": "group-anagrams",
        "title": "Group Anagrams",
        "difficulty": "Medium",
        "topics": ["Array", "Hash Table", "String", "Sorting"],
        "url": "https://leetcode.com/problems/group-anagrams/",
        "func": "group_anagrams",
        "signature": "def group_anagrams(strs: List[str]) -> List[List[str]]:",
        "description": (
            "Group the strings that are anagrams of one another. Return the groups in any "
            "order, and the strings within each group in any order."
        ),
        "examples": [
            'strs = ["eat","tea","tan","ate","nat","bat"]  ->  [["bat"],["nat","tan"],["ate","eat","tea"]]',
            'strs = [""]   ->  [[""]]',
        ],
        "constraints": ["1 <= len(strs) <= 10^4", "0 <= len(strs[i]) <= 100", "lowercase letters only"],
        "hints": [
            "Anagrams need a canonical form — a key that is identical for every member of a group.",
            "Sorting the letters of a word gives such a key: 'eat' and 'tea' both become 'aet'.",
            "A 26-length count tuple is an O(len) key instead of O(len log len).",
        ],
        "target": {"time": "O(n * k)", "space": "O(n * k)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "sorted_inner",
        "tests": [
            {
                "args": [["eat", "tea", "tan", "ate", "nat", "bat"]],
                "expect": [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]],
            },
            {"args": [[""]], "expect": [[""]]},
            {"args": [["a"]], "expect": [["a"]]},
            {"args": [["abc", "cba", "bca", "xyz"]], "expect": [["abc", "cba", "bca"], ["xyz"]]},
            {"args": [["ddddddddddd", "dgpwvchdwn"]], "expect": [["ddddddddddd"], ["dgpwvchdwn"]]},
        ],
        "stress": {
            "args": lambda: [["abcdefghij"[i % 10 :] + "abcdefghij"[: i % 10] for i in range(20_000)]],
            "budget": 2.0,
        },
        "pitfalls": [
            "A list cannot be a dict key — use a tuple or a string.",
            "Comparing every pair of words is O(n^2) and times out.",
        ],
        "solution": """
def group_anagrams(strs):
    groups = {}
    for word in strs:
        key = tuple(sorted(word))
        groups.setdefault(key, []).append(word)
    return list(groups.values())
""",
    },
    {
        "slug": "top-k-frequent-elements",
        "title": "Top K Frequent Elements",
        "difficulty": "Medium",
        "topics": ["Array", "Hash Table", "Heap", "Bucket Sort"],
        "url": "https://leetcode.com/problems/top-k-frequent-elements/",
        "func": "top_k_frequent",
        "signature": "def top_k_frequent(nums: List[int], k: int) -> List[int]:",
        "description": (
            "Return the `k` most frequent elements of `nums`. The answer is guaranteed to be "
            "unique, and you may return it in any order."
        ),
        "examples": ["nums = [1,1,1,2,2,3], k = 2  ->  [1,2]", "nums = [1], k = 1  ->  [1]"],
        "constraints": [
            "1 <= len(nums) <= 10^5",
            "k is in the range [1, number of distinct elements]",
        ],
        "hints": [
            "Start by counting frequencies into a dict.",
            "Sorting the counts is O(n log n); a heap of size k is O(n log k).",
            "Frequencies are bounded by len(nums), so you can bucket by count and read buckets "
            "from the top for O(n).",
        ],
        "target": {"time": "O(n)", "space": "O(n)"},
        "argspec": ["raw", "raw"],
        "retspec": "raw",
        "compare": "sorted",
        "tests": [
            {"args": [[1, 1, 1, 2, 2, 3], 2], "expect": [1, 2]},
            {"args": [[1], 1], "expect": [1]},
            {"args": [[4, 4, 4, 5, 5, 6], 3], "expect": [4, 5, 6]},
            {"args": [[-1, -1, 3], 1], "expect": [-1]},
            {"args": [[5, 5, 6, 6, 7], 2], "expect": [5, 6]},
        ],
        "stress": {
            "args": lambda: [[i % 5_000 for i in range(200_000)], 10],
            "budget": 2.0,
        },
        "pitfalls": ["Ties are excluded by the problem guarantee — don't over-engineer them."],
        "solution": """
def top_k_frequent(nums, k):
    counts = {}
    for x in nums:
        counts[x] = counts.get(x, 0) + 1
    buckets = [[] for _ in range(len(nums) + 1)]
    for value, freq in counts.items():
        buckets[freq].append(value)
    out = []
    for freq in range(len(buckets) - 1, 0, -1):
        for value in buckets[freq]:
            out.append(value)
            if len(out) == k:
                return out
    return out
""",
    },
    {
        "slug": "product-of-array-except-self",
        "title": "Product of Array Except Self",
        "difficulty": "Medium",
        "topics": ["Array", "Prefix Sum"],
        "url": "https://leetcode.com/problems/product-of-array-except-self/",
        "func": "product_except_self",
        "signature": "def product_except_self(nums: List[int]) -> List[int]:",
        "description": (
            "Return an array `out` where `out[i]` is the product of every element of `nums` "
            "except `nums[i]`. Solve it without using division and in O(n) time."
        ),
        "examples": [
            "nums = [1,2,3,4]     ->  [24,12,8,6]",
            "nums = [-1,1,0,-3,3] ->  [0,0,9,0,0]",
        ],
        "constraints": ["2 <= len(nums) <= 10^5", "the product of any prefix or suffix fits in 32 bits"],
        "hints": [
            "out[i] = (product of everything left of i) * (product of everything right of i).",
            "Build the prefix products in one forward pass.",
            "Then walk backwards with a running suffix product and multiply it in — O(1) extra space.",
        ],
        "target": {"time": "O(n)", "space": "O(1) extra (output not counted)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[1, 2, 3, 4]], "expect": [24, 12, 8, 6]},
            {"args": [[-1, 1, 0, -3, 3]], "expect": [0, 0, 9, 0, 0]},
            {"args": [[2, 3]], "expect": [3, 2]},
            {"args": [[0, 0]], "expect": [0, 0]},
            {"args": [[1, 0, 3]], "expect": [0, 3, 0]},
            {"args": [[-1, -2, -3]], "expect": [6, 3, 2]},
        ],
        "stress": {"args": lambda: [[1] * 200_000], "budget": 1.5},
        "pitfalls": [
            "Division breaks on zeros (and is disallowed).",
            "Two zeros means every entry is 0 — a division-based special case has to handle that.",
        ],
        "solution": """
def product_except_self(nums):
    n = len(nums)
    out = [1] * n
    prefix = 1
    for i in range(n):
        out[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):
        out[i] *= suffix
        suffix *= nums[i]
    return out
""",
    },
    {
        "slug": "longest-consecutive-sequence",
        "title": "Longest Consecutive Sequence",
        "difficulty": "Medium",
        "topics": ["Array", "Hash Table", "Union Find"],
        "url": "https://leetcode.com/problems/longest-consecutive-sequence/",
        "func": "longest_consecutive",
        "signature": "def longest_consecutive(nums: List[int]) -> int:",
        "description": (
            "Return the length of the longest run of consecutive integers present in `nums` "
            "(the numbers need not be adjacent in the array). Aim for O(n) time."
        ),
        "examples": [
            "nums = [100,4,200,1,3,2]        ->  4   (1,2,3,4)",
            "nums = [0,3,7,2,5,8,4,6,0,1]    ->  9",
        ],
        "constraints": ["0 <= len(nums) <= 10^5", "-10^9 <= nums[i] <= 10^9"],
        "hints": [
            "Sorting gives O(n log n) — the O(n) solution needs a set.",
            "Only start counting a run at its smallest element.",
            "x starts a run when x - 1 is not in the set; then walk x+1, x+2, ... Each element is "
            "visited at most twice overall.",
        ],
        "target": {"time": "O(n)", "space": "O(n)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[100, 4, 200, 1, 3, 2]], "expect": 4},
            {"args": [[0, 3, 7, 2, 5, 8, 4, 6, 0, 1]], "expect": 9},
            {"args": [[]], "expect": 0},
            {"args": [[1, 2, 0, 1]], "expect": 3},
            {"args": [[-1, 1, 0]], "expect": 3},
            {"args": [[5]], "expect": 1},
        ],
        "stress": {
            "args": lambda: [random.Random(7).sample(range(400_000), 150_000)],
            "budget": 2.0,
        },
        "pitfalls": [
            "Duplicates must not extend a run.",
            "Walking outward from every element without the 'is x-1 present?' guard is O(n^2).",
        ],
        "solution": """
def longest_consecutive(nums):
    pool = set(nums)
    best = 0
    for x in pool:
        if x - 1 in pool:
            continue
        length = 1
        while x + length in pool:
            length += 1
        best = max(best, length)
    return best
""",
    },
    {
        "slug": "subarray-sum-equals-k",
        "title": "Subarray Sum Equals K",
        "difficulty": "Medium",
        "topics": ["Array", "Hash Table", "Prefix Sum"],
        "url": "https://leetcode.com/problems/subarray-sum-equals-k/",
        "func": "subarray_sum",
        "signature": "def subarray_sum(nums: List[int], k: int) -> int:",
        "description": (
            "Return the total number of contiguous subarrays whose elements sum to `k`. "
            "Values may be negative."
        ),
        "examples": ["nums = [1,1,1], k = 2  ->  2", "nums = [1,2,3], k = 3  ->  2"],
        "constraints": ["1 <= len(nums) <= 2 * 10^4", "-1000 <= nums[i] <= 1000", "-10^7 <= k <= 10^7"],
        "hints": [
            "sum(i..j) == prefix[j] - prefix[i-1]. Rewrite the condition in terms of prefixes.",
            "You need the count of earlier prefixes equal to prefix - k.",
            "Keep a dict of prefix-sum counts seeded with {0: 1}.",
        ],
        "target": {"time": "O(n)", "space": "O(n)"},
        "argspec": ["raw", "raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[1, 1, 1], 2], "expect": 2},
            {"args": [[1, 2, 3], 3], "expect": 2},
            {"args": [[1], 0], "expect": 0},
            {"args": [[-1, -1, 1], 0], "expect": 1},
            {"args": [[0, 0, 0], 0], "expect": 6},
            {"args": [[3, 4, 7, 2, -3, 1, 4, 2], 7], "expect": 4},
        ],
        "stress": {
            "args": lambda: [[1] * 20_000, 100],
            "budget": 1.5,
        },
        "pitfalls": [
            "Negative numbers break the sliding-window approach — the window is not monotonic.",
            "Forgetting the {0: 1} seed loses every subarray that starts at index 0.",
        ],
        "solution": """
def subarray_sum(nums, k):
    counts = {0: 1}
    total = 0
    prefix = 0
    for x in nums:
        prefix += x
        total += counts.get(prefix - k, 0)
        counts[prefix] = counts.get(prefix, 0) + 1
    return total
""",
    },
]
