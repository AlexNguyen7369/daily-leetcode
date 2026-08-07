#!/usr/bin/env python
"""daily-leetcode — a problem a day, checked locally, with feedback.

    python leet.py today          today's problem (creates the solution file)
    python leet.py check          run the hidden tests + get advice
    python leet.py hint           reveal the next hint
    python leet.py solution       show a reference answer
    python leet.py serve          open the browser UI
    python leet.py stats          progress and streak
    python leet.py list           everything in the problem bank
    python leet.py reroll         swap today's problem for another
    python leet.py selftest       verify the bank itself
"""

from __future__ import annotations

import argparse
import os
import sys
import webbrowser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dlc import bank, config, gitsync, picker, submit  # noqa: E402

# --------------------------------------------------------------------------- #
# terminal colour
# --------------------------------------------------------------------------- #
def _enable_ansi() -> bool:
    if os.name != "nt":
        return sys.stdout.isatty()
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)
        mode = ctypes.c_uint32()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            return False
        kernel32.SetConsoleMode(handle, mode.value | 0x0004)
        return True
    except Exception:
        return False


COLOUR = _enable_ansi()


def c(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m" if COLOUR else text


BOLD, DIM = "1", "2"
RED, GREEN, YELLOW, BLUE, CYAN, MAGENTA = "31", "32", "33", "34", "36", "35"

LEVEL_STYLE = {
    "fail": ("x", RED),
    "warn": ("!", YELLOW),
    "tip": ("i", CYAN),
    "good": ("+", GREEN),
}


def rule(char: str = "-", width: int = 76) -> str:
    return c(char * width, DIM)


# --------------------------------------------------------------------------- #
# rendering
# --------------------------------------------------------------------------- #
def show_problem(problem, path: str, date_key: str) -> None:
    diff_colour = GREEN if problem["difficulty"] == "Easy" else YELLOW
    print()
    print(rule("="))
    print(f"  {c(problem['title'], BOLD)}   "
          f"{c(problem['difficulty'], diff_colour)}   "
          f"{c(', '.join(problem['topics']), DIM)}")
    print(f"  {c(problem['url'], DIM)}")
    print(rule("="))
    print()
    for line in problem["description"].split("\n"):
        print(f"  {line}")
    print()
    print(c("  Examples", BOLD))
    for line in problem["examples"]:
        print(f"    {line}")
    print()
    print(c("  Constraints", BOLD))
    for line in problem["constraints"]:
        print(f"    - {line}")
    print()
    print(c("  Target", BOLD) + f"  {problem['target']['time']} time, "
          f"{problem['target']['space']} space")
    print()
    print(rule())
    print(f"  Write your answer in  {c(os.path.relpath(path, config.ROOT), CYAN)}")
    print(f"  Then run              {c('python leet.py check', CYAN)}")
    print(f"  Or use the browser    {c('python leet.py serve', CYAN)}")
    print(rule())
    print()


def show_check(payload) -> int:
    problem = payload["problem"]
    if payload["error"]:
        print(c(f"\n  {payload['error']}\n", RED))
        return 2

    result = payload["result"]
    print()
    print(rule("="))
    print(f"  {c(problem['title'], BOLD)}   {c(problem['difficulty'], DIM)}")
    print(rule("="))

    # per-case table
    if result["func_found"] and result["cases"]:
        print()
        for i, case in enumerate(result["cases"], 1):
            mark = c("PASS", GREEN) if case["ok"] else c("FAIL", RED)
            timing = c(f"{case['ms']:>7.2f} ms", DIM)
            print(f"  {mark}  case {i:>2}  {timing}   {_short(case['args'])}")
            if not case["ok"]:
                if case.get("error"):
                    detail = case["error"].strip().splitlines()[-1]
                    print(f"          {c(detail, RED)}")
                else:
                    print(f"          expected {c(_short(case['expect'], 90), GREEN)}")
                    print(f"          got      {c(_short(case['got'], 90), RED)}")

    stress = result.get("stress")
    if stress:
        if stress.get("error"):
            print(f"  {c('FAIL', RED)}  stress    {c(stress['error'].splitlines()[-1], RED)}")
        elif stress["ok"]:
            slow = stress["ms"] > stress["budget"]
            mark = c("SLOW", YELLOW) if slow else c("PASS", GREEN)
            timing = c(f"{stress['ms']:>7.0f} ms", DIM)
            print(f"  {mark}  stress   {timing}   large input "
                  f"(budget {stress['budget']:.0f} ms)")
        else:
            print(f"  {c('FAIL', RED)}  stress     large input gave the wrong answer")

    if result["stray_output"]:
        print()
        print(c("  Your code printed:", DIM))
        for line in result["stray_output"][:5]:
            print(c(f"    {line}", DIM))

    # feedback
    print()
    print(rule())
    print(c("  FEEDBACK", BOLD))
    print(rule())
    for note in payload["notes"]:
        glyph, colour = LEVEL_STYLE.get(note["level"], ("-", DIM))
        print(f"  {c(glyph, colour)} {c(note['title'], BOLD if note['level'] != 'tip' else '0')}")
        if note["detail"]:
            for line in note["detail"].split("\n"):
                print(f"      {c(line, DIM)}")
    print()

    # git
    git = payload.get("git")
    if git:
        print(rule())
        if git["pushed"]:
            print(f"  {c('pushed', GREEN)}  {git['commit']}")
        elif git["committed"]:
            print(f"  {c('committed', GREEN)}  {git['commit']}")
        for step in git["steps"]:
            print(c(f"    {step}", DIM))
        if git.get("skipped"):
            print(c(f"    {git['skipped']}", DIM))
        if git.get("error"):
            print(f"  {c('git: ' + git['error'].splitlines()[0], YELLOW)}")
            print(c("    (your solution is safe on disk; fix git and run check again)", DIM))
        print(rule())
        print()

    if result["all_passed"]:
        print(c("  Solved.", GREEN + ";1"))
        print(c("  `python leet.py solution` shows a reference answer to compare against.\n", DIM))
        return 0

    print(c("  Not there yet — `python leet.py hint` for a nudge.\n", YELLOW))
    return 1


def _short(value, limit: int = 70) -> str:
    text = repr(value)
    return text if len(text) <= limit else text[: limit - 3] + "..."


# --------------------------------------------------------------------------- #
# commands
# --------------------------------------------------------------------------- #
def cmd_today(args) -> int:
    problem = picker.problem_for(reroll=getattr(args, "reroll", False))
    path = picker.ensure_solution_file(problem)
    show_problem(problem, path, picker.today_key())
    return 0


def cmd_check(args) -> int:
    problem = picker.problem_for()
    path = args.file or picker.solution_path(problem)
    payload = submit.check(problem["slug"], path, with_stress=not args.quick,
                           allow_push=not args.no_push)
    return show_check(payload)


def cmd_hint(args) -> int:
    problem = picker.problem_for()
    outcome = submit.next_hint(problem["slug"])
    print()
    if outcome["exhausted"]:
        print(c("  No hints left. `python leet.py solution` shows a full answer.", YELLOW))
        for pitfall in problem.get("pitfalls", []):
            print(c(f"    - {pitfall}", DIM))
    else:
        label = c(f"Hint {outcome['shown']}/{outcome['total']}", BOLD)
        print(f"  {label}  {outcome['hint']}")
    print()
    return 0


def cmd_solution(args) -> int:
    problem = picker.problem_for()
    print()
    print(rule("="))
    print(f"  Reference solution — {c(problem['title'], BOLD)}")
    print(f"  {problem['target']['time']} time, {problem['target']['space']} space")
    print(rule("="))
    print(problem["solution"].strip())
    print()
    if problem.get("pitfalls"):
        print(c("  Watch out for", BOLD))
        for pitfall in problem["pitfalls"]:
            print(c(f"    - {pitfall}", DIM))
        print()
    return 0


def cmd_stats(args) -> int:
    info = picker.summary()
    print()
    print(rule("="))
    print(c("  PROGRESS", BOLD))
    print(rule("="))
    print(f"  solved      {c(str(info['solved']), GREEN)} of {info['bank']['total']} "
          f"({info['by_difficulty']['Easy']} easy, {info['by_difficulty']['Medium']} medium)")
    print(f"  attempted   {info['attempted']}")
    print(f"  streak      {c(str(info['streak']), CYAN)} day(s)")
    print(f"  bank        {info['bank']['easy']} easy / {info['bank']['medium']} medium")

    git = gitsync.status()
    print()
    print(c("  GIT", BOLD))
    if not git["is_repo"]:
        print(c("    not a git repository yet (created on your first passing submission)", DIM))
    else:
        print(f"    branch      {git['branch']}")
        print(f"    remote      {git['remote'] or c('none', DIM)}")
        print(f"    auto push   {'on' if git['auto_push'] else 'off'}")
        if git["last_commit"]:
            print(f"    last commit {c(git['last_commit'], DIM)}")
        if git["unpushed"]:
            print(c(f"    {git['unpushed']} commit(s) not pushed yet", YELLOW))

    recent = sorted(info["assignments"].items())[-10:]
    if recent:
        print()
        print(c("  RECENT", BOLD))
        for date_key, slug in recent:
            record = info["records"].get(slug, {})
            mark = c("done", GREEN) if record.get("solved") else c("open", YELLOW)
            print(f"    {date_key}  {mark}  {slug}")
    print()
    return 0


def cmd_list(args) -> int:
    state = picker.load_state()
    print()
    for problem in bank.all_problems():
        record = state["records"].get(problem["slug"], {})
        mark = c("x", GREEN) if record.get("solved") else " "
        colour = GREEN if problem["difficulty"] == "Easy" else YELLOW
        print(f"  [{mark}] {c(problem['difficulty'][:1], colour)}  "
              f"{problem['title']:<48} {c(', '.join(problem['topics'][:2]), DIM)}")
    stats = bank.stats()
    print(f"\n  {stats['total']} problems — {stats['easy']} easy, {stats['medium']} medium\n")
    return 0


def cmd_serve(args) -> int:
    from dlc import server

    port = args.port or config.get("server_port")
    url = f"http://127.0.0.1:{port}/"
    print()
    print(rule("="))
    print(f"  daily-leetcode UI  ->  {c(url, CYAN)}")
    print(c("  Ctrl+C to stop", DIM))
    print(rule("="))
    print()
    if not args.no_browser:
        webbrowser.open(url)
    server.serve(port)
    return 0


def cmd_selftest(args) -> int:
    """Every reference solution must pass its own tests."""
    from dlc import harness

    failures = []
    problems = bank.all_problems()
    for problem in problems:
        try:
            func = harness.load_reference(problem)
        except Exception as exc:
            failures.append((problem["slug"], f"reference failed to load: {exc}"))
            continue
        for i, case in enumerate(problem["tests"]):
            try:
                got, _ = harness.run_case(problem, func, case["args"])
                if not harness.matches(problem["compare"], got, case["expect"]):
                    failures.append((problem["slug"],
                                     f"case {i + 1}: expected {case['expect']!r}, got {got!r}"))
            except Exception as exc:
                failures.append((problem["slug"], f"case {i + 1}: {type(exc).__name__}: {exc}"))
        if args.stress and problem.get("stress"):
            try:
                harness.run_case(problem, func, problem["stress"]["args"]())
            except Exception as exc:
                failures.append((problem["slug"], f"stress: {type(exc).__name__}: {exc}"))

    print()
    if failures:
        for slug, detail in failures:
            print(f"  {c('FAIL', RED)}  {slug}: {detail}")
        print(f"\n  {len(failures)} problem(s) in the bank are broken\n")
        return 1
    print(f"  {c('OK', GREEN)}  {len(problems)} problems, "
          f"{sum(len(p['tests']) for p in problems)} cases, all references agree\n")
    return 0


def cmd_config(args) -> int:
    values = config.load()
    if args.key is None:
        print()
        for key, value in sorted(values.items()):
            print(f"  {key:<16} {value}")
        print(f"\n  edit {c(config.CONFIG_PATH, DIM)}\n")
        return 0
    if args.value is None:
        print(values.get(args.key))
        return 0
    parsed = args.value
    if parsed.lower() in ("true", "false"):
        parsed = parsed.lower() == "true"
    elif parsed.isdigit():
        parsed = int(parsed)
    config.set_value(args.key, parsed)
    print(f"  {args.key} = {parsed}")
    return 0


# --------------------------------------------------------------------------- #
def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="leet", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest="command")

    p = subparsers.add_parser("today", help="show today's problem")
    p.set_defaults(func=cmd_today, reroll=False)

    p = subparsers.add_parser("reroll", help="draw a different problem for today")
    p.set_defaults(func=cmd_today, reroll=True)

    p = subparsers.add_parser("check", help="run the tests and get feedback")
    p.add_argument("--file", help="check a specific file instead of today's")
    p.add_argument("--quick", action="store_true", help="skip the large stress input")
    p.add_argument("--no-push", action="store_true", help="do not commit/push on success")
    p.set_defaults(func=cmd_check)

    p = subparsers.add_parser("hint", help="reveal the next hint")
    p.set_defaults(func=cmd_hint)

    p = subparsers.add_parser("solution", help="show the reference solution")
    p.set_defaults(func=cmd_solution)

    p = subparsers.add_parser("stats", help="progress, streak and git status")
    p.set_defaults(func=cmd_stats)

    p = subparsers.add_parser("list", help="list the whole problem bank")
    p.set_defaults(func=cmd_list)

    p = subparsers.add_parser("serve", help="start the local web UI")
    p.add_argument("--port", type=int)
    p.add_argument("--no-browser", action="store_true")
    p.set_defaults(func=cmd_serve)

    p = subparsers.add_parser("selftest", help="check the problem bank itself")
    p.add_argument("--stress", action="store_true", help="also run the large inputs")
    p.set_defaults(func=cmd_selftest)

    p = subparsers.add_parser("config", help="read or write config.json")
    p.add_argument("key", nargs="?")
    p.add_argument("value", nargs="?")
    p.set_defaults(func=cmd_config)

    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        return cmd_today(argparse.Namespace(reroll=False))
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
