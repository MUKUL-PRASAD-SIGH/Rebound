# Worker instruction — what to push, which day

Read this before any `git add` / `git commit` / `git push`.

**Already on `origin/main`:** Day 00–08 through `4d31342` (`docs: Day 08 Baseline B policy comparison in eval`).

**Do not** amend pushed commits. **Do not** force-push. **Do not** push all remaining files in one commit. The Sep 1 exception is intentional: Day 10 and Day 11 ship together as one regression-and-benchmark commit.

## Current release cadence (supersedes the original dates)

The remaining milestones are compressed into two delivery days, while preserving one commit and one push per milestone:

| Date | Milestones | Outcome |
| --- | --- | --- |
| **1 Sep (today)** | Day 09 → Day 12, in order | Day 09; combined Day 10–11; Day 12 (three commits) |
| **2 Sep (tomorrow)** | Day 13 → Day 15, in order | Differentiation, demo polish, submission package — **build complete** |
| **3 Sep** | No planned feature/documentation push | Full test, demo rehearsal, evidence capture, verified-fix commits only |
| **5 Sep** | Submission | Submit the verified package |

If the operator asks to push **“today”**, continue with the first unpushed item in this sequence: Day 09, combined Day 10–11, then Day 12. If they ask to push **“tomorrow”**, use the Day 13–15 sequence only after Day 09–12 are pushed. “Next” means the first unpushed item in this order.

---

## Hard rules

1. Push **exactly** the files listed for that day. Leave everything else unstaged.
2. After each commit, run `git status` and confirm later-day files are still untracked/unstaged.
3. Keep `README.md`, `SCHEDULE.md`, `BUILD_LOG.md`, and `docs/build-log/README.md` accurate for the milestone being pushed; never mark a later milestone as pushed early.
4. Never commit: `.env`, `rebound.db`, `src/scripts/recover_model.json`, `node_modules/`, `__pycache__/`.
5. Tests live under `src/tests/` — include them from **Day 06** (they cover eval/workflow; do not wait for Day 10 to add the file, then only add extra cases on Day 10 if any).
6. `docs/build-log/day-09.md` … `day-15.md` stay **local** until their own milestone push. Do not combine later milestones into an earlier commit.

Commit message style (match history):

```
feat: Day 0N <short what> — <short why>
```

or `docs:` when the commit is logs/README only.

---

## Day 05 — DONE (do not push again)

Already committed. Includes EV scoring, propose, policy min-EV, `generate_batch.py`, `train_model.py`, `sample_batch.json`, `docs/EXTERNAL_REQUIREMENTS.md`, `docs/build-log/day-05.md`.

If `src/rebound/propose/__init__.py` is dirty again, that is **Day 06** (`ignore_history` for eval), not a Day 05 amend.

---

## Day 06 — already pushed (eval + MVP loop)

**When:** historical record — shipped on 26 Aug. Do not push again.
**Goal:** Baseline A vs Rebound `lift_value`, outcomes, ingest validation, Eval UI.

### Stage only

```
src/rebound/eval/__init__.py
src/rebound/workflow.py
src/rebound/ingest/__init__.py
src/rebound/propose/__init__.py
src/apps/api/main.py
src/scripts/run_eval.py
src/apps/web/src/App.tsx
src/apps/web/src/api.ts
src/apps/web/src/pages/EvalPage.tsx
src/apps/web/src/pages/HomePage.tsx
src/apps/web/src/pages/AuditPage.tsx
src/tests/test_core.py
docs/build-log/day-06.md
docs/EXTERNAL_REQUIREMENTS.md
```

Also patch (same commit) status docs **through Day 06 only**:

```
BUILD_LOG.md
README.md
SCHEDULE.md
docs/build-log/README.md
```

### Leave unstaged

- `Makefile`
- `docs/build-log/day-07.md` … `day-15.md`
- `README.md`
- `evidence/benchmarks/`

Note: `main.py` also contains batch decide + `/audit/recent`. That is acceptable in Day 06 because the eval/outcome loop needs those routes to demo. Do **not** split `main.py` across days.

### Suggested commit

```
feat: Day 06 eval lift — paired Baseline A vs Rebound and outcome audit
```

### After commit

```
cd src && python -m pytest tests -q
git push origin HEAD
```

---

## Day 07 — batch ops + global audit (docs-first if code already in Day 06)

**When:** 27 Aug or operator says “push day 7”.

If Day 06 already shipped batch decide + Audit page (it will, via `main.py` / `AuditPage.tsx`), Day 07 is **docs + copy only**:

```
docs/build-log/day-07.md
BUILD_LOG.md
README.md
docs/build-log/README.md
```

If those UI/API files were **not** in Day 06 (worker split them out), include instead:

```
src/apps/api/main.py          # only if batch/audit routes were withheld
src/apps/web/src/pages/AuditPage.tsx
src/apps/web/src/pages/HomePage.tsx
src/apps/web/src/api.ts
```

Commit: `docs: Day 07 batch decide and global audit trail` (or `feat:` if code is new).

---

## Day 08 — Baseline B in eval UI

**When:** 28 Aug / “push day 8”.

Code is already inside `eval/__init__.py` + `EvalPage.tsx` from Day 06. Push:

```
docs/build-log/day-08.md
BUILD_LOG.md
docs/build-log/README.md
```

Only add code if Baseline B table is still missing on remote.

Commit: `docs: Day 08 Baseline B policy comparison in eval`

---

## Day 09 — escalate / min-EV gate clarity

**When:** 1 Sep (today), commit 1 of 3 / “push day 9”.

Gate logic already shipped Day 05/06. Push:

```
docs/build-log/day-09.md
BUILD_LOG.md
docs/build-log/README.md
```

Commit: `docs: Day 09 high-value escalate and min-EV stop path`

---

## Day 10 — tests as a named milestone

**When:** 1 Sep (today), combined with Day 11 in commit 2 of 3 / “push day 10”.

`src/tests/test_core.py` should already be on remote from Day 06. Push:

```
docs/build-log/day-10.md
BUILD_LOG.md
docs/build-log/README.md
```

If new tests were added after Day 06:

```
src/tests/test_core.py
```

Commit: `docs: Day 10 regression suite checkpoint` (or `test:` if the file changes).

---

## Day 11 — benchmarks + edge cases

**When:** 1 Sep (today), combined with Day 10 in commit 2 of 3 / “push day 11”.

```
evidence/benchmarks/README.md
docs/build-log/day-11.md
BUILD_LOG.md
docs/build-log/README.md
```

Commit: `docs: Day 11 synthetic benchmark reproduction notes`

---

## Day 12 — sensitivity

**When:** 1 Sep (today), commit 3 of 3 / “push day 12”.

```
evidence/benchmarks/sensitivity.md
docs/build-log/day-12.md
BUILD_LOG.md
docs/build-log/README.md
```

Commit: `docs: Day 12 eval seed sensitivity notes`

---

## Day 13 — differentiation copy

**When:** 2 Sep (tomorrow), push 1 of 3 / “push day 13”.

```
docs/build-log/day-13.md
BUILD_LOG.md
docs/build-log/README.md
README.md
```

Include UI copy files **only if** Home/Eval/Audit copy is still Day-05 wording on remote.

Commit: `docs: Day 13 differentiation — stop and lift vs retry bots`

---

## Day 14 — demo polish

**When:** 2 Sep (tomorrow), push 2 of 3 / “push day 14”.

```
Makefile
README.md
docs/build-log/day-14.md
BUILD_LOG.md
docs/build-log/README.md
```

Commit: `chore: Day 14 Makefile and local demo runbook`

---

## Day 15 — submission package (last)

**When:** 2 Sep (tomorrow), push 3 of 3 / “push day 15” / “push submit docs”. Complete this package before the protected Sep 3 test day.

```
README.md
docs/build-log/day-15.md
BUILD_LOG.md
README.md
SCHEDULE.md
docs/build-log/README.md
```

Do **not** invent a “Days 00–15 complete” badge until this commit.

Commit: `docs: Day 15 submission checklist and video outline`

---

## Operator shortcuts

| Operator says | Worker does |
| --- | --- |
| push day 5–8 | **Refuse** — already on `origin/main` |
| push next / today | First unpushed item: Day 09, combined Day 10–11, then Day 12; then `git push` |
| push tomorrow | First unpushed milestone in the Day 13–15 sequence, only after Day 09–12 |
| push everything | **Refuse** — follow the Sep 1–2 milestone order |
| push day 9–15 | That milestone’s list only; never include later `day-N.md` files |
| don’t push | Commit locally if asked; **no** `git push` |

---

## Pre-push checklist (every day)

```bash
git status -sb
cd src && python -m pytest tests -q
git log -3 --oneline
```

Confirm HEAD message is the day you intend, then:

```bash
git push origin HEAD
```

If pytest fails, **do not push**. Fix, new commit (do not amend a commit that is already on remote).
