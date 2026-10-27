# Grand Ideation Funnel — Round 2 Report (FINAL)

## Pool
- Round 1 (incumbent): 2449 ideas (76 LLM lenses, saved funnel `ideation/funnel/`)
- Round 2 (new): 5419 ideas =
    5150 combinatorial (100 hand-curated work contexts x 46 mechanisms x 60 twists, seeded RNG)
    + 30 hand-crafted elite specs
    + 261 LLM elite (8 work-domain lenses: trades, frontline, owner-ops, inspect,
      institutional-memory, legacy-bridge, SAM-physical, voice-first) = 261 raw, 239 after dedupe
- **Grand pool: 7868 unique ideas** (title-Jaccard dedupe within and across rounds)

## Scoring (unified, fair across rounds)
Heuristic rubric 0-100 = creativity*2 + works*2 + ambition*1.5 + wow*1.5 + work_real*1.5 + meta*1 + fit*0.5
- round-2 mean 72.79 vs round-1 mean 63.36 (round-2 hard rules reward real-work specificity)
- Top-200 by heuristic -> LLM judge (5 axes: wow, spec, build, meta, moat; 10 batches, 200/200 scored)
- Final rank = judge_total + heuristic/10; diversity cap 3 per lens family -> 47 seeds
- Incumbent round-1 champion seeded at rank 1 (top seed = hardest path, title-holder rule)

## Arena (single elimination, LLM arena-master with attack verdicts)
48 -> 16 (8 serpentine groups of 6) -> 8 (4x4) -> 4 (2x4) -> 2 (semifinals) -> 1 (grand final)
- R1 kill of the incumbent seed "Offline Language Preserver" (Bhasha): "Endangered language
  documentation requires deep cultural context that transcription alone can't capture" /
  "Too vague on actual preservation methodology" — the round-2 hard rules (NEW + REAL WORK) applied.
- Elite "Shadow Copy" fell in R1 to "too similar to existing SOP creation tools"; the SAME
  concept family re-entered through the combinatorial path as "Cleat for stall chains"
  (film_sop + expert-approval loop + street-food vertical) and won the whole bracket —
  an independent replication of the strongest concept by two different generation paths.
- Grand final verdict on runner-up "Lintel for maintenance teams" (same mechanism, maintenance
  vertical): "Generic maintenance solution... too similar to existing CMMS products".
- Arena champion: "Bellows Bench" (manual-oracle mechanism, jewelry vertical).

## Council (5 personas over the final four — overrides arena per round-1 methodology)
1. **Cleat for stall chains** — 22 pts, 5/5 votes
2. **Bellows Bench** — 16 pts, 5/5 votes
3. **Lintel for maintenance teams** — 12 pts, 5/5 votes
4. **Produce Quality Inspector** — 0 pts, 0/5 votes

Judge champions: A-creativity -> Bellows Bench; B-feasibility, C-platform, D-demo-hunter,
E-work-realist -> Cleat for stall chains. **Council grand champion: Cleat for stall chains**
(film-once living SOP + expert approval + trainee quiz, street-food stall chains).

## Red-team of the champion
5 kill risks (filming adoption, approval bottleneck, SAM 3.1 in chaos, kitchen noise, UI
complexity) + 90-second demo beat sheet + scope cut (drop supply counts; live mode is bonus).
See `docs/CHAMPION_V2.md` for the full build-grade spec, 8-day plan and compliance checklist.

## Deliverables
- `ideation/round2/grand_corpus.csv` — all 7868 ideas with unified scores
- `ideation/round2/round2_ideas.csv` — round-2 ideas
- `ideation/round2/g_*.json` — complete arena/council/red-team audit trail
- `docs/CHAMPION_V2.md`, `docs/FORMS_READY.md` — champion spec + ready forms
- Champion: **Ustad** (arena alias "Cleat for stall chains") — Indie track, Build for Your World
