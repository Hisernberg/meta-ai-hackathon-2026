# NUSKHA — Round-4 GRAND CHAMPION Spec (Final. Build This One.)

**Product:** Nuskha — "every methods section, runnable."
**Version:** V4 — validated across the full 4-round battle of ideas (30,568 unique ideas), now upgraded with novel agent architecture from Round-4's mandate.

**Battle provenance (Round 4, Oct 28, 2026):**
- Pool: 10,568 (R1–R3) + **20,000 new R4 ideas** (10,000 winner-thought lane + 10,000 builder-profile lane; every idea embodies a novel mechanism: Mixture of World Agents / Role-based Experts / geometry-aware segmentation-embeddings / verifiable harnesses) = **30,568 total**.
- Funnel: heuristic → LLM triage (240→80, 0 fallback batches) → LLM deep-judging (80→24) → **HF + GitHub originality sweep on all 24** (0 clones; 11 clean / 12 related / 1 close).
- Arena: 24 finalists + defending champion seeded into the *hardest* heat (against the top-4 scorers). Bracket pressure-test eliminated Nuskha at semis (8.2 vs 7.5 — attack mode punishes the visible incumbent); the **fresh-eyes Council of 5 personas then ranked the final 4: NUSKHA 25/30 — unanimous #1 from all five judges** (skeptical Meta research scientist, demo judge, Modal infra engineer, target user, VC). Bracket champion R4-08143 took 14, R4-12533 9, R4-01930 7.
- Verdict rule (same as R3): arena = elimination pressure-test, council = final decision. **Nuskha survives its third battle (R2: beat Bhasha-line; R3: beat Ustad; R4: beat 20,000 architecture-first challengers unanimously).**

**Track:** Indie (⅓ creativity · ⅓ technical ambition · ⅓ whether it works)
**Theme:** Push the Frontier — the idea *requires* Muse Wonder's 1M context + computer use + Modal sandboxes; it cannot exist without the newest capabilities.

---

## 1. One-liner

Nuskha turns a research paper's methods section into a **runnable recipe** — environment, data, seeds, commands, expected outputs — executes it step-by-step in a Modal sandbox behind a **gated role-expert bench** (Mixture of Role-based Experts: Ingestion Expert → Auditor → Executor → Reconciler, each returning structured sign-offs, cheap gates escalating on disagreement), **flags every missing or ambiguous step**, reconciles reproduced figures with **numeric mask-geometry scoring and three-ladder consistency**, and issues a quorum-signed **Reproduction Receipt** with a verified / mismatch / not-runnable badge per claim.

## 2. Problem statement (real, defensible, huge)

- Nature's 2016 survey: **70% of researchers** have failed to reproduce another scientist's experiment; more than half fail to reproduce their *own*.
- Reproducing one paper costs a grad student **days to weeks**; most attempts die quietly on undocumented details — an unstated seed, an unspecified split, a "proprietary dataset" wall, an unpinned dependency.
- Reviewers, journal clubs, and research-engineering freelancers re-do this archaeology daily with zero tooling beyond a text editor and hope.
- The AI-community answer so far is *auto-research* (Sakana's AI Scientist) or *benchmarks* (PaperBench). **Nobody ships the verification tool for the methods section itself.** Nuskha is that narrow, honest slice — and Round-4's HF/GitHub sweep found no clone of it.

## 3. Users (named, reachable, weekly)

| User | Moment of pain | What Nuskha returns |
|---|---|---|
| Grad student starting a reproduction | Monday, paper + repo open, cursor blinking | Recipe + missing-steps list before they waste the week |
| Research-engineering freelancer | Client: "replicate Table 2 by Friday" | Sandbox run + figure reconciliation + receipt to invoice against |
| Journal club / teaching lab | Weekly paper, nobody ran the code | Dry-run audit mode with gap flags, no execution needed |
| Open-source maintainer | "Does the README actually reproduce the paper?" | Receipt badge for the repo README |

## 4. Why it is NEW (novelty defense, evidence-backed)

1. **Verification artifact, not another paper-chatbot.** Output = per-claim verdicts (verified / mismatch / not-runnable / flagged-gap), not summaries.
2. **The missing-steps auditor is the product.** Failure cases ARE the demo: "watch it catch this paper's missing random seed" never fails live.
3. **Originality sweep (Oct 28, 2026):** GitHub repo search + Hugging Face models/datasets/spaces queries found **no clone** — AI Scientist (auto-research), PaperBench (eval suite) and paper-chat RAG tools are *adjacent, not equal*; the auditor-with-receipt slice is unclaimed.
4. **Sandbox-native.** Recipes execute in Modal sandboxes with streamed logs — the audience watches code run, not slides.
5. **Round-4 architecture is load-bearing, not decoration** (see §5): gates, quorum, geometry-scored reconciliation and ladder consistency are *why* the receipt can be trusted.

## 5. Architecture V4 — novel mechanisms integrated (R4 upgrades)

```
Paper (PDF) ─┐
             ├─► [1] INGEST EXPERT   Wonder 1M-ctx full read (incl. appendix);
Repo (zip/URL)┘        cost-aware router: Spark bulk-extracts the Recipe DSL,
                       escalates to Wonder only on high-uncertainty sections (R4-10763)
                              │
                              ▼
             [2] AUDIT EXPERT    Missing-steps auditor (rule pack + Wonder pass):
                              │  missing seed? split unspecified? version unpinned?
                              ▼
             [3] GATE CHAIN      each recipe step must pass structured sign-off
                              │  gates (Glimmer gate → Spark on disagreement) —
                              │  no silent skips (MoRBE: role-expert gates)
                              ▼
             [4] EXECUTE EXPERT  Modal Sandbox per step (CPU; GPU when training)
                              │  streamed logs, per-step artifacts, timeouts
                              ▼
             [5] RECONCILE EXPERT  Spark vision reads reproduced figures;
                              │  NUMERIC mask-geometry score (shape-overlap decimals,
                              │  topology-stability gate — R4-01930) + THREE-LADDER
                              │  consistency (line/step/paper must agree — R4-08143)
                              ▼
             [6] QUORUM RECEIPT  risky verdicts need 2-of-3 independent verifiers;
                              │  every claim carries an evidence pointer (quote/line/log);
                              │  runs are deterministically replayable → one-page
                              │  "Reproduction Receipt" (web + PDF/MD), badges per claim
```

**Why this architecture wins the rubric:** judges scored R4 ideas higher when the novel mechanism is *the reason the product works*. Here: gates kill silent skips, quorum makes the receipt trustworthy, geometry scoring makes figure-match a decimal answer instead of a vibe, and ladder consistency kills single-scale false positives. One product, five defensible novel mechanisms.

**Graceful degradation ladder (the demo cannot die):** full run → partial run → dry-run audit only. Every level produces a valuable receipt.

## 6. Meta model stack (every credit justified)

| Model | Role | Why needed | Cost basis |
|---|---|---|---|
| **muse-wonder-1.0** | Full-paper read (1M ctx), recipe planning, missing-step reasoning, section sub-agents | Papers exceed normal context; auditor needs the whole paper | $4/M in · $0.20/M cached · $20/M out |
| **muse-spark-1.3** | DSL bulk extraction, gate escalation tier, per-step commentary | Cheap workhorse for high-volume extraction | low |
| **muse-spark-1.3 (vision)** | Read reproduced plots/figures for reconciliation | Multimodal figure comparison | low |
| **muse-glimmer** (self-hosted on Modal) | First-tier gate classification, log triage | Apache-2.0; zero marginal API cost; *Best Build on Open Weights* eligible | Modal compute only |
| **muse-spark-open** (Baseten) | LoRA-tuned "recipe-quality grader" + batch scoring | Open weights fine-tune + serve story deepens Baseten use | Baseten credits |
| **muse-image-1.0** | Receipt header figures / annotated callouts (light) | $0.01/img | trivial |

**Budget:** ~$40–90 of $150 Meta credits covers the golden set (15–20 papers), judging-day load, retries. Modal ≈ $50–100 of $100 (sandboxes + optional A10G steps). Baseten ≈ $20–40 of $100 (grader serving). The cost-aware router (Spark-first, Wonder-on-uncertainty) is what keeps this inside budget.

## 7. 7-day build plan (deadline: Nov 4, 9:00 PM ET = **Nov 5, 8:00 AM Dhaka**)

- **D1 (Wed Oct 29):** Repo bootstrap (private dev → public flip plan), PDF parse → Wonder ingestion, Recipe DSL v0, JSON schema + tests.
- **D2 (Thu Oct 30):** Missing-steps auditor (rule pack + Wonder pass), gate chain v0, receipt data model.
- **D3 (Fri Oct 31):** Modal sandbox runner (step executor, log streaming, timeouts, artifact capture).
- **D4 (Sat Nov 1):** Reconciliation engine: Spark vision on plots + numeric geometry score + ladder consistency; receipt web page.
- **D5 (Sun Nov 2):** Quorum verifier (2-of-3) + evidence pointers + replay log; golden set: 15–20 papers (5 end-to-end seed-locked, 10 dry-run); fallback ladder tested.
- **D6 (Mon Nov 3):** UI polish + 3-minute demo video (beat sheet below), README with prior-art paragraph, docs.
- **D7 (Tue Nov 4):** Buffer + CV form submission (**public repo flip**, YouTube link, X post for Most Viral). Dhaka deadline 8:00 AM Nov 5.

## 8. 3-minute demo beat sheet

1. **0:00–0:25 Hook:** "70% of researchers can't reproduce a paper. Watch me catch this paper's missing random seed — live."
2. **0:25–1:00 Ingest:** Drop in a real NeurIPS-style paper + repo. Wonder reads all 40 pages; the role-expert bench lights up; recipe DSL appears step-by-step.
3. **1:00–1:40 Audit + gates:** Missing-steps list blooms — red flag: *"train/val split unstated (Fig. 3 irreproducible as written)"; yellow: "seed absent; assumed 42."* A gate refuses to run step 4 until the split is declared.
4. **1:40–2:30 Execute + reconcile:** Modal sandbox runs the recipe; logs stream; figures render; reconciliation turns Fig. 3 **green (geometry score 0.96)** and Table 2 **red (tolerance exceeded)**; three-ladder panel shows agreement.
5. **2:30–3:00 Receipt + close:** Quorum-signed one-page Receipt with per-claim badges and evidence pointers; "every claim, checked. Nuskha." + repo URL.

## 9. Risks & mitigations

| Risk | Mitigation |
|---|---|
| Env setup fails live | Failure IS content (audit mode); seed-locked golden set rehearsed |
| Repo unavailable/dirty | Dry-run audit delivers full value with zero execution |
| Cost blowup on 40-page papers | Cost-aware router + prompt caching ($0.20/M) + Glimmer gates |
| "AI already does this" judge | Prior-art paragraph + originality sweep table (HF/GitHub, Oct 28) in README |
| Gates/quorum feel like overhead | Demo shows one caught bad step = the gate paying for itself in 10 seconds |
| Scope creep | Python/ML repos only; 15–20 paper golden set; no web-scale claims |

## 10. Compliance checklist (hackathon rules)

- [x] Indie track, solo builder — buildable by 1 person in ≤7 days
- [x] Theme declared: Push the Frontier (and honestly why)
- [x] Meta models required & deep: Wonder (1M ctx + sub-agents), Spark (+vision), Glimmer self-host, Spark Open (Baseten), Image (light)
- [x] Partner infra used meaningfully: Modal (sandboxes = core), Baseten (open-weight grader) — also eligible: *Best Build on Meta Open Weight Models* (Glimmer + Spark Open), *Best Agentic Use-Case* (gated role-expert bench with quorum)
- [x] NEW: verification-tool positioning vs AI Scientist / PaperBench / paper-chatbots, backed by HF+GitHub sweep
- [x] REAL work use case: named users, defensible days-saved, reachable community
- [x] 90-second core demo (ingest → flag → receipt) and 3-minute video plan
- [x] Consent/safety: public papers + public repos only; no PII; no diagnosis
- [x] Submission assets: public GitHub repo (flip before Nov 4), 3-min YouTube demo, X post (Most Viral optional), all CV form fields (see FORMS_READY_V4.md)
- [x] Timezone-safe deadline: submit by Nov 5, 8:00 AM Dhaka
