# daily-leetcode

A local practice system: it hands you **one LeetCode-style problem a day** (easy through
medium), gives you a place to write Python, runs a hidden test suite against your code,
tells you what is wrong and how to think about it — and when everything passes, it
**commits and pushes your solution to GitHub automatically**.

No accounts, no API keys, no `pip install`. Standard-library Python only.

```
python leet.py serve     # browser UI  (recommended)
python leet.py today     # or work in your own editor
python leet.py check
```

---

## Contents

1. [Quick start](#quick-start)
2. [The browser UI](#the-browser-ui)
3. [The command line](#the-command-line)
4. [How the daily problem is chosen](#how-the-daily-problem-is-chosen)
5. [What the checker actually checks](#what-the-checker-actually-checks)
6. [The feedback you get](#the-feedback-you-get)
7. [Auto-commit and auto-push](#auto-commit-and-auto-push)
8. [Configuration](#configuration)
9. [Project layout](#project-layout)
10. [Adding your own problems](#adding-your-own-problems)
11. [Troubleshooting](#troubleshooting)

---

## Quick start

Requirements: Python 3.9+ and (for pushing) git. Verify with `python --version`.

```bash
cd daily-leetcode
python leet.py serve
```

Your browser opens on `http://127.0.0.1:8777`. Today's problem is on the left, the editor
on the right. Write your function, press **Ctrl+Enter**, read the feedback. When every
test passes, the solution is committed and pushed for you.

Prefer a terminal and your own editor?

```bash
python leet.py today      # prints the problem, creates solutions/<date>_<slug>.py
# ...write your code in that file...
python leet.py check      # runs the tests, prints feedback, commits + pushes on success
```

---

## The browser UI

`python leet.py serve` starts a small local web server (bound to `127.0.0.1` only — it is
not reachable from other machines) and opens the page.

| Element | What it does |
|---|---|
| **Run tests** / `Ctrl+Enter` | Saves your code to today's solution file, runs the full hidden suite, shows per-case results, feedback, and the git result |
| `Ctrl+S` | Save without running (the editor also autosaves every 8 s) |
| **Reveal a hint** | Hints come one at a time, from "what is the shape of the idea" to "here is the technique". Revealing one is remembered |
| **Show reference solution** | A worked answer plus the pitfalls list. Asks for confirmation first |
| **stress test** toggle | Include the large performance input (leave it on — it is what catches accidental O(n²)) |
| **auto-push** toggle | Turn off for a single run if you do not want that submission pushed |
| **Reset file** | Throw away your code and restore the starter template |
| **New problem** | Draw a different problem for today |
| **Progress** | Solved count, streak, per-difficulty totals, last two weeks |
| Git chip (top right) | Current branch, unpushed commit count, remote URL on hover |

The editor is a plain textarea with the conveniences that matter: tab inserts four spaces,
Tab/Shift-Tab indents and dedents a selection, Enter keeps your indentation and adds a
level after a `:`.

---

## The command line

| Command | What it does |
|---|---|
| `python leet.py today` | Show today's problem and create `solutions/<date>_<slug>.py` from a template |
| `python leet.py check` | Run the hidden tests on today's file, print feedback, commit + push if it all passes |
| `python leet.py check --quick` | Skip the large stress input (faster loop while you iterate) |
| `python leet.py check --no-push` | Run everything, but do not commit or push |
| `python leet.py check --file path.py` | Check some other file against today's problem |
| `python leet.py hint` | Reveal the next hint |
| `python leet.py solution` | Print the reference solution and the pitfalls |
| `python leet.py stats` | Solved count, streak, git status, recent days |
| `python leet.py list` | The whole problem bank, with a mark next to what you have solved |
| `python leet.py reroll` | Replace today's problem with a different one |
| `python leet.py serve [--port N] [--no-browser]` | Start the web UI |
| `python leet.py selftest [--stress]` | Verify the bank: every reference solution must pass its own tests |
| `python leet.py config [key] [value]` | Read or write `config.json` |

On Windows you can also just run `leet today`, `leet check`, … via the included
`leet.bat`.

---

## How the daily problem is chosen

The bank holds **69 problems** (curated LeetCode classics — arrays and hashing, two
pointers and sliding windows, stacks, binary search, linked lists, trees, dynamic
programming, graphs, intervals and heaps, matrix/math/bits), roughly a third easy and
two thirds medium.

Selection is a **shuffled deck, not a dice roll**:

- A seeded shuffle produces an order; each day pops the next problem off it.
- You therefore **never repeat a problem** until the whole bank is exhausted, after which
  a new cycle is shuffled.
- The shuffle is post-processed to break up runs of three or more problems of the same
  difficulty, so a week genuinely spans easy through medium.
- The day's assignment is written to `state/state.json`, so asking twice on the same day
  gives you the same problem — even after a reboot.

`python leet.py reroll` (or **New problem** in the UI) discards today's assignment and
draws the next one from the deck.

---

## What the checker actually checks

Your code runs in a **separate process**, so an infinite loop or a crash takes down the
sandbox rather than the tool. Each run reports:

- **5–7 hidden cases per problem**, including the edge cases the problem is famous for
  (empty input, single element, duplicates, negative numbers, the `"abba"` trap, the
  `[10,5,15,null,null,6,20]` BST trap, and so on).
- **A large stress input** whose expected answer is computed by the reference solution at
  run time, with a time budget. This is the difference between "correct" and "correct at
  n = 200,000" — it is what catches a hidden O(n²).
- **Per-case timings**, so you can see which input is expensive.
- **A hard timeout**. If the run is killed, the report names the case it died on.

Arguments are deep-copied per case, so in-place problems (`move-zeroes`, `rotate-image`,
`set-matrix-zeroes`, `reorder-list`) are graded on what you did to the input, and one
case can never contaminate the next.

Linked-list and tree problems hand you real `ListNode` / `TreeNode` objects, built from
the LeetCode level-order notation, and read your returned node back into a list. Import
them in your solution with:

```python
from dlc.structures import ListNode, TreeNode
```

Answers are compared the way the problem intends: exact, order-insensitive
(`top-k-frequent-elements`), order-insensitive at both levels (`group-anagrams`, `3sum`),
any-of (`longest-palindromic-substring`), or by inspecting the mutated input for in-place
problems.

---

## The feedback you get

Beyond pass/fail, every run produces notes at four levels:

| | Meaning |
|---|---|
| ✗ **fail** | It does not work yet — with the exact failing input, what was expected, and what you returned |
| ! **warn** | It works, but something will bite you (too slow on the big input, `x in list` inside a loop, `list.pop(0)`, `.count()`/`.index()` in a loop, nested loops when the target is linear, recursion on a DP problem with no memoisation) |
| i **tip** | Idiom and interview polish — string `+=` in a loop, leftover `print()`, `global` state, deeply nested conditionals, an over-long function |
| ✓ **good** | What you got right — a single pass matching the target complexity, comfortable margin on the stress input, using `deque` for a BFS queue |

Failures come with targeted nudges: an `IndexError` prompts a boundary check, a `None`
result points at a missing `return`, and a failing case that happens to be empty / a
single element / full of duplicates is called out as an edge case.

The advice comes from two sources: **measured behaviour** (timings against a budget,
which case failed) and **static analysis of your source** (an AST pass that counts loop
nesting, finds linear scans inside loops, spots recursion without memoisation, and so
on). It is deliberately specific — it quotes line numbers.

---

## Auto-commit and auto-push

When — and only when — **every** test passes (including the stress input), the system:

1. stages **exactly two paths**: the solution file you just passed, and `state/state.json`;
2. commits with a descriptive message;
3. pushes to `origin` on your current branch.

```
solve: Two Sum (Easy)

Problem: https://leetcode.com/problems/two-sum/
Topics:  Array, Hash Table
Solved:  2026-08-06
All hidden tests passed via `leet check`.
```

### The safety rules

These are enforced in `dlc/gitsync.py`, and they are the reason a submission can never
break the tool:

- **Only your solution and the state file are ever staged.** There is no `git add -A`,
  and no path under `dlc/`, `web/` or `leet.py` is ever staged by a submission. Pushing an
  answer cannot change how the checker, the problem bank, or the server behave afterwards.
- **Nothing under `solutions/` is ever imported by the system.** The problem bank only
  loads `dlc/problems/*.py`; your solutions are executed in a throwaway subprocess. A
  solution file with a syntax error, a monkeypatch or an infinite loop affects that one
  run and nothing else.
- **Git failure never fails a passing submission.** No remote, no credentials, no network,
  no git at all — you still get "Solved", and the reason git did not finish is reported
  underneath. Your code is already safe on disk.
- **Git is never allowed to block on a prompt.** `GIT_TERMINAL_PROMPT=0` plus a timeout,
  because this runs behind a web request.
- **No force pushing, ever.** If the remote has moved on, the push fails loudly and you
  resolve it yourself.

### First run

On the first passing submission the system will, if needed: `git init` on branch `main`,
write a `.gitignore`, add `origin`, and set a local git identity if you have no global
one. The remote it uses comes from `config.json`.

If the push fails because GitHub needs credentials, run `git push` once manually in a
terminal to let Git Credential Manager store them; after that the automatic push works.
The UI also shows a **Retry push** button on failure.

### Turning it off

```bash
python leet.py config auto_push false     # permanently
python leet.py check --no-push            # once
```
…or untick **auto-push** in the UI for a single run.

---

## Configuration

`config.json` at the project root (created on demand, editable by hand or via
`python leet.py config <key> <value>`):

| Key | Default | Meaning |
|---|---|---|
| `auto_push` | `true` | Commit and push when a submission passes |
| `remote` | your repo URL | Added as `origin` if no remote exists |
| `branch` | `"main"` | Branch used when initialising the repo |
| `commit_prefix` | `"solve"` | Prefix of the commit subject line |
| `difficulty_mix` | `"both"` | `both`, `easy` or `medium` — filters the deck |
| `server_port` | `8777` | Port for `leet.py serve` |
| `seed` | `null` | Fix it to make the schedule reproducible |

Changing `difficulty_mix` or `seed` affects the **next** deck, not assignments already made.

---

## Project layout

```
daily-leetcode/
├── leet.py                  CLI entry point
├── leet.bat                 Windows convenience wrapper
├── config.json              your settings
├── README.md                this file
├── CLAUDE.md                notes for Claude Code sessions in this repo
├── dlc/                     the system  (never touched by a submission)
│   ├── bank.py              loads and validates the problem bank
│   ├── picker.py            the deck, the schedule, file scaffolding
│   ├── runner.py            spawns the sandboxed subprocess
│   ├── _worker.py           the sandbox itself
│   ├── harness.py           argument/result conversion and answer comparison
│   ├── feedback.py          the advice engine (AST + measurements)
│   ├── gitsync.py           narrow, non-fatal commit + push
│   ├── submit.py            the one pipeline used by both CLI and UI
│   ├── server.py            the local web server
│   ├── structures.py        ListNode / TreeNode and their serialisers
│   └── problems/            the problem bank, by topic
├── web/                     the UI (index.html, app.css, app.js)
├── solutions/               your answers  — this is what gets pushed
└── state/state.json         schedule, attempts, streak, hints revealed
```

---

## Adding your own problems

Drop a new module in `dlc/problems/` exposing a `PROBLEMS` list. Copy the shape of an
existing entry — the required keys are documented at the top of `dlc/bank.py`. The
important ones:

```python
{
    "slug": "my-problem",
    "func": "my_problem",              # the function the checker calls
    "signature": "def my_problem(nums: List[int]) -> int:",
    "argspec": ["raw"],                # raw | linked | linked_cycle | tree | node_in_0
    "retspec": "raw",                  # raw | none | linked | tree | node_val
    "compare": "exact",                # exact | sorted | sorted_inner | any_of |
                                       # approx | inplace | inplace_linked
    "tests": [{"args": [[1, 2]], "expect": 3}],
    "stress": {"args": lambda: [list(range(100_000))], "budget": 1.5},
    "solution": "def my_problem(nums):\n    return sum(nums)",
}
```

Then run `python leet.py selftest --stress`. It executes every reference solution against
every test case (and every stress input) and fails loudly if any expectation is wrong —
run it after any edit to the bank.

---

## Troubleshooting

**"No function named `x` was found"** — the checker calls one specific function name.
Keep the signature from the template; add helpers around it freely.

**The push fails with an authentication error** — run `git push` once by hand so
credentials get stored, then click **Retry push** (or just run `check` again).

**"The test runner itself failed to start"** — that is a bug in the tool, not your code.
`python leet.py selftest` will confirm whether the installation is intact.

**A recursive solution hits RecursionError** — the sandbox already raises the limit to
60,000 and runs on a large stack, so if you still hit it, the recursion depth is growing
with the input in a way the problem does not intend.

**Port already in use** — `python leet.py serve --port 9000`.

**You want a clean slate** — delete `state/state.json` (schedule and progress) and/or the
contents of `solutions/`. Nothing else holds state.
