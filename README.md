# Bhasha — Offline Language Preservation Studio

**Meta Global AI Developer Hackathon 2026 entry** · Indie track · Build for Your World
Deadline: **Nov 4, 9:00 PM ET = Nov 5, 8:00 AM Dhaka** — submit ≥12h early.

> Record an elder speaking a low-resource language. Get a searchable cultural archive —
> diarized transcript, glossary, translations, illustrated cultural cards — running
> **fully offline** on self-hosted Muse Glimmer. The community owns the data.

- **Full spec & build plan:** [`docs/CHAMPION.md`](docs/CHAMPION.md)
- **Day-by-day playbook:** [`PLAYBOOK.md`](PLAYBOOK.md)
- **How this idea was chosen:** [`ideation/FUNNEL.md`](ideation/FUNNEL.md) — 2,449 ideas → 1 champion
- **Standing rubric for every agent session:** [`skills/00-hackathon-rubric/SKILL.md`](skills/00-hackathon-rubric/SKILL.md)

## Stack

| Layer | Choice |
|---|---|
| App | Next.js PWA (installable, offline-first, airplane-mode UI states) |
| Data | SQLite + file blobs, local-first; opt-in open export (JSON + audio) |
| Online AI | Meta Model API — `muse-voice-transcribe-1.0`, `muse-spark-1.3`, `sam-3.1`, `muse-image-1.0` |
| Offline AI | `muse-glimmer` 30B self-hosted (Apache 2.0) via llama.cpp |
| Credits | $150 Meta API (claim by Nov 4 ET!) + Baseten/Modal/Fireworks for open-weights |

## Quick start (dev)

```bash
cp .env.example .env       # fill MODEL_API_KEY (never commit .env)
npm install
npm run dev
```

## Repo map

```
docs/       champion spec, submission drafts, diagrams
ideation/   the full ideation funnel audit trail (2,449 ideas → champion)
skills/     curated agent-skill pack (36 skills, phase-ordered) + hackathon rubric
src/        the app (built during the hackathon)
```

## Non-negotiables

1. Every session starts with `skills/00-hackathon-rubric/SKILL.md` in context.
2. Scope cut is pre-authorized: SAM+Image garnish can be dropped; core loop cannot.
3. No secrets in git — ever. Tokens live in `.env` / `.secrets` (ignored).
4. Submission ships ≥12h before deadline; buffer time is sacred.
