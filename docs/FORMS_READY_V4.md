# FORMS READY — Round 4 (aligned to THIKANA)

Every field below is paste-ready. 3 items remain `[FILL]`: Modal workspace name,
public repo URL, YouTube link. Deadline: **Nov 4, 9:00 PM ET = Nov 5, 8:00 AM Dhaka.**

---

## A. MODAL FORM ($100 credits — first 1,000 participants)

**Name:** nabidnur abrar
**Email:** nurnabid754@gmail.com
**Team name:** team blackbox
**Track:** Indie Developer
**Modal account email:** nurnabid754@gmail.com
**Workspace name:** `[FILL — create free workspace at modal.com, e.g. "blackbox"]`

**What are you building? (one-liner, 2–4 sentences incl. how you use Modal):**
> Thikana turns routine site photos into a region-addressed memory of solar rooftop fleets:
> SAM 3.1 segments every panel, rail and cable into a queryable visual address, and a
> hierarchical crew of agents closes the loop from inspection to fault ticket to verified fix,
> with receipts for every verdict. Modal hosts the Thikana API, runs the self-hosted Muse
> Glimmer router (Apache-2.0) for cheap in-index labeling, and executes nightly sandbox jobs
> that rebuild each site's region index and re-embed new visits.

**GitHub profile:** https://github.com/Hisernberg
**Project repo:** `[FILL — public repo URL, e.g. github.com/Hisernberg/thikana]`

**How will you use Modal? (checkboxes):**
- [x] Inference on open-weight models (self-hosted Muse Glimmer router)
- [x] Sandboxes (nightly region-index rebuild + re-embedding jobs)
- [ ] Fine-tuning
- [x] GPUs for training (only if LoRA region-classifier trains on Modal instead of Baseten)
- [ ] Other

**Estimated compute usage:** `$50–100`

**Acknowledgement:** credits not guaranteed, distributed at Modal's sole discretion — [x] I understand.

---

## B. BASETEN FORM ($100 credits + 2M TPM — up to 2,000 participants)

**Name:** Nabidnur abrar
**Team:** team-blackbox
**Track:** Indie Developer
**GitHub profile:** https://github.com/Hisernberg
**Project repo:** `[FILL — same public repo URL]`

**What are you building? (one-liner incl. Baseten usage):**
> Thikana is a region-addressed operations memory for solar rooftop fleets: SAM 3.1 gives every
> panel, rail and cable run a persistent visual address, and an agentic role-crew closes the
> inspection loop with per-verdict receipts. On Baseten I serve meta-models/muse-spark-open-1026
> with a LoRA-tuned region-grade head (clean / soiled / damaged / arcing-risk) that batch-grades
> every segmented region, and a Spark Open "receipt grader" that sanity-checks each closure
> verdict — batch scoring across the whole fleet between visits.

**Request volume:** `Heavy (agents, batch)` — batch grading of full fleets + agent traffic.

**Acknowledgement:** credits granted per individual, reviewed by use case — [x] I understand.
**Note for implementation:** use model id `meta-models/muse-spark-open-1026` (per the official
Participant Guide — NOT `muse-spark-open`).

---

## C. CEREBRAL VALLEY — FINAL SUBMISSION FORM (due Nov 4 9PM ET)

**Team name:** team blackbox
**Team members + CV usernames:** navi12 / Nabid Nur
**Track:** Indie Developer
**Theme:** Push the Frontier

**Problem statement (short field):**
> Rooftop-solar fleets are photographed for commissioning and O&M, but nobody can answer "what
> changed on THIS roof since the last visit?" Photos pile up; degradation is found late. The
> gap between "a photo was taken" and "a decision was closed with evidence" is unowned.

**Project description (paste block):**
> Thikana (ঠিকানা, "address") gives machines a persistent, region-addressed memory of physical
> infrastructure. SAM 3.1 segments every panel, mounting rail, cable run and inverter into a
> queryable visual address; a geometry-aware mask-manifold embedding aligns visits so the
> system answers temporal queries ("what changed in region 3 since the monsoon?") with masks,
> deltas and confidence. A hierarchical role-crew of agents (surveyor → auditor → dispatcher →
> verifier) closes the whole loop: inspection → fault ticket → field fix (voice-first via Muse
> Voice Transcribe) → re-verification of the same region → closure receipt. A LoRA-tuned Muse
> Spark Open (1026) classifier on Baseten batch-grades every region; Muse Glimmer self-hosted
> on Modal routes cheap labels; Muse Wonder plans across the fleet's full history; Muse Image
> renders hard negatives that grow the classifier where it fails. Every verdict ships receipts.

**Public GitHub repo URL:** `[FILL — MUST be public before submitting]`
**3-minute demo video (YouTube):** `[FILL — upload, unlisted OK but link must work]`
**Which Meta products did you use?**
> Meta Model API: SAM 3.1 (segmentation index), Muse Spark 1.3 (vision describe + drafting),
> Muse Wonder 1.0 (crew planning, fleet-history reasoning), Muse Voice Transcribe (field
> notes), Muse Image (hard negatives, dossier renders). Open weights: Muse Spark Open (1026)
> served on Baseten with a LoRA region-grade head; Muse Glimmer self-hosted on Modal. Muse
> Code used as the coding agent during the build.

**Why were Meta's models important to this project?**
> Thikana is impossible without SAM 3.1 — the region-address registry IS the product, and only
> SAM's mask quality + tracking make persistent visual addresses reliable across visits. Muse
> Wonder's 1M context holds an entire fleet's visit history in one reasoning pass, which the
> planner crew needs for cross-visit verdicts. Spark Open (1026) being open-weight is what
> makes per-region grading economically viable at fleet scale (LoRA on Baseten, ~zero marginal
> cost), and Glimmer's Apache-2.0 license lets us self-host the router on Modal. The stack is
> not decorative: each model does a distinct, load-bearing job.

**Feedback for Meta / Fireworks / Modal / Baseten (optional but good form):**
> The three-protocol Meta Model API (Responses / Chat Completions / Anthropic Messages) made
> the crew trivial to wire. Wishlist: per-mask confidence in SAM responses, and a sandboxed
> LoRA fine-tune recipe for Spark Open on Baseten.

**X post link (optional, for Most Viral $20K):** `[FILL — post a 30–45s region-query clip]`

---

## D. Pre-submission checklist (hard rules)

- [ ] Repo **flipped to public** (rules: repositories must be public)
- [ ] Demo video shows ONLY features built during the hackathon (new-work rule)
- [ ] Everyone who worked on it is listed (solo: you)
- [ ] Meta credits claimed (by Nov 4 9PM ET) + card on file for API
- [ ] Video link + repo tested in incognito before submitting
