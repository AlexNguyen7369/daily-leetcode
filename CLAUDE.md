# CLAUDE.md

Notes for Claude Code sessions working in this repository.

## What this project is

A local daily LeetCode practice system. It picks one problem a day (easy→medium) from a
curated bank, scaffolds a Python file, runs a hidden test suite in a sandboxed
subprocess, produces coaching feedback, and **auto-commits and pushes solutions that
pass**. Standard library only — do not add third-party dependencies.

User-facing documentation is `README.md`. Keep it in sync when behaviour changes.

## Commands

```bash
python leet.py serve                # local web UI on 127.0.0.1:8777
python leet.py today                # today's problem + scaffold
python leet.py check [--quick] [--no-push] [--file PATH]
python leet.py selftest --stress    # MUST pass after any change to dlc/problems/
python leet.py stats | list | hint | solution | reroll
python leet.py config <key> <value>
```

`selftest` runs every reference solution against every test case in the bank. **Run it
after touching anything in `dlc/problems/`, `dlc/harness.py` or `dlc/structures.py`.**

## Auto-commit and auto-push — the contract

Implemented in `dlc/gitsync.py`, triggered from `dlc/submit.py:check()` only when
`result["all_passed"]` is true (all hidden cases **and** the stress case).

These invariants exist so that pushing a solution can never change how the system
behaves afterwards. Do not weaken them:

1. **Path-scoped staging only.** `sync_solution()` stages exactly the passing solution
   file plus `state/state.json`, using `git add -- <path>`. Never introduce `git add -A`,
   `git add .`, or `git commit -a` anywhere in this repo's automation.
2. **`dlc/`, `web/`, `leet.py` and the docs are never staged by a submission.** Changes to
   the system itself are committed deliberately by a human (or by you, when asked) — never
   as a side effect of solving a problem.
3. **Nothing under `solutions/` is ever imported by the system.** `dlc/bank.py` only
   loads `dlc/problems/*.py`. User code is executed exclusively in the `dlc/_worker.py`
   subprocess. Keep it that way: no `import` of a solution file from the main process.
4. **Git failure is non-fatal.** Every git path is wrapped so that a missing remote,
   absent credentials, offline network, or missing git binary still yields a passing
   submission with an explanatory note. Never let a git error propagate as an exception
   into `submit.check()`.
5. **Never force push, never rewrite history, never auto-resolve a conflict.** If the
   remote has diverged, the push fails and the user handles it.
6. **Git must never block on a prompt.** `GIT_TERMINAL_PROMPT=0`, `GCM_INTERACTIVE=never`
   and an explicit timeout on every subprocess call — this code runs behind a web request.
7. **Respect the kill switches.** `config.json: auto_push`, the `--no-push` CLI flag, and
   the UI's auto-push toggle all route into `allow_push` / `config.get("auto_push")`.

Commit message format produced by the automation:

```
solve: <Title> (<Difficulty>)

Problem: <url>
Topics:  <topics>
Solved:  <YYYY-MM-DD>
All hidden tests passed via `leet check`.
```

When *you* commit changes to the system itself, use a normal descriptive message
instead, and stage only the files you actually changed.

## Architecture

```
leet.py           argparse CLI + terminal rendering
dlc/submit.py     the single pipeline: run -> feedback -> record -> git
dlc/runner.py     parent side of the sandbox; owns the timeout
dlc/_worker.py    child process; emits one JSON line per case so a timeout still
                  tells us which case hung
dlc/harness.py    argspec/retspec conversion + the comparators
dlc/feedback.py   advice engine: AST analysis + measured timings
dlc/picker.py     shuffled-deck scheduling, state, file scaffolding
dlc/gitsync.py    narrow commit + push
dlc/server.py     stdlib http.server UI backend (127.0.0.1 only)
dlc/problems/     the bank, one module per topic, each exposing PROBLEMS
web/              index.html + app.css + app.js, no external assets
```

Data flow for a submission: UI/CLI → `submit.check()` → `runner.run()` spawns
`_worker` → worker converts args per `argspec`, calls the user function, converts the
result per `retspec`, compares per `compare` → parent assembles the result →
`feedback.build()` adds notes → `picker.record_attempt()` → `gitsync.sync_solution()`
if everything passed.

## Conventions

- **No third-party packages.** Standard library only, in both the tool and the web UI
  (no CDN scripts, no external fonts).
- **The server binds to 127.0.0.1 and validates the Host header.** It executes arbitrary
  user code by design; do not expose it on `0.0.0.0` or add a CORS wildcard.
- **Problem entries are data.** The required keys are documented at the top of
  `dlc/bank.py`; `bank.all_problems()` validates them on load.
- **Test expectations must be verified, not guessed.** Every expectation in the bank is
  cross-checked against the reference solution by `selftest`. If a reference and a
  hand-written expectation disagree, work out which is actually right before changing
  either.
- **Stress cases compare against the reference at run time**, so a stress input must be
  valid for the problem's stated preconditions (e.g. a BST problem needs an actual BST,
  or correct solutions will legitimately disagree).
- Keep terminal output ASCII-safe; Windows consoles are the primary target.
