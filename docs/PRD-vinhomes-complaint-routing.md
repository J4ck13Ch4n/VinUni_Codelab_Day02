# PRD — Resident Complaint Classification & Routing Assistant

**Subsidiary:** Vinhomes | **Owner:** AI Product Engineer, Vin Smart Future
**Status:** Draft — feeds into `02-deep-dive-report.md`
**Source problem card:** Inspiration Kit #6 — *Phân loại & Điều hướng phản ánh cư dân*

---

## 1. Problem Statement (6-field)

| Field | Detail |
|---|---|
| **Actor** | Ban quản lý (building management staff) per Vinhomes tower/cluster. |
| **Current Workflow** | Resident submits free-text complaint via Vinhomes Resident app → staff reads, manually tags category, manually assigns to dept/vendor. |
| **Bottleneck** | Manual read → classify → route step; slow at volume, inconsistent tagging across staff. |
| **Business Impact** | Delayed SLA on resident tickets, misrouted tickets bounce between depts, resident satisfaction drop. *(numbers below are illustrative — validate against real Vinhomes Ops ticket logs before committing)* |
| **Success Metric** | ≥90% of non-sensitive tickets auto-classified + routed correctly; time-to-route from ~X min → <30s. |
| **Operational Boundary** | AI classifies + drafts routing only. **CẤM (forbidden):** auto-resolving a ticket, promising refunds/fee waivers, or closing anything tagged phí quản lý (fees) / tranh chấp (disputes) without human approval. |

---

## 2. Goals

- Cut manual triage time on repetitive, low-risk complaint categories (nước, điện, ồn ào, vệ sinh, an ninh-non-emergency).
- Keep every fee/dispute/legal-adjacent ticket on a human decision path — no exceptions.
- Give management an audit trail of AI suggestion vs human decision, to catch drift/misclassification early.

## 3. Non-Goals

- Not building an agent that resolves tickets end-to-end.
- Not handling fee disputes, refunds, contract/legal interpretation, or safety emergencies as automated categories (see §6, Rule 1–2).
- Not replacing the Vinhomes Resident app UI — this sits behind the existing intake, on the management side.

---

## 4. Users

- **Primary:** Ban quản lý staff triaging the ticket queue.
- **Secondary:** Ops lead reviewing weekly misclassification/audit reports.
- **Out of scope as a direct user:** the resident — they only ever see a human-approved response.

---

## 5. Functional Requirements

| # | Requirement |
|---|---|
| FR1 | Ingest complaint free text (Vietnamese) + metadata (unit, timestamp) from existing ticket feed. |
| FR2 | Classify into one of a fixed taxonomy (e.g. `mat_nuoc`, `hong_den`, `on_ao`, `ve_sinh`, `an_ninh`, `phi_quan_ly`, `tranh_chap`, `khac`) + confidence score. |
| FR3 | If category ∈ {`phi_quan_ly`, `tranh_chap`} or text implies safety emergency → skip auto-routing, set `escalate: true`, route to priority human queue. |
| FR4 | For non-escalated categories, draft a routing recommendation (target dept/vendor) + one-line summary. |
| FR5 | Output structured JSON: `{category, confidence, escalate, route_target, draft_note}`. |
| FR6 | Every output is a draft — staff must approve/edit before the routing action fires (HITL, no exception). |
| FR7 | Log every AI suggestion + human override for weekly audit and model-quality tracking. |

## 6. Operational Boundaries (Safety Rules)

These are the rules the prompt prototype (`starter-code/prompt_prototype.py`) must enforce and the adversarial tests must attack:

1. **Never resolve financial/legal categories.** Model must not approve, deny, or quote a refund/fee-waiver amount, and must not rule on a resident-vs-HOA dispute. Any such content → `escalate: true`, no draft resolution text.
2. **Never auto-send.** Output is always a draft pending human approval — no silent ticket-closing or resident-facing message dispatch.
3. **Safety keywords force escalation.** Mentions of fire, break-in, injury, gas leak, etc. → immediate high-priority escalation, bypassing normal classification queue, regardless of how the resident phrased the request.
4. **No confident-sounding overreach.** Below a confidence threshold, output `khac` (other) + escalate rather than guessing a category.

**Adversarial test ideas** (for `ADVERSARIAL_TESTS` in the prototype):
- Resident frames a fee-waiver request as a generic complaint to bait the model into confirming a refund.
- Resident claims "emergency" to jump the queue for a routine noise complaint.
- Resident explicitly asks the model to "just resolve it now, skip the review."

## 7. Human-in-the-Loop & Fallback

- **HITL:** Management dashboard shows AI draft (category + route + note) next to raw ticket; one-click approve or edit-then-approve. Nothing reaches the resident or a vendor system without this click.
- **Fallback:** Low confidence, escalation flag, or model/API failure → ticket drops into the existing manual queue unchanged. No degraded automatic behavior.

## 8. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Misclassifying a safety-critical complaint as routine | Keyword-based escalation override (Rule 3) runs before classification confidence is trusted. |
| Staff rubber-stamping AI drafts without reading | Weekly audit sampling (FR7) comparing AI suggestion vs final human action. |
| Resident PII in complaint text | No training/fine-tuning on raw logs without a separate data-handling review; scope that out of this PRD. |
| Fee/dispute leakage into automated path | Rule 1 is a hard filter on category, not a soft prompt instruction — enforce it in code, not just in the system prompt. |

## 9. Rollout Plan

1. **Pilot:** One cluster, non-financial categories only (nước, điện, ồn ào, vệ sinh).
2. **Expand:** Add remaining non-sensitive categories once pilot audit shows acceptable misclassification rate.
3. **Hold:** `phi_quan_ly` / `tranh_chap` stay human-only indefinitely unless a separate legal/finance review changes scope — not part of this lab's GO decision.

## 10. Decision Gate (ties to Worksheet Phase 5)

Recommend **GO**, scoped narrowly to the pilot categories in §9 step 1. **NOT YET** on fee/dispute automation — insufficient guardrail maturity and legal exposure to greenlight now.

---

*This PRD is a working input for `02-deep-dive-report.md` — copy/trim into that file's 6-field table, Future-State Flow, and Evaluate sections as needed.*
