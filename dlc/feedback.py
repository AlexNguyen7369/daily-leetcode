"""Turns a test run plus the source code into concrete advice.

Notes have a level:
    fail  - it does not work yet
    warn  - it works (or nearly does) but something will bite you
    tip   - style / idiom / interview polish
    good  - worth knowing you got this right
"""

from __future__ import annotations

import ast
from typing import Any, Dict, List, Optional

Note = Dict[str, str]


def _note(level: str, title: str, detail: str = "") -> Note:
    return {"level": level, "title": title, "detail": detail}


# --------------------------------------------------------------------------- #
# static analysis
# --------------------------------------------------------------------------- #
class _Analysis:
    def __init__(self) -> None:
        self.max_loop_depth = 0
        self.recursive = False
        self.has_memo = False
        self.sorts = False
        self.list_pop_zero: Optional[int] = None
        self.insert_zero: Optional[int] = None
        self.linear_scan_in_loop: List[str] = []
        self.membership_in_loop: Optional[int] = None
        self.str_concat_in_loop: Optional[int] = None
        self.prints: List[int] = []
        self.globals_used = False
        self.body_lines = 0
        self.returns = 0
        self.only_pass = False
        self.deque_used = False
        self.max_if_depth = 0


def _collect_list_names(tree: ast.AST) -> set:
    """Names that were assigned a list literal / list() / comprehension."""
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            value = node.value
            is_list = (
                isinstance(value, (ast.List, ast.ListComp))
                or (isinstance(value, ast.Call) and isinstance(value.func, ast.Name)
                    and value.func.id in ("list", "sorted"))
            )
            if is_list:
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        names.add(target.id)
    return names


def _collect_str_names(tree: ast.AST) -> set:
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
            if isinstance(node.value.value, str):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        names.add(target.id)
    return names


def analyse_source(source: str, func_name: str) -> Optional[_Analysis]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None

    target = None
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == func_name:
            target = node
            break
    if target is None:
        return None

    a = _Analysis()
    list_names = _collect_list_names(target)
    str_names = _collect_str_names(target)

    a.body_lines = (max(
        (getattr(n, "end_lineno", n.lineno) for n in ast.walk(target) if hasattr(n, "lineno")),
        default=target.lineno,
    ) - target.lineno + 1)

    a.only_pass = len(target.body) == 1 and isinstance(target.body[0], (ast.Pass, ast.Expr))

    for decorator in target.decorator_list:
        text = ast.unparse(decorator)
        if "cache" in text:
            a.has_memo = True

    def walk(node: ast.AST, loop_depth: int, if_depth: int) -> None:
        a.max_loop_depth = max(a.max_loop_depth, loop_depth)
        a.max_if_depth = max(a.max_if_depth, if_depth)

        for child in ast.iter_child_nodes(node):
            child_loop = loop_depth
            child_if = if_depth

            if isinstance(child, (ast.For, ast.While, ast.AsyncFor)):
                child_loop += 1
            elif isinstance(child, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                child_loop += len(child.generators)
            elif isinstance(child, ast.If):
                child_if += 1

            if isinstance(child, ast.Return):
                a.returns += 1
            elif isinstance(child, ast.Global):
                a.globals_used = True
            elif isinstance(child, ast.Subscript) and isinstance(child.ctx, ast.Store):
                a.has_memo = True
            elif isinstance(child, ast.Compare):
                for op, comparator in zip(child.ops, child.comparators):
                    if isinstance(op, (ast.In, ast.NotIn)) and loop_depth > 0:
                        if isinstance(comparator, ast.List) or (
                            isinstance(comparator, ast.Name) and comparator.id in list_names
                        ):
                            a.membership_in_loop = a.membership_in_loop or child.lineno
            elif isinstance(child, ast.AugAssign):
                if (isinstance(child.op, ast.Add) and loop_depth > 0
                        and isinstance(child.target, ast.Name) and child.target.id in str_names):
                    a.str_concat_in_loop = a.str_concat_in_loop or child.lineno
            elif isinstance(child, ast.Call):
                fn = child.func
                if isinstance(fn, ast.Name):
                    if fn.id == func_name:
                        a.recursive = True
                    elif fn.id == "sorted":
                        a.sorts = True
                    elif fn.id == "print":
                        a.prints.append(child.lineno)
                    elif fn.id == "deque":
                        a.deque_used = True
                elif isinstance(fn, ast.Attribute):
                    if fn.attr == "sort":
                        a.sorts = True
                    elif fn.attr == "deque":
                        a.deque_used = True
                    elif fn.attr == "pop" and child.args:
                        arg = child.args[0]
                        if isinstance(arg, ast.Constant) and arg.value == 0:
                            a.list_pop_zero = a.list_pop_zero or child.lineno
                    elif fn.attr == "insert" and child.args:
                        arg = child.args[0]
                        if isinstance(arg, ast.Constant) and arg.value == 0:
                            a.insert_zero = a.insert_zero or child.lineno
                    elif fn.attr in ("count", "index") and loop_depth > 0:
                        a.linear_scan_in_loop.append(f"{fn.attr}() on line {child.lineno}")

            walk(child, child_loop, child_if)

    walk(target, 0, 0)
    return a


# --------------------------------------------------------------------------- #
# the report
# --------------------------------------------------------------------------- #
def _target_exponent(target_time: str) -> float:
    text = target_time.lower()
    if "n^3" in text:
        return 3.0
    if "n^2" in text or "n*m" in text or "m*n" in text or "n * m" in text or "m * n" in text:
        return 2.0
    return 1.0


def build(problem: Dict[str, Any], result: Dict[str, Any], source: str) -> List[Note]:
    notes: List[Note] = []
    func = problem["func"]

    # ---- did it even load ------------------------------------------------- #
    if result.get("harness_error"):
        notes.append(_note("fail", "The test runner itself failed to start",
                           result["harness_error"].strip().splitlines()[-1]))
        notes.append(_note("tip", "This is a bug in the checker, not in your solution",
                           "Run `python leet.py selftest` to confirm the installation."))
        return notes

    if result.get("import_error"):
        notes.append(_note("fail", "Your file raised an error while being imported",
                           result["import_error"].strip().splitlines()[-1]))
        notes.append(_note("tip", "Fix the import/syntax error first",
                           "Nothing below could be checked until the module loads."))
        return notes

    if not result.get("func_found"):
        notes.append(_note("fail", f"No function named `{func}` was found",
                           f"The checker calls `{func}(...)`. Keep the given signature — "
                           "you can add helper functions around it."))
        return notes

    analysis = analyse_source(source, func)
    if analysis is not None and analysis.only_pass:
        notes.append(_note("fail", "The function body is still a stub",
                           "Write your solution inside it, then check again."))
        return notes

    # ---- correctness ------------------------------------------------------ #
    failed = [c for c in result["cases"] if not c["ok"]]
    errored = [c for c in failed if c.get("error")]

    if result["timed_out"]:
        idx = result.get("timeout_index")
        where = "the large stress input" if idx == -1 else (
            f"test case {idx + 1}" if isinstance(idx, int) else "one of the cases")
        notes.append(_note("fail", f"The run was killed for taking too long, on {where}",
                           "That is either an infinite loop, or a complexity far above the "
                           f"target of {problem['target']['time']}."))

    if errored:
        first = errored[0]
        last_line = first["error"].strip().splitlines()[-1]
        notes.append(_note("fail", f"{len(errored)} case(s) raised an exception",
                           f"e.g. args={_brief(first['args'])} -> {last_line}"))
        if "IndexError" in first["error"]:
            notes.append(_note("tip", "IndexError usually means an unguarded boundary",
                               "Check the empty input, the single-element input, and any i+1 / "
                               "i-1 access at the ends."))
        if "TypeError" in first["error"] and "NoneType" in first["error"]:
            notes.append(_note("tip", "Something is None that you expected to be a value",
                               "A missing `return` makes a function hand back None — that is the "
                               "usual cause."))
        if "RecursionError" in first["error"]:
            notes.append(_note("tip", "Recursion is not terminating",
                               "Make sure every path reduces the problem and that the base case "
                               "is reachable."))

    wrong = [c for c in failed if not c.get("error")]
    if wrong:
        first = wrong[0]
        notes.append(_note(
            "fail",
            f"{len(wrong)} case(s) returned the wrong answer",
            f"args={_brief(first['args'])}\n     expected {_brief(first['expect'])}\n"
            f"     got      {_brief(first['got'])}",
        ))
        edge = _edge_case_hint(first["args"])
        if edge:
            notes.append(_note("tip", "That failing case looks like an edge case", edge))

    stress = result.get("stress")
    if stress and not stress["ok"] and not stress.get("error"):
        notes.append(_note("fail", "The large input produced a different answer than the reference",
                           "Small cases pass but a big random one does not — usually a "
                           "dedup, overflow-of-logic or tie-breaking bug."))
    elif stress and stress.get("error"):
        notes.append(_note("fail", "The large input raised an error",
                           stress["error"].strip().splitlines()[-1]))

    # ---- performance ------------------------------------------------------ #
    if stress and stress["ok"] and not result["timed_out"]:
        ratio = stress["ms"] / max(stress["budget"], 1.0)
        if ratio > 1.0:
            notes.append(_note(
                "warn",
                f"Correct, but slow on the big input ({stress['ms']:.0f} ms vs a "
                f"{stress['budget']:.0f} ms budget)",
                f"The intended complexity is {problem['target']['time']}. On LeetCode this is "
                "the difference between Accepted and Time Limit Exceeded.",
            ))
        elif ratio < 0.35:
            notes.append(_note("good", f"Fast on the large input ({stress['ms']:.0f} ms, "
                                       f"budget {stress['budget']:.0f} ms)"))

    # ---- static analysis -------------------------------------------------- #
    if analysis is not None:
        notes.extend(_static_notes(problem, analysis, result))

    # ---- closing ---------------------------------------------------------- #
    if result["all_passed"]:
        notes.insert(0, _note("good", f"All {result['total']} tests passed"
                              + (" plus the large stress input" if stress else "")))
        notes.append(_note("tip", "Target complexity for this problem",
                           f"time {problem['target']['time']}, space {problem['target']['space']}"
                           " — run `python leet.py solution` to compare with a reference answer."))
    elif not failed and not result["timed_out"]:
        notes.append(_note("warn", "The visible tests passed but something else did not",
                           "See the notes above."))

    return notes


def _static_notes(problem: Dict[str, Any], a: _Analysis, result: Dict[str, Any]) -> List[Note]:
    notes: List[Note] = []
    target_exp = _target_exponent(problem["target"]["time"])

    if a.max_loop_depth >= 2 and target_exp < 2:
        notes.append(_note(
            "warn",
            f"There are {a.max_loop_depth} nested loops, but the target is "
            f"{problem['target']['time']}",
            "Nested iteration over the same data is the usual sign of a brute-force pass. "
            "Ask what you could remember from the first pass to avoid the second.",
        ))

    if a.membership_in_loop:
        notes.append(_note(
            "warn",
            f"`x in <list>` inside a loop (line {a.membership_in_loop})",
            "Membership on a list is O(n), which quietly multiplies your complexity. "
            "A set or dict makes it O(1).",
        ))

    if a.linear_scan_in_loop:
        notes.append(_note(
            "warn",
            "Linear scans inside a loop: " + ", ".join(a.linear_scan_in_loop[:3]),
            ".count() and .index() each walk the whole sequence, so calling them per element "
            "is quadratic. Count once into a dict instead.",
        ))

    if a.list_pop_zero:
        notes.append(_note(
            "warn",
            f"`list.pop(0)` on line {a.list_pop_zero}",
            "Popping the front of a list shifts every remaining element — O(n) per call. "
            "collections.deque().popleft() is O(1) and is what BFS queues want.",
        ))

    if a.insert_zero:
        notes.append(_note("warn", f"`list.insert(0, ...)` on line {a.insert_zero}",
                           "Also O(n) per call. Append and reverse at the end, or use a deque."))

    if a.str_concat_in_loop:
        notes.append(_note(
            "tip",
            f"String built with `+=` in a loop (line {a.str_concat_in_loop})",
            "Strings are immutable, so each += copies. Collect the pieces in a list and "
            "''.join(...) at the end.",
        ))

    if a.recursive and not a.has_memo and "Dynamic Programming" in problem["topics"]:
        notes.append(_note(
            "warn",
            "Recursion on a DP problem with no memoisation in sight",
            "Overlapping subproblems get recomputed exponentially. Cache on the arguments "
            "(a dict, or @functools.cache) or rewrite it bottom-up.",
        ))

    if a.sorts and problem["target"]["time"].strip() in ("O(n)", "O(n) average"):
        notes.append(_note(
            "tip",
            "You sort, but the target is linear",
            f"Sorting locks you at O(n log n); {problem['target']['time']} is reachable here. "
            "Worth knowing the linear approach for an interview.",
        ))

    if a.prints:
        notes.append(_note("tip", f"print() left in the solution (line {a.prints[0]})",
                           "Harmless here, but it is noise in a submission — and it slows down "
                           "large runs a lot."))

    if a.globals_used:
        notes.append(_note("tip", "`global` inside the solution",
                           "State that survives between calls will corrupt the next test case. "
                           "Prefer a nested function with `nonlocal`, or pass state as arguments."))

    if a.max_if_depth >= 4:
        notes.append(_note("tip", f"Conditionals nested {a.max_if_depth} deep",
                           "Deep nesting is where off-by-one bugs hide. Early `return`s and "
                           "guard clauses usually flatten it."))

    if a.body_lines > 60:
        notes.append(_note("tip", f"The function is {a.body_lines} lines long",
                           "Long enough that an interviewer would lose the thread. Consider "
                           "naming a piece of it as a helper."))

    if result["all_passed"] and a.max_loop_depth <= 1 and target_exp == 1.0:
        notes.append(_note("good", "Single pass over the input — this matches the intended "
                                   "complexity"))

    if result["all_passed"] and a.deque_used:
        notes.append(_note("good", "Using collections.deque for the queue — the right call"))

    return notes


def _edge_case_hint(args: Any) -> str:
    try:
        first = args[0]
    except (IndexError, TypeError):
        return ""
    if isinstance(first, (list, str)) and len(first) == 0:
        return "The input is empty. Handle it before the main loop."
    if isinstance(first, (list, str)) and len(first) == 1:
        return "A single-element input often skips loops entirely — check what you return then."
    if isinstance(first, list) and len(first) == 2:
        return "Two elements is the smallest case where two pointers can cross. Check the boundary."
    if isinstance(first, int) and first in (0, 1):
        return "Small integers (0 and 1) are usually the base cases."
    if isinstance(first, list) and len(set(map(str, first))) < len(first):
        return "This input contains duplicates — make sure they are handled the way the "\
               "statement requires."
    return ""


def _brief(value: Any, limit: int = 120) -> str:
    text = repr(value)
    return text if len(text) <= limit else text[: limit - 3] + "..."
