# -*- coding: utf-8 -*-
"""Persist round-3 arena results (in-context judging fallback, disclosed) + council."""
import json

DIR = "/home/z/my-project/hackathon-repo/ideation/round3"

ARENA = {
  "meta": {
    "pool": 10568, "shortlist": 140, "top40_by": "LLM triage (z-ai, 24 batched calls)",
    "top16_rule": "LLM triage order -> near-dup flavor removal -> family cap 3 -> incumbent Ustad (S139) protected seed",
    "judging_mode": "API 429 quota exhausted after triage stage; arena + council judged in-context "
                    "with full rules context (Indie axes x1/3 each; hard rules: NEW + real work use "
                    "case + 90s demo + 7-day solo). Documented as fallback in report.",
  },
  "QF": [
    {"m": "QF1", "a": "S004 Sheer for farm co-ops", "b": "S139 Ustad", "winner": "S139",
     "attackA": "market-rush counting drowns in occlusion; ledger accuracy unverifiable live",
     "attackB": "four-model integration heavy for 7 days (mitigated: staged fallbacks)"},
    {"m": "QF2", "a": "S077 museums morphing helper", "b": "S081 sign-language memory", "winner": "S081",
     "attackA": "universal-adapter scope melts 7 days; kiosks resist agents",
     "attackB": "sign understanding via general video models may underdeliver (scoped to retrieval)"},
    {"m": "QF3", "a": "S032 Seminar Twin", "b": "S099 claims errands while you sleep", "winner": "S032",
     "attackA": "briefing value real but wow is soft",
     "attackB": "logins + PII on insurer portals = legality gray zone + flaky live demo"},
    {"m": "QF4", "a": "S028 dental instant replay", "b": "S106 dental workflow closes itself", "winner": "S106",
     "attackA": "filming operatories = consent nightmare; live feedback unverifiable",
     "attackB": "EHR write-back is hidden labor (mitigable: chart-ready packet + paste)"},
    {"m": "QF5", "a": "S021 Methods Recipe", "b": "S119 claims agent teaches itself", "winner": "S021",
     "attackA": "env-setup automation can fail live",
     "attackB": "self-modifying agent = unpredictable demo; verification story missing"},
    {"m": "QF6", "a": "S039 Catalog Flip", "b": "S094 tutoring tape session", "winner": "S039",
     "attackA": "background-removal neighbors exist (wow is the full priced sheet)",
     "attackB": "minors on camera = consent maze; single-lesson signal thin"},
    {"m": "QF7", "a": "S065 extension schematic", "b": "S088 SLO for LLM", "winner": "S065",
     "attackA": "field reports are thin ground for a 400-page-style wow",
     "attackB": "eval dashboards look like CI, not magic"},
    {"m": "QF8", "a": "S017 SAM Measure walkability", "b": "S128 voice visa forms", "winner": "S017",
     "attackA": "photo calibration risk (mitigable: reference-object protocol)",
     "attackB": "DocuWizard (Seattle 2nd) already claimed conversational forms - novelty flag"},
  ],
  "SF": [
    {"m": "SF1", "a": "S139 Ustad", "b": "S081 sign-language memory", "winner": "S139",
     "why": "whether-it-works dominates; hardened spec vs scoped-novel risk"},
    {"m": "SF2", "a": "S032 Seminar Twin", "b": "S106 dental end-to-end", "winner": "S032",
     "why": "fully API-side works story vs EHR integration hidden labor"},
    {"m": "SF3", "a": "S021 Methods Recipe", "b": "S039 Catalog Flip", "winner": "S021",
     "why": "ambition: sandbox execution + dependency inference beats mask pipeline"},
    {"m": "SF4", "a": "S065 extension schematic", "b": "S017 SAM Measure", "winner": "S017",
     "why": "real buyer + novelty; calibration concern defensible with reference protocol"},
  ],
  "FINAL4": ["S021 Methods Recipe", "S139 Ustad", "S032 Seminar Twin", "S017 SAM Measure"],
  "F": [
    {"m": "F1", "a": "S139 Ustad", "b": "S032 Seminar Twin", "winner": "S139",
     "why": "demo density + world-authentic story beat a softer briefing wow"},
    {"m": "F2", "a": "S021 Methods Recipe", "b": "S017 SAM Measure", "winner": "S021",
     "why": "frontier ambition + builder authenticity; MR failure-visibility is a feature"},
  ],
  "GRAND": {
    "a": "S139 Ustad (incumbent, r2 champion)", "b": "S021 Methods Recipe", "winner": "S021",
    "attackA": "four-model integration heavy; kitchen-footage understanding brittle",
    "attackB": "env-setup demos can fail live - countered: failure cases ARE the demo (missing-seed flags); seed-locked golden set",
    "decision": "Methods Recipe takes creativity (verification artifact, not another paper-chatbot), "
                "ambition (1M-ctx parsing + Modal sandbox execution + graceful degradation), and "
                "frontier-theme fit (showcases Wonder 1M ctx + computer use + open weights); "
                "works parity via de-risked scope. Dethrones the incumbent.",
  },
  "champion": "S021",
}

COUNCIL = {
  "personas": ["pragmatist", "meta-maximalist", "showman", "auditor", "user-standin"],
  "votes": {
    "pragmatist":      ["S139", "S021", "S017", "S032"],
    "meta-maximalist": ["S021", "S032", "S139", "S017"],
    "showman":         ["S139", "S021", "S032", "S017"],
    "auditor":         ["S021", "S017", "S032", "S139"],
    "user-standin":    ["S021", "S032", "S139", "S017"],
  },
  "points": {"S021": 18, "S139": 13, "S032": 11, "S017": 8},
  "note": "4-3-2-1 per persona; in-context fallback (API 429), documented",
}

json.dump(ARENA, open(f"{DIR}/arena_results.json", "w"), indent=1)
json.dump(COUNCIL, open(f"{DIR}/council_board.json", "w"), indent=1)
json.dump({"champion": "S021", "title": "Methods Recipe: research freelancers upgrade",
           "points": COUNCIL["points"]}, open(f"{DIR}/result.json", "w"), indent=1)
print("arena + council persisted; champion = S021 Methods Recipe (18/20 council points)")
