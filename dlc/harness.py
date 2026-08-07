"""Argument conversion, result conversion and answer comparison.

Imported by both the checker (parent process) and the sandboxed worker.
"""

from __future__ import annotations

import copy
import time
from typing import Any, Dict, List, Tuple

from dlc import structures


# --------------------------------------------------------------------------- #
# conversion
# --------------------------------------------------------------------------- #
def convert_args(argspec: List[str], raw_args: List[Any]) -> List[Any]:
    converted: List[Any] = []
    for spec, value in zip(argspec, raw_args):
        value = copy.deepcopy(value)
        if spec == "raw":
            converted.append(value)
        elif spec == "linked":
            converted.append(structures.build_linked(value))
        elif spec == "linked_cycle":
            converted.append(structures.build_cycle(value))
        elif spec == "tree":
            converted.append(structures.build_tree(value))
        elif spec == "node_in_0":
            converted.append(structures.find_node(converted[0], value))
        else:
            raise ValueError(f"unknown argspec: {spec}")
    return converted


def convert_result(retspec: str, result: Any) -> Any:
    if retspec == "raw":
        return result
    if retspec == "none":
        return None
    if retspec == "linked":
        return structures.linked_to_list(result)
    if retspec == "tree":
        return structures.tree_to_list(result)
    if retspec == "node_val":
        return None if result is None else result.val
    raise ValueError(f"unknown retspec: {retspec}")


# --------------------------------------------------------------------------- #
# comparison
# --------------------------------------------------------------------------- #
def _sort_key(item: Any):
    return (str(type(item).__name__), item if isinstance(item, (int, float, str)) else str(item))


def observed_value(problem: Dict[str, Any], result: Any, converted_args: List[Any]) -> Any:
    """What the solution actually produced, in comparable/printable form."""
    mode = problem["compare"]
    if mode == "inplace":
        return converted_args[0]
    if mode == "inplace_linked":
        return structures.linked_to_list(converted_args[0])
    return convert_result(problem["retspec"], result)


def matches(mode: str, got: Any, expect: Any) -> bool:
    if mode in ("exact", "inplace", "inplace_linked"):
        return got == expect
    if mode == "sorted":
        try:
            return sorted(got) == sorted(expect)
        except TypeError:
            return sorted(got, key=_sort_key) == sorted(expect, key=_sort_key)
    if mode == "sorted_inner":
        if not isinstance(got, list):
            return False
        try:
            g = sorted([sorted(item) for item in got])
            e = sorted([sorted(item) for item in expect])
        except TypeError:
            return False
        return g == e
    if mode == "any_of":
        return got in expect
    if mode == "approx":
        try:
            return abs(got - expect) < 1e-6
        except TypeError:
            return False
    raise ValueError(f"unknown compare mode: {mode}")


# --------------------------------------------------------------------------- #
# running a single case
# --------------------------------------------------------------------------- #
def run_case(problem: Dict[str, Any], func, raw_args: List[Any]) -> Tuple[Any, float]:
    """Call `func` on a fresh copy of `raw_args`. Returns (observed, elapsed_ms)."""
    converted = convert_args(problem["argspec"], raw_args)
    start = time.perf_counter()
    result = func(*converted)
    elapsed = (time.perf_counter() - start) * 1000.0
    return observed_value(problem, result, converted), elapsed


def load_reference(problem: Dict[str, Any]):
    namespace: Dict[str, Any] = {}
    exec(compile(problem["solution"], f"<reference:{problem['slug']}>", "exec"), namespace)
    return namespace[problem["func"]]


# --------------------------------------------------------------------------- #
# display helpers
# --------------------------------------------------------------------------- #
def brief(value: Any, limit: int = 160) -> str:
    text = repr(value)
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def jsonable(value: Any, limit: int = 4000) -> Any:
    """Best-effort conversion to something json.dumps can handle."""
    try:
        import json

        text = json.dumps(value)
        if len(text) <= limit:
            return value
        return brief(value, limit)
    except (TypeError, ValueError):
        return brief(value, limit)
