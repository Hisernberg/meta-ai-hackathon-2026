# AGENTS.md — standing instructions for every coding agent in this repo

You are building **Bhasha**, the hackathon entry described in `docs/CHAMPION.md`.
Read it before anything else. Then follow `PLAYBOOK.md`.

## Prime directives

1. **Rubric in context:** re-read `skills/00-hackathon-rubric/SKILL.md` at session start.
   Every decision must be defensible against the judging criteria (creativity, technical
   ambition, WHETHER IT WORKS — indie track).
2. **The core loop is sacred:** record → assist-transcribe (human correction) → enrich →
   archive. It must always work end-to-end before any garnish is added.
3. **Scope cut is pre-authorized:** SAM 3.1 + Muse Image cultural cards are optional
   garnish. Drop them under time pressure without asking. Never drop offline-first or
   the consent/ownership screens.
4. **Incremental, tested slices:** thin vertical slice first (ugly but end-to-end by
   Day 3), then breadth. Tests on all logic. Nightly: script a 60-second browser walk
   of the demo path.
5. **Deadline is morning (Dhaka):** submission ships the morning of Nov 4 Dhaka time,
   12h before the real deadline. Demo video starts Day 7, not Day 8.

## Engineering rules

- Meta Model API: base `https://api.meta.ai/v1`, Bearer `MODEL_API_KEY`. Use the
  OpenAI-compatible `/v1/chat/completions` for Spark; streaming STT via
  `wss://api.meta.ai/v1/asr/realtime` for Voice; `/v1/images/*` for Image.
- One clean `src/lib/metaClient.ts` wraps ALL model calls (retries, cost logging,
  graceful degradation). No model calls scattered in components.
- Route routine calls to Spark 1.3; escalate only hard steps to Wonder.
- Offline-first: every UI state has an airplane-mode variant. Glimmer (llama.cpp) sits
  behind the same interface as the online path.
- Never commit `.env` or any token. `skills/00-hackathon-rubric/SKILL.md` §6 checklist
  gates every "done" claim.

## Available skill pack

`skills/` contains the curated 36-skill pack, phase-ordered (01-ideate … 07-meta).
Key ones for this build: `03-build/incremental-implementation`, `03-build/test-driven-development`,
`03-build/debugging-and-error-recovery`, `04-design/taste-skill` (UI polish pass Day 7),
`05-diagrams-docs/diagram-design` (architecture diagram), `06-verify-ship/webapp-testing`,
`06-verify-ship/ponytail-audit` (Day 7 sweep), `01-ideate/arena` (adversarial review of
the final submission).
