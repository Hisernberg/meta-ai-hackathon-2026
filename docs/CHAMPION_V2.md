# GRAND CHAMPION (Round 2, Final) — Ustad: The Job That Teaches Itself

**Survived a 7,868-idea grand arena** (2,449 round-1 + 5,419 round-2) · Meta Global AI Developer Hackathon 2026
Track: **Indie** · Theme: **Build for Your World** (with a Push-the-Frontier engine)
Arena alias: "Cleat for stall chains" (bulk-film_sop+expert_loop) · Council verdict: **22 pts, 5/5 judge votes**

> **One-liner:** Film a job once on a phone. Ustad turns that video into a step-by-step
> illustrated SOP with checkpoints, a trainee quiz, and an expert-approval loop — so the
> same task is done the same way at every stall, bench and line, even when the expert isn't there.

**Dethroned:** Round-1 champion "Bhasha" (Offline Language Preserver) — eliminated in arena R1
under the round-2 hard rules ("must be NEW + a REAL WORK use case"; verdict: "too vague on
actual preservation methodology"). Bhasha remains the documented runner-up lineage.

---

## 1. Why this wins the Indie rubric (each axis = 1/3)

| Axis | How Ustad scores it |
|---|---|
| **Creativity** | SOP tools exist; a *self-teaching job* does not: the filmed task becomes the standard, the standard becomes a quiz, the quiz becomes a readiness score — and the expert's approval is the signature that makes it official. The demo vertical (street-food stall chains) is a world judges have all tasted but never seen engineered. |
| **Technical ambition** | A real multimodal pipeline, not a wrapper: Muse Spark 1.3 video understanding segments the take into steps; Muse Voice Transcribe lifts the narrated know-how ($0.18/hr); SAM 3.1 segments tools/ingredients per step; Muse Image renders clean step cards; Glimmer self-hosts the trainee mode offline. |
| **Whether it works** | Every loop demos with the builder's own phone: film cha-making at a real Dhaka stall, SOP materializes in ~60s, trainee answers the quiz, expert taps approve. No external dependency that can die on stage; graceful fallbacks at every layer. |
| **Theme fit** | Build for Your World, literally: street-food stall chains (and every trade like them) train people by shouting. The builder knows this world firsthand. |
| **Meta-native** | 4 Meta models across 3 modalities + open-weights edge path + partner infra (Modal sandboxes for video workers, Baseten for open-weight Spark Open batch jobs). A generic GPT-wrapper cannot copy the SAM 3.1 + video-understanding core. |

**The 20-second hook:** film it wrong on purpose — skip a step — and the trainee quiz and
live mode catch it. Judges remember being *quizzed by a video of a stranger's hands*.

## 2. The problem, precisely

A street-food stall chain (5-20 stalls) lives and dies on consistency: the same cha, the
same cut, the same portion. Today the recipe lives in one person's hands. New hires learn
by shadowing for weeks (and breaking real things), quality drifts stall by stall, and when
the expert quits, the chain re-learns by customer complaints. Formal SOP tools assume
desk workers and PDFs; videos filmed on phones sit unwatched on WhatsApp. The missing
artifact: a **living, checkable procedure** that costs one filming and trains by itself.

## 3. Product — the core loop (MVP scope)

1. **Film once (expert):** phone records the task start-to-finish while the expert talks
   through it (Bengali welcome). One take, no editing.
2. **Structure (Meta pipeline):** Spark 1.3 segments the video into steps with timestamps;
   Voice Transcribe aligns the narration; SAM 3.1 isolates the key object per step (the
   strainer, the flame, the seal); Muse Image renders a clean step card from the keyframe.
3. **Standardize:** the draft SOP gets checkpoints ("did the milk boil twice?") —
   editable in one tap; the **expert approves** (the signature that makes it the standard).
4. **Train (trainee mode):** the SOP becomes a tap-through quiz with "spot the mistake"
   scenes (Muse Image regenerates the scene with a step deliberately wrong); trainee gets
   a readiness score on a shared phone, PIN-per-worker.
5. **Live mode (garnish, ship only if time allows):** a tripod phone watches the task and
   ticks checkpoints in real time (SAM 3.1 + self-hosted Glimmer at the edge), flagging
   skips before the cup is served.

**Scope cut (red-team, feasibility hawk):** drop "supply counts" and any inventory angle.
Core = film → SOP → quiz → expert approval. Live mode is the last 2 days' bonus only.

## 4. Architecture (8-day solo build)

```
Phone camera + mic (one take, no edits)
   ├─ video ─► muse-spark-1.3 (video understanding: step segmentation, timestamps, JSON)
   ├─ audio ─► muse-voice-transcribe-1.0 (streaming STT + diarization, $0.18/hr)
   ├─ frames ─► sam-3.1 (segment the key object per step; text-prompted)
   ├─ cards ──► muse-image-1.0 (clean step cards + "spot the mistake" quiz scenes, $0.01/img)
   └─ all ────► Next.js PWA + SQLite (job = stall = task = steps = checkpoints = quiz)
                  ├─ expert approval screen (the signature)
                  ├─ trainee mode (shared phone, PINs, readiness scores)
                  └─ offline path: muse-glimmer-30B (llama.cpp) for quiz gen when signal dies
Batch/infra: Modal sandboxes run ffmpeg frame-extraction workers; Baseten serves
muse-spark-open for nightly batch re-processing of new videos (2M TPM headroom).
```

## 5. Cost budget (of $150 Meta API + $100 Modal + $100 Baseten)

| Item | Est. |
|---|---|
| Spark 1.3 video understanding: 15 demo videos × ~5 min | ~$6-12 |
| Voice Transcribe: ~2 hrs narration | ~$0.40 |
| SAM 3.1: ~200 step frames | <$2 |
| Muse Image: ~80 step cards + 20 quiz scenes | ~$1 |
| Glimmer self-host (Modal CPU/GPU box) | ~$10-20 |
| Modal sandboxes (video workers, demo scale) | ~$10-20 |
| Baseten Spark Open batch (nightly reprocess) | ~$10-20 of credit |
| **Total** | **~$40-75** — inside every credit envelope |

## 6. 3-minute demo video beat sheet (submission requirement)

| Beat | Content |
|---|---|
| 0:00-0:20 | Cold open at a real stall: trainee makes cha wrong; owner visibly frustrated. Title card: "Every job has a master. The master can't be everywhere." |
| 0:20-0:50 | The expert films ONCE on a phone. Narration in Bengali. Raw, unedited. |
| 0:50-1:30 | Pipeline montage: steps materialize with timestamps, SAM 3.1 outlines the strainer, step cards render, checkpoints appear. "60 seconds after filming, the job is documented." |
| 1:30-2:10 | Expert reviews and taps APPROVE (the signature moment). Trainee takes the quiz on a shared phone; the "spot the mistake" scene catches a skipped step; readiness score ticks up. |
| 2:10-2:35 | Live mode (if shipped): tripod phone watches a real take and flags the skipped step in real time. Else: offline mode flip — airplane mode, quiz still works on Glimmer. |
| 2:35-3:00 | The why: model stack + costs on screen, Meta API + SAM 3.1 + Voice credits + Modal/Baseten infra named explicitly. End card: "Film it once. Everyone becomes the master's second pair of hands." |

## 7. 8-day build plan (today = Day 2, Oct 27; deadline Nov 5, 8:00 AM Dhaka)

| Day | Ship |
|---|---|
| **2 (today)** | API smoke tests (Spark video, Voice, SAM, Image); film 3 real stall tasks; repo + PWA shell; schema |
| **3** | Core loop online: upload film → Spark step segmentation → side-by-side step editor |
| **4** | Voice alignment + SAM 3.1 key-object extraction + Muse Image step cards |
| **5** | Checkpoints + expert approval flow; trainee quiz with generated wrong-step scenes |
| **6** | Shared-phone mode (PINs, readiness scores); offline path (Glimmer via llama.cpp); Modal sandbox for video workers |
| **7** | Hardening (browser tests, error recovery), Baseten batch job, demo video shoot + edit |
| **8 (Nov 3-4)** | Buffer + submission: public repo flip, YouTube upload, form submission — DONE by Nov 4 evening Dhaka, 12h before the deadline |

## 8. Risks & mitigations (from the red-team)

| Risk | Severity | Mitigation |
|---|---|---|
| Filming is labor-intensive; busy workers won't adopt | HIGH | One take, no editing, phone-mount + voice-activation; demo shows the 60s habit |
| Expert-approval bottleneck | HIGH | Tiered approval: senior trainee can sign routine tasks; approval queue with reminders |
| SAM 3.1 on chaotic stall footage | MED | Hybrid: AI suggestion + one-tap manual correction is part of the product, not an apology |
| STT errors in noisy kitchens | MED | Phone close-mic guidance; narration is optional — video-only SOP still generates |
| UI too complex for stall workers | HIGH | Two screens only: Film and Train. Voice-first Bengali. Everything else is owner-side |
| Over-scoping (feasibility hawk) | MED | Scope cut enforced: no inventory/POS integration; live mode only if Day 6 target hit |

## 9. Rules & submission compliance checklist

- [x] Track: **Indie** (creativity · ambition · whether-it-works each 1/3) — matches team blackbox registration
- [x] Theme: **Build for Your World** (firsthand domain) — both themes allowed, one chosen
- [x] Uses Meta models via Model API as primary engine (4 models named in submission text)
- [x] Uses partner credits honestly (Modal sandboxes, Baseten open-weight batch) — claim only what is built
- [ ] **Public GitHub repo** (currently private `Hisernberg/meta-ai-hackathon-2026`): flip to public or publish the project repo before submission
- [ ] **3-minute demo video on YouTube** (link field) — shoot Day 7, upload Day 8
- [ ] **X post** for the Most Viral Track consideration (optional bonus track)
- [ ] Submit via Cerebral Valley before **Nov 5, 8:00 AM Dhaka (Nov 4, 9:00 PM ET)** — target Nov 4 evening Dhaka

## 10. Provenance (audit trail)

- Pool: **7,868** ideas = 2,449 (round 1, 76 LLM lenses) + 5,419 (round 2: 5,150 combinatorial
  from 100 work-contexts × 46 mechanisms × 60 twists + 30 hand-crafted elite + 239 LLM elite
  from 8 work-domain lenses), deduped by title-Jaccard.
- Funnel: unified rubric heuristic (creativity/ambition/works/wow/work-real/meta/fit) → top 200 →
  LLM judge (5 axes: wow, spec, build, meta, moat) → top 47 + incumbent seed.
- Arena: 48 → 16 (8 groups) → 8 → 4 → 2 → 1. All verdicts in `ideation/round2/g_*.json`.
- Council: 5 personas (creativity hawk, feasibility hawk, platform native, demo hunter,
  work-realist) ranked the final four; **Ustad family: 22 pts, 5/5 votes** vs Bellows Bench 16,
  Lintel 12, Produce Quality Inspector 0.
- Red-team: 5 kill risks + demo beats + scope cut (above).
- Incumbent "Bhasha" entered as top seed and was eliminated in R1 — documented, not hidden.
