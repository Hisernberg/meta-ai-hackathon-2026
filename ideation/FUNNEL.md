# Ideation Funnel — 2,449 ideas → 1 champion (audit trail)

Method: idea-refine (divergent) + arena (adversarial elimination) + 5-persona judge council.

## Stage A — Divergent generation (76 lenses)
76 specialized lenses (16 domains x 3 personas, 8 Meta-capability lenses, 12 theme twists,
8 wildcards) x ~32 ideas each = **2,449 raw ideas** → `raw/`, `corpus.csv`, `corpus.jsonl`.

## Stage B — Heuristic pre-score
Rules tuned to the indie rubric: multi-model bonus, flagship (Wonder/SAM) bonus,
specificity bonus, Dhaka/Bangladesh authenticity bonus; penalties for clichés,
hardware-dependence, and banned categories. All 2,449 scored.

## Stage C — LLM judge (first-round)
Top 420 scored 0-10 on five axes (wow, spec, build, meta, moat) by an LLM judge in
batches of 20 → 400 successfully judged → combined rank (judge total + heuristic/40).

## Stage D — Single-elimination arena
Top 60 → bracket rounds with adversarial attack verdicts:
- R1: 60 → 16 (12 groups of 5, top 2 advance)
- R2: 16 → 8 · R3: 8 → 4 · R4: 4 → 3 → Final-3

## Stage E — Council of 5 judge personas (over final 15 = final-3 + next best 12)
Personas: creativity hawk, feasibility hawk, Meta-platform native, demo-moment hunter,
contrarian. Each ranked all 15; points 5/3/2/1; votes counted.

**Board (top 8 of 15):**
| # | Idea | Council pts | Votes |
|---|------|------------|-------|
| 1 | **Offline Language Preserver** → became **Bhasha** | 20 | 4 |
| 2 | ChalkboardAI | 7 | — |
| 3 | AI Chef's Flavor Matrix | 6 | — |
| 4 | Product Prototype Visualizer | 4 | — |
| 5 | Medical Research Swarm | 3 | — |

Champion red-teamed (5 kill-risks + mitigations + demo beat sheet) → hardened spec in
`docs/CHAMPION.md`.

## Files
- `raw/` — 76 per-lens idea batches (JSON)
- `corpus.csv` / `corpus.jsonl` — full 2,449-idea corpus
- `funnel/stage1.json` — deduped + heuristic scores
- `funnel/stage2.json` — LLM judge scores (flagged red flags per idea)
- `funnel/arena_*.json` — every bracket round with attack verdicts
- `funnel/council.json`, `funnel/council_board.json` — council votes
- `funnel/redteam.json` — champion attack + demo beat sheet
