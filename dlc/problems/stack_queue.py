"""Stacks, monotonic stacks and backtracking on stacks."""

import random

PROBLEMS = [
    {
        "slug": "valid-parentheses",
        "title": "Valid Parentheses",
        "difficulty": "Easy",
        "topics": ["String", "Stack"],
        "url": "https://leetcode.com/problems/valid-parentheses/",
        "func": "is_valid",
        "signature": "def is_valid(s: str) -> bool:",
        "description": (
            "Given a string of '(', ')', '{', '}', '[' and ']', return True if every bracket is "
            "closed by the same type in the correct order."
        ),
        "examples": ['s = "()[]{}"  ->  True', 's = "(]"      ->  False', 's = "([)]"   ->  False'],
        "constraints": ["1 <= len(s) <= 10^4", "s consists of bracket characters only"],
        "hints": [
            "The most recently opened bracket must be the first one closed — that is a stack.",
            "Push openers; on a closer, pop and check that it matches.",
            "At the end the stack must be empty, and popping from an empty stack means invalid.",
        ],
        "target": {"time": "O(n)", "space": "O(n)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": ["()"], "expect": True},
            {"args": ["()[]{}"], "expect": True},
            {"args": ["(]"], "expect": False},
            {"args": ["([)]"], "expect": False},
            {"args": ["{[]}"], "expect": True},
            {"args": ["]"], "expect": False},
            {"args": ["(("], "expect": False},
        ],
        "stress": {"args": lambda: ["(" * 100_000 + ")" * 100_000], "budget": 1.5},
        "pitfalls": [
            "An odd-length string is always invalid — a cheap early exit.",
            "Leftover openers at the end must fail.",
        ],
        "solution": """
def is_valid(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    stack = []
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)
    return not stack
""",
    },
    {
        "slug": "evaluate-reverse-polish-notation",
        "title": "Evaluate Reverse Polish Notation",
        "difficulty": "Medium",
        "topics": ["Array", "Math", "Stack"],
        "url": "https://leetcode.com/problems/evaluate-reverse-polish-notation/",
        "func": "eval_rpn",
        "signature": "def eval_rpn(tokens: List[str]) -> int:",
        "description": (
            "Evaluate an arithmetic expression in Reverse Polish Notation. Valid operators are "
            "+, -, * and /. Division between two integers truncates toward zero."
        ),
        "examples": [
            'tokens = ["2","1","+","3","*"]      ->  9    ((2 + 1) * 3)',
            'tokens = ["4","13","5","/","+"]     ->  6    (4 + 13 / 5)',
        ],
        "constraints": ["1 <= len(tokens) <= 10^4", "the expression is always valid"],
        "hints": [
            "Push numbers; when you meet an operator, pop the two most recent values.",
            "Order matters for - and /: the first popped value is the right operand.",
            "Python's // floors (-7 // 2 == -4). Use int(a / b) for truncation toward zero.",
        ],
        "target": {"time": "O(n)", "space": "O(n)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [["2", "1", "+", "3", "*"]], "expect": 9},
            {"args": [["4", "13", "5", "/", "+"]], "expect": 6},
            {"args": [["5"]], "expect": 5},
            {"args": [["-7", "2", "/"]], "expect": -3},
            {"args": [["4", "-2", "/", "2", "-3", "-", "-"]], "expect": -7},
            {
                "args": [["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]],
                "expect": 22,
            },
        ],
        "stress": {
            "args": lambda: [["1"] + ["1", "+"] * 5_000],
            "budget": 1.5,
        },
        "pitfalls": [
            "-7 / 2 must be -3, not -4 — Python's // is the wrong operator here.",
            "Negative literals like '-11' are operands; check membership in the operator set "
            "rather than calling str.isdigit().",
        ],
        "solution": """
def eval_rpn(tokens):
    stack = []
    for token in tokens:
        if token in ('+', '-', '*', '/'):
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            else:
                stack.append(int(a / b))
        else:
            stack.append(int(token))
    return stack[-1]
""",
    },
    {
        "slug": "daily-temperatures",
        "title": "Daily Temperatures",
        "difficulty": "Medium",
        "topics": ["Array", "Stack", "Monotonic Stack"],
        "url": "https://leetcode.com/problems/daily-temperatures/",
        "func": "daily_temperatures",
        "signature": "def daily_temperatures(temperatures: List[int]) -> List[int]:",
        "description": (
            "For each day, return how many days you must wait for a warmer temperature. "
            "If no warmer day exists, put 0 in that position."
        ),
        "examples": [
            "temperatures = [73,74,75,71,69,72,76,73]  ->  [1,1,4,2,1,1,0,0]",
            "temperatures = [30,40,50,60]              ->  [1,1,1,0]",
        ],
        "constraints": ["1 <= len(temperatures) <= 10^5", "30 <= temperatures[i] <= 100"],
        "hints": [
            "Days still waiting for a warmer temperature form a decreasing sequence.",
            "Keep a stack of indices whose answer is still unknown.",
            "When today beats the temperature at the top of the stack, pop it and record the "
            "index difference. Each index is pushed and popped once, so it is O(n).",
        ],
        "target": {"time": "O(n)", "space": "O(n)"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[73, 74, 75, 71, 69, 72, 76, 73]], "expect": [1, 1, 4, 2, 1, 1, 0, 0]},
            {"args": [[30, 40, 50, 60]], "expect": [1, 1, 1, 0]},
            {"args": [[30, 60, 90]], "expect": [1, 1, 0]},
            {"args": [[90, 80, 70]], "expect": [0, 0, 0]},
            {"args": [[50]], "expect": [0]},
            {"args": [[50, 50, 51]], "expect": [2, 1, 0]},
        ],
        "stress": {
            "args": lambda: [random.Random(4).choices(range(30, 101), k=150_000)],
            "budget": 2.0,
        },
        "pitfalls": [
            "Equal temperatures do not count as warmer.",
            "The naive double loop is O(n^2) and will time out at n = 10^5.",
        ],
        "solution": """
def daily_temperatures(temperatures):
    out = [0] * len(temperatures)
    stack = []
    for i, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            j = stack.pop()
            out[j] = i - j
        stack.append(i)
    return out
""",
    },
    {
        "slug": "generate-parentheses",
        "title": "Generate Parentheses",
        "difficulty": "Medium",
        "topics": ["String", "Backtracking", "Dynamic Programming"],
        "url": "https://leetcode.com/problems/generate-parentheses/",
        "func": "generate_parenthesis",
        "signature": "def generate_parenthesis(n: int) -> List[str]:",
        "description": (
            "Given `n` pairs of parentheses, generate every combination of well-formed "
            "parentheses. Any order is accepted."
        ),
        "examples": [
            'n = 3  ->  ["((()))","(()())","(())()","()(())","()()()"]',
            'n = 1  ->  ["()"]',
        ],
        "constraints": ["1 <= n <= 8"],
        "hints": [
            "Build the string one character at a time and prune invalid prefixes early.",
            "You may add '(' while you have used fewer than n of them.",
            "You may add ')' only while closed < opened. Recurse, append, then undo.",
        ],
        "target": {"time": "O(4^n / sqrt(n))", "space": "O(n) recursion depth"},
        "argspec": ["raw"],
        "retspec": "raw",
        "compare": "sorted",
        "tests": [
            {"args": [1], "expect": ["()"]},
            {"args": [2], "expect": ["(())", "()()"]},
            {"args": [3], "expect": ["((()))", "(()())", "(())()", "()(())", "()()()"]},
            {
                "args": [4],
                "expect": ["(((())))", "((()()))", "((())())", "((()))()", "(()(()))",
                           "(()()())", "(()())()", "(())(())", "(())()()", "()((()))",
                           "()(()())", "()(())()", "()()(())", "()()()()"],
            },
        ],
        "stress": {"args": lambda: [8], "budget": 1.5},
        "pitfalls": [
            "Generating all 2^(2n) strings and filtering works for n=8 but is the slow path.",
            "If you mutate a shared list, remember to pop after the recursive call.",
        ],
        "solution": """
def generate_parenthesis(n):
    out = []
    current = []

    def backtrack(opened, closed):
        if len(current) == 2 * n:
            out.append(''.join(current))
            return
        if opened < n:
            current.append('(')
            backtrack(opened + 1, closed)
            current.pop()
        if closed < opened:
            current.append(')')
            backtrack(opened, closed + 1)
            current.pop()

    backtrack(0, 0)
    return out
""",
    },
]
