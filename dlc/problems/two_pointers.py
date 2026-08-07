"""Two pointers and sliding windows."""

import random

PROBLEMS = [
    {
        "slug": "valid-palindrome",
        "title": "Valid Palindrome",
        "difficulty": "Easy",
        "topics": ["Two Pointers", "String"],
        "url": "https://leetcode.com/problems/valid-palindrome/",
        "func": "is_palindrome",
        "signature": "def is_palindrome(s: str) -> bool:",
        "description": (
            "A phrase is a palindrome if, after lowercasing and removing every character that "
            "is not a letter or digit, it reads the same forwards and backwards. Return whether "
            "`s` is a palindrome."
        ),
        "examples": [
            's = "A man, a plan, a canal: Panama"  ->  True',
            's = "race a car"  ->  False',
            's = " "           ->  True   (empty after filtering)',
        ],
        "constraints": ["1 <= len(s) <= 2 * 10^5", "s consists of printable ASCII"],
        "hints": [
            "str.isalnum() and str.lower() do the filtering for you.",
            "Building the cleaned string and comparing it to its reverse is O(n) time, O(n) space.",
            "Two pointers from both ends, each skipping non-alphanumerics, gets you O(1) space.",
        ],
        "target": {"time": "O(n)", "space": "O(1)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": ["A man, a plan, a canal: Panama"], "expect": True},
            {"args": ["race a car"], "expect": False},
            {"args": [" "], "expect": True},
            {"args": ["0P"], "expect": False},
            {"args": ["ab_a"], "expect": True},
            {"args": ["a."], "expect": True},
        ],
        "stress": {"args": lambda: ["ab,cd " * 40_000 + "dc,ba" * 40_000], "budget": 1.5},
        "pitfalls": [
            "'0P' is not a palindrome — compare after lowercasing, not by ASCII value.",
            "Underscore is not alphanumeric.",
        ],
        "solution": """
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True
""",
    },
    {
        "slug": "best-time-to-buy-and-sell-stock",
        "title": "Best Time to Buy and Sell Stock",
        "difficulty": "Easy",
        "topics": ["Array", "Dynamic Programming", "Sliding Window"],
        "url": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/",
        "func": "max_profit",
        "signature": "def max_profit(prices: List[int]) -> int:",
        "description": (
            "`prices[i]` is the price of a stock on day i. Choose one day to buy and a later day "
            "to sell to maximise profit. Return the maximum profit, or 0 if no profit is possible."
        ),
        "examples": [
            "prices = [7,1,5,3,6,4]  ->  5   (buy at 1, sell at 6)",
            "prices = [7,6,4,3,1]    ->  0",
        ],
        "constraints": ["1 <= len(prices) <= 10^5", "0 <= prices[i] <= 10^4"],
        "hints": [
            "For each selling day you only care about the cheapest price before it.",
            "Track the running minimum while you scan.",
            "profit = max(profit, price - min_so_far), then update min_so_far.",
        ],
        "target": {"time": "O(n)", "space": "O(1)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[7, 1, 5, 3, 6, 4]], "expect": 5},
            {"args": [[7, 6, 4, 3, 1]], "expect": 0},
            {"args": [[1]], "expect": 0},
            {"args": [[2, 4, 1]], "expect": 2},
            {"args": [[3, 3]], "expect": 0},
        ],
        "stress": {
            "args": lambda: [random.Random(11).choices(range(10_000), k=200_000)],
            "budget": 1.5,
        },
        "pitfalls": [
            "You must buy before you sell — max(prices) - min(prices) is wrong if the min comes last.",
            "Never return a negative profit.",
        ],
        "solution": """
def max_profit(prices):
    cheapest = float('inf')
    best = 0
    for price in prices:
        if price < cheapest:
            cheapest = price
        elif price - cheapest > best:
            best = price - cheapest
    return best
""",
    },
    {
        "slug": "move-zeroes",
        "title": "Move Zeroes",
        "difficulty": "Easy",
        "topics": ["Array", "Two Pointers"],
        "url": "https://leetcode.com/problems/move-zeroes/",
        "func": "move_zeroes",
        "signature": "def move_zeroes(nums: List[int]) -> None:",
        "description": (
            "Move every 0 in `nums` to the end while keeping the relative order of the non-zero "
            "elements. Modify the list in place and return nothing."
        ),
        "examples": ["nums = [0,1,0,3,12]  ->  [1,3,12,0,0]", "nums = [0]  ->  [0]"],
        "constraints": ["1 <= len(nums) <= 10^4", "minimise the number of writes"],
        "hints": [
            "Keep a write pointer for the next slot a non-zero value belongs in.",
            "First pass: copy every non-zero forward. Second: fill the tail with zeros.",
            "Or swap nums[read] and nums[write] whenever nums[read] is non-zero — one pass.",
        ],
        "target": {"time": "O(n)", "space": "O(1)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "inplace",
        "tests": [
            {"args": [[0, 1, 0, 3, 12]], "expect": [1, 3, 12, 0, 0]},
            {"args": [[0]], "expect": [0]},
            {"args": [[1, 2, 3]], "expect": [1, 2, 3]},
            {"args": [[0, 0, 1]], "expect": [1, 0, 0]},
            {"args": [[4, 0, 0, 5, 0]], "expect": [4, 5, 0, 0, 0]},
        ],
        "stress": {
            "args": lambda: [[0 if i % 3 else i for i in range(200_000)]],
            "budget": 1.5,
        },
        "pitfalls": [
            "`nums = [...]` rebinds the local name and does not modify the caller's list — "
            "use nums[:] = ... or per-index assignment.",
            "list.remove(0) inside a loop is O(n^2) and skips elements.",
        ],
        "solution": """
def move_zeroes(nums):
    write = 0
    for read in range(len(nums)):
        if nums[read] != 0:
            nums[write], nums[read] = nums[read], nums[write]
            write += 1
""",
    },
    {
        "slug": "two-sum-ii-input-array-is-sorted",
        "title": "Two Sum II - Input Array Is Sorted",
        "difficulty": "Medium",
        "topics": ["Array", "Two Pointers", "Binary Search"],
        "url": "https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/",
        "func": "two_sum_sorted",
        "signature": "def two_sum_sorted(numbers: List[int], target: int) -> List[int]:",
        "description": (
            "`numbers` is sorted in non-decreasing order. Find the two numbers that add up to "
            "`target` and return their **1-indexed** positions as [i, j] with i < j. "
            "Exactly one solution exists and you must use O(1) extra space."
        ),
        "examples": [
            "numbers = [2,7,11,15], target = 9   ->  [1,2]",
            "numbers = [2,3,4],     target = 6   ->  [1,3]",
            "numbers = [-1,0],      target = -1  ->  [1,2]",
        ],
        "constraints": ["2 <= len(numbers) <= 3 * 10^4", "numbers is sorted ascending"],
        "hints": [
            "The hash map trick is banned by the O(1) space rule — use the sortedness.",
            "Point at both ends. The sum can only be too big or too small.",
            "Too big -> move the right pointer left; too small -> move the left pointer right.",
        ],
        "target": {"time": "O(n)", "space": "O(1)"},
        "argspec": ["raw", "raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[2, 7, 11, 15], 9], "expect": [1, 2]},
            {"args": [[2, 3, 4], 6], "expect": [1, 3]},
            {"args": [[-1, 0], -1], "expect": [1, 2]},
            {"args": [[1, 2, 3, 4, 4, 9, 56, 90], 8], "expect": [4, 5]},
            {"args": [[0, 0, 3, 4], 0], "expect": [1, 2]},
        ],
        "stress": {"args": lambda: [list(range(0, 60_000, 2)), 59_994], "budget": 1.5},
        "pitfalls": ["The answer is 1-indexed, not 0-indexed."],
        "solution": """
def two_sum_sorted(numbers, target):
    left, right = 0, len(numbers) - 1
    while left < right:
        total = numbers[left] + numbers[right]
        if total == target:
            return [left + 1, right + 1]
        if total < target:
            left += 1
        else:
            right -= 1
    return []
""",
    },
    {
        "slug": "3sum",
        "title": "3Sum",
        "difficulty": "Medium",
        "topics": ["Array", "Two Pointers", "Sorting"],
        "url": "https://leetcode.com/problems/3sum/",
        "func": "three_sum",
        "signature": "def three_sum(nums: List[int]) -> List[List[int]]:",
        "description": (
            "Return all unique triplets [nums[i], nums[j], nums[k]] with distinct indices that "
            "sum to zero. The solution set must not contain duplicate triplets; order does not matter."
        ),
        "examples": [
            "nums = [-1,0,1,2,-1,-4]  ->  [[-1,-1,2],[-1,0,1]]",
            "nums = [0,1,1]           ->  []",
            "nums = [0,0,0]           ->  [[0,0,0]]",
        ],
        "constraints": ["3 <= len(nums) <= 3000", "-10^5 <= nums[i] <= 10^5"],
        "hints": [
            "Sort first — it makes duplicates adjacent and enables two pointers.",
            "Fix the first element, then solve two-sum on the remaining sorted suffix.",
            "Skip an outer value equal to the previous one, and after recording a hit skip equal "
            "values from both pointers.",
        ],
        "target": {"time": "O(n^2)", "space": "O(1) extra"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "sorted_inner",
        "tests": [
            {"args": [[-1, 0, 1, 2, -1, -4]], "expect": [[-1, -1, 2], [-1, 0, 1]]},
            {"args": [[0, 1, 1]], "expect": []},
            {"args": [[0, 0, 0]], "expect": [[0, 0, 0]]},
            {"args": [[-2, 0, 1, 1, 2]], "expect": [[-2, 0, 2], [-2, 1, 1]]},
            {"args": [[0, 0, 0, 0]], "expect": [[0, 0, 0]]},
            {"args": [[-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6]],
             "expect": [[-4, -2, 6], [-4, 0, 4], [-4, 1, 3], [-4, 2, 2], [-2, -2, 4],
                        [-2, 0, 2]]},
        ],
        "stress": {
            "args": lambda: [random.Random(3).choices(range(-200, 200), k=1200)],
            "budget": 3.0,
        },
        "pitfalls": [
            "Deduplicating with a set of tuples works but is slower — skipping equal values is the point.",
            "Once nums[i] > 0 in the sorted array no triplet can sum to zero; you can break early.",
        ],
        "solution": """
def three_sum(nums):
    nums = sorted(nums)
    n = len(nums)
    out = []
    for i in range(n - 2):
        if nums[i] > 0:
            break
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        left, right = i + 1, n - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                out.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1
    return out
""",
    },
    {
        "slug": "container-with-most-water",
        "title": "Container With Most Water",
        "difficulty": "Medium",
        "topics": ["Array", "Two Pointers", "Greedy"],
        "url": "https://leetcode.com/problems/container-with-most-water/",
        "func": "max_area",
        "signature": "def max_area(height: List[int]) -> int:",
        "description": (
            "Each `height[i]` is a vertical line at x = i. Pick two lines that together with the "
            "x-axis hold the most water and return that area: min(h[i], h[j]) * (j - i)."
        ),
        "examples": [
            "height = [1,8,6,2,5,4,8,3,7]  ->  49",
            "height = [1,1]                ->  1",
        ],
        "constraints": ["2 <= len(height) <= 10^5", "0 <= height[i] <= 10^4"],
        "hints": [
            "Start with the widest possible container: both ends.",
            "Narrowing always loses width, so it only pays off if the height can grow.",
            "The shorter line caps the area, so move that pointer inward — the taller one can "
            "never be improved by keeping the shorter one.",
        ],
        "target": {"time": "O(n)", "space": "O(1)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[1, 8, 6, 2, 5, 4, 8, 3, 7]], "expect": 49},
            {"args": [[1, 1]], "expect": 1},
            {"args": [[4, 3, 2, 1, 4]], "expect": 16},
            {"args": [[1, 2, 1]], "expect": 2},
            {"args": [[0, 0]], "expect": 0},
        ],
        "stress": {
            "args": lambda: [random.Random(5).choices(range(10_000), k=200_000)],
            "budget": 1.5,
        },
        "pitfalls": ["The lines have no width and water is not blocked by lines in between."],
        "solution": """
def max_area(height):
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        best = max(best, min(height[left], height[right]) * (right - left))
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return best
""",
    },
    {
        "slug": "longest-substring-without-repeating-characters",
        "title": "Longest Substring Without Repeating Characters",
        "difficulty": "Medium",
        "topics": ["Hash Table", "String", "Sliding Window"],
        "url": "https://leetcode.com/problems/longest-substring-without-repeating-characters/",
        "func": "length_of_longest_substring",
        "signature": "def length_of_longest_substring(s: str) -> int:",
        "description": (
            "Return the length of the longest substring of `s` that contains no repeated character. "
            "A substring is contiguous."
        ),
        "examples": [
            's = "abcabcbb"  ->  3   ("abc")',
            's = "bbbbb"     ->  1',
            's = "pwwkew"    ->  3   ("wke")',
        ],
        "constraints": ["0 <= len(s) <= 5 * 10^4", "s consists of letters, digits, symbols and spaces"],
        "hints": [
            "Maintain a window [left, right] that always holds distinct characters.",
            "Extend right one step at a time; when the new character is already inside, shrink from the left.",
            "Store {char: last index} so left can jump straight past the previous occurrence.",
        ],
        "target": {"time": "O(n)", "space": "O(min(n, alphabet))"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": ["abcabcbb"], "expect": 3},
            {"args": ["bbbbb"], "expect": 1},
            {"args": ["pwwkew"], "expect": 3},
            {"args": [""], "expect": 0},
            {"args": [" "], "expect": 1},
            {"args": ["dvdf"], "expect": 3},
            {"args": ["abba"], "expect": 2},
        ],
        "stress": {
            "args": lambda: ["".join(random.Random(2).choices("abcdefghij", k=200_000))],
            "budget": 1.5},
        "pitfalls": [
            '"abba" is the classic trap: when you jump `left`, never let it move backwards.',
            "Checking `char in current_window_string` is O(window) — use a dict or set.",
        ],
        "solution": """
def length_of_longest_substring(s):
    last = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best
""",
    },
    {
        "slug": "longest-repeating-character-replacement",
        "title": "Longest Repeating Character Replacement",
        "difficulty": "Medium",
        "topics": ["Hash Table", "String", "Sliding Window"],
        "url": "https://leetcode.com/problems/longest-repeating-character-replacement/",
        "func": "character_replacement",
        "signature": "def character_replacement(s: str, k: int) -> int:",
        "description": (
            "You may change at most `k` characters of `s` to any uppercase letter. Return the "
            "length of the longest substring that can be made to contain a single repeated letter."
        ),
        "examples": [
            's = "ABAB", k = 2     ->  4',
            's = "AABABBA", k = 1  ->  4   ("AABA" -> "AAAA")',
        ],
        "constraints": ["1 <= len(s) <= 10^5", "0 <= k <= len(s)", "s consists of uppercase letters"],
        "hints": [
            "A window is valid when (window length - count of its most frequent letter) <= k.",
            "Slide right, update counts, and shrink from the left while the window is invalid.",
            "You never need to shrink the max-count back down — the answer only grows.",
        ],
        "target": {"time": "O(n)", "space": "O(1) — 26 counters"},
        "argspec": ["raw", "raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": ["ABAB", 2], "expect": 4},
            {"args": ["AABABBA", 1], "expect": 4},
            {"args": ["A", 0], "expect": 1},
            {"args": ["AAAA", 0], "expect": 4},
            {"args": ["ABCDE", 1], "expect": 2},
            {"args": ["ABAA", 0], "expect": 2},
        ],
        "stress": {
            "args": lambda: ["".join(random.Random(9).choices("ABCD", k=100_000)), 5],
            "budget": 1.5,
        },
        "pitfalls": ["Recomputing max(counts.values()) inside the loop is fine for 26 letters but "
                     "unnecessary — the running max suffices."],
        "solution": """
def character_replacement(s, k):
    counts = {}
    left = 0
    max_count = 0
    best = 0
    for right, ch in enumerate(s):
        counts[ch] = counts.get(ch, 0) + 1
        max_count = max(max_count, counts[ch])
        while (right - left + 1) - max_count > k:
            counts[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
""",
    },
]
