"""Subprocess that executes a solution against a problem's test cases.

Reads a JSON config on stdin, writes one JSON object per line to stdout so the
parent still learns which case was running if we get killed for taking too long.

    {"solution": "...path...", "slug": "two-sum", "stress": true}

Emitted records:
    {"kind": "meta",  "func_found": bool, "import_error": str|null}
    {"kind": "start", "index": int}
    {"kind": "case",  "index": int, "ok": bool, "got": ..., "ms": float,
                      "error": str|null}
    {"kind": "stress","ok": bool, "ms": float, "budget": float, "error": str|null}
    {"kind": "end"}
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import threading
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dlc import bank, harness  # noqa: E402


def emit(record) -> None:
    sys.stdout.write(json.dumps(record, default=str) + "\n")
    sys.stdout.flush()


def load_solution_module(path: str):
    spec = importlib.util.spec_from_file_location("user_solution", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["user_solution"] = module
    spec.loader.exec_module(module)
    return module


def main(config) -> None:
    problem = bank.get(config["slug"])

    try:
        module = load_solution_module(config["solution"])
    except Exception:
        emit({"kind": "meta", "func_found": False, "import_error": traceback.format_exc(limit=6)})
        emit({"kind": "end"})
        return

    func = getattr(module, problem["func"], None)
    if not callable(func):
        emit({"kind": "meta", "func_found": False, "import_error": None})
        emit({"kind": "end"})
        return
    emit({"kind": "meta", "func_found": True, "import_error": None})

    for index, case in enumerate(problem["tests"]):
        emit({"kind": "start", "index": index})
        try:
            got, elapsed = harness.run_case(problem, func, case["args"])
            ok = harness.matches(problem["compare"], got, case["expect"])
            emit({
                "kind": "case",
                "index": index,
                "ok": bool(ok),
                "got": harness.jsonable(got),
                "ms": round(elapsed, 3),
                "error": None,
            })
        except RecursionError:
            emit({"kind": "case", "index": index, "ok": False, "got": None, "ms": 0.0,
                  "error": "RecursionError: the recursion went too deep (infinite recursion, "
                           "or a depth the input does not justify)"})
        except Exception:
            emit({"kind": "case", "index": index, "ok": False, "got": None, "ms": 0.0,
                  "error": traceback.format_exc(limit=4)})

    stress = problem.get("stress")
    if stress and config.get("stress", True):
        emit({"kind": "start", "index": -1})
        try:
            args = stress["args"]()
            expected, _ = harness.run_case(problem, harness.load_reference(problem), args)
            got, elapsed = harness.run_case(problem, func, args)
            ok = harness.matches(problem["compare"], got, expected)
            emit({"kind": "stress", "ok": bool(ok), "ms": round(elapsed, 1),
                  "budget": stress["budget"] * 1000.0, "error": None})
        except RecursionError:
            emit({"kind": "stress", "ok": False, "ms": 0.0, "budget": stress["budget"] * 1000.0,
                  "error": "RecursionError on the large input — recursion depth grows with n here"})
        except Exception:
            emit({"kind": "stress", "ok": False, "ms": 0.0, "budget": stress["budget"] * 1000.0,
                  "error": traceback.format_exc(limit=4)})

    emit({"kind": "end"})


def _grow_stack() -> None:
    """Deep recursion is normal for tree/DFS problems, so run the work on a
    thread with a bigger stack than the default 1 MB. Windows rejects sizes it
    does not like, so try progressively smaller ones."""
    for megabytes in (64, 32, 16, 8):
        try:
            threading.stack_size(megabytes * 1024 * 1024)
            return
        except (ValueError, RuntimeError):
            continue


if __name__ == "__main__":
    cfg = json.loads(sys.stdin.read().lstrip("﻿"))
    sys.setrecursionlimit(60_000)
    _grow_stack()
    worker = threading.Thread(target=main, args=(cfg,))
    worker.start()
    worker.join()
