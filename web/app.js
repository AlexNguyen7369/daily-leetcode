/* daily-leetcode — local UI */

const $ = (id) => document.getElementById(id);
const el = (tag, cls, text) => {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text !== undefined) node.textContent = text;
  return node;
};

let STATE = { problem: null, dirty: false, running: false };

/* ------------------------------------------------------------- network -- */
async function api(path, body) {
  const options = body
    ? { method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body) }
    : {};
  const response = await fetch(path, options);
  if (!response.ok) throw new Error(`${path} -> ${response.status}`);
  return response.json();
}

function toast(message, ms = 2600) {
  const node = $("toast");
  node.textContent = message;
  node.classList.remove("hidden");
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => node.classList.add("hidden"), ms);
}

/* ------------------------------------------------------------- problem -- */
function renderProblem(data) {
  STATE.problem = data.problem;
  const p = data.problem;

  document.title = `${p.title} — daily-leetcode`;
  $("title").textContent = p.title;
  $("difficulty").textContent = p.difficulty;
  $("difficulty").className = "pill" + (p.difficulty === "Medium" ? " medium" : "");
  $("topics").textContent = p.topics.join(" · ");
  $("url").href = p.url;
  $("description").textContent = p.description;
  $("examples").textContent = p.examples.join("\n");
  $("target").textContent = `${p.target.time} time · ${p.target.space} space`;
  $("file-label").textContent = data.path;

  const list = $("constraints");
  list.innerHTML = "";
  p.constraints.forEach((line) => list.appendChild(el("li", null, line)));

  renderHints(data.hints || [], p.hint_count);
  setCode(data.code);
  $("solution-box").classList.add("hidden");

  $("date-label").textContent = data.date;
  renderTop(data.stats, data.git_status);
}

function renderHints(hints, total) {
  const box = $("hints");
  box.innerHTML = "";
  if (!hints.length) {
    box.appendChild(el("div", "placeholder", `${total} hints available — reveal them one at a time.`));
  }
  hints.forEach((text, i) => {
    const node = el("div", "hint");
    node.appendChild(el("b", null, `${i + 1}.`));
    node.appendChild(document.createTextNode(text));
    box.appendChild(node);
  });
  $("btn-hint").disabled = hints.length >= total;
  $("btn-hint").textContent = hints.length >= total ? "No hints left" : "Reveal a hint";
}

function renderTop(stats, git) {
  if (stats) $("streak-label").textContent = `streak ${stats.streak} · solved ${stats.solved}/${stats.bank.total}`;
  if (!git) return;
  const label = $("git-label");
  if (!git.is_repo) {
    label.textContent = "git: not set up";
    label.className = "chip ghost";
  } else if (!git.remote) {
    label.textContent = "git: local only";
    label.className = "chip warn";
  } else {
    const unpushed = git.unpushed ? ` · ${git.unpushed} unpushed` : "";
    label.textContent = `${git.branch}${unpushed}`;
    label.className = "chip " + (git.unpushed ? "warn" : "ok");
    label.title = git.remote + (git.last_commit ? `\nlast: ${git.last_commit}` : "");
  }
}

/* -------------------------------------------------------------- editor -- */
function setCode(text) {
  $("code").value = text;
  STATE.dirty = false;
  syncGutter();
}

function syncGutter() {
  const lines = $("code").value.split("\n").length;
  const gutter = $("gutter");
  let out = "";
  for (let i = 1; i <= lines; i++) out += i + "\n";
  gutter.textContent = out;
  gutter.scrollTop = $("code").scrollTop;
}

function setupEditor() {
  const code = $("code");

  code.addEventListener("input", () => { STATE.dirty = true; syncGutter(); });
  code.addEventListener("scroll", () => { $("gutter").scrollTop = code.scrollTop; });

  code.addEventListener("keydown", (event) => {
    if (event.key === "Tab") {
      event.preventDefault();
      const { selectionStart: start, selectionEnd: end, value } = code;
      if (start === end && !event.shiftKey) {
        code.value = value.slice(0, start) + "    " + value.slice(end);
        code.selectionStart = code.selectionEnd = start + 4;
      } else {
        // indent / dedent whole lines
        const from = value.lastIndexOf("\n", start - 1) + 1;
        const block = value.slice(from, end);
        const shifted = event.shiftKey
          ? block.replace(/^ {1,4}/gm, "")
          : block.replace(/^/gm, "    ");
        code.value = value.slice(0, from) + shifted + value.slice(end);
        code.selectionStart = from;
        code.selectionEnd = from + shifted.length;
      }
      STATE.dirty = true;
      syncGutter();
      return;
    }

    if (event.key === "Enter") {
      // keep the current indentation, and add one level after a colon
      const { selectionStart: start, value } = code;
      const lineStart = value.lastIndexOf("\n", start - 1) + 1;
      const line = value.slice(lineStart, start);
      const indent = (line.match(/^[ \t]*/) || [""])[0];
      const extra = /:\s*$/.test(line) ? "    " : "";
      if (indent || extra) {
        event.preventDefault();
        const insert = "\n" + indent + extra;
        code.value = value.slice(0, start) + insert + value.slice(code.selectionEnd);
        code.selectionStart = code.selectionEnd = start + insert.length;
        STATE.dirty = true;
        syncGutter();
      }
    }
  });

  document.addEventListener("keydown", (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
      event.preventDefault();
      run();
    }
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "s") {
      event.preventDefault();
      save().then(() => toast("saved"));
    }
  });

  setInterval(() => { if (STATE.dirty && !STATE.running) save(); }, 8000);
  window.addEventListener("beforeunload", () => {
    if (STATE.dirty) navigator.sendBeacon?.("/api/save",
      new Blob([JSON.stringify({ code: $("code").value })], { type: "application/json" }));
  });
}

async function save() {
  await api("/api/save", { code: $("code").value });
  STATE.dirty = false;
}

/* ------------------------------------------------------------- results -- */
function short(value, limit = 90) {
  const text = typeof value === "string" ? JSON.stringify(value) : JSON.stringify(value);
  if (text === undefined) return String(value);
  return text.length > limit ? text.slice(0, limit - 3) + "..." : text;
}

function renderResults(payload) {
  const box = $("results");
  box.innerHTML = "";

  if (payload.error) {
    box.appendChild(el("div", "placeholder", payload.error));
    return;
  }

  const r = payload.result;
  const passed = r.all_passed;

  const verdict = el("div", "verdict " + (passed ? "pass" : "fail"));
  verdict.appendChild(el("span", null, passed ? "✓ All tests passed" :
    `✗ ${r.passed}/${r.total} tests passed`));
  const sub = el("span", "sub");
  if (r.timed_out) sub.textContent = "timed out";
  else if (r.cases.length) {
    const slowest = Math.max(...r.cases.map((c) => c.ms));
    sub.textContent = `slowest case ${slowest.toFixed(2)} ms`;
  }
  verdict.appendChild(sub);
  box.appendChild(verdict);

  /* cases */
  const cases = el("div", "cases");
  r.cases.forEach((c, i) => {
    const row = el("div", "case " + (c.ok ? "ok" : "bad"));
    row.appendChild(el("span", "mark", c.ok ? "PASS" : "FAIL"));
    row.appendChild(el("span", "args", short(c.args, 120)));
    row.appendChild(el("span", "ms", `${c.ms.toFixed(2)} ms`));
    cases.appendChild(row);

    if (!c.ok) {
      const detail = el("div", "case-detail");
      if (c.error) {
        detail.textContent = c.error.trim().split("\n").slice(-3).join("\n");
      } else {
        const exp = el("div", "exp", `expected  ${short(c.expect, 300)}`);
        const got = el("div", "got", `got       ${short(c.got, 300)}`);
        detail.appendChild(exp);
        detail.appendChild(got);
      }
      cases.appendChild(detail);
    }
  });

  if (r.stress) {
    const s = r.stress;
    const slow = s.ok && s.ms > s.budget;
    const row = el("div", "case " + (s.ok ? (slow ? "slow" : "ok") : "bad"));
    row.appendChild(el("span", "mark", s.ok ? (slow ? "SLOW" : "PASS") : "FAIL"));
    row.appendChild(el("span", "args", `large input (budget ${s.budget.toFixed(0)} ms)`));
    row.appendChild(el("span", "ms", `${s.ms.toFixed(0)} ms`));
    cases.appendChild(row);
    if (s.error) {
      const detail = el("div", "case-detail", s.error.trim().split("\n").slice(-2).join("\n"));
      cases.appendChild(detail);
    }
  }
  box.appendChild(cases);

  /* feedback */
  const glyphs = { fail: "✗", warn: "!", tip: "i", good: "✓" };
  const notes = el("div", "notes");
  payload.notes.forEach((note) => {
    const card = el("div", "note " + note.level);
    card.appendChild(el("span", "glyph", glyphs[note.level] || "•"));
    const body = el("div");
    body.appendChild(el("div", "title", note.title));
    if (note.detail) body.appendChild(el("div", "detail", note.detail));
    card.appendChild(body);
    notes.appendChild(card);
  });
  box.appendChild(notes);

  /* git */
  if (payload.git) renderGit(payload.git, box);

  renderTop(payload.stats, payload.git_status);
  box.scrollTop = 0;
}

function renderGit(git, box) {
  const ok = git.pushed || (git.committed && !git.error);
  const card = el("div", "git-box " + (ok ? "ok" : "warn"));

  let headline;
  if (git.pushed) headline = "Committed and pushed to GitHub";
  else if (git.committed) headline = "Committed locally";
  else if (git.skipped) headline = "Nothing to sync";
  else headline = "Not synced";

  const head = el("div", "git-head");
  head.appendChild(el("span", null, ok ? "⬆" : "⚠"));
  head.appendChild(el("span", null, headline));
  card.appendChild(head);

  const body = el("div", "git-body");
  if (git.commit) body.appendChild(el("div", null, git.commit));
  (git.steps || []).forEach((step) => body.appendChild(el("div", null, "· " + step)));
  if (git.skipped) body.appendChild(el("div", null, git.skipped));
  if (git.error) {
    body.appendChild(el("div", null, git.error.split("\n")[0]));
    const retry = el("button", "btn subtle small", "Retry push");
    retry.onclick = async () => {
      retry.disabled = true;
      const out = await api("/api/push", {});
      renderTop(null, out.status);
      toast(out.git.pushed ? "pushed" : (out.git.error || "still not pushed"));
      retry.disabled = false;
    };
    body.appendChild(retry);
  }
  card.appendChild(body);
  box.appendChild(card);
}

/* ------------------------------------------------------------ actions -- */
async function run() {
  if (STATE.running) return;
  STATE.running = true;
  const button = $("btn-run");
  const label = button.innerHTML;
  button.disabled = true;
  button.textContent = "Running…";
  $("results").innerHTML = '<div class="placeholder">Running the test suite…</div>';

  try {
    const payload = await api("/api/run", {
      code: $("code").value,
      stress: $("opt-stress").checked,
      push: $("opt-push").checked,
    });
    STATE.dirty = false;
    renderResults(payload);
    if (payload.result && payload.result.all_passed) {
      toast(payload.git && payload.git.pushed ? "Solved — pushed to GitHub" : "Solved");
    }
  } catch (error) {
    $("results").innerHTML = "";
    $("results").appendChild(el("div", "placeholder", "The checker failed: " + error.message));
  } finally {
    button.disabled = false;
    button.innerHTML = label;
    STATE.running = false;
  }
}

async function showStats() {
  const data = await api("/api/stats");
  const s = data.stats;
  const body = $("modal-body");
  body.innerHTML = "";
  body.appendChild(el("h2", null, "Progress"));

  const grid = el("div", "stat-grid");
  const add = (n, k) => {
    const stat = el("div", "stat");
    stat.appendChild(el("div", "n", String(n)));
    stat.appendChild(el("div", "k", k));
    grid.appendChild(stat);
  };
  add(s.solved, "solved");
  add(s.streak, "day streak");
  add(s.by_difficulty.Easy, "easy");
  add(s.by_difficulty.Medium, "medium");
  add(s.bank.total, "in the bank");
  body.appendChild(grid);

  body.appendChild(el("h2", null, "Recent days"));
  const history = el("div", "history");
  Object.entries(s.assignments).sort().reverse().slice(0, 14).forEach(([date, slug]) => {
    const record = s.records[slug] || {};
    const row = el("div");
    row.appendChild(el("span", null, date));
    row.appendChild(el("span", record.solved ? "done" : "open", record.solved ? "solved" : "open"));
    row.appendChild(el("span", null, slug));
    history.appendChild(row);
  });
  body.appendChild(history);
  $("modal").classList.remove("hidden");
}

async function reload() {
  const data = await api("/api/today");
  renderProblem(data);
  $("results").innerHTML = '<div class="placeholder">Write your solution, then run the tests.</div>';
}

/* --------------------------------------------------------------- boot -- */
function setupButtons() {
  $("btn-run").onclick = run;

  $("btn-hint").onclick = async () => {
    const out = await api("/api/hint", {});
    if (out.exhausted) { toast("No hints left — try the reference solution."); return; }
    const data = await api("/api/today");
    renderHints(data.hints, data.problem.hint_count);
  };

  $("btn-solution").onclick = async () => {
    const box = $("solution-box");
    if (!box.classList.contains("hidden")) { box.classList.add("hidden"); return; }
    if (!confirm("Show a full reference solution for this problem?")) return;
    const data = await api("/api/solution");
    box.innerHTML = "";
    box.appendChild(el("div", "caption",
      `reference · ${data.target.time} time · ${data.target.space} space`));
    box.appendChild(el("pre", null, data.solution));
    if (data.pitfalls.length) {
      const caption = el("div", "caption", "watch out for");
      box.appendChild(caption);
      const list = el("pre", null, data.pitfalls.map((p) => "- " + p).join("\n"));
      box.appendChild(list);
    }
    box.classList.remove("hidden");
  };

  $("btn-reroll").onclick = async () => {
    if (!confirm("Draw a different problem for today?")) return;
    renderProblem(await api("/api/reroll", {}));
    toast("new problem drawn");
  };

  $("btn-reset").onclick = async () => {
    if (!confirm("Discard your code and restore the starter template?")) return;
    renderProblem(await api("/api/reset", {}));
    toast("file reset");
  };

  $("btn-stats").onclick = showStats;
  $("modal-close").onclick = () => $("modal").classList.add("hidden");
  $("modal").onclick = (event) => {
    if (event.target === $("modal")) $("modal").classList.add("hidden");
  };
}

setupEditor();
setupButtons();
reload().catch((error) => toast("could not load: " + error.message, 6000));
