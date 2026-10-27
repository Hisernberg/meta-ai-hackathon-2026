# NUSKHA — Round-3 Champion Spec (Build This One)

**Product:** Nuskha — "every methods section, runnable."
**Arena provenance:** S021 "Methods Recipe: research freelancers upgrade" (lane U-U6, user-profile) — Round-3 grand-arena champion; dethroned incumbent "Ustad" in the grand final; 18/20 council points (3/5 first-place votes).
**Track:** Indie (judged ⅓ creativity · ⅓ technical ambition · ⅓ whether it works)
**Theme:** Push the Frontier — the idea *needs* Muse Wonder's 1M context + computer use + Modal sandboxes; it cannot exist without the newest capabilities.

---

## 1. One-liner

Nuskha turns a research paper's methods section into a **runnable recipe** — environment, data, seeds, commands, expected outputs — executes it step-by-step in a Modal sandbox, **flags every missing or ambiguous step** (the unspoken "obviously use seed 42"), and reconciles the reproduced figures against the paper's claimed numbers, issuing a shareable **Reproduction Receipt** with a verified / mismatch / not-runnable badge per claim.

## 2. Problem statement (real, defensible, huge)

- Nature's 2016 survey: **70% of researchers** have failed to reproduce another scientist's experiment; more than half fail to reproduce their *own*.
- Reproducing a single paper costs a grad student **days to weeks**; most attempts fail quietly on undocumented details — an unstated random seed, an unspecified train/val split, a "proprietary dataset" wall, an unpinned dependency.
- Reviewers, journal clubs, and research-engineering freelancers re-do this painful archaeology daily, with zero tooling beyond a text editor and hope.
- The AI-community fix so far is *auto-research* (Sakana's AI Scientist) or *evaluations* (PaperBench). **Nobody ships the verification tool for the methods section itself.** Nuskha is that narrow, honest slice.

## 3. Users (named, reachable, weekly)

| User | Moment of pain | What Nuskha returns |
|---|---|---|
| Grad student starting a reproduction | Monday, paper + repo open, cursor blinking | Recipe + missing-steps list before they waste the week |
| Research-engineering freelancer | Client: "replicate Table 2 by Friday" | Sandbox run + figure reconciliation + receipt to invoice against |
| Journal club / teaching lab | Weekly paper, nobody ran the code | Dry-run audit mode (no execution needed) with gap flags |
| Open-source maintainer | "Does the README actually reproduce the paper?" | Receipt badge for the repo README |

## 4. Why it is NEW (novelty defense)

1. **Verification artifact, not another paper-chatbot.** Output is a per-claim verdict (verified / mismatch / not-runnable) — not a summary, not a chat.
2. **The missing-steps auditor is the product.** Failure cases ARE the demo: "watch it catch this paper's missing random seed" never fails live, because the flag fires even when execution can't.
3. **Sandbox-native.** Recipes execute in Modal sandboxes with streamed logs — the audience watches code run, not slides.
4. **Reconciliation closes the loop.** Spark vision reads the reproduced plots; numeric tolerance checks compare against claimed values; the receipt shows red/green per claim.
5. Honest scope: Python/ML repos first, seed-locked golden set, graceful dry-run fallback. No "AI Scientist" overreach.

## 5. Architecture (all demoable solo)

```
Paper (PDF) ─┐
             ├─► [1] INGEST     Wonder 1M-ctx read: full paper incl. methods/appendix
Repo (zip/URL)┘        Spark 1.3: extraction into a structured Recipe DSL
                       (env · deps · data · seeds · commands · expected outputs)
                              │
                              ▼
             [2] AUDIT         Missing-steps auditor: recipe vs claims cross-check
                              │  (missing seed? split unspecified? version unpinned?
                              │   dataset wall? implicit preprocessing?)
                              ▼
             [3] EXECUTE       Modal Sandbox per step (CPU; GPU when training)
                              │  streamed logs, per-step artifacts, timeouts
                              ▼
             [4] RECONCILE     Spark vision reads reproduced figures;
                              tolerance check vs claimed numbers → per-claim verdict
                              │
                              ▼
             [5] RECEIPT       One-page "Reproduction Receipt" (web + PDF/MD export)
                              badges: verified / mismatch / not-runnable / flagged-gap
```

**Graceful degradation ladder** (the demo cannot die): full run → partial run (some steps) → dry-run audit only. Every level produces a valuable receipt.

## 6. Meta model stack (every credit justified)

| Model | Role | Why it's needed | Cost basis |
|---|---|---|---|
| **muse-wonder-1.0** | Full-paper read (1M ctx), recipe planning, missing-step reasoning, sub-agents per section | Papers exceed normal context; the auditor needs the *whole* paper incl. appendix | $4/M in · $0.20/M cached · $20/M out |
| **muse-spark-1.3** | DSL extraction, summarization, per-step commentary | Cheap workhorse for high-volume extraction | low |
| **muse-spark-1.3 (vision)** | Read reproduced plots/figures for reconciliation | Multimodal figure comparison | low |
| **muse-glimmer** (self-hosted on Modal) | Cheap classification (step-type routing, log triage) | Apache-2.0; zero marginal API cost at load | Modal compute only |
| **muse-spark-open** (Baseten) | Optional LoRA-tuned "recipe-quality grader" + batch scoring | Open weights = fine-tune + serve story; Deepens Baseten usage | Baseten credits |
| **muse-image-1.0** | Receipt header figures / annotated figure callouts (light use) | $0.01/img | trivial |

**Budget:** ~$40–90 of the $150 Meta API credits covers the golden set (15–20 papers), judging-day demo load, and retries. Modal: sandboxes + optional A10G steps ≈ $50–100 of the $100 credits. Baseten: grader serving ≈ $20–40 of $100.

## 7. 7-day build plan (deadline: Nov 4, 9:00 PM ET = **Nov 5, 8:00 AM Dhaka**)

- **D1 (Tue):** Repo bootstrap (private→public flip plan), PDF parse → Wonder ingestion, Recipe DSL v0, JSON schema + tests.
- **D2 (Wed):** Missing-steps auditor (rule pack + Wonder pass), receipt data model.
- **D3 (Thu):** Modal sandbox runner (step executor, log streaming, timeouts, artifact capture).
- **D4 (Fri):** Reconciliation engine (Spark vision on plots, tolerance checks), receipt web page.
- **D5 (Sat):** Golden set: 15–20 papers (5 executed end-to-end seed-locked, 10 dry-run), fallback ladder tested.
- **D6 (Sun):** UI polish + 3-minute demo video (script below), README, docs.
- **D7 (Mon):** Buffer + CV form submission (public repo flip, YouTube link, X post for Most Viral).

## 8. 3-minute demo beat sheet

1. **0:00–0:25 Hook:** "70% of researchers can't reproduce a paper. Watch me catch this paper's missing random seed — live."
2. **0:25–1:00 Ingest:** Drop in a real NeurIPS-style paper + repo. Wonder reads all 40 pages; recipe DSL appears step-by-step on screen.
3. **1:00–1:40 Audit:** The missing-steps list blooms — red flag: *"train/val split unstated (Fig. 3 irreproducible as written)"; yellow: "seed absent; assumed 42."*
4. **1:40–2:30 Execute:** Modal sandbox runs the recipe; logs stream; figures render; reconciliation turns Fig. 3 **green** and Table 2 **red** (tolerance exceeded).
5. **2:30–3:00 Receipt + close:** The one-page Receipt with per-claim badges; "every claim, checked. Nuskha." + repo URL.

## 9. Risks & mitigations

| Risk | Mitigation |
|---|---|
| Env setup fails live | Failure IS content (audit mode); seed-locked golden set rehearsed |
| Repo unavailable/dirty | Dry-run audit delivers full value with zero execution |
| Cost blowup on 40-page papers | Prompt caching ($0.20/M), Spark for bulk extraction, Glimmer routing |
| "AI already does this" judge | Tight prior-art paragraph in README: AI Scientist = auto-research; PaperBench = eval; Nuskha = *the auditor you run before wasting a week* |
| Scope creep | Python/ML repos only; 15–20 paper golden set; no web-scale claims |

## 10. Compliance checklist (hackathon rules)

- [x] Indie track, solo builder — buildable by 1 person in ≤7 days
- [x] Theme declared: Push the Frontier (and honestly why)
- [x] Meta models required & deep: Wonder (1M ctx + sub-agents), Spark (+vision), Glimmer self-host, Spark Open (Baseten), Image (light)
- [x] Partner infra used meaningfully: Modal (sandboxes = core), Baseten (open-weight grader)
- [x] NEW: verification-tool positioning vs AI Scientist / PaperBench / paper-chatbots
- [x] REAL work use case: named users, defensible days-saved, reachable community (grad students, freelancers, journal clubs)
- [x] 90-second core demo (ingest → flag → receipt) and 3-minute video plan
- [x] Consent/safety: public papers + public repos only; no PII; no diagnosis
- [x] Submission assets: public GitHub repo (flip before Nov 4), 3-min YouTube demo, X post (Most Viral optional), all CV form fields (see FORMS_READY_V3.md)
- [x] Timezone-safe deadline: submit by Nov 5, 8:00 AM Dhaka (48h buffer before finals prep)
