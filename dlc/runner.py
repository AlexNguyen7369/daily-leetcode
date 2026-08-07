"""Runs a solution file against a problem's tests in a separate process."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import Any, Dict, Optional

from dlc import bank

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _timeout_for(problem: Dict[str, Any], with_stress: bool) -> float:
    budget = 10.0 + 0.5 * len(problem["tests"])
    stress = problem.get("stress")
    if with_stress and stress:
        # generous: the reference run plus a slow-but-not-hopeless user run
        budget += stress["budget"] * 4 + 10.0
    return budget


def run(slug: str, solution_path: str, with_stress: bool = True) -> Dict[str, Any]:
    problem = bank.get(slug)
    config = json.dumps({"slug": slug, "solution": os.path.abspath(solution_path),
                         "stress": with_stress})

    proc = subprocess.Popen(
        [sys.executable, "-X", "utf8", "-m", "dlc._worker"],
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    timed_out = False
    try:
        out, err = proc.communicate(config, timeout=_timeout_for(problem, with_stress))
    except subprocess.TimeoutExpired:
        timed_out = True
        proc.kill()
        out, err = proc.communicate()

    records = []
    for line in (out or "").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            pass  # stray prints from the user's own code

    result: Dict[str, Any] = {
        "slug": slug,
        "func_found": False,
        "import_error": None,
        "harness_error": None,
        "cases": [],
        "stress": None,
        "timed_out": timed_out,
        "timeout_index": None,
        "stderr": (err or "").strip(),
        "stray_output": [
            ln for ln in (out or "").splitlines()
            if ln.strip() and not ln.strip().startswith("{")
        ][:10],
    }

    last_started: Optional[int] = None
    for record in records:
        kind = record.get("kind")
        if kind == "meta":
            result["func_found"] = record["func_found"]
            result["import_error"] = record["import_error"]
        elif kind == "start":
            last_started = record["index"]
        elif kind == "case":
            index = record["index"]
            case = problem["tests"][index]
            record["args"] = case["args"]
            record["expect"] = case["expect"]
            result["cases"].append(record)
            last_started = None
        elif kind == "stress":
            result["stress"] = record
            last_started = None
        elif kind == "end":
            last_started = None

    if timed_out:
        result["timeout_index"] = last_started

    # The worker died before it could report anything: that is our bug, not the
    # user's, and it must not be reported as "your function is missing".
    if not records and not timed_out:
        result["harness_error"] = (err or "").strip() or "the test runner exited unexpectedly"

    result["total"] = len(problem["tests"])
    result["passed"] = sum(1 for c in result["cases"] if c["ok"])
    result["all_passed"] = (
        result["func_found"]
        and not timed_out
        and result["passed"] == result["total"]
        and result["total"] > 0
        and (result["stress"] is None or result["stress"]["ok"])
    )
    return result
