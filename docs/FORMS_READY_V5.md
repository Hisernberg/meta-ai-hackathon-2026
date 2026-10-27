# FORMS_READY_V4 — Paste-ready answers (aligned to champion "Nuskha")

> Fill the three `[FILL]` items before submitting. Everything else is paste-ready.
> Deadline: **Nov 4, 9:00 PM ET = Nov 5, 8:00 AM Dhaka.** Submit Nov 3 Dhaka-time to be safe.

---

## FORM 1 — Modal Credits application

**Full name:** nabidnur abrar
**Email:** nurnabid754@gmail.com
**Team name:** team blackbox
**Teammate emails:** nurnabid754@gmail.com
**Track:** Indie

**Project one-liner (2–4 sentences):**
Nuskha turns a research paper's methods section into a runnable recipe and executes it step-by-step, flagging every missing or ambiguous step and reconciling reproduced figures against the paper's claimed numbers. Each recipe step passes a **gate chain** (structured sign-offs; a cheap Glimmer gate escalates to Spark on disagreement — no silent skips) and then runs in a **Modal Sandbox** with streamed logs and captured artifacts — sandboxes are the execution core of the product — and we self-host Apache-2.0 Muse Glimmer on Modal serverless GPUs as the first-tier gate and log triage. Output is a one-page "Reproduction Receipt" with verified / mismatch / not-runnable badges per claim.

**GitHub profile link:** https://github.com/Hisernberg
**Project repo link:** https://github.com/Hisernberg/meta-ai-hackathon-2026 *(flip to public before final submission; final public URL: [FILL — same repo renamed/public link])*
**Modal workspace name:** [FILL — create free account at modal.com, name it `team-blackbox`]
**Modal account email:** nurnabid754@gmail.com

**What will you use Modal for? (check all that apply):**
- [x] **Sandboxes** — every recipe step of every paper executes in an isolated Modal Sandbox (core feature)
- [x] **Inference on open-weight models via Endpoints** — Muse Glimmer self-hosted on Modal for step-classification + log triage
- [ ] Fine-tuning or post-training *(done via Baseten for muse-spark-open)*
- [ ] GPUs for training *(only if a golden-set paper requires a small training step — sandbox GPUs on demand)*

**Estimated compute:** **$50–100** (sandbox CPU-minutes for 15–20 paper runs + Glimmer endpoint; within $100 credits)

**Acknowledgement:** ✅ I understand Modal credits are limited and subject to review.

---

## FORM 2 — Baseten Credits application

**Full name:** Nabidnur abrar
**Team name:** team-blackbox
**Track:** Indie

**Project one-liner (2–4 sentences):**
Nuskha converts research papers' methods sections into runnable recipes, executes them in Modal sandboxes, and issues per-claim reproduction verdicts. On **Baseten** we serve Meta's open-weight **Muse Spark Open** as our "recipe-quality grader" — scoring each extracted recipe step for completeness — and prototype a small LoRA post-training of that grader on our golden set of 15–20 papers. This gives the auditor a fast, dedicated open-weight judge instead of burning frontier-model tokens on every step.

**GitHub link:** https://github.com/Hisernberg/meta-ai-hackathon-2026

**Expected request volume:** **Heavy (agents, batch)** — batch scoring runs across the full golden set (15–20 papers × dozens of recipe steps each), plus grader serving during the live demo and judging window; agentic loops call the grader repeatedly per paper.

**Acknowledgement:** ✅ I understand Baseten credits are limited and subject to review.

---

## FORM 3 — Cerebral Valley final submission

**Team Name:** team blackbox
**Team Members:** navi12 / Nabid Nur
**Track:** Indie
**Project Title:** Nuskha — every methods section, runnable

**Problem statement:**
70% of researchers have failed to reproduce someone else's experiment (Nature survey), and reproducing a single paper costs days to weeks — usually failing quietly on undocumented details: an unstated random seed, an unspecified data split, an unpinned dependency, a dataset wall. Reviewers, journal clubs, grad students and research-engineering freelancers repeat this archaeology every week with no tooling. The current AI answers — auto-research systems and benchmarks — don't help a person verify one specific paper before they sink a week into it.

**Project Description:**
Nuskha ingests a paper (PDF) and its code repository, uses Muse Wonder's 1M-token context to read the whole paper and extract a structured **Recipe DSL** — environment, dependencies, data, seeds, commands, expected outputs. A **missing-steps auditor** cross-checks the recipe against the paper's claims and flags every gap ("train/val split unstated — Fig. 3 irreproducible as written"). A **gate chain of role-experts** (Mixture of Role-based Experts) signs each step before execution; steps then run in a Modal Sandbox with streamed logs, and Muse Spark vision reconciles reproduced figures against claimed numbers using a **numeric mask-geometry score** (shape-overlap decimals, topology-stability gate) plus **three-ladder consistency** (line / step / paper must agree). Risky verdicts are signed by a **2-of-3 verifier quorum** with evidence pointers, and every run is deterministically replayable. The output is a one-page **Reproduction Receipt**: verified / mismatch / not-runnable / flagged-gap badges per claim, exportable as web page, Markdown, or PDF. A dry-run audit mode delivers the full missing-steps value even when code can't execute — the demo cannot die. A cost-aware router (Spark-first, Wonder-on-uncertainty) keeps the whole pipeline inside $150 of credits.

**Public GitHub Repository URL:** [FILL — flip https://github.com/Hisernberg/meta-ai-hackathon-2026 to public before submitting; paste the public URL here]

**3-Minute Demo Video (YouTube URL):** [FILL — beat sheet in CHAMPION_V5.md §8: hook (0:00) → live ingest (0:25) → missing-steps bloom (1:00) → sandbox run + red/green reconciliation (1:40) → receipt (2:30)]

**Describe your use of Meta products:**
- **muse-wonder-1.0** — the brain: 1M-context reads of full papers (incl. appendices), recipe planning, missing-step reasoning, sub-agents auditing one paper section each.
- **muse-spark-1.3** (+vision) — bulk Recipe-DSL extraction, per-step commentary, and reading reproduced plots for reconciliation.
- **muse-glimmer** — self-hosted on Modal for cheap step-type routing and log triage (Apache-2.0 open weights).
- **muse-spark-open** — served on Baseten as the recipe-quality grader, with a LoRA post-training pass on our golden set.
- **muse-image-1.0** — annotated figure callouts on the Receipt ($0.01/img).
- **Cost-aware model router** — Spark bulk-extracts and only escalates to Wonder on high-uncertainty sections; prompt caching keeps 40-page-paper ingestion affordable; structured-JSON outputs drive the DSL; the quorum verifiers re-check every risky claim.

**Why are Meta's models important to your solution?**
Nuskha is impossible without them: whole-paper reasoning at 1M tokens is what makes methods extraction trustworthy (summaries lose the appendix details where reproducibility dies); Wonder's computer-use and sub-agents let one solo builder run a multi-agent audit that would otherwise need a team; Spark vision closes the figure-reconciliation loop; and the open-weight family (Spark Open, Glimmer) lets us fine-tune and self-host a dedicated grader AND run the gate tier — a full frontier-to-open pipeline that no other model family offers in one stack. The novel architecture is load-bearing: gates, quorum and geometry-scored reconciliation are why the Receipt can be trusted, and they are built from Meta models end to end.

**Feedback on Meta products:**
Wonder's 1M context + sub-agents are genuinely differentiating for document-scale reasoning; prompt caching makes it viable on hobby budgets. Requests: (1) publish per-model tokenizer/limits clearly to plan long-document ingestion; (2) a files-API with persistent storage across calls would remove re-upload overhead for multi-pass paper analysis; (3) expose usage dashboards per model so builders can throttle spend mid-hackathon.

**Feedback on Fireworks / Modal / Baseten:**
Modal sandboxes are a perfect fit for "run untrusted recipe steps" — the streamed-log UX is demo gold; a first-class "artifact volume" primitive (persist /tmp across sandbox restarts) would help long pipelines. Baseten's open-weight serving + LoRA flow is the easiest path to a dedicated grader; a prebuilt Muse Spark Open one-click template would shorten onboarding. Fireworks: not used this build; fast open-weight endpoints are on our roadmap for scale-up.

**Most Viral Track — X post link (optional):** [FILL — post a 45–60s clip: "watch AI catch this paper's missing random seed live" with #MetaAIHackathon; paste link]

---

### Pre-submission checklist (Dhaka time)
1. [ ] Modal workspace created; credits form submitted (Form 1)
2. [ ] Baseten form submitted (Form 2)
3. [ ] Repo: private → **public**; README = Nuskha spec + demo GIF
4. [ ] 3-min video uploaded to YouTube (public/unlisted); link into Form 3
5. [ ] X demo clip posted; link into Form 3 (Most Viral)
6. [ ] Form 3 submitted — **before Nov 4, 9:00 PM ET / Nov 5, 8:00 AM Dhaka**
