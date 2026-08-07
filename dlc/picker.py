"""Chooses the problem of the day, keeps history, and scaffolds solution files.

The schedule is a shuffled deck rather than an independent random draw, so you
never see the same problem twice until the whole bank has been worked through.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import random
from typing import Any, Dict, List, Optional

from dlc import bank, config

ROOT = config.ROOT
STATE_DIR = os.path.join(ROOT, "state")
STATE_PATH = os.path.join(STATE_DIR, "state.json")
SOLUTIONS_DIR = os.path.join(ROOT, "solutions")


# --------------------------------------------------------------------------- #
# state
# --------------------------------------------------------------------------- #
def _blank_state() -> Dict[str, Any]:
    return {"seed": None, "deck": [], "cycle": 1, "assignments": {}, "records": {}}


def load_state() -> Dict[str, Any]:
    if not os.path.exists(STATE_PATH):
        return _blank_state()
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as handle:
            state = json.load(handle)
    except (json.JSONDecodeError, OSError):
        return _blank_state()
    for key, value in _blank_state().items():
        state.setdefault(key, value)
    return state


def save_state(state: Dict[str, Any]) -> None:
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2, sort_keys=True)
        handle.write("\n")


# --------------------------------------------------------------------------- #
# the deck
# --------------------------------------------------------------------------- #
def _eligible() -> List[Dict[str, Any]]:
    mix = config.get("difficulty_mix")
    problems = bank.all_problems()
    if mix == "easy":
        return [p for p in problems if p["difficulty"] == "Easy"]
    if mix == "medium":
        return [p for p in problems if p["difficulty"] == "Medium"]
    return problems


def _build_deck(seed: int, cycle: int) -> List[str]:
    problems = _eligible()
    rng = random.Random(f"{seed}:{cycle}")
    ordered = problems[:]
    rng.shuffle(ordered)

    # Break up runs of three or more problems at the same difficulty so the
    # week actually spans easy through medium.
    for i in range(2, len(ordered)):
        window = ordered[i - 2 : i + 1]
        if len({p["difficulty"] for p in window}) == 1:
            for j in range(i + 1, len(ordered)):
                if ordered[j]["difficulty"] != ordered[i]["difficulty"]:
                    ordered[i], ordered[j] = ordered[j], ordered[i]
                    break
    return [p["slug"] for p in ordered]


def _ensure_deck(state: Dict[str, Any]) -> None:
    if state["seed"] is None:
        configured = config.get("seed")
        state["seed"] = configured if configured is not None else random.randrange(10**9)
    if state["deck"]:
        return

    cycle = state.get("cycle") or 1
    used = set(state["assignments"].values())
    remaining = [slug for slug in _build_deck(state["seed"], cycle) if slug not in used]
    if remaining:
        state["cycle"] = cycle
        state["deck"] = remaining
        return

    # Every problem in the bank has been handed out — start a fresh cycle.
    state["cycle"] = cycle + 1
    state["deck"] = _build_deck(state["seed"], state["cycle"])


# --------------------------------------------------------------------------- #
# assignment
# --------------------------------------------------------------------------- #
def today_key() -> str:
    return dt.date.today().isoformat()


def problem_for(date_key: Optional[str] = None, *, reroll: bool = False) -> Dict[str, Any]:
    date_key = date_key or today_key()
    state = load_state()

    if reroll:
        state["assignments"].pop(date_key, None)

    slug = state["assignments"].get(date_key)
    if slug is None or not _slug_exists(slug):
        _ensure_deck(state)
        slug = state["deck"].pop(0)
        state["assignments"][date_key] = slug
        save_state(state)

    return bank.get(slug)


def _slug_exists(slug: str) -> bool:
    try:
        bank.get(slug)
        return True
    except KeyError:
        return False


def record_attempt(slug: str, date_key: str, passed: bool, ms: Optional[float] = None) -> None:
    state = load_state()
    record = state["records"].setdefault(
        slug, {"attempts": 0, "solved": False, "solved_on": None, "best_ms": None}
    )
    record["attempts"] += 1
    if passed:
        if not record["solved"]:
            record["solved"] = True
            record["solved_on"] = date_key
        if ms is not None and (record["best_ms"] is None or ms < record["best_ms"]):
            record["best_ms"] = ms
    save_state(state)


def summary() -> Dict[str, Any]:
    state = load_state()
    records = state["records"]
    solved = [slug for slug, r in records.items() if r["solved"]]
    solved_dates = sorted({r["solved_on"] for r in records.values() if r["solved_on"]})

    streak = 0
    if solved_dates:
        cursor = dt.date.today()
        as_set = set(solved_dates)
        if cursor.isoformat() not in as_set:
            cursor -= dt.timedelta(days=1)
        while cursor.isoformat() in as_set:
            streak += 1
            cursor -= dt.timedelta(days=1)

    by_difficulty = {"Easy": 0, "Medium": 0}
    for slug in solved:
        try:
            by_difficulty[bank.get(slug)["difficulty"]] += 1
        except KeyError:
            pass

    return {
        "solved": len(solved),
        "attempted": len(records),
        "bank": bank.stats(),
        "streak": streak,
        "by_difficulty": by_difficulty,
        "assignments": state["assignments"],
        "records": records,
    }


# --------------------------------------------------------------------------- #
# scaffolding
# --------------------------------------------------------------------------- #
TEMPLATE = '''"""
{title}  -  {difficulty}
{topics}
{url}

Assigned: {date}

{description}

Examples
--------
{examples}

Constraints
-----------
{constraints}

Target complexity: {time} time, {space} space

  Check it        python leet.py check
  Nudge           python leet.py hint
  Reference       python leet.py solution
  Browser UI      python leet.py serve
"""

from typing import List, Optional
{extra_imports}

# ==========================================================================
#  YOUR SOLUTION
# ==========================================================================
{signature}
    pass


# ==========================================================================
#  SCRATCH TESTS - yours to play with.
#  `python leet.py check` runs the full hidden suite; this block is just for
#  poking at the function while you work.  Run it with:  python "{filename}"
# ==========================================================================
if __name__ == "__main__":
{scratch}
'''


def solution_path(problem: Dict[str, Any], date_key: Optional[str] = None) -> str:
    date_key = date_key or today_key()
    return os.path.join(SOLUTIONS_DIR, f"{date_key}_{problem['slug']}.py")


def _scratch_block(problem: Dict[str, Any]) -> str:
    lines = []
    for case in problem["tests"][:3]:
        args = ", ".join(repr(a) for a in case["args"])
        lines.append(f"    print({problem['func']}({args}))")
        lines.append(f"    #  expected: {case['expect']!r}")
    return "\n".join(lines)


def ensure_solution_file(problem: Dict[str, Any], date_key: Optional[str] = None) -> str:
    date_key = date_key or today_key()
    path = solution_path(problem, date_key)
    if os.path.exists(path):
        return path

    os.makedirs(SOLUTIONS_DIR, exist_ok=True)
    needs_nodes = any(spec in ("linked", "linked_cycle", "tree", "node_in_0")
                      for spec in problem["argspec"])
    extra = ("from dlc.structures import ListNode, TreeNode  # noqa: F401\n"
             if needs_nodes else "")

    body = TEMPLATE.format(
        title=problem["title"],
        difficulty=problem["difficulty"],
        topics=", ".join(problem["topics"]),
        url=problem["url"],
        date=date_key,
        description=problem["description"],
        examples="\n".join(f"  {line}" for line in problem["examples"]),
        constraints="\n".join(f"  - {line}" for line in problem["constraints"]),
        time=problem["target"]["time"],
        space=problem["target"]["space"],
        signature=problem["signature"],
        extra_imports=extra,
        filename=os.path.basename(path),
        scratch=_scratch_block(problem),
    )
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(body)
    return path
