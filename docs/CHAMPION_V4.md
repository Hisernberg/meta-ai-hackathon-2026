# THIKANA — Round-4 Champion Spec (Build This One)

**Product:** Thikana (ঠিকানা — "address") — *the physical world, addressable.*
**Provenance:** Round-4 grand arena champion (bracket 64→1, final 87.1) + council confirmation 4/5
first-place votes. Pool: 30,568 unique ideas (10,568 from rounds 1–3 + 20,000 new in Round-4:
10,000 winner-pattern lane + 10,000 user-profile lane). Novelty-verified against Hugging Face +
GitHub (146/150 arena-eligible ideas: zero collisions).
**Track:** Indie · **Theme: Push the Frontier** — *"give a machine a new capability … unlock a
better way to understand and control a physical system."* Thikana gives a machine a persistent,
region-addressed memory of physical infrastructure. That sentence IS the problem statement.

---

## 1. One-liner

Thikana turns routine site photos into a **living, region-addressed memory of a solar rooftop
fleet**: SAM 3.1 segments every panel, rail, cable run and inverter into **queryable visual
addresses** ("what changed in region 3 since the last monsoon?"), a **hierarchical role-crew of
agents** completes the whole loop — commissioning checklist → fault ticket → field fix →
**re-verification of the same region** — and every verdict ships with **receipts**: masks,
timestamps, prior evidence, model confidence. Under the hood, retrieval walks a **geometry-aware
mask-manifold embedding** (masks as priors, geodesic search instead of flat vectors).

## 2. Problem (real, verifiable, growing)

- Bangladesh added record rooftop-solar capacity under net-metering; **commissioning photo
  documentation is already required**, and O&M is a decade-long obligation almost nobody has
  tooling for. Fleet owners and EPC contractors track hundreds of sites in WhatsApp galleries
  and spreadsheets.
- The core pain: **nobody can answer "what changed on THIS roof since last visit?"** Photos
  exist; answers don't. Degradation, soiling, loose cabling and hotspots are found late —
  when output drops or an inspector visits.
- Existing tools are either (a) one-shot defect classifiers on a single image — no memory, no
  follow-up, no closure — or (b) heavyweight enterprise asset-management suites that ignore the
  photo-first reality of the field. **The gap between "a photo was taken" and "a decision was
  closed with evidence" is unowned.** Thikana owns it.

## 3. Users (named, reachable, weekly)

| User | Moment of pain | What Thikana returns |
|---|---|---|
| EPC O&M engineer (5–200 sites) | Monthly visit round; 300 photos; no comparison baseline | Region cards + change list per site, ranked by urgency |
| Fleet owner / asset manager | "Is site 12 getting worse or is it the monsoon?" | Per-region trend: three visits side-by-side, masks aligned |
| Field technician (hands busy, gloves on) | Fixing panel 14, needs the ticket | Voice-first region briefing + step list; fixes get re-verified |
| Inspector / lender doing technical due diligence | Weeks of report archaeology | Exportable site dossier: every claim carries its mask + timestamp |

## 4. Why it is NEW (novelty defense — verified)

1. **Segment-as-index architecture (A20).** Existing solar-vision repos on GitHub/HF are
   single-shot defect classifiers (plain CNN/YOLO on EL/IR/RGB crops). Thikana's index is
   **persistent and addressable**: region = primary key; queries are temporal and spatial
   ("region 3 across visits"). Lexical novelty check vs GitHub + Hugging Face returned **zero
   collisions** for the finalist slate (146/150 original, 3 inconclusive API retries, 0 hits).
2. **Geometry-aware mask-manifold retrieval (A03).** Region similarity uses the mask itself as
   a geometric prior (shape descriptors on the segmentation manifold, geodesic-style ranking) —
   a conference-level mechanism (topological data analysis, geometric deep learning) productized
   for field ops, not a paper demo.
3. **The loop closes (W17 end-to-end ops + H05 hierarchical crew).** Not a copilot that
   "suggests" — a role-crew (surveyor → auditor → dispatcher → verifier) that re-verifies the
   exact region after the fix and issues a **closure receipt**. Judges see autonomy with
   accountability: the Best-Agentic bonus in one product.
4. **Open-weight economics (A22 light).** A LoRA-tuned **Muse Spark Open (1026)** region-classifier
   on Baseten grades each region (clean / soiled / damaged / arcing-risk) at ~zero marginal cost,
   with Muse Spark 1.3 escalating only on low confidence — the Best-Open-Weight bonus, honestly used.
5. **Failure grows the data (A23, light).** When the classifier and the Skeptic-role disagree,
   Muse Image renders targeted hard negatives for the next fine-tune round. Data compounds.

## 5. Architecture (all demoable solo, no custom training required for v1)

```
Site photos (phone, per visit) ──► [1] SURVEY   SAM 3.1: mask every panel/rail/cable/inverter
                                 │              Muse Spark 1.3 (vision): per-region describe
                                 ▼
                [2] INDEX        Region registry: every mask = an address (site > array > region)
                                 Geometry-aware embedding: mask shape descriptors + geodesic kNN
                                 to past visits → "changed / unchanged / degraded" per region
                                 ▼
                [3] CREW         Hierarchical role-crew (planner·auditor·dispatcher·verifier):
                                 auditor grades regions (Spark Open LoRA on Baseten; Spark on doubt)
                                 dispatcher writes fault tickets; skeptic role contests low-confidence calls
                                 ▼
                [4] FIELD        Technician voice notes (Muse Voice Transcribe) + fix photos
                                 ▼
                [5] VERIFY       Re-segment the fixed region → compare across visits →
                                 closure receipt (masks, deltas, confidence, who/when/what)
                                 ▼
                [6] DOSSIER      Fleet view + per-site dossier export (web page + PDF)
```

**Graceful degradation ladder (the demo cannot die):** full loop → index + audit without field
fix → single-visit dossier (works with ONE photo set). Every rung ships value.

## 6. Meta model stack (every credit justified)

| Model | Role | Why it's needed | Cost basis |
|---|---|---|---|
| **SAM 3.1** (Meta Model API) | Segment + track panels/rails/cables/inverters per photo | The region index IS the product; SAM is the foundation | core spend |
| **muse-spark-1.3** | Vision describe per region, ticket drafting, change-note writing | Cheap workhorse, vision-capable | low |
| **muse-wonder-1.0** | Crew planning, cross-visit reasoning over the full site history, dossier narrative | 1M ctx holds an entire fleet's history; sub-agents power the crew | $4/M in · $0.20/M cached · $20/M out |
| **muse-spark-open-1026** (Baseten, LoRA-tuned) | Region grade classifier (clean/soiled/damaged/risk) + grader for receipts | Open weights fine-tune story; 2M TPM covers batch grading | Baseten credits |
| **muse-glimmer** (self-host on Modal, Apache-2.0) | Cheap routing/labels inside the index builder | Zero marginal API cost at load | Modal compute only |
| **muse-voice-transcribe-1.0** | Hands-busy technician voice briefings → structured notes | $0.18/hr; field-real | trivial |
| **muse-image-1.0** | Synthetic hard negatives for the classifier loop; dossier cover renders | $0.01/img; Creative-bonus eligible | trivial |

**Budget:** Meta API ≈ $40–80 of $150 (golden fleet = 3 demo sites × 4 visits + judging load) ·
Modal ≈ $30–70 of $100 (API hosting + Glimmer + nightly index rebuild sandbox) · Baseten ≈ $20–40
of $100 (LoRA grade + batch scoring) · Fireworks optional ($25, select teams).

## 7. 8-day build plan (today = Oct 27; deadline Nov 4 9PM ET = **Nov 5 8:00 AM Dhaka**)

- **D1 (Tue, tonight):** repo bootstrap (public), schema for site/array/region/visit; SAM 3.1
  call on 10 sample photos; mask→address registry v0.
- **D2 (Wed):** index builder: geometry descriptors (mask shape stats) + cross-visit alignment;
  "changed/unchanged" heuristic v1.
- **D3 (Thu):** role-crew v1 (planner/auditor/dispatcher/verifier) on Spark + Wonder; receipts model.
- **D4 (Fri):** Baseten: LoRA-tune Spark Open region-grade classifier (~500 labeled regions from
  public PV fault datasets + Muse Image hard negatives); wire into auditor role.
- **D5 (Sat):** web UI: region cards, mask overlays, visit slider, fleet view; Voice notes in.
- **D6 (Sun):** golden fleet: 3 demo sites × 4 visits (public solar O&M imagery + own
  compositions); full-loop run; dossier export.
- **D7 (Mon):** 3-minute demo video (beat sheet below); README with prior-art section;
  X post for Most Viral.
- **D8 (Tue, Nov 4):** buffer + submit via CV platform **before 9:00 PM ET**.

## 8. 3-minute demo beat sheet

1. **0:00–0:20 Hook:** "This roof has been photographed 4 times. Ask the machine: *what changed
   in region 3 since the monsoon?* — answered, with receipts." (type the query live)
2. **0:20–1:00 Index:** drop a visit's photos → SAM 3.1 masks bloom → region cards with
   addresses appear ("SITE-7/ARRAY-B/R-03: panel, 72% mask confidence").
3. **1:00–1:40 Crew:** auditor grades regions; skeptic contests one low-confidence call; the
   planner turns a soiled-array finding into a cleaning ticket; receipts visible per step.
4. **1:40–2:20 Close the loop:** technician voice note + fix photo → Thikana re-segments THE
   SAME region → side-by-side mask delta → **closure receipt** with badges.
5. **2:20–3:00 Fleet + open weights:** fleet view ranks sites by risk; Baseten classifier badge
   shown; "every panel an address. Thikana." + repo URL.

## 9. Risks & mitigations

| Risk | Mitigation |
|---|---|
| SAM masks drift across visits | Address = mask centroid + shape descriptors matched by geodesic kNN; manual address pinning UI |
| "Solar defect detectors exist" judge | Prior-art table in README: they classify ONE image; Thikana is the persistent addressable memory + closed loop — categories differ |
| Domain access | Golden fleet built from public PV O&M imagery + composed visits; no client PII |
| Crew loops burn credits | Glimmer routing, Wonder only for planning/cross-visit, hard budget envelope per site |
| 8 days solo | Degradation ladder; D1-D3 is the demo core; field-fix closure is the stretch that can shrink to simulated fix |

## 10. Compliance checklist (updated Participant Guide)

- [x] Indie track, solo builder — buildable in ≤8 days by one person (D1–D8 above)
- [x] Theme: Push the Frontier — stated with the exact problem-statement language
- [x] Meta models required & deep: SAM 3.1 + Spark (+vision) + Wonder + Voice + Image + Spark
      Open (Baseten) + Glimmer (self-host) — 7 of the listed models, each load-bearing
- [x] Partner infra meaningful: Modal (hosting, Glimmer, sandbox rebuilds), Baseten
      (`meta-models/muse-spark-open-1026`, LoRA grader), Meta API credits ($150 claimed)
- [x] NEW work only, built during the event; repo **public** (rules now require); demo shows
      only hackathon-built features
- [x] Not an anti-project: no medical advice, no RAG chatbot, no generic image analyzer, no
      education chatbot, no job screener, no nutrition/personality/sports/politics
- [x] Real work use case: named users (EPC O&M, fleet owners, technicians, inspectors),
      verifiable pain (photo-first O&M), reachable community (rooftop solar EPCs, lender DD)
- [x] Bonus-prize alignment: Best Agentic (role-crew closure loop) · Best Open-Weight Build
      (Spark Open 1026 LoRA on Baseten + Glimmer self-host) · Best Creative (Image hard
      negatives + dossier renders) · Most Viral (region-query clip is X-native)
- [x] Judging rubric mapping: Impact 30% (real sector, closure receipts) · Meta Tooling 25%
      (7-model stack, capability-surfacing) · Technical 20% (A20+A03+H05, geometry) · Demo 25%
      (live query wow + working loop)
- [x] Submission assets: public repo, 3-min YouTube demo, X post link, CV form fields (FORMS_READY_V4)
