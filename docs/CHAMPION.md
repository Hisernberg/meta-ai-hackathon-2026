# CHAMPION — Bhasha: The Offline Language Preservation Studio

**Champion of the 2,449-idea ideation funnel** · Meta Global AI Developer Hackathon 2026
Track: **Indie developer** · Primary theme: **Build for Your World** (with a Push-the-Frontier engine)

> **One-liner:** A local-first studio that records an elder speaking a low-resource language
> and, within minutes, turns that audio into a searchable, culturally-annotated language
> archive — transcript, translations, glossary and illustrated cultural cards — that works
> with **zero connectivity** and that the community, not the cloud, owns.

---

## 1. Why this idea wins (the cold logic)

| Judging criterion | How Bhasha scores it |
|---|---|
| **Creativity** | Language-tech is flooded with translation apps; nobody ships an *offline preservation studio* built on self-hosted open weights. Survived 5 adversarial judge personas with 4/5 votes. |
| **Technical ambition** | Offline/edge AI with self-hosted **Muse Glimmer**, streaming diarized ASR, SAM 3.1 visual annotation — frontier engineering, not a GPT wrapper. |
| **Whether it works** | Every core loop is demoable with recordings of the builder's own family — no field trip, no hardware, no cloud dependency to fail on stage. |
| **Theme fit** | Firsthand problem: the builder's own linguistic heritage (Sylheti, Chittagonian, Chakma and other Bangladeshi languages are massively under-served by tech). |
| **Meta-native** | 4 Meta models across 3 modalities (audio, vision, text) + open-weights self-hosting — the exact story this hackathon exists to showcase. |

**The demo moment (0:00–0:20):** an elder's voice plays; words materialize as glossary
cards with illustrations; the presenter flips the laptop to **airplane mode** and everything
still works. That flip is the memory judges keep.

## 2. The problem, precisely

Of ~7,000 living languages, one dies roughly every few weeks. Bangladesh alone carries
dozens of under-resourced varieties — Sylheti (~11M speakers), Chittagonian (~14M),
Chakma, Garo, Kokborok, Rohingya — with essentially **no** speech datasets, no keyboards,
no archives. Children shift to Bengali/English; the grandparent generation is the last
fluent one. Existing preservation tooling assumes: internet (gone in the communities that
need it), cloud storage (trust barrier — communities lose ownership), linguist manpower
(there aren't enough). Missing: a tool a grandchild can run on one laptop at the kitchen
table tonight.

## 3. Product: what it actually does (MVP scope)

**The core loop — "record → archive" in under 10 minutes:**

1. **Record** an elder telling a story, naming objects, singing — phone or laptop mic,
   one take. Speaker split (elder vs. interviewer) via **Muse Voice Transcribe** diarization.
2. **Assist-transcribe** — first-pass transcript; the grandchild (native speaker, no
   linguistics degree) corrects it in a side-by-side editor. *Human-in-the-loop is the
   product, not a limitation — this answers the #1 red-team risk.*
3. **Enrich** — Spark produces word-level glossary entries, idioms, an English meaning
   column; suggested cultural-context questions ("What is a *kula*? Who uses it?").
4. **Illustrate cultural cards** — photograph the object; **SAM 3.1** segments it;
   **Muse Image** renders a clean archival illustration; audio + photo + transcript +
   story bound into one "cultural card."
5. **Archive** — local-first database; community-owned export (open JSON + audio bundle).
   Sync to GitHub/HF only when the community chooses.

**Scope cut (red-team):** SAM 3.1 + Image illustration is optional garnish. If the deadline
threatens, audio→transcript→glossary→archive ships alone and still demos beautifully.

## 4. Architecture (7-day solo build)

```
Phone/Laptop mic ──► Recorder (MediaRecorder API, offline-first)
      │
      ├─ audio ──► muse-voice-transcribe-1.0 (streaming STT + diarization, $0.18/hr)
      │                └─ OFFLINE: queue audio; process on next sync window
      ├─ text ───► muse-spark-1.3 (glossary, idioms, translation, context questions)
      │                └─ OFFLINE path: muse-glimmer-30B self-hosted (llama.cpp)
      ├─ photo ──► sam-3.1 (segment object) ──► muse-image-1.0 (archival illustration)
      └─ all ────► Local-first store (SQLite + file blobs, Next.js PWA shell)
                       └─ explicit export: JSON+audio bundle → GitHub/HF (opt-in)
```

- **Frontend:** Next.js PWA — installable, runs from disk, airplane-mode-proof UI states.
- **Online path:** Meta Model API (`https://api.meta.ai/v1`, OpenAI-compatible).
- **Offline path:** **Muse Glimmer 30B** (Apache 2.0) via llama.cpp on CPU for glossary/
  translation assist + queued STT processing. Glimmer being open-weight is what makes the
  offline story honest — say it out loud in the demo.
- **Data ownership:** consent screen is first-class; export = one click, open formats.

## 5. Model cost budget (of the $150 credits)

| Usage | Est. cost |
|---|---|
| Voice Transcribe: 3 hrs demo recordings | ~$0.54 |
| Spark 1.3: glossary/enrichment ~100 cards, cached prompts | ~$2–5 |
| Muse Image: ~50 illustrations | $0.50 |
| SAM 3.1: ~50 photos | <$1 |
| Wonder (one-shot: scaffold + hardening agent via Muse Code) | ~$3–8 |
| **Total** | **< $15** — $135 headroom; "efficient by design" is a demo line |

## 6. 7-day build plan (today is Day 2 of the hackathon)

| Day | Ship |
|---|---|
| **2 (today)** | API smoke tests (Voice/Spark/Image/SAM); record 3 family sample clips (home dialect); repo + PWA shell; SQLite schema |
| **3** | Core loop online path: record → transcribe → correct (side-by-side editor) |
| **4** | Spark enrichment: glossary, idioms, context questions; complete card data model |
| **5** | Offline path: Glimmer via llama.cpp behind same interface; sync-queue; airplane-mode UI |
| **6** | SAM 3.1 + Muse Image cultural-card garnish; consent/export screens |
| **7** | Hardening (ponytail-audit + browser tests), demo video, architecture diagram, README, submission text |
| **buffer** | 12h reserved — submission DONE the morning of Nov 4 (Dhaka time) |

## 7. Risks & honest fallbacks (from the 5-judge red team)

| Risk | Severity | Mitigation in plan |
|---|---|---|
| ASR quality on undocumented languages | HIGH | ASR is *first-pass assist*; native-speaker correction is a core screen — demo shows it proudly. |
| Community trust / data ownership | HIGH | Consent + ownership screens first-class; open export; nothing leaves device without opt-in. |
| No internet in target communities | MED | Local-first architecture + Glimmer offline path — this IS the product, not an excuse. |
| Cultural context loss | HIGH | Card model binds audio+object+story; generated context questions asked live. |
| SAM 3.1 on low-light phone photos | MED | Garnish-only scope; degrade to photo-without-segmentation. |

## 8. Submission text (draft, edit at submission)

> **Bhasha — the offline language preservation studio.** Every few weeks a language dies;
> in Bangladesh dozens — Sylheti, Chittagonian, Chakma — have no datasets, no keyboards,
> no archives. Bhasha lets a grandchild record an elder and, in minutes, build a searchable
> cultural archive: diarized transcript (Muse Voice Transcribe), glossary and translations
> (Muse Spark), illustrated cultural cards (SAM 3.1 + Muse Image) — running **fully offline**
> on self-hosted Muse Glimmer, because the communities who need it have no reliable internet,
> and their languages belong to them, not to a cloud. Built for our world, on the frontier
> of open weights. Every artifact exports openly. The last fluent generation is talking —
> Bhasha makes sure the next one can listen.

## 9. Funnel provenance

2,449 raw ideas → dedupe → heuristic top 420 → LLM-judged on 5 rubric axes (400 scored) →
top 60 → single-elimination arena (60→16→8→4→3) → 5-persona judge council over the final
15 → **champion: 20/30 council points, top-3 votes from 4 of 5 judges** (creativity hawk,
platform native, demo hunter, contrarian). The one dissent (feasibility hawk) is answered
by the scope cut and day-by-day plan. Full audit trail: `ideation/funnel/`.
