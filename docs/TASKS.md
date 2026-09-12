# Team Task Assignment — Vinhomes Complaint Routing Project

Source: `PRD-vinhomes-complaint-routing.md` + `TRD-vinhomes-complaint-routing.md`
Team size: 5. Swap `Member 1–5` for real names/branch names (per README §4 Step 2: `git checkout -b <ten-cua-ban>`).

**Reprioritized for an MVP demo.** Goal: one working script, live on demo day, that shows the core value prop and the safety story — not the full paperwork package. Full lab deliverables are still due (README grading rules don't change) but are pushed to §2, after the demo.

---

## 1. MVP Demo (ship this first)

**Demo promise:** run `prompt_prototype.py` live, show (a) a routine complaint auto-classified+routed correctly, (b) a fee/dispute ticket forced to escalate — never auto-resolved, (c) an adversarial attempt to bypass escalation fails anyway. That third one is the actual "wow" — code overrides the model, not just a polite prompt.

**Unlock for parallel work:** the interface is already frozen — taxonomy (TRD §4), JSON schema (TRD §5), escalation rules (TRD §6–7). Nobody needs to wait on anybody else's code; everyone builds directly against that written contract. The only sequential moment is the final wiring in Task 5, and that's a copy-paste, not a rebuild.

| # | Owner | Task | Deliverable | Depends on |
|---|---|---|---|---|
| 1 | Member 1 | Implement `evaluate_prompt()`: `SYSTEM_PROMPT` + real Gemini 2.5 Flash call, output matching the JSON schema in TRD §5 | working `evaluate_prompt()` | TRD contract only |
| 2 | Member 2 | Implement `validate_boundaries()` + a tiny self-test using hardcoded mock JSON dicts — pure function, no live API needed, test against the schema in TRD §5 directly | working function + self-test | TRD contract only |
| 3 | Member 3 | Curate 4 demo inputs (2 happy-path, 1 direct fee/dispute, 1 adversarial bypass) + the expected `category`/`escalate` for each, using the taxonomy in TRD §4 | demo input set + talking points | TRD contract only |
| 4 | Member 4 | One-pager narrative: problem statement (PRD §1) + a simple before/after workflow sketch | 1-page doc/slide | none |
| 5 | Member 5 | Write the integration harness **now**, against stub versions of `evaluate_prompt()`/`validate_boundaries()` (canned returns matching the schema) so the wiring is proven before anyone's real code lands. Swap in Members 1 & 2's real functions when ready, run Member 3's inputs through it, then the reliability pass (API key check, 2+ live runs, fallback recording, "known limitations" note) | integrated script + test log + fallback plan | swaps in Tasks 1–2's output at the very end; the harness itself starts immediately |

**Definition of done for the demo:** script runs to completion with no crash, all 4 curated inputs (Task 3) produce the expected escalate/route behavior, Member 5 has run it live at least twice successfully before demo day.

**Why this works in parallel:** Tasks 1–4 all code/write against the already-written TRD contract, not against each other — start all four the moment this doc is read. Task 5 also starts immediately (harness + stubs), and only needs Tasks 1–2's *real* functions for the final swap-in, which takes minutes, not days.

---

## 2. Full lab submission (due per README, not needed for the demo itself)

| Task | Owner | Deliverable | Rubric Gate |
|---|---|---|---|
| Current-state workflow diagram (polished) | Member 4 (extends their Task 4 sketch) | `04-workflow-diagram.png` | G1 (20pt) |
| 6-field Problem Statement + business case write-up | Member 1 or 2 | `02-deep-dive-report.md` §3.2 | G2 (20pt) |
| Future-state flow + AI-Fit write-up | Member 3 | `02-deep-dive-report.md` §3.3 | G3 (10pt) |
| Readiness checklist + GO/NOT-YET/NO-GO + final assembly + `main` merge | Member 5 | `02-deep-dive-report.md` (final) + merge | G4 (10pt) |

### Individual-only (every member, own branch — not delegable)
- `01-problem-scan.md`, `03-ai-log.md`, personal `prompt_prototype.py` copy. Everyone forks the MVP script from §1 into their own branch/file — code is graded per-branch, not merged to `main` (README §3.2).

**Autograder note (unchanged):** keyword check looks for `draft_only` / `5%` / `dispatch_mobile_charger` (EV-battery scenario), not Vinhomes terms. MVP script uses Vinhomes rules on purpose (coherent demo) — costs ~0.5/10 pts on that one autograder line item. Fine to accept for the demo; revisit before final individual submission if squeezing that half-point matters.
