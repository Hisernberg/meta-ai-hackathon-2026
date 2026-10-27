# -*- coding: utf-8 -*-
"""Round-3 idea composer: winner-DNA lane (W) + user-profile lane (U).
Renders structured idea genomes, dedupes against the 7,868-idea grand pool,
scores with the same heuristic axes as rounds 1-2 for fair comparison."""
import csv, json, math, random, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from winner_dna import WINNER_DNA, W_CONTEXTS
from profile_domains import PROFILE_DOMAINS

CAP_NAME = {"W": "muse-wonder-1.0", "S": "muse-spark-1.3", "I": "muse-image-1.0",
            "V": "muse-voice-transcribe-1.0", "SAM": "sam-3.1", "SO": "muse-spark-open",
            "G": "muse-glimmer"}

GRAND_CSV = "/home/z/my-project/download/hackathon_ideas_grand_corpus_7868.csv"
OUT_CSV = "/home/z/my-project/download/hackathon_ideas_round3.csv"

# ---------- dedupe ----------
_tok = re.compile(r"[a-z0-9]+")
def toks(s): return set(_tok.findall(s.lower()))
def jaccard(a, b):
    if not a or not b: return 0.0
    return len(a & b) / len(a | b)

def load_existing_titles():
    ts = []
    with open(GRAND_CSV, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ts.append(toks(r.get("title", "")))
    return ts

# ---------- rendering ----------
def render_title(rng, angle, ctx_short):
    t = angle.format(c=ctx_short)
    t = re.sub(r"\s+", " ", t).strip(" ,.")
    return t[0].upper() + t[1:]

TWISTS = [
    "with every step logged for audit", "fully voice-first for hands-busy users",
    "works on a 40-dollar Android", "Bengali-first, English next",
    "with a consent-first camera policy", "runs offline on self-hosted open weights",
    "with replayable evidence for every verdict", "priced at less than a cup of tea per day",
    "with graceful fallback when the network dies", "output exportable to the tools people already use",
]

def pick_twist(rng, i):
    return TWISTS[(rng.randrange(len(TWISTS)) + i) % len(TWISTS)]

def render_pitch(rng, cap_ids, ctx_full, artifact, conf_hook=None, lane="W",
                 lens_desc=None, pat_note=None):
    cap_txt = " + ".join(CAP_NAME[c].replace("muse-", "Muse ").replace("muse-", "") for c in cap_ids[:2])
    cap_txt = cap_txt.replace("wonder-1.0", "Wonder (1M ctx, computer use)").replace(
        "spark-1.3", "Spark").replace("image-1.0", "Image").replace(
        "voice-transcribe-1.0", "Voice").replace("sam-3.1", "SAM 3.1").replace(
        "spark-open", "Spark Open (open weights)").replace("glimmer", "Glimmer")
    if lane == "U" and lens_desc:
        lead = lens_desc[0].upper() + lens_desc[1:]
        p = f"{lead}. For {ctx_full}"
        if conf_hook: p += f" — grounded in {conf_hook}"
        return (p + f". Stack: {cap_txt}.")[:280]
    base = (f"{pat_note}. Applied to {ctx_full}: {artifact} become decisions, "
            f"not paperwork — {cap_txt} behind it")
    if conf_hook: base += f"; grounded in {conf_hook}"
    return base[:280]

# ---------- scoring (same axes as r1/r2 for comparability) ----------
def score_idea(rng, feas, wow, amb, n_caps, rare_cap, artifact_concrete, ctx_specific, twist):
    creativity = min(10, 4.5 + (2.0 if twist else 0) + (1.5 if rare_cap else 0) + rng.uniform(-0.6, 0.6))
    ambition = min(10, amb * 0.8 + 0.8 * (n_caps >= 3) + rng.uniform(-0.5, 0.5))
    works = max(1, min(10, feas + (0.5 if n_caps <= 2 else -0.5) + rng.uniform(-0.8, 0.8)))
    work_real = min(10, 5.5 + 2.2 * artifact_concrete + 1.4 * ctx_specific + rng.uniform(-0.6, 0.6))
    meta = min(10, 3.5 + 1.3 * n_caps + (1.2 if rare_cap else 0) + rng.uniform(-0.5, 0.5))
    fit = min(10, 7.6 + rng.uniform(-0.8, 0.8))
    days = max(3, min(7, int(round(9 - works + rng.uniform(0, 1.4)))))
    feasv = max(1, min(10, 11 - days + rng.uniform(-0.4, 0.4)))
    total = round((creativity * 0.14 + ambition * 0.12 + works * 0.18 + work_real * 0.18 +
                   meta * 0.12 + fit * 0.10 + wow * 0.16) * 10, 1)
    return dict(score_total=total, creativity=round(creativity, 1), ambition=round(ambition, 1),
                works=round(works, 1), work_real=round(work_real, 1), meta=round(meta, 1),
                fit=round(fit, 1), wow=wow, feas=round(feasv, 1), days=days)

RARE_CAPS = {"SAM", "SO", "G", "W"}

def compose(rng, pattern, ctx, cap_ids, lens=None, lens_desc=None, conf_hook=None, lane="W"):
    ctx_full, ctx_short, artifact = ctx
    angle = rng.choice(pattern["angles"])
    title = render_title(rng, angle, ctx_short)
    twist = pick_twist(rng, rng.randrange(97))
    if lane == "W":
        pitch = render_pitch(rng, cap_ids, ctx_full, artifact, pat_note=pattern.get("note", ""))
    else:
        pitch = render_pitch(rng, cap_ids, ctx_full, artifact, conf_hook, lane="U", lens_desc=lens_desc)
    sc = score_idea(rng, pattern["feas"], pattern["wow"], pattern["amb"], len(cap_ids),
                    any(c in RARE_CAPS for c in cap_ids),
                    artifact_concrete=1 if len(artifact) > 6 else 0,
                    ctx_specific=1, twist=twist)
    models = "+".join(CAP_NAME[c] for c in cap_ids)
    return dict(lens=f"{lane}-{pattern['id']}" + (f"-{lens}" if lens else ""),
                title=title, pitch=pitch, theme=pattern.get("theme", "world"),
                domain=ctx_full, models=models, twist=twist,
                **{k: sc[k] for k in ("score_total", "creativity", "ambition", "works",
                                      "work_real", "meta", "fit", "wow", "feas", "days")})

def fingerprint(idea):
    parts = idea["lens"].split("-")
    key_id = "-".join(parts[:3]) if parts[0] == "U" else "-".join(parts[:2])
    return (key_id, idea["domain"], idea["models"])

SLUG_FIX = {"lora": "LoRA", "ab": "A/B", "dag": "DAG", "slo": "SLO", "llm": "LLM",
            "ci": "CI", "qa": "QA", "ml": "ML", "sam": "SAM 3.1", "a": "A"}
def slug_title(slug):
    words = slug.split("-")
    return " ".join(SLUG_FIX.get(w, w.capitalize()) for w in words)

U_TITLE_T = ["{s} for {c}", "{s}: {c} upgrade", "Self-serve {s} for {c}",
             "{c} run on {s}", "The {c} {s}", "{s}, built for {c}"]

def generate(rng_seed=33, target_w=1300, target_u=1400):
    rng = random.Random(rng_seed)
    existing = load_existing_titles()
    print(f"existing titles loaded: {len(existing)}")
    seen_exact, seen_titles = set(), []
    out = []

    def add(idea):
        key = fingerprint(idea)
        tt = toks(idea["title"])
        if key in seen_exact: return False
        for et in seen_titles[-6000:]:
            if jaccard(tt, et) > 0.85: return False
        for et in existing:
            if jaccard(tt, et) > 0.78: return False
        seen_exact.add(key); seen_titles.append(tt); out.append(idea); return True

    # ---- lane W: winner-DNA compositions ----
    made_w = 0; guard = 0
    while made_w < target_w and guard < target_w * 60:
        guard += 1
        p = WINNER_DNA[guard % len(WINNER_DNA)] if rng.random() < 0.55 else rng.choice(WINNER_DNA)
        ctx = W_CONTEXTS[guard % len(W_CONTEXTS)] if rng.random() < 0.5 else rng.choice(W_CONTEXTS)
        caps = list(rng.choice(p["caps"]))
        if rng.random() < 0.30:  # enrich with a third model for ambition spread
            extra = rng.choice([c for c in ["S", "V", "I", "SAM", "G", "SO", "W"] if c not in caps])
            caps = caps + [extra]
        idea = compose(rng, p, ctx, caps, lane="W")
        idea["round"] = 3
        if add(idea): made_w += 1
        if made_w % 300 == 0 and made_w: print(f"  lane W: {made_w}")

    # ---- lane U: user-profile compositions ----
    made_u = 0; guard = 0
    while made_u < target_u and guard < target_u * 60:
        guard += 1
        d = PROFILE_DOMAINS[guard % len(PROFILE_DOMAINS)] if rng.random() < 0.55 else rng.choice(PROFILE_DOMAINS)
        lens_name, lens_desc = d["lenses"][guard % len(d["lenses"])] if rng.random() < 0.5 else rng.choice(d["lenses"])
        ctx = d["contexts"][guard % len(d["contexts"])] if rng.random() < 0.5 else rng.choice(d["contexts"])
        caps = list(rng.choice(d["caps"]))
        if rng.random() < 0.30:
            extra = rng.choice([c for c in ["S", "V", "I", "SAM", "G", "SO", "W"] if c not in caps])
            caps = caps + [extra]
        pat = dict(id=d["id"], angles=[rng.choice(U_TITLE_T).format(
                       s=slug_title(lens_name), c=ctx[1])],
                   feas=d["feas"], wow=d["wow"], amb=d["amb"], theme=d["theme"])
        idea = compose(rng, pat, ctx, caps, lens=lens_name, lens_desc=lens_desc,
                       conf_hook=rng.choice(d["conf_hooks"]), lane="U")
        idea["round"] = 3
        idea["lens"] = f"U-{d['id']}-{lens_name}"
        if add(idea): made_u += 1
        if made_u % 300 == 0 and made_u: print(f"  lane U: {made_u}")

    cols = ["round", "lens", "title", "pitch", "theme", "domain", "models", "twist",
            "score_total", "creativity", "ambition", "works", "work_real", "meta",
            "fit", "wow", "feas", "days"]
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in sorted(out, key=lambda x: -x["score_total"]):
            w.writerow({k: r.get(k, "") for k in cols})
    print(f"round-3 generated: {len(out)} (W={made_w}, U={made_u}) -> {OUT_CSV}")
    return out

if __name__ == "__main__":
    generate()
