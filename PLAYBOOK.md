# Hackathon Playbook — Skills × Meta Models × Days

Meta Global AI Developer Hackathon · Oct 26 – Nov 4, 2026
Your timezone: **Asia/Dhaka (UTC+6)** — every "ET" deadline is ~11 hours later for you.

**Submission deadline: Nov 4, 9:00 PM ET = Nov 5, 8:00 AM Dhaka.**
Work backwards from the morning, not the evening.

---

## Standing setup (do once, Day 1)

| # | Action | Why |
|---|---|---|
| 1 | Claim **$150 Meta Model API credits** (form → Billing page → card on file → Spend Limit alert) | Card setup trips people up; batches take time |
| 2 | Apply for **Baseten $100 / Modal $100 / Fireworks $25** credits | Only useful if you touch open-weights (Spark Open / Glimmer) |
| 3 | Join the hackathon **Discord**, read the Official Rules on the event page | Workshop schedule, submission format live there |
| 4 | Copy this pack's `skills/` into your repo, load `00-hackathon-rubric` | Rubric in context for every session |
| 5 | Smoke-test the API: one Spark call, one Image call, one Voice call | Fail early, not on Day 8 |

## Day-by-day

### Day 1–2 (Oct 27–28) — DEFINE · *skills: 01-ideate + 02-spec-plan*
- Run `interview-me` then `idea-refine` on your raw idea. Lock ONE painful, specific
  problem (Build for Your World) or one frontier capability (Push the Frontier).
- `arena --quick` on the idea itself: 16 agents attack the concept, not the code.
  Cheap way to find the fatal flaw while it's still free to fix.
- `spec-driven-development` → one-page spec. `constraint-driven-development` → write
  the quality bar (this is your anti-scope-creep contract for Day 5).
- **Meta models:** smoke tests only. Pick your model combo and name it in the spec.

### Day 2–3 (Oct 28–29) — PLAN · *skills: 02-spec-plan*
- `planning-and-task-breakdown` → ordered tasks, each ending in something demoable.
- Mark the *demo path*: the exact 90 seconds the judges will see. Build toward it.
- `context-engineering` → set up your per-session priming so the agent stays sharp
  all week.

### Day 3–7 (Oct 29–Nov 2) — BUILD · *skills: 03-build*
- `incremental-implementation`: thin vertical slice through the whole stack by end of
  Day 4 — ugly but end-to-end. Then breadth.
- `api-and-interface-design` + `source-driven-development`: one clean `metaClient`
  module; verify every call against official docs, not memory.
- Route routine calls to **Muse Spark 1.3**; escalate the hard agentic loop to
  **Muse Wonder**; add **Muse Image / Voice / SAM 3.1** where they create the "wow"
  moment — a multi-model combo is platform fluency the judges notice.
- `test-driven-development` on anything with logic; `debugging-and-error-recovery`
  when it breaks (it will); `performance-optimization` only after it works.
- Nightly: 60-second browser walk of the demo path.

### Day 7–8 (Nov 2–3) — DESIGN · *skills: 04-design + 05-diagrams-docs*
- `taste-skill` pass on the UI: kills the "AI-made" look judges have seen 500 times.
- `diagram-design` → one architecture diagram for the README (styled, not default).
- `canvas-design` → cover image / social card; `image-enhancer` → sharpen screenshots.
- `theme-factory` if you need consistent slide/doc styling fast.
- **Start the demo video today.** Open on the payoff, <10 seconds in.

### Day 8–9 (Nov 3–4) — VERIFY → SHIP · *skills: 06-verify-ship*
- `webapp-testing` + `browser-testing-with-devtools`: scripted clean-machine run of the
  full demo path. "Whether it works" is ⅓ of the indie score.
- `ponytail-audit` → whole-repo sweep for bugs/security; `code-review-and-quality` on
  the final diff; `doubt-driven-development` → adversarial attack on every remaining
  assumption; full `arena` run on the submission text.
- `shipping-and-launch` checklist; `changelog-generator` if iterations are worth showing.
- README via the rubric checklist: value prop, diagram, model list, setup, theme
  statement, fallback behavior.
- **Submit ≥12h before deadline** (Nov 4 morning Dhaka-time), not at 7:59 AM Nov 5.

---

## Skill → judging-criteria map (why each exists in this pack)

| Judging signal | Skills that directly serve it |
|---|---|
| **Whether it works** (indie ⅓) | webapp-testing, browser-testing-with-devtools, test-driven-development, debugging-and-error-recovery, shipping-and-launch |
| **Creativity** (indie ⅓) | idea-refine, arena, taste-skill, canvas-design |
| **Technical ambition** (indie ⅓) | api-and-interface-design, mcp-builder, multi-model Meta stack, source-driven-development |
| **Technical execution** (startup) | incremental-implementation, performance-optimization, security-and-hardening, ponytail-review |
| **Production readiness** (startup) | shipping-and-launch, ponytail-audit, code-review-and-quality, observability habits from the rubric checklist |
| **Theme fit** (both) | hackathon-rubric (theme statement generator), interview-me |
| **Submission quality** | diagram-design, docx/pdf/pptx, changelog-generator, image-enhancer, README checklist in rubric |

## Two ways to use this pack — pick deliberately

1. **Build faster (default):** skills drive *your* coding agent (Claude Code, Codex,
   Cursor...) while your app calls Meta Model API. The agent is the carpenter; Meta
   models are the material. This is the intended use.
2. **Meta-native experiment:** Muse Code is a terminal coding agent in the same
   product family. The Agent Skills format (`SKILL.md`) is an open standard — try
   loading `00-hackathon-rubric` + a few phase skills into your Muse Code setup and
   note what happens. If it works, "skills running natively on Muse Code" is itself a
   demo-able capability story for a Push the Frontier entry. Treat as experimental;
   verify against Muse Code's docs before relying on it.
