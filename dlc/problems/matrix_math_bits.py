"""Matrix manipulation, integer math and bit tricks."""

PROBLEMS = [
    {
        "slug": "plus-one",
        "title": "Plus One",
        "difficulty": "Easy",
        "topics": ["Array", "Math"],
        "url": "https://leetcode.com/problems/plus-one/",
        "func": "plus_one",
        "signature": "def plus_one(digits: List[int]) -> List[int]:",
        "description": (
            "`digits` holds the decimal digits of a large integer, most significant first. "
            "Add one to that integer and return the resulting digit list."
        ),
        "examples": ["digits = [1,2,3]  ->  [1,2,4]", "digits = [9]  ->  [1,0]", "digits = [9,9]  ->  [1,0,0]"],
        "constraints": ["1 <= len(digits) <= 100", "no leading zeros"],
        "hints": [
            "Walk from the last digit backwards.",
            "A digit below 9 can just be incremented — you are done immediately.",
            "A 9 becomes 0 and the carry continues. If you fall off the front, prepend a 1.",
        ],
        "target": {"time": "O(n)", "space": "O(1) extra"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[1, 2, 3]], "expect": [1, 2, 4]},
            {"args": [[4, 3, 2, 1]], "expect": [4, 3, 2, 2]},
            {"args": [[9]], "expect": [1, 0]},
            {"args": [[9, 9]], "expect": [1, 0, 0]},
            {"args": [[0]], "expect": [1]},
            {"args": [[1, 9, 9]], "expect": [2, 0, 0]},
        ],
        "stress": {"args": lambda: [[9] * 100_000], "budget": 1.5},
        "pitfalls": ["The all-nines case grows the list by one element."],
        "solution": """
def plus_one(digits):
    out = digits[:]
    for i in range(len(out) - 1, -1, -1):
        if out[i] < 9:
            out[i] += 1
            return out
        out[i] = 0
    return [1] + out
""",
    },
    {
        "slug": "roman-to-integer",
        "title": "Roman to Integer",
        "difficulty": "Easy",
        "topics": ["Hash Table", "Math", "String"],
        "url": "https://leetcode.com/problems/roman-to-integer/",
        "func": "roman_to_int",
        "signature": "def roman_to_int(s: str) -> int:",
        "description": (
            "Convert a Roman numeral to an integer. Values: I=1, V=5, X=10, L=50, C=100, D=500, "
            "M=1000. A smaller value placed before a larger one is subtracted (IV = 4, IX = 9, "
            "XL = 40, CM = 900)."
        ),
        "examples": ['s = "III"      ->  3', 's = "LVIII"    ->  58', 's = "MCMXCIV"  ->  1994'],
        "constraints": ["1 <= len(s) <= 15", "s is a valid roman numeral in [1, 3999]"],
        "hints": [
            "Handle the six subtractive pairs, or find a rule that covers them all.",
            "Scan left to right: if the current value is smaller than the next one, subtract it.",
            "Otherwise add it. No special-casing of pairs needed.",
        ],
        "target": {"time": "O(n)", "space": "O(1)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": ["III"], "expect": 3},
            {"args": ["LVIII"], "expect": 58},
            {"args": ["MCMXCIV"], "expect": 1994},
            {"args": ["IV"], "expect": 4},
            {"args": ["IX"], "expect": 9},
            {"args": ["MMMCMXCIX"], "expect": 3999},
        ],
        "stress": {"args": lambda: ["MCMXCIV" * 2], "budget": 1.0},
        "pitfalls": ["The last character is never subtracted — guard the i+1 lookup."],
        "solution": """
def roman_to_int(s):
    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    for i, ch in enumerate(s):
        if i + 1 < len(s) and values[ch] < values[s[i + 1]]:
            total -= values[ch]
        else:
            total += values[ch]
    return total
""",
    },
    {
        "slug": "palindrome-number",
        "title": "Palindrome Number",
        "difficulty": "Easy",
        "topics": ["Math"],
        "url": "https://leetcode.com/problems/palindrome-number/",
        "func": "is_palindrome_number",
        "signature": "def is_palindrome_number(x: int) -> bool:",
        "description": (
            "Return True if the integer `x` reads the same forwards and backwards. "
            "Try to solve it without converting the number to a string."
        ),
        "examples": ["x = 121   ->  True", "x = -121  ->  False", "x = 10    ->  False"],
        "constraints": ["-2^31 <= x <= 2^31 - 1"],
        "hints": [
            "Negative numbers are never palindromes because of the leading minus sign.",
            "Build the reverse with repeated divmod by 10 and compare.",
            "You only need to reverse half the digits: stop when the reversed half >= what's left.",
        ],
        "target": {"time": "O(log x)", "space": "O(1)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [121], "expect": True},
            {"args": [-121], "expect": False},
            {"args": [10], "expect": False},
            {"args": [0], "expect": True},
            {"args": [1221], "expect": True},
            {"args": [1000021], "expect": False},
        ],
        "stress": {"args": lambda: [1234554321], "budget": 1.0},
        "pitfalls": ["Any non-zero number ending in 0 cannot be a palindrome."],
        "solution": """
def is_palindrome_number(x):
    if x < 0 or (x % 10 == 0 and x != 0):
        return False
    reversed_half = 0
    while x > reversed_half:
        x, digit = divmod(x, 10)
        reversed_half = reversed_half * 10 + digit
    return x == reversed_half or x == reversed_half // 10
""",
    },
    {
        "slug": "missing-number",
        "title": "Missing Number",
        "difficulty": "Easy",
        "topics": ["Array", "Math", "Bit Manipulation"],
        "url": "https://leetcode.com/problems/missing-number/",
        "func": "missing_number",
        "signature": "def missing_number(nums: List[int]) -> int:",
        "description": (
            "`nums` holds n distinct numbers drawn from the range [0, n]. Return the one that is "
            "missing, in O(n) time and O(1) extra space."
        ),
        "examples": ["nums = [3,0,1]  ->  2", "nums = [0,1]  ->  2", "nums = [9,6,4,2,3,5,7,0,1]  ->  8"],
        "constraints": ["1 <= n <= 10^4", "all values are unique and within [0, n]"],
        "hints": [
            "You know exactly what the complete set should sum to.",
            "n*(n+1)//2 minus the actual sum is the answer.",
            "XOR-ing every index and every value together also leaves the missing number.",
        ],
        "target": {"time": "O(n)", "space": "O(1)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[3, 0, 1]], "expect": 2},
            {"args": [[0, 1]], "expect": 2},
            {"args": [[9, 6, 4, 2, 3, 5, 7, 0, 1]], "expect": 8},
            {"args": [[0]], "expect": 1},
            {"args": [[1]], "expect": 0},
        ],
        "stress": {
            "args": lambda: [[i for i in range(200_001) if i != 137_000]],
            "budget": 1.5,
        },
        "pitfalls": ["The missing value can be 0 or n itself — both ends are in play."],
        "solution": """
def missing_number(nums):
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)
""",
    },
    {
        "slug": "number-of-1-bits",
        "title": "Number of 1 Bits",
        "difficulty": "Easy",
        "topics": ["Bit Manipulation"],
        "url": "https://leetcode.com/problems/number-of-1-bits/",
        "func": "hamming_weight",
        "signature": "def hamming_weight(n: int) -> int:",
        "description": "Return the number of set bits (1s) in the binary representation of `n`.",
        "examples": ["n = 11   ->  3   (1011)", "n = 128  ->  1", "n = 2147483645  ->  30"],
        "constraints": ["1 <= n <= 2^31 - 1"],
        "hints": [
            "Shift right one bit at a time and test the low bit with n & 1.",
            "n & (n - 1) clears the lowest set bit.",
            "So looping while n: n &= n - 1 runs once per set bit, not once per bit.",
        ],
        "target": {"time": "O(number of set bits)", "space": "O(1)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [11], "expect": 3},
            {"args": [128], "expect": 1},
            {"args": [2147483645], "expect": 30},
            {"args": [1], "expect": 1},
            {"args": [7], "expect": 3},
        ],
        "stress": {"args": lambda: [2**31 - 1], "budget": 1.0},
        "pitfalls": ["bin(n).count('1') is a legitimate Python answer — but know the bit trick too."],
        "solution": """
def hamming_weight(n):
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count
""",
    },
    {
        "slug": "counting-bits",
        "title": "Counting Bits",
        "difficulty": "Easy",
        "topics": ["Dynamic Programming", "Bit Manipulation"],
        "url": "https://leetcode.com/problems/counting-bits/",
        "func": "count_bits",
        "signature": "def count_bits(n: int) -> List[int]:",
        "description": (
            "Return an array `ans` of length n+1 where `ans[i]` is the number of set bits in i. "
            "Aim for a single O(n) pass."
        ),
        "examples": ["n = 2  ->  [0,1,1]", "n = 5  ->  [0,1,1,2,1,2]"],
        "constraints": ["0 <= n <= 10^5"],
        "hints": [
            "Counting bits for each number independently is O(n log n) — you can reuse earlier answers.",
            "i >> 1 is i with its last bit dropped, and you already computed its answer.",
            "ans[i] = ans[i >> 1] + (i & 1).",
        ],
        "target": {"time": "O(n)", "space": "O(n)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [2], "expect": [0, 1, 1]},
            {"args": [5], "expect": [0, 1, 1, 2, 1, 2]},
            {"args": [0], "expect": [0]},
            {"args": [1], "expect": [0, 1]},
            {"args": [8], "expect": [0, 1, 1, 2, 1, 2, 2, 3, 1]},
        ],
        "stress": {"args": lambda: [100_000], "budget": 1.5},
        "pitfalls": ["The output has n+1 entries, including 0."],
        "solution": """
def count_bits(n):
    ans = [0] * (n + 1)
    for i in range(1, n + 1):
        ans[i] = ans[i >> 1] + (i & 1)
    return ans
""",
    },
    {
        "slug": "rotate-image",
        "title": "Rotate Image",
        "difficulty": "Medium",
        "topics": ["Array", "Math", "Matrix"],
        "url": "https://leetcode.com/problems/rotate-image/",
        "func": "rotate",
        "signature": "def rotate(matrix: List[List[int]]) -> None:",
        "description": (
            "Rotate the n x n matrix 90 degrees clockwise, in place. Do not allocate another "
            "matrix. Return nothing."
        ),
        "examples": [
            "matrix = [[1,2,3],[4,5,6],[7,8,9]]  ->  [[7,4,1],[8,5,2],[9,6,3]]",
            "matrix = [[1]]  ->  [[1]]",
        ],
        "constraints": ["1 <= n <= 20", "-1000 <= matrix[i][j] <= 1000"],
        "hints": [
            "A clockwise rotation is the composition of two simple operations.",
            "Transpose the matrix (swap across the main diagonal), then reverse each row.",
            "When transposing, only loop over j > i or you will undo your own work.",
        ],
        "target": {"time": "O(n^2)", "space": "O(1)"},
        "argspec": ["raw"],
        "retspec": "none",
        "compare": "inplace",
        "tests": [
            {"args": [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], "expect": [[7, 4, 1], [8, 5, 2], [9, 6, 3]]},
            {"args": [[[1]]], "expect": [[1]]},
            {"args": [[[1, 2], [3, 4]]], "expect": [[3, 1], [4, 2]]},
            {
                "args": [[[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]],
                "expect": [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]],
            },
        ],
        "stress": {
            "args": lambda: [[[r * 20 + c for c in range(20)] for r in range(20)]],
            "budget": 1.0,
        },
        "pitfalls": [
            "Rebinding `matrix` to a new list does not modify the caller's matrix.",
            "Transposing over the full index range swaps every pair twice, leaving it unchanged.",
        ],
        "solution": """
def rotate(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix:
        row.reverse()
""",
    },
    {
        "slug": "spiral-matrix",
        "title": "Spiral Matrix",
        "difficulty": "Medium",
        "topics": ["Array", "Matrix", "Simulation"],
        "url": "https://leetcode.com/problems/spiral-matrix/",
        "func": "spiral_order",
        "signature": "def spiral_order(matrix: List[List[int]]) -> List[int]:",
        "description": "Return all elements of the m x n matrix in spiral order, starting at the top-left.",
        "examples": [
            "matrix = [[1,2,3],[4,5,6],[7,8,9]]        ->  [1,2,3,6,9,8,7,4,5]",
            "matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]  ->  [1,2,3,4,8,12,11,10,9,5,6,7]",
        ],
        "constraints": ["1 <= m, n <= 10", "-100 <= matrix[i][j] <= 100"],
        "hints": [
            "Track four boundaries: top, bottom, left, right.",
            "Walk right along the top, down the right, left along the bottom, up the left — then shrink.",
            "Before the bottom and left passes, check that the boundaries have not crossed, or a "
            "single remaining row/column gets emitted twice.",
        ],
        "target": {"time": "O(m*n)", "space": "O(1) extra"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], "expect": [1, 2, 3, 6, 9, 8, 7, 4, 5]},
            {
                "args": [[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]],
                "expect": [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7],
            },
            {"args": [[[1]]], "expect": [1]},
            {"args": [[[1, 2], [3, 4]]], "expect": [1, 2, 4, 3]},
            {"args": [[[1], [2], [3]]], "expect": [1, 2, 3]},
            {"args": [[[1, 2, 3]]], "expect": [1, 2, 3]},
        ],
        "stress": {
            "args": lambda: [[[r * 10 + c for c in range(10)] for r in range(10)]],
            "budget": 1.0,
        },
        "pitfalls": ["A single row or single column is where the duplicate-emission bug shows up."],
        "solution": """
def spiral_order(matrix):
    out = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            out.append(matrix[top][c])
        top += 1
        for r in range(top, bottom + 1):
            out.append(matrix[r][right])
        right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1):
                out.append(matrix[bottom][c])
            bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1):
                out.append(matrix[r][left])
            left += 1
    return out
""",
    },
    {
        "slug": "set-matrix-zeroes",
        "title": "Set Matrix Zeroes",
        "difficulty": "Medium",
        "topics": ["Array", "Hash Table", "Matrix"],
        "url": "https://leetcode.com/problems/set-matrix-zeroes/",
        "func": "set_zeroes",
        "signature": "def set_zeroes(matrix: List[List[int]]) -> None:",
        "description": (
            "If any cell of the m x n matrix is 0, set its entire row and column to 0. "
            "Do it in place and return nothing."
        ),
        "examples": [
            "matrix = [[1,1,1],[1,0,1],[1,1,1]]  ->  [[1,0,1],[0,0,0],[1,0,1]]",
            "matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]  ->  [[0,0,0,0],[0,4,5,0],[0,3,1,0]]",
        ],
        "constraints": ["1 <= m, n <= 200", "-2^31 <= matrix[i][j] <= 2^31 - 1"],
        "hints": [
            "Zeroing as you scan destroys the information you still need — record first, write second.",
            "Collect the set of rows and the set of columns that contain a zero, then apply them.",
            "For O(1) space, use the first row and first column as the marker storage, tracking "
            "separately whether they themselves must be zeroed.",
        ],
        "target": {"time": "O(m*n)", "space": "O(1) with the marker trick"},
        "argspec": ["raw"],
        "retspec": "none",
        "compare": "inplace",
        "tests": [
            {"args": [[[1, 1, 1], [1, 0, 1], [1, 1, 1]]], "expect": [[1, 0, 1], [0, 0, 0], [1, 0, 1]]},
            {
                "args": [[[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]],
                "expect": [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]],
            },
            {"args": [[[0]]], "expect": [[0]]},
            {"args": [[[1, 2], [3, 4]]], "expect": [[1, 2], [3, 4]]},
            {"args": [[[1, 0], [1, 1]]], "expect": [[0, 0], [1, 0]]},
        ],
        "stress": {
            "args": lambda: [[[0 if (r == 100 and c == 100) else 1 for c in range(200)]
                              for r in range(200)]],
            "budget": 2.0,
        },
        "pitfalls": [
            "Writing zeros during the first pass cascades and blanks the whole matrix.",
            "Rebinding rows instead of mutating them loses the in-place requirement.",
        ],
        "solution": """
def set_zeroes(matrix):
    rows_to_zero = set()
    cols_to_zero = set()
    for r, row in enumerate(matrix):
        for c, value in enumerate(row):
            if value == 0:
                rows_to_zero.add(r)
                cols_to_zero.add(c)
    for r, row in enumerate(matrix):
        for c in range(len(row)):
            if r in rows_to_zero or c in cols_to_zero:
                row[c] = 0
""",
    },
]
