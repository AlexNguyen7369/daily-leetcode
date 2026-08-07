"""Commits and pushes a passing solution.

Deliberately narrow: only the solution file you just passed and the schedule
state file are ever staged. Nothing in `dlc/` (the checker, the problem bank,
the server) is touched by a submission, so pushing an answer can never change
how the system behaves afterwards.

Every failure here is non-fatal — a broken remote must never turn a passing
submission into a failure.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from typing import Any, Dict, List, Optional

from dlc import config

ROOT = config.ROOT

# git must never stop and wait for a username/password prompt: this runs
# behind a web request.
_ENV = {**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "never"}

GITIGNORE = """\
__pycache__/
*.py[cod]
.venv/
venv/
.env
.idea/
.vscode/
.DS_Store
scratch/
"""


def _git(*args: str, timeout: int = 60) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        env=_ENV,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def git_available() -> bool:
    return shutil.which("git") is not None


def is_repo() -> bool:
    if not git_available():
        return False
    try:
        return _git("rev-parse", "--is-inside-work-tree").returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def current_branch() -> Optional[str]:
    try:
        result = _git("rev-parse", "--abbrev-ref", "HEAD")
        name = result.stdout.strip()
        return name if result.returncode == 0 and name and name != "HEAD" else None
    except (OSError, subprocess.SubprocessError):
        return None


def remote_url() -> Optional[str]:
    try:
        result = _git("remote", "get-url", "origin")
        return result.stdout.strip() if result.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


def ensure_repo() -> Dict[str, Any]:
    """Create the repo, the .gitignore and the origin remote if they are missing."""
    steps: List[str] = []
    if not git_available():
        return {"ok": False, "steps": steps, "error": "git is not installed or not on PATH"}

    branch = config.get("branch") or "main"
    if not is_repo():
        result = _git("init", "-b", branch)
        if result.returncode != 0:  # older git without -b
            result = _git("init")
            if result.returncode == 0:
                _git("checkout", "-b", branch)
        if result.returncode != 0:
            return {"ok": False, "steps": steps, "error": result.stderr.strip()}
        steps.append(f"initialised a git repository on branch {branch}")

    gitignore = os.path.join(ROOT, ".gitignore")
    if not os.path.exists(gitignore):
        with open(gitignore, "w", encoding="utf-8") as handle:
            handle.write(GITIGNORE)
        steps.append("wrote .gitignore")

    wanted_remote = config.get("remote")
    if wanted_remote and remote_url() is None:
        result = _git("remote", "add", "origin", wanted_remote)
        if result.returncode == 0:
            steps.append(f"added remote origin -> {wanted_remote}")

    if _git("config", "user.email").returncode != 0:
        _git("config", "user.email", "daily-leetcode@localhost")
        _git("config", "user.name", "daily-leetcode")
        steps.append("set a local git identity (override with `git config user.name/email`)")

    return {"ok": True, "steps": steps, "error": None}


def status() -> Dict[str, Any]:
    info: Dict[str, Any] = {
        "git_available": git_available(),
        "is_repo": is_repo(),
        "branch": None,
        "remote": None,
        "auto_push": bool(config.get("auto_push")),
        "last_commit": None,
        "unpushed": None,
    }
    if not info["is_repo"]:
        return info

    info["branch"] = current_branch()
    info["remote"] = remote_url()
    try:
        last = _git("log", "-1", "--pretty=%h %s")
        if last.returncode == 0:
            info["last_commit"] = last.stdout.strip()
        counts = _git("rev-list", "--count", "@{u}..HEAD")
        if counts.returncode == 0:
            info["unpushed"] = int(counts.stdout.strip() or 0)
    except (OSError, ValueError, subprocess.SubprocessError):
        pass
    return info


def sync_solution(solution_path: str, problem: Dict[str, Any], date_key: str) -> Dict[str, Any]:
    """Stage exactly the solution + state, commit, and push. Never raises."""
    outcome: Dict[str, Any] = {
        "attempted": True,
        "committed": False,
        "pushed": False,
        "skipped": None,
        "commit": None,
        "steps": [],
        "error": None,
    }

    if not config.get("auto_push"):
        outcome.update(attempted=False, skipped="auto_push is turned off in config.json")
        return outcome

    try:
        prepared = ensure_repo()
        outcome["steps"].extend(prepared["steps"])
        if not prepared["ok"]:
            outcome["error"] = prepared["error"]
            return outcome

        # --- stage only what this submission owns -------------------------- #
        paths = [os.path.relpath(solution_path, ROOT).replace("\\", "/")]
        state_file = "state/state.json"
        if os.path.exists(os.path.join(ROOT, state_file)):
            paths.append(state_file)

        for path in paths:
            result = _git("add", "--", path)
            if result.returncode != 0:
                outcome["error"] = f"git add {path}: {result.stderr.strip()}"
                return outcome

        staged = _git("diff", "--cached", "--name-only").stdout.split()
        if not staged:
            outcome["skipped"] = "no changes to commit (already synced)"
            return outcome

        prefix = config.get("commit_prefix") or "solve"
        message = (
            f"{prefix}: {problem['title']} ({problem['difficulty']})\n\n"
            f"Problem: {problem['url']}\n"
            f"Topics:  {', '.join(problem['topics'])}\n"
            f"Solved:  {date_key}\n"
            f"All hidden tests passed via `leet check`."
        )
        committed = _git("commit", "-m", message)
        if committed.returncode != 0:
            outcome["error"] = committed.stderr.strip() or committed.stdout.strip()
            return outcome
        outcome["committed"] = True
        outcome["commit"] = _git("log", "-1", "--pretty=%h %s").stdout.strip()
        outcome["steps"].append(f"committed {', '.join(staged)}")

        # --- push ---------------------------------------------------------- #
        if remote_url() is None:
            outcome["skipped"] = "committed locally; no `origin` remote is configured"
            return outcome

        branch = current_branch() or config.get("branch") or "main"
        pushed = _git("push", "-u", "origin", branch, timeout=120)
        if pushed.returncode == 0:
            outcome["pushed"] = True
            outcome["steps"].append(f"pushed to origin/{branch}")
        else:
            outcome["error"] = (pushed.stderr.strip() or pushed.stdout.strip()
                                or "git push failed")
    except subprocess.TimeoutExpired:
        outcome["error"] = ("git timed out — it is probably waiting for credentials. "
                            "Run `git push` once in a terminal to store them.")
    except Exception as exc:  # never let git break a passing submission
        outcome["error"] = f"{type(exc).__name__}: {exc}"

    return outcome
