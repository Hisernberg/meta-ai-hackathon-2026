---
name: hackathon-rubric
description: >
  Context skill for the Meta Global AI Developer Hackathon (Oct 26 - Nov 4, 2026).
  Encodes the official tracks, themes, judging criteria, submission strategy, and a
  Meta Model API cheat sheet (models, pricing, endpoints, credits). Use this skill in
  EVERY session while building the hackathon project: when planning what to build,
  when making architecture decisions, when choosing which Meta models to integrate,
  when writing the submission text, when preparing the demo video, and before
  finalizing any deliverable. If a decision affects scope, pick the option that
  scores highest against the judging criteria in this skill.
---

# Meta Global AI Developer Hackathon — Project Rubric & API Cheat Sheet

You are building the entry for the Meta Global AI Developer Hackathon. Internalize this
page before any planning or building decision. Every choice must be defensible against
the judging criteria below.

## 1. Event facts

- 10-day virtual hackathon: Oct 26 (kickoff) → Nov 4, 9:00 PM ET submissions.
- Hosts: Meta + Cerebral Valley. Prize pool $1,000,000. Up to 20,000 participants.
- Timezone guard: the deadline (Nov 4, 9:00 PM ET) is Nov 5, ~8:00 AM Asia/Dhaka.
  Reserve the final 48 hours for demo video + submission buffer. Submit early.

## 2. Tracks — pick one and optimize for its rubric

| | Indie developer track | Startup track |
|---|---|---|
| Who | Individual builders, students | Teams/founders with a real product |
| Judged on | **creativity, technical ambition, whether it works** | **technical execution, whether it holds up in production** |

Implication for indie: a smaller, flawless, surprising demo beats an ambitious broken
one. "Whether it works" is one third of the score — reliability engineering is scoring
work, not overhead.
Implication for startup: production readiness = auth, error handling, rate-limit
resilience, logging, deployment story. Show health checks and graceful degradation.

## 3. Themes — every project must fit one

1. **Build for Your World** — solve a problem you know firsthand in your own domain.
   Judges look for authenticity and domain insight: real pain, real users, measurable
   time saved or new capability unlocked.
2. **Push the Frontier** — give a machine a new capability in software, robotics,
   manufacturing, energy, materials, science. Physical-world or scientific angle;
   SAM 3.1 perception, agentic tool use, or experiment automation score well here.

State the chosen theme explicitly in the submission and explain the fit in one sentence.

## 4. Model usage strategy (implicit fourth criterion)

Provider-run hackathons reward projects that showcase the provider's newest models.
Use multiple Meta models in combination and say so in the submission:

- **Muse Spark 1.3** (`muse-spark-1.3`) — default workhorse: reasoning, tool calling,
  1M context. Cheapest capable tier; Contributor mode discounts further.
- **Muse Wonder** (`muse-wonder-1.0`) — flagship (released Oct 12): long-horizon agents,
  computer use, multimodal input, sub-agent delegation. Use for the hard agentic loop.
- **Muse Image** (`muse-image-1.0`) — $0.01/image generation + anchored multi-turn edits.
- **Muse Voice Transcribe** (`muse-voice-transcribe-1.0`) — $0.18/hr streaming STT with
  diarization (WebSocket `wss://api.meta.ai/v1/asr/realtime`).
- **SAM 3.1** (`sam-3.1`) — text/point/box-prompted segmentation of images and video;
  the "Push the Frontier" differentiator.
- **Muse Spark Open** (816B MoE open weights) and **Muse Glimmer** (30B, Apache 2.0) —
  self-hosted story via Baseten/Modal/Fireworks credits when local control matters.

Name the models in the README and demo. "Built with Muse Wonder + SAM 3.1" reads as
platform fluency.

## 5. Meta Model API cheat sheet

- Base URL `https://api.meta.ai/v1`, Bearer token (`MODEL_API_KEY`).
- Three protocol surfaces — reuse existing SDKs by changing base URL:
  - Responses API (`POST /v1/responses`) — agentic, reasoning replay, structured output.
  - Chat Completions (OpenAI-compatible) — `/v1/chat/completions`.
  - Messages (Anthropic-compatible) — `/v1/messages`.
- Pricing: Wonder $4/M in, $0.20 cached, $20/M out · Spark 1.1 $1.25/$4.25 ·
  Image $0.01/image · Voice $0.18/hr. 1M context on Wonder/Spark. No long-context surcharge.
- Capabilities: parallel + streamed tool calls, tool search, search grounding with
  citations, image understanding/generation, video understanding, media segmentation,
  file handling (upload once, reference by ID), reasoning effort control, structured
  JSON output, prompt caching, token counting.
- **$150 API credits** per participant — claim via the event form, credit card required
  on the billing account, set a Spend Limit alert. Deadline Nov 4, 9:00 PM ET.
  Partner credits: Baseten $100 (+2M TPM), Modal $100, Fireworks $25.
- Cost discipline: budget roughly $20–40 of the $150 for the demo period; cache prompt
  prefixes; route routine calls to Spark, escalate to Wonder only for hard steps.

## 6. Submission scoring checklist (apply before finishing anything)

- [ ] Works end-to-end on a clean machine (one-command setup, seeded demo data).
- [ ] Live demo path rehearsed; demo video opens on the working payoff in <10 seconds.
- [ ] README: one-line value prop, 30-second architecture diagram, model list, setup,
      theme statement ("This is a Build for Your World project because...").
- [ ] Fallback behavior when a model call fails or rate-limits (never a dead screen).
- [ ] Cost visible and bounded (token accounting in logs; spend limit alert on).
- [ ] Repo hygiene: MIT license, .env.example, no secrets in git history.
- [ ] Scope honesty: everything demoed is implemented; nothing demoed is half-wired.

## 7. Timeline discipline (started Oct 26; assume 9 usable days)

- Days 1–2: idea lock (indie: one painful, specific problem), spec, API smoke tests.
- Days 3–7: core build, thin vertical slice first, then breadth; nightly browser test
  of the demo path.
- Day 7–8: harden, degrade-gracefully paths, polish UI with taste pass.
- Final 48h: demo video, README, architecture diagram, arena-style adversarial review,
  submit at least 12h before the deadline (portal congestion is real).
