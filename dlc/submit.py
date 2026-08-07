"""One entry point used by both the CLI and the web UI.

check() -> run the tests, build the advice, record the attempt, and (only when
everything passes) commit and push the solution.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

from dlc import bank, feedback, gitsync, picker, runner


def read_source(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()
    except OSError:
        return ""


def check(slug: str, solution_path: str, date_key: Optional[str] = None,
          with_stress: bool = True, allow_push: bool = True) -> Dict[str, Any]:
    problem = bank.get(slug)
    date_key = date_key or picker.today_key()

    if not os.path.exists(solution_path):
        return {
            "problem": _problem_summary(problem),
            "error": f"no solution file at {solution_path}",
            "result": None,
            "notes": [],
            "git": None,
        }

    result = runner.run(slug, solution_path, with_stress=with_stress)
    source = read_source(solution_path)
    notes = feedback.build(problem, result, source)

    slowest = max((c["ms"] for c in result["cases"]), default=None)
    picker.record_attempt(slug, date_key, result["all_passed"], slowest)

    git_outcome = None
    if result["all_passed"] and allow_push:
        git_outcome = gitsync.sync_solution(solution_path, problem, date_key)

    return {
        "problem": _problem_summary(problem),
        "error": None,
        "result": result,
        "notes": notes,
        "git": git_outcome,
        "solution_path": solution_path,
    }


def _problem_summary(problem: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "slug": problem["slug"],
        "title": problem["title"],
        "difficulty": problem["difficulty"],
        "topics": problem["topics"],
        "url": problem["url"],
        "func": problem["func"],
        "signature": problem["signature"],
        "description": problem["description"],
        "examples": problem["examples"],
        "constraints": problem["constraints"],
        "target": problem["target"],
        "hint_count": len(problem["hints"]),
        "pitfalls": problem.get("pitfalls", []),
    }


def next_hint(slug: str) -> Dict[str, Any]:
    problem = bank.get(slug)
    state = picker.load_state()
    record = state["records"].setdefault(
        slug, {"attempts": 0, "solved": False, "solved_on": None, "best_ms": None}
    )
    shown = record.get("hints_shown", 0)
    if shown >= len(problem["hints"]):
        return {"hint": None, "shown": shown, "total": len(problem["hints"]),
                "exhausted": True}
    record["hints_shown"] = shown + 1
    picker.save_state(state)
    return {"hint": problem["hints"][shown], "shown": shown + 1,
            "total": len(problem["hints"]), "exhausted": False}


def hints_shown(slug: str) -> int:
    state = picker.load_state()
    return state["records"].get(slug, {}).get("hints_shown", 0)
