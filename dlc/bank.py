"""Loads the problem bank and validates its shape.

A problem is a plain dict:

    slug        str   - leetcode slug, unique id in this system
    title       str
    difficulty  "Easy" | "Medium"
    topics      [str]
    url         str
    func        str   - the function name your solution must define
    signature   str   - the stub written into your solution file
    description str
    examples    [str]
    constraints [str]
    hints       [str] - revealed one at a time by `leet hint`
    target      {"time": "O(n)", "space": "O(1)"}
    argspec     [str] - per-argument converter (see runner.CONVERTERS)
    retspec     str   - return converter
    compare     str   - comparator (see runner.COMPARATORS)
    tests       [{"args": [...], "expect": ...}]
    stress      {"args": callable() -> list, "budget": seconds}   (optional)
    pitfalls    [str] (optional)
    solution    str   - reference implementation, also used by `leet selftest`
"""

from __future__ import annotations

import importlib
import pkgutil
from typing import Any, Dict, List

_REQUIRED = (
    "slug", "title", "difficulty", "topics", "url", "func", "signature",
    "description", "examples", "constraints", "hints", "target",
    "argspec", "retspec", "compare", "tests", "solution",
)

_CACHE: List[Dict[str, Any]] | None = None


def all_problems() -> List[Dict[str, Any]]:
    global _CACHE
    if _CACHE is not None:
        return _CACHE

    from dlc import problems as problems_pkg

    found: List[Dict[str, Any]] = []
    for mod in pkgutil.iter_modules(problems_pkg.__path__):
        module = importlib.import_module(f"dlc.problems.{mod.name}")
        found.extend(getattr(module, "PROBLEMS", []))

    seen = set()
    for p in found:
        missing = [k for k in _REQUIRED if k not in p]
        if missing:
            raise ValueError(f"problem {p.get('slug', '?')} missing keys: {missing}")
        if p["slug"] in seen:
            raise ValueError(f"duplicate slug: {p['slug']}")
        if p["difficulty"] not in ("Easy", "Medium"):
            raise ValueError(f"{p['slug']}: difficulty must be Easy or Medium")
        if len(p["argspec"]) != len(p["tests"][0]["args"]):
            raise ValueError(f"{p['slug']}: argspec length != number of test args")
        seen.add(p["slug"])

    found.sort(key=lambda p: p["slug"])
    _CACHE = found
    return _CACHE


def get(slug: str) -> Dict[str, Any]:
    for p in all_problems():
        if p["slug"] == slug:
            return p
    raise KeyError(f"unknown problem: {slug}")


def stats() -> Dict[str, int]:
    probs = all_problems()
    return {
        "total": len(probs),
        "easy": sum(1 for p in probs if p["difficulty"] == "Easy"),
        "medium": sum(1 for p in probs if p["difficulty"] == "Medium"),
    }
