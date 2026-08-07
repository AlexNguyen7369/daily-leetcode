"""1-D and 2-D dynamic programming."""

import random

PROBLEMS = [
    {
        "slug": "climbing-stairs",
        "title": "Climbing Stairs",
        "difficulty": "Easy",
        "topics": ["Math", "Dynamic Programming", "Memoization"],
        "url": "https://leetcode.com/problems/climbing-stairs/",
        "func": "climb_stairs",
        "signature": "def climb_stairs(n: int) -> int:",
        "description": (
            "You are climbing a staircase of `n` steps and can take either 1 or 2 steps at a time. "
            "Return how many distinct ways you can reach the top."
        ),
        "examples": ["n = 2  ->  2   (1+1, 2)", "n = 3  ->  3   (1+1+1, 1+2, 2+1)"],
        "constraints": ["1 <= n <= 45"],
        "hints": [
            "The last move onto step n came from either step n-1 or step n-2.",
            "So ways(n) = ways(n-1) + ways(n-2) — this is Fibonacci.",
            "Iterate with two rolling variables instead of recursing; plain recursion is O(2^n).",
        ],
        "target": {"time": "O(n)", "space": "O(1)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [1], "expect": 1},
            {"args": [2], "expect": 2},
            {"args": [3], "expect": 3},
            {"args": [5], "expect": 8},
            {"args": [10], "expect": 89},
            {"args": [45], "expect": 1836311903},
        ],
        "stress": {"args": lambda: [45], "budget": 1.0},
        "pitfalls": ["Un-memoised recursion at n=45 takes minutes — the checker will flag the runtime."],
        "solution": """
def climb_stairs(n):
    prev, current = 1, 1
    for _ in range(n - 1):
        prev, current = current, prev + current
    return current
""",
    },
    {
        "slug": "min-cost-climbing-stairs",
        "title": "Min Cost Climbing Stairs",
        "difficulty": "Easy",
        "topics": ["Array", "Dynamic Programming"],
        "url": "https://leetcode.com/problems/min-cost-climbing-stairs/",
        "func": "min_cost_climbing_stairs",
        "signature": "def min_cost_climbing_stairs(cost: List[int]) -> int:",
        "description": (
            "`cost[i]` is what you pay to step off stair i, after which you may climb 1 or 2 "
            "stairs. You may start at index 0 or index 1. Return the cheapest way to reach the "
            "top (one past the last index)."
        ),
        "examples": [
            "cost = [10,15,20]                      ->  15",
            "cost = [1,100,1,1,1,100,1,1,100,1]     ->  6",
        ],
        "constraints": ["2 <= len(cost) <= 1000", "0 <= cost[i] <= 999"],
        "hints": [
            "Define dp[i] as the cheapest cost to *reach* stair i (before paying for it).",
            "dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2]).",
            "dp[0] = dp[1] = 0, and the answer is dp[len(cost)]. Two rolling variables suffice.",
        ],
        "target": {"time": "O(n)", "space": "O(1)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[10, 15, 20]], "expect": 15},
            {"args": [[1, 100, 1, 1, 1, 100, 1, 1, 100, 1]], "expect": 6},
            {"args": [[0, 0]], "expect": 0},
            {"args": [[5, 5]], "expect": 5},
            {"args": [[1, 2, 3]], "expect": 2},
        ],
        "stress": {
            "args": lambda: [random.Random(21).choices(range(1000), k=1000)],
            "budget": 1.0,
        },
        "pitfalls": ["The top is past the end of the array — you never pay for a stair you don't step off."],
        "solution": """
def min_cost_climbing_stairs(cost):
    a, b = 0, 0
    for i in range(2, len(cost) + 1):
        a, b = b, min(b + cost[i - 1], a + cost[i - 2])
    return b
""",
    },
    {
        "slug": "house-robber",
        "title": "House Robber",
        "difficulty": "Medium",
        "topics": ["Array", "Dynamic Programming"],
        "url": "https://leetcode.com/problems/house-robber/",
        "func": "rob",
        "signature": "def rob(nums: List[int]) -> int:",
        "description": (
            "Each house holds `nums[i]` money, but robbing two adjacent houses triggers the alarm. "
            "Return the maximum you can steal."
        ),
        "examples": ["nums = [1,2,3,1]    ->  4   (houses 0 and 2)", "nums = [2,7,9,3,1]  ->  12"],
        "constraints": ["1 <= len(nums) <= 100", "0 <= nums[i] <= 400"],
        "hints": [
            "At each house you either take it (plus the best up to i-2) or skip it.",
            "dp[i] = max(dp[i-1], dp[i-2] + nums[i]).",
            "Only the last two values matter, so keep two variables.",
        ],
        "target": {"time": "O(n)", "space": "O(1)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[1, 2, 3, 1]], "expect": 4},
            {"args": [[2, 7, 9, 3, 1]], "expect": 12},
            {"args": [[5]], "expect": 5},
            {"args": [[2, 1, 1, 2]], "expect": 4},
            {"args": [[0, 0, 0]], "expect": 0},
        ],
        "stress": {
            "args": lambda: [random.Random(31).choices(range(400), k=100_000)],
            "budget": 1.5,
        },
        "pitfalls": [
            "Alternating even/odd indices is not optimal — [2,1,1,2] proves it.",
            "Greedy on the largest value first fails too.",
        ],
        "solution": """
def rob(nums):
    skip, take = 0, 0
    for x in nums:
        skip, take = max(skip, take), skip + x
    return max(skip, take)
""",
    },
    {
        "slug": "maximum-subarray",
        "title": "Maximum Subarray",
        "difficulty": "Medium",
        "topics": ["Array", "Divide and Conquer", "Dynamic Programming"],
        "url": "https://leetcode.com/problems/maximum-subarray/",
        "func": "max_sub_array",
        "signature": "def max_sub_array(nums: List[int]) -> int:",
        "description": "Return the largest sum of any contiguous non-empty subarray of `nums`.",
        "examples": [
            "nums = [-2,1,-3,4,-1,2,1,-5,4]  ->  6   ([4,-1,2,1])",
            "nums = [1]     ->  1",
            "nums = [5,4,-1,7,8]  ->  23",
        ],
        "constraints": ["1 <= len(nums) <= 10^5", "-10^4 <= nums[i] <= 10^4"],
        "hints": [
            "Scan left to right keeping the best sum of a subarray that ends at the current index.",
            "If the running sum turns negative it can only hurt what comes next.",
            "Kadane: current = max(x, current + x); best = max(best, current).",
        ],
        "target": {"time": "O(n)", "space": "O(1)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[-2, 1, -3, 4, -1, 2, 1, -5, 4]], "expect": 6},
            {"args": [[1]], "expect": 1},
            {"args": [[5, 4, -1, 7, 8]], "expect": 23},
            {"args": [[-1]], "expect": -1},
            {"args": [[-2, -1, -3]], "expect": -1},
            {"args": [[0, -1]], "expect": 0},
        ],
        "stress": {
            "args": lambda: [random.Random(41).choices(range(-10_000, 10_000), k=200_000)],
            "budget": 1.5,
        },
        "pitfalls": [
            "The subarray must be non-empty, so an all-negative array answers with its largest element.",
            "Initialising best to 0 is the classic bug.",
        ],
        "solution": """
def max_sub_array(nums):
    best = current = nums[0]
    for x in nums[1:]:
        current = max(x, current + x)
        best = max(best, current)
    return best
""",
    },
    {
        "slug": "coin-change",
        "title": "Coin Change",
        "difficulty": "Medium",
        "topics": ["Array", "Dynamic Programming", "BFS"],
        "url": "https://leetcode.com/problems/coin-change/",
        "func": "coin_change",
        "signature": "def coin_change(coins: List[int], amount: int) -> int:",
        "description": (
            "You have an unlimited supply of each coin denomination. Return the fewest coins that "
            "sum to `amount`, or -1 if it cannot be made."
        ),
        "examples": [
            "coins = [1,2,5], amount = 11  ->  3   (5+5+1)",
            "coins = [2], amount = 3       ->  -1",
            "coins = [1], amount = 0       ->  0",
        ],
        "constraints": ["1 <= len(coins) <= 12", "1 <= coins[i] <= 2^31 - 1", "0 <= amount <= 10^4"],
        "hints": [
            "Greedy (always take the biggest coin) fails — try coins [1,3,4] and amount 6.",
            "dp[a] = fewest coins to make amount a; dp[0] = 0.",
            "dp[a] = 1 + min(dp[a - c]) over coins c <= a. Use infinity for unreachable amounts.",
        ],
        "target": {"time": "O(amount * len(coins))", "space": "O(amount)"},
        "argspec": ["raw", "raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[1, 2, 5], 11], "expect": 3},
            {"args": [[2], 3], "expect": -1},
            {"args": [[1], 0], "expect": 0},
            {"args": [[1, 3, 4], 6], "expect": 2},
            {"args": [[2, 5, 10, 1], 27], "expect": 4},
            {"args": [[186, 419, 83, 408], 6249], "expect": 20},
        ],
        "stress": {"args": lambda: [[1, 5, 6, 9], 10_000], "budget": 2.5},
        "pitfalls": [
            "amount = 0 answers 0, not -1.",
            "Return -1 when dp[amount] is still infinity.",
        ],
        "solution": """
def coin_change(coins, amount):
    INF = float('inf')
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return -1 if dp[amount] == INF else dp[amount]
""",
    },
    {
        "slug": "longest-increasing-subsequence",
        "title": "Longest Increasing Subsequence",
        "difficulty": "Medium",
        "topics": ["Array", "Binary Search", "Dynamic Programming"],
        "url": "https://leetcode.com/problems/longest-increasing-subsequence/",
        "func": "length_of_lis",
        "signature": "def length_of_lis(nums: List[int]) -> int:",
        "description": (
            "Return the length of the longest strictly increasing subsequence of `nums`. "
            "A subsequence keeps order but need not be contiguous."
        ),
        "examples": [
            "nums = [10,9,2,5,3,7,101,18]  ->  4   ([2,3,7,101])",
            "nums = [0,1,0,3,2,3]          ->  4",
            "nums = [7,7,7,7]              ->  1",
        ],
        "constraints": ["1 <= len(nums) <= 2500", "-10^4 <= nums[i] <= 10^4"],
        "hints": [
            "O(n^2): dp[i] = 1 + max(dp[j]) over j < i with nums[j] < nums[i].",
            "For O(n log n), keep `tails` where tails[k] is the smallest possible tail of an "
            "increasing subsequence of length k+1.",
            "For each x, binary search for the first tail >= x and overwrite it (bisect_left); "
            "append if there is none. len(tails) is the answer.",
        ],
        "target": {"time": "O(n log n)", "space": "O(n)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[10, 9, 2, 5, 3, 7, 101, 18]], "expect": 4},
            {"args": [[0, 1, 0, 3, 2, 3]], "expect": 4},
            {"args": [[7, 7, 7, 7]], "expect": 1},
            {"args": [[1]], "expect": 1},
            {"args": [[4, 10, 4, 3, 8, 9]], "expect": 3},
            {"args": [[3, 2, 1]], "expect": 1},
        ],
        "stress": {
            "args": lambda: [random.Random(51).sample(range(100_000), 20_000)],
            "budget": 2.5,
        },
        "pitfalls": [
            "Strictly increasing — equal values do not extend a subsequence (use bisect_left, not bisect_right).",
            "`tails` is not itself a valid subsequence; only its length is meaningful.",
        ],
        "solution": """
def length_of_lis(nums):
    import bisect
    tails = []
    for x in nums:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)
""",
    },
    {
        "slug": "unique-paths",
        "title": "Unique Paths",
        "difficulty": "Medium",
        "topics": ["Math", "Dynamic Programming", "Combinatorics"],
        "url": "https://leetcode.com/problems/unique-paths/",
        "func": "unique_paths",
        "signature": "def unique_paths(m: int, n: int) -> int:",
        "description": (
            "A robot starts at the top-left of an m x n grid and may only move right or down. "
            "Return how many distinct paths reach the bottom-right corner."
        ),
        "examples": ["m = 3, n = 7  ->  28", "m = 3, n = 2  ->  3", "m = 1, n = 1  ->  1"],
        "constraints": ["1 <= m, n <= 100"],
        "hints": [
            "Every cell is reached from the one above it or the one to its left.",
            "dp[i][j] = dp[i-1][j] + dp[i][j-1], with the first row and column all 1s.",
            "One row of the table is enough: row[j] += row[j-1] sweeping left to right.",
        ],
        "target": {"time": "O(m*n)", "space": "O(n)"},
        "argspec": ["raw", "raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [3, 7], "expect": 28},
            {"args": [3, 2], "expect": 3},
            {"args": [1, 1], "expect": 1},
            {"args": [7, 3], "expect": 28},
            {"args": [10, 10], "expect": 48620},
            {"args": [1, 100], "expect": 1},
        ],
        "stress": {"args": lambda: [100, 100], "budget": 1.0},
        "pitfalls": ["Plain recursion without memoisation blows up exponentially."],
        "solution": """
def unique_paths(m, n):
    row = [1] * n
    for _ in range(m - 1):
        for j in range(1, n):
            row[j] += row[j - 1]
    return row[-1]
""",
    },
    {
        "slug": "longest-palindromic-substring",
        "title": "Longest Palindromic Substring",
        "difficulty": "Medium",
        "topics": ["String", "Dynamic Programming", "Two Pointers"],
        "url": "https://leetcode.com/problems/longest-palindromic-substring/",
        "func": "longest_palindrome",
        "signature": "def longest_palindrome(s: str) -> str:",
        "description": (
            "Return the longest palindromic substring of `s`. If several have the same maximum "
            "length, any one of them is accepted."
        ),
        "examples": ['s = "babad"  ->  "bab"  (or "aba")', 's = "cbbd"   ->  "bb"'],
        "constraints": ["1 <= len(s) <= 1000", "s consists of digits and English letters"],
        "hints": [
            "Every palindrome has a centre — there are 2n-1 of them (each character and each gap).",
            "From each centre, expand outward while the characters match.",
            "Keep the longest span you find. That is O(n^2) time and O(1) space.",
        ],
        "target": {"time": "O(n^2)", "space": "O(1)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "any_of",
        "tests": [
            {"args": ["babad"], "expect": ["bab", "aba"]},
            {"args": ["cbbd"], "expect": ["bb"]},
            {"args": ["a"], "expect": ["a"]},
            {"args": ["ac"], "expect": ["a", "c"]},
            {"args": ["forgeeksskeegfor"], "expect": ["geeksskeeg"]},
            {"args": ["abb"], "expect": ["bb"]},
        ],
        "stress": {
            "args": lambda: ["".join(random.Random(61).choices("ab", k=1000))],
            "budget": 2.5,
        },
        "pitfalls": [
            "Even-length palindromes need the gap centres too — 'cbbd' fails without them.",
            "Checking every substring for palindromicity is O(n^3).",
        ],
        "solution": """
def longest_palindrome(s):
    best_start, best_len = 0, 1

    def expand(left, right):
        nonlocal best_start, best_len
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        if right - left - 1 > best_len:
            best_len = right - left - 1
            best_start = left + 1

    for i in range(len(s)):
        expand(i, i)
        expand(i, i + 1)
    return s[best_start:best_start + best_len]
""",
    },
    {
        "slug": "word-break",
        "title": "Word Break",
        "difficulty": "Medium",
        "topics": ["Hash Table", "String", "Dynamic Programming", "Trie"],
        "url": "https://leetcode.com/problems/word-break/",
        "func": "word_break",
        "signature": "def word_break(s: str, word_dict: List[str]) -> bool:",
        "description": (
            "Return True if `s` can be segmented into a sequence of one or more dictionary words. "
            "Words may be reused any number of times."
        ),
        "examples": [
            's = "leetcode", wordDict = ["leet","code"]                 ->  True',
            's = "applepenapple", wordDict = ["apple","pen"]            ->  True',
            's = "catsandog", wordDict = ["cats","dog","sand","and","cat"]  ->  False',
        ],
        "constraints": ["1 <= len(s) <= 300", "1 <= len(wordDict) <= 1000", "all words are unique"],
        "hints": [
            "dp[i] means 'the first i characters can be segmented'. dp[0] = True.",
            "dp[i] is True if some word ends at i and dp[i - len(word)] is True.",
            "Put the dictionary in a set for O(1) lookups; greedy longest-match-first is wrong.",
        ],
        "target": {"time": "O(n^2 * k)", "space": "O(n)"},
        "argspec": ["raw", "raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": ["leetcode", ["leet", "code"]], "expect": True},
            {"args": ["applepenapple", ["apple", "pen"]], "expect": True},
            {"args": ["catsandog", ["cats", "dog", "sand", "and", "cat"]], "expect": False},
            {"args": ["a", ["a"]], "expect": True},
            {"args": ["ab", ["a"]], "expect": False},
            {"args": ["cars", ["car", "ca", "rs"]], "expect": True},
        ],
        "stress": {
            "args": lambda: ["a" * 300, ["a" * k for k in range(1, 21)]],
            "budget": 2.0,
        },
        "pitfalls": [
            "Plain recursion without memoisation is exponential on inputs like 'aaaa...ab'.",
            "'cars' with ['car','ca','rs'] breaks greedy matching.",
        ],
        "solution": """
def word_break(s, word_dict):
    words = set(word_dict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break
    return dp[n]
""",
    },
]
