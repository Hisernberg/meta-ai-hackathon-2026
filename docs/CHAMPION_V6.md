# CHAMPION V6 — **BHORA** (ভরা)
### *The phone that loads the boat.* Live geometry coach for physical loading work.

**Provenance:** Round-6 Worldwide Battle champion. Out of **10,000,000 enumerated lattice ideas** (seeded by 2025–26 global hackathon winners: TreeHacks, Claude Code hackathons, Gemini Live Agent Challenge, AI Engineer WFF, Cerebral Valley 2026), 2,000,000 scored, 32 deep-scored finalists entered the arena. BHORA's seed won the bracket, took the council **25/15/10/5**, and **defeated the three-time defending champion Nuskha 38–36** in the superfinal under the full official rulebook. Nuskha was eliminated in Round 1 — the old idea is officially retired.

- Track: **Indie** · Theme: **Build for Your World** (+ Push-the-Frontier architecture story)
- Team: team blackbox (solo) · Deadline: **Nov 4, 9:00 PM ET = Nov 5, 8:00 AM Dhaka**

---

## 1. The one-liner (say it exactly like this)

> **Point your phone at any load-out — a fish hold, a truck bed, a container — BHORA sees the space as geometry, coaches you by voice while you load, interrupts you at the exact second you're about to stack it wrong, and hands you a signed load receipt when you close the door.**

## 2. The real-work problem

Loading physical cargo into constrained spaces (fish holds, refrigerated trucks, containers, cold rooms) is still an apprenticeship skill. A bad load costs real money: crushed catch under ice, failed reefer temperature maps, axle-weight violations, re-work at the dock. In Chattogram and the Gulf ports, hold-loading decisions are made by a handful of aging experts; everyone else learns by ruining fish. There is no CAD here, no warehouse software — just a phone in a wet hand and a deadline before the ice melts. That is the gap: planning tools live in offices, the decision happens on the deck.

## 3. What BHORA does (3 interactions, 90 seconds)

1. **Walk the space.** One slow phone pass. SAM 3.1 segments the hold/truck/room into mask geometry; Spark estimates usable volume, door swing, tie-down points. Ten seconds.
2. **Load with a voice that can see.** As the worker loads, the camera keeps segmenting. The coach speaks only when it matters — *interruptions at the right second* are the product: "Stop. Rotate that crate 15° — the mask shows 6 cm left of clearance." "That stack will crush the ice bed — the geometry quorum flagged it." Between interrupts, silence. No chat window, ever.
3. **Close with a receipt.** Every load ends with a **signed geometry receipt**: fill %, clearances, weight-band estimate, violations caught, mask overlays — exportable to the tools people already use (PDF/WhatsApp). The receipt is the audit trail the port master never had.

## 4. The novel architecture (LOAD-BEARING — this is the Depth 20%)

**Geometry-Quorum Live Coach (GQLC)** — three mechanisms fused, each one doing work nothing else in the product can do:

- **Three-segmenter geometry quorum.** Every frame's masks are computed by three independent segmenters: SAM 3.1 (API), a fine-tuned open segmenter (Spark-Open-hosted / SAM-2-weights on Modal), and a geometric prior model (box/hold priors). **2-of-3 mask agreement gates every voice interrupt.** Disagreement = measurement-risk flag, never silent output. This is why the demo cannot die: when segmentation fails (wet reflective fish, occlusion), the quorum *says so out loud* — failure cases are a feature of the show.
- **Geodesic expert routing.** The live state (mask geometry, load progress, noise level) is embedded on a learned manifold; routing decides *which* expert interrupts (packing expert, weight expert, safety expert) by geodesic distance — distance IS confidence, so low-confidence states produce silence instead of nagging. The "interrupts at the right second" magic IS this router.
- **Live mask-math receipts.** Clearances, fill %, and crush-risk are computed from mask geometry (not guessed by an LLM) and signed into an attestation receipt (prompt/model/tool hashes included). The receipt is machine-checkable months later.

**Why nobody has shipped this:** segmentation-as-measurement with quorum gating + geodesic interrupt routing is research-grade (geometry-aware optimization, hyperbolic/manifold routing) — no product puts it in a fish hold. The architecture is not decoration: remove the quorum and the coach lies; remove the geodesic router and it nags; remove mask-math and the receipt is fiction.

## 5. Rubric mapping (official weights)

| Criterion (weight) | Evidence |
|---|---|
| **Impact 30%** | Cargo damage + reefer failures are multi-billion-$ global losses; every port/market/cold-chain worker is a user. Works from a $40 Android + WhatsApp-export; Bengali-first voice, deployable Dhaka→Gulf→worldwide. Live outcome counter: loads completed without re-work. |
| **Meta Tooling 25%** | SAM 3.1 (geometry), muse-spark-1.3 (planner + voice-loop brain), muse-voice-transcribe-1.0 (noisy-port ASR), muse-image-1.0 (renders the *target* arrangement as an overlay), muse-wonder-1.0 (agentic harness that plans the interrupt policy), muse-glimmer + muse-spark-open (open-weights edge segmenter on **Baseten** `meta-models/muse-spark-open-1026`, zero-day path), **Modal** sandboxes run the optimizer workers + fine-tune jobs. All 7 model lines, each load-bearing. |
| **Technical Depth 20%** | GQLC architecture (above): quorum gating, geodesic interrupt routing, signed mask-math receipts, sim2real-tuned geometric priors, offline fallback ladder (SAM-3.1 API → open segmenter on Modal GPU → Glimmer-only text coach → paper receipt). |
| **Demo 25%** | Live phone demo loading a real cooler on camera (below). Cannot die: quorum announces its own failures. Viral X clip built in: "AI interrupts fish loader at the exact wrong-second-turned-right." |

## 6. Model stack & budget (free-credits-only; card exposure $0)

| Component | Model / service | Cost path |
|---|---|---|
| Segmentation (primary) | SAM 3.1 API | Meta credits: $2.50/1k images ≈ $4 for demo+dev |
| Segmentation (quorum #2) | SAM-2 open weights / Spark-Open-hosted on **Modal** GPU | Modal $100 credits (free) |
| Segmenter fine-tune (quorum #3 prior) | Spark-Open on **Baseten** | Baseten $100 + 2M TPM (free) |
| Voice-loop brain + planner | muse-spark-1.3 | Meta credits ≈ $15 (contributor mode for bulk tests: ≈ $1) |
| Noisy-port ASR | muse-voice-transcribe-1.0 | ≈ $1 (5 hrs) |
| Target-overlay renders | muse-image-1.0 | ≈ $2 (200 renders) |
| Harness planning + spec hardening | muse-wonder-1.0 | ≈ $10 (bounded max_tokens) |
| Edge offline coach | muse-glimmer self-host | $0 (Apache-2.0, own GPU) |
| **Total planned** | | **≤ $35 of $150 Meta credits + $0 partner credits** |

Meta API account status: billing verification fix in progress (account restricted → models locked). **Zero-day plan:** Baseten + Modal carry segmentation/planning until unlock; no schedule risk.

## 7. 90-second demo beat sheet (cannot die)

| Beat | Seconds | What the judges see |
|---|---|---|
| Cold open | 0–10 | Wet hand, phone out, real cooler box on a dock table. "No CAD. Just a phone." Walk the space — masks paint themselves live. |
| The interrupt | 10–35 | Worker loads wrong; BHORA interrupts mid-motion with the exact fix + overlay. Voice is calm, specific, mask-referenced. |
| The quorum moment | 35–50 | Deliberately splash the camera / occlude the box → coach says: "Two segmenters disagree — measuring blind. Wait." → recovers. **Failure is the flex.** |
| The receipt | 50–70 | Load closes → signed geometry receipt appears in WhatsApp: fill %, clearances, violations caught. |
| The counter | 70–90 | Outcome counter: loads-without-rework this week; Bengali voice toggle; "Chattogram today, Gulf tomorrow." End card: team blackbox. |

**X/viral strategy ($20K Most Viral):** the 10-second interrupt clip (beat 2) is the hook; post the quorum-failure clip as the follow-up ("we taught AI to admit it's blind"). Hashtag story: built in Dhaka, works in any port.

## 8. Six-day build plan (Nov 29 → Nov 4 ET)

- **D1 (today):** repo scaffold (public-ready), SAM 3.1 mask pipeline + mask-math lib (volume, clearance, crush-risk), cooler-box test rig.
- **D2:** three-segmenter quorum (SAM 3.1 + SAM-2-weights on Modal + geometric priors) + agreement gating.
- **D3:** voice loop — Spark 1.3 interrupt policy, Voice Transcribe ASR, interrupt-at-the-right-second state machine.
- **D4:** geodesic router (embed live state, expert selection, silence threshold) + Muse Image target overlays.
- **D5:** receipts (attestation signing, WhatsApp/PDF export) + Glimmer offline fallback + Bengali voice.
- **D6:** demo polish, outcome counter, 3-min video shoot + edit, README/docs, public repo flip, submit.

## 9. Bonus-prize targeting

| Bonus | Play |
|---|---|
| Most Viral $20K | Interrupt clip + quorum-admits-blindness clip; daily build-in-public thread |
| Best Open Weights $10K | Glimmer + Spark-Open run the edge segmenter/coach — open weights are load-bearing, not garnish |
| Best Agentic $5K | The coach IS an agent org: segmenter agents, planner, router, receipt-attester with budgets + kill switches |
| Best Creative $5K | Muse Image target-arrangement overlays rendered live during the demo |

## 10. Risks & fallbacks

| Risk | Mitigation |
|---|---|
| Meta API still restricted at build time | Open segmenter on Modal + Spark-Open planner on Baseten = full function, $0; SAM 3.1 upgrades the quorum when unlocked |
| Wet/reflective surfaces break masks | Quorum flags it aloud (demo beat 3); polarizing filter + distance coaching in-app |
| ASR in port noise | Voice Transcribe + push-to-talk mode; voice is output-only if needed |
| 6-day solo scope | Cooler-box demo vertical only; fish hold = b-roll; receipt export = WhatsApp first, PDF second |
| "SAM wrapper" objection | Quorum + geodesic routing + mask-math receipts are the product; SAM is one of three segmenters |

## 11. Compliance checklist

- [ ] All code written during hackathon window; prior-art (R1–R5 ideation) is idea-only, disclosed in repo
- [ ] Repo **public** before Nov 4 9PM ET; demo video ≤ 3 min; new-work sections labeled
- [ ] No medical/surveillance/job-screening/political content (anti-project list clear)
- [ ] Meta Model API used for scoring-visible features (SAM 3.1, Spark, Voice, Image) + open weights on Baseten/Modal
- [ ] $150 free credits only — budget guard active (`scripts/meta_api_client.py`), card exposure $0
