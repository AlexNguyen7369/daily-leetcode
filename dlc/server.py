"""A dependency-free local web UI.

Binds to 127.0.0.1 only. It runs code you type, so it is deliberately not
reachable from other machines, and requests whose Host header is not localhost
are rejected (that blocks DNS-rebinding from a random web page).
"""

from __future__ import annotations

import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict

from dlc import bank, config, gitsync, picker, submit

WEB_DIR = os.path.join(config.ROOT, "web")
_RUN_LOCK = threading.Lock()

CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".svg": "image/svg+xml",
}


class Handler(BaseHTTPRequestHandler):
    server_version = "daily-leetcode"

    # ----------------------------------------------------------------- utils
    def log_message(self, fmt, *args):  # quieter console
        if "/api/" in str(args[0] if args else ""):
            return
        return

    def _host_ok(self) -> bool:
        host = (self.headers.get("Host") or "").split(":")[0]
        return host in ("localhost", "127.0.0.1", "[::1]", "")

    def _send(self, code: int, body: bytes, content_type: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionAbortedError):
            pass

    def _json(self, payload: Dict[str, Any], code: int = 200) -> None:
        self._send(code, json.dumps(payload, default=str).encode("utf-8"),
                   "application/json; charset=utf-8")

    def _read_json(self) -> Dict[str, Any]:
        length = int(self.headers.get("Content-Length") or 0)
        if not length:
            return {}
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {}

    # ------------------------------------------------------------------- GET
    def do_GET(self) -> None:
        if not self._host_ok():
            return self._send(403, b"forbidden", "text/plain")

        path = self.path.split("?")[0]
        if path == "/":
            return self._serve_file("index.html")
        if path.startswith("/api/"):
            return self._api_get(path)
        if "/" in path.strip("/") or ".." in path:
            return self._send(404, b"not found", "text/plain")
        return self._serve_file(path.lstrip("/"))

    def _serve_file(self, name: str) -> None:
        full = os.path.join(WEB_DIR, name)
        if not os.path.isfile(full):
            return self._send(404, b"not found", "text/plain")
        with open(full, "rb") as handle:
            body = handle.read()
        ext = os.path.splitext(name)[1]
        self._send(200, body, CONTENT_TYPES.get(ext, "application/octet-stream"))

    def _api_get(self, path: str) -> None:
        if path == "/api/today":
            return self._json(_today_payload())
        if path == "/api/stats":
            return self._json({"stats": picker.summary(), "git": gitsync.status()})
        if path == "/api/solution":
            problem = picker.problem_for()
            return self._json({"slug": problem["slug"],
                               "solution": problem["solution"].strip(),
                               "pitfalls": problem.get("pitfalls", []),
                               "target": problem["target"]})
        if path == "/api/list":
            state = picker.load_state()
            return self._json({"problems": [
                {"slug": p["slug"], "title": p["title"], "difficulty": p["difficulty"],
                 "topics": p["topics"],
                 "solved": bool(state["records"].get(p["slug"], {}).get("solved"))}
                for p in bank.all_problems()
            ]})
        return self._json({"error": "unknown endpoint"}, 404)

    # ------------------------------------------------------------------ POST
    def do_POST(self) -> None:
        if not self._host_ok():
            return self._send(403, b"forbidden", "text/plain")

        path = self.path.split("?")[0]
        body = self._read_json()

        if path == "/api/save":
            problem = picker.problem_for()
            _write_solution(problem, body.get("code", ""))
            return self._json({"saved": True})

        if path == "/api/run":
            return self._run(body)

        if path == "/api/hint":
            problem = picker.problem_for()
            return self._json(submit.next_hint(problem["slug"]))

        if path == "/api/reroll":
            problem = picker.problem_for(reroll=True)
            picker.ensure_solution_file(problem)
            return self._json(_today_payload())

        if path == "/api/reset":
            problem = picker.problem_for()
            path_ = picker.solution_path(problem)
            if os.path.exists(path_):
                os.remove(path_)
            picker.ensure_solution_file(problem)
            return self._json(_today_payload())

        if path == "/api/push":
            problem = picker.problem_for()
            outcome = gitsync.sync_solution(picker.solution_path(problem), problem,
                                            picker.today_key())
            return self._json({"git": outcome, "status": gitsync.status()})

        return self._json({"error": "unknown endpoint"}, 404)

    def _run(self, body: Dict[str, Any]) -> None:
        problem = picker.problem_for()
        code = body.get("code", "")
        with_stress = bool(body.get("stress", True))
        allow_push = bool(body.get("push", True))

        path = _write_solution(problem, code)
        # one run at a time: the checker spawns a subprocess and the runs would
        # otherwise fight over the same solution file
        with _RUN_LOCK:
            payload = submit.check(problem["slug"], path, with_stress=with_stress,
                                   allow_push=allow_push)
        payload["git_status"] = gitsync.status()
        payload["stats"] = picker.summary()
        payload["hints_shown"] = submit.hints_shown(problem["slug"])
        return self._json(payload)


def _write_solution(problem: Dict[str, Any], code: str) -> str:
    path = picker.ensure_solution_file(problem)
    if code.strip():
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(code if code.endswith("\n") else code + "\n")
    return path


def _today_payload() -> Dict[str, Any]:
    problem = picker.problem_for()
    path = picker.ensure_solution_file(problem)
    with open(path, "r", encoding="utf-8") as handle:
        code = handle.read()
    return {
        "problem": submit._problem_summary(problem),
        "code": code,
        "path": os.path.relpath(path, config.ROOT).replace("\\", "/"),
        "date": picker.today_key(),
        "hints_shown": submit.hints_shown(problem["slug"]),
        "hints": problem["hints"][: submit.hints_shown(problem["slug"])],
        "stats": picker.summary(),
        "git_status": gitsync.status(),
        "solved": bool(picker.load_state()["records"].get(problem["slug"], {}).get("solved")),
    }


def serve(port: int = 8777) -> None:
    httpd = ThreadingHTTPServer(("127.0.0.1", int(port)), Handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  stopped")
    finally:
        httpd.server_close()
