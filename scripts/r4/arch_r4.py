# -*- coding: utf-8 -*-
"""Round-4 core: novel architecture signatures + agentic harness styles +
NEW hackathon rubric scorer (Impact 30 / Meta Tooling 25 / Tech Depth 20 / Demo 25)
+ anti-project filter from the updated Participant Guide (pasted by user, Oct 27 2026).

Rule changes encoded here vs rounds 1-3:
- Repos must be PUBLIC (no scoring effect; affects checklist)
- Stage-2 rubric weights: impact .30, meta_tooling .25, tech .20, demo .25
- Banned sample anti-projects: AI medical advice, basic RAG, simple image analyzers,
  AI-for-education chatbots, job application screener, nutrition coach, personality
  analyzers, sports analyzers/coaches, political/war projects.
- Baseten model id: meta-models/muse-spark-open-1026
- Bonus prizes: Most Viral ($20K, X), Best Open-Weight Build ($10K, Muse Glimmer /
  Spark Open), Community Vote ($10K), Best Agentic ($5K), Best Creative ($5K, Image/Wonder).
"""

# ---------------------------------------------------------------- architecture layer
# ARCH = the mechanism that makes the idea structurally novel (the "how nobody else does it")
# rarity: 1 = rarest/most distinctive (score bonus), 2 = solid.
ARCHS = [
 dict(id="A01", name="mixture-of-world-agents", rarity=1,
      mech="several world-model agents each simulate a different version of how the environment will respond; a gating router picks the rollout that best matches live evidence before any action is taken"),
 dict(id="A02", name="mixture-of-role-based-experts", rarity=1,
      mech="a standing cast of role experts — planner, skeptic, executor, auditor, historian — with a gate that routes each decision to the cheapest expert who can answer with attached evidence"),
 dict(id="A03", name="geometry-aware-segmentation-embedding", rarity=1,
      mech="SAM 3.1 masks act as geometric priors for the embedding space: features live on the mask-shaped manifold, retrieval walks geodesics instead of straight lines, and optimization respects segment curvature"),
 dict(id="A04", name="conformal-autonomy-gates", rarity=1,
      mech="every agent action ships with a statistically calibrated confidence band; below the gate the system must ask a human or escalate models — autonomy is bought with evidence, never assumed"),
 dict(id="A05", name="world-model-rollout-planner", rarity=2,
      mech="before acting, the agent imagines three rollouts of the outcome, scores each against the goal, and executes only the survivor"),
 dict(id="A06", name="process-reward-verifier", rarity=2,
      mech="a verifier model scores each intermediate step, not just the final answer; any step that cannot show receipts is redone"),
 dict(id="A07", name="tool-forge", rarity=2,
      mech="when no existing tool fits, the agent forges one — writes, tests and version-pins a new function in a sandbox, then banks it for reuse"),
 dict(id="A08", name="skill-library-compounding", rarity=2,
      mech="every solved task is distilled into a reusable skill card, so the agent's library compounds and each new job starts smarter"),
 dict(id="A09", name="speculative-ensemble-early-exit", rarity=1,
      mech="several cheap agents race in parallel on partial evidence; the moment two agree, slower experts are cancelled — consensus doubles as an early-exit signal"),
 dict(id="A10", name="blackboard-arena", rarity=2,
      mech="specialists post competing claims to a shared blackboard; a moderator agent resolves conflicts and promotes only the best-evidenced claim to action"),
 dict(id="A11", name="debate-consensus", rarity=2,
      mech="two adversary agents argue opposite verdicts from the same evidence; a judge model accepts only verdicts that survive cross-examination"),
 dict(id="A12", name="causal-probe-suite", rarity=1,
      mech="the agent runs interventions on its own inputs — perturb, ablate, shuffle, relabel — and only reports conclusions that survive the probe battery"),
 dict(id="A13", name="object-centric-episodic-memory", rarity=1,
      mech="SAM 3.1 tracks become first-class memory addresses: events are indexed by which objects appeared, moved or changed, not by text alone"),
 dict(id="A14", name="optimal-transport-alignment", rarity=1,
      mech="datasets, plans and outputs are matched by optimal transport, so 'how close is this run to the spec' finally has one honest number"),
 dict(id="A15", name="hypergraph-task-decomposition", rarity=2,
      mech="tasks split into a hypergraph where one shared node serves many subtasks, and the scheduler reuses completed work instead of redoing it"),
 dict(id="A16", name="test-time-training-loop", rarity=1,
      mech="whenever the router detects distribution shift, the small open-weight model LoRA-fine-tunes on the spot from the last batch of labeled outcomes"),
 dict(id="A17", name="self-play-curriculum", rarity=2,
      mech="the system generates its own graded exercises, solves them, and promotes itself only after beating its previous best score"),
 dict(id="A18", name="digital-twin-divergence-watch", rarity=2,
      mech="a twin of the real process runs slightly ahead of reality; when twin and reality drift past tolerance, an agent opens the delta and names the cause"),
 dict(id="A19", name="trace-indexed-retrieval", rarity=1,
      mech="retrieval indexes executable traces — runs, logs, diffs, receipts — instead of documents: you search what the machine DID, not what it said"),
 dict(id="A20", name="segment-as-index", rarity=1,
      mech="every visual region is a queryable address; ask 'what changed in region 3 since Tuesday' and the segmentation index answers with receipts"),
 dict(id="A21", name="cross-modal-lattice", rarity=1,
      mech="frames, transcripts and segment masks align into one lattice where every fact carries its three witnesses — pixel, timestamp, utterance"),
 dict(id="A22", name="uncertainty-cascade-router", rarity=2,
      mech="requests start on the cheapest open-weight model and climb the cascade (Glimmer to Spark Open to Spark to Wonder) only while uncertainty stays high"),
 dict(id="A23", name="synthetic-contrastive-loop", rarity=1,
      mech="SAM segments real cases, Muse Image synthesizes hard negatives targeted at the current confusion pair, and the classifier must beat both before shipping"),
 dict(id="A24", name="eval-first-harness", rarity=2,
      mech="the agent writes the acceptance tests before the solution; nothing ships until its own eval suite passes in CI"),
 dict(id="A25", name="market-negotiation-agents", rarity=1,
      mech="sub-agents bid compute and claim tasks with priced bids; an auctioneer agent allocates work to maximize value per credit"),
 dict(id="A26", name="supervisor-swarm-budget", rarity=2,
      mech="a supervisor hires a swarm under explicit budgets — time, tokens, GPU-seconds — and re-hires on failure; autonomy with an accountant"),
]
ARCH_BY_ID = {a["id"]: a for a in ARCHS}

# ---------------------------------------------------------------- harness layer
# HARNESS = the agentic orchestration style (how the work is coordinated)
HARNESS = [
 dict(id="H01", name="planner-executor-verifier", depth=3, note="plans, acts, and a third agent verifies every step against the plan"),
 dict(id="H02", name="blackboard-crew", depth=3, note="specialists coordinate through a shared working memory rather than a chain"),
 dict(id="H03", name="adversarial-debate", depth=3, note="rival agents argue the verdict before it is allowed to ship"),
 dict(id="H04", name="supervisor-swarm", depth=4, note="one supervisor fans work out to a parallel swarm and merges results"),
 dict(id="H05", name="hierarchical-crew", depth=3, note="team leads own subgoals; workers own steps; escalation is explicit"),
 dict(id="H06", name="tool-forge-loop", depth=4, note="the agent extends its own toolset mid-task when gaps appear"),
 dict(id="H07", name="skill-library", depth=3, note="solutions are banked as skills and replayed on similar future tasks"),
 dict(id="H08", name="process-reward-loop", depth=4, note="a step-level judge scores progress and restarts bad branches early"),
 dict(id="H09", name="rollout-plan-act", depth=4, note="imagine, evaluate, then act — world-model rollouts gate every action"),
 dict(id="H10", name="market-auction", depth=4, note="tasks are auctioned to the best-priced competent agent"),
 dict(id="H11", name="speculative-race", depth=3, note="parallel attempts with early exit on consensus"),
 dict(id="H12", name="human-gated-autonomy", depth=2, note="the agent is autonomous inside calibrated confidence, human outside it"),
 dict(id="H13", name="critic-self-repair", depth=3, note="a standing critic finds flaws and the worker repairs before delivery"),
 dict(id="H14", name="eval-first-ci", depth=3, note="acceptance tests are authored first; agents work to make CI green"),
]
HARNESS_BY_ID = {h["id"]: h for h in HARNESS}

# ---------------------------------------------------------------- anti-project filter
import re
ANTI_PATTERNS = [
    (r"\bmental health\b|\btherapy\b|\bsuicid|\bself[- ]harm", "medical/mental-health advice"),
    (r"\bdiagnos|\bmedical advice\b|\bsymptom checker\b|\bskin (blemish|lesion|rash|cancer)|\bderma\b|\bx[- ]ray\b|\bradiolog|\bprescri", "medical advice"),
    (r"\bnutrition|\bdiet plan\b|\bcalorie|\bmeal plan", "nutrition coach"),
    (r"\bpersonality (test|quiz|analy)|\bmbti\b|\bhoroscope|\bastrolog|\bdating match", "personality analyzer"),
    (r"\bsports? analyz|\bsports? coach|\bmatch analy|\bfootball analy|\bcricket analyz|\bathlete track|\bfitness coach|\btraining load", "sports analyzer/coach"),
    (r"\bjob application\b|\bresume screen|\bcv screen\b|\bapplicant (tracking|screen)|\bhiring (filter|screen)|\bcandidate rank", "job application screener"),
    (r"\bpolitical\b|\belection\b|\bcampaign ads?\b|\bwar\b|\bmilitary\b|\bweapon|\bdrone strike", "political/war"),
    (r"\b(homework helper|study buddy|tutor chatbot|education chatbot)\b|\bai tutor app\b", "generic AI-for-education chatbot"),
    (r"\b(basic|simple|plain) rag\b|\brag chatbot\b|\bchatbot (over|for) (documents|pdfs?)\b|\bchat with (your )?(pdf|docs?|notes)\b|\bpdf (qa|chat|summariz)", "basic RAG app"),
    (r"\bsimple image analyz|\bimage (tagger|describer|captioner) app\b|\bphoto (tagger|organizer) app\b", "simple image analyzer"),
]
BANNED_CTX_SUBSTR = ("amateur league", "amateur football", "gaming club", "e-sports",
                     "village clinic", "physio", "dental", "nursing home", "care home",
                     "special-ed", "coaching center", "sports")

def anti_check(text):
    t = text.lower()
    for pat, label in ANTI_PATTERNS:
        if re.search(pat, t):
            return label
    return None

def ctx_banned(ctx_full):
    low = ctx_full.lower()
    return any(b in low for b in BANNED_CTX_SUBSTR)

# ---------------------------------------------------------------- NEW rubric scorer
CAP_NAME = {"W": "muse-wonder-1.0", "S": "muse-spark-1.3", "I": "muse-image-1.0",
            "V": "muse-voice-transcribe-1.0", "SAM": "sam-3.1",
            "SO": "muse-spark-open-1026", "G": "muse-glimmer"}
RARE_CAPS = {"SAM", "SO", "G", "W"}
SIG_CAP = {"W": 1.0, "SAM": 1.0, "SO": 0.9, "G": 0.7, "V": 0.6, "I": 0.6, "S": 0.2}

def arch_bonus(arch):
    return {1: 1.9, 2: 1.1, 3: 0.5}.get(arch["rarity"], 0.5)

def score_idea_r4(rng, pattern, arch, harness, caps, ctx_boost, users_n):
    """NEW Stage-2 rubric: impact .30, meta_tooling .25, tech .20, demo .25 (0-100 total).
    pattern needs: wow (0-10), impact (0-10 prior). ctx_boost: 0/1/2 impact multiplier."""
    n = len(caps)
    rare = any(c in RARE_CAPS for c in caps)
    sig = sum(SIG_CAP.get(c, 0.2) for c in caps) / max(1, n)
    u = rng.uniform

    impact = (pattern["impact"] * 0.55 + ctx_boost * 1.1
              + (1.2 if users_n > 1 else 0) + u(-0.5, 0.5))
    impact = max(1, min(10, impact))

    meta = (3.0 + 1.15 * min(n, 4) + (1.2 if rare else 0) + 0.7 * sig
            + (0.8 if arch["id"] in ("A03", "A13", "A20", "A21", "A23") else 0) + u(-0.4, 0.4))
    meta = max(1, min(10, meta))

    complexity = harness["depth"] + (2 if arch["rarity"] == 1 else 0)
    tech = (3.6 + arch_bonus(arch) + harness["depth"] * 0.45
            + (0.9 if any(c in ("SO", "G") for c in caps) else 0) + u(-0.4, 0.4))
    tech = max(1, min(10, tech))
    days = max(4, min(9, int(round(3.2 + complexity * 0.55 + (0 if n <= 3 else 0.6) + u(0, 1.2)))))

    demo = (pattern["wow"] * 0.62
            + (1.8 if arch["id"] in ("A01", "A02", "A09", "A13", "A20", "A23") else 0.9)
            + (1.0 if pattern.get("visual") else 0) + u(-0.5, 0.5))
    demo = max(1, min(10, demo))

    total = (impact * 0.30 + meta * 0.25 + tech * 0.20 + demo * 0.25) * 10
    flags = dict(
        open_weight=bool(any(c == "SO" for c in caps) or
                         (arch["id"] in ("A16", "A22") and any(c in ("SO", "G") for c in caps))),
        agentic=bool(harness["depth"] >= 3),
        creative=bool("I" in caps and n >= 2),
        viral=bool(demo >= 8.6),
    )
    return dict(impact=round(impact, 1), meta_tooling=round(meta, 1),
                tech=round(tech, 1), demo=round(demo, 1), total=round(total, 1),
                days=days, flags=flags)
