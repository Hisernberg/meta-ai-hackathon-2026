# -*- coding: utf-8 -*-
"""Round-6 WORLDWIDE mega-composer.
Lattice (per lane): winner-DNA patterns x global contexts x 60 mechanisms x twists
  lane W: 48 patterns x ~430 contexts x 60 mechs x 22 twists  ~= 27 billion
  lane U: ~80 lenses  x ~430 contexts x 60 mechs x 22 twists  ~= 45 billion
Pipeline (deterministic, seed 61104):
  1) enumerate 10,000,000 unique lattice points (5M/lane, LCG over combo space)
  2) expand+score 2,000,000 candidates (1M/lane) - feature scoring, hash-stable
  3) materialize full text for top ~60k, title-Jaccard dedupe vs 30,568 prior pool
  4) diversity caps (mech/pattern/region) -> TOP 5,000 -> CSV + JSONL
"""
import csv, gzip, heapq, json, os, random, re, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "/home/z/my-project/scripts/r3")
sys.path.insert(0, "/home/z/my-project/scripts/r4")
from winner_dna import WINNER_DNA, W_CONTEXTS
from profile_domains import PROFILE_DOMAINS
from corpora_r4 import DNA_R4, W_CONTEXTS_R4, PROFILE_R4, CTX_BOOST
from dna_r6 import DNA_R6, GLOBAL_CONTEXTS, PROFILE_R6, GLOBAL_TWISTS, REGION
from mechs_r6 import ALL_MECHS, FAM_WEIGHT, TIER_BOOST, MECH_TAG

SEED = 61104
ENUM_PER_LANE = 5_000_000      # step 1
EXPAND_PER_LANE = 1_000_000    # step 2
TOP_MATERIALIZE = 60_000       # step 3
FINAL_N = 5_000
OUT_DIR = "/home/z/my-project/hackathon-repo/ideation/round6"
DL = "/home/z/my-project/download"
GRAND_CSV = f"{DL}/hackathon_ideas_grand_corpus_round5_30568.csv"

CAP_NAME = {"W": "Muse Wonder", "S": "Muse Spark", "I": "Muse Image",
            "V": "Muse Voice", "SAM": "SAM 3.1", "SO": "Muse Spark Open (open weights)",
            "G": "Muse Glimmer"}
CAP_SHORT = {"W": "W", "S": "S", "I": "I", "V": "V", "SAM": "SAM", "SO": "SO", "G": "G"}

TWISTS = ["with every step logged for audit", "fully voice-first for hands-busy users",
          "works on a 40-dollar Android", "Bengali-first, English next",
          "with a consent-first camera policy", "runs offline on self-hosted open weights",
          "with replayable evidence for every verdict", "priced at less than a cup of tea per day",
          "with graceful fallback when the network dies",
          "output exportable to the tools people already use"] + GLOBAL_TWISTS

ALL_W_PATTERNS = WINNER_DNA + DNA_R4 + DNA_R6
ALL_U_DOMAINS = PROFILE_DOMAINS + PROFILE_R4 + PROFILE_R6
ALL_CTX = list(W_CONTEXTS) + list(W_CONTEXTS_R4) + list(GLOBAL_CONTEXTS)
CTX_SET = {}
for c in ALL_CTX:                      # dedupe contexts by short name
    CTX_SET[c[1]] = c
ALL_CTX = list(CTX_SET.values())

def ctx_boost(short):
    b = CTX_BOOST.get(short, 0)
    r = REGION.get(short)
    return b + (1.5 if r in ("SA", "AF", "SEA", "LATAM", "ME", "GX") else 1.0 if r else 0.8)

_tok = re.compile(r"[a-z0-9]+")
def toks(s): return frozenset(_tok.findall(s.lower()))

# ---------------------------------------------------------------- prior ----
def load_prior():
    titles = []
    with open(GRAND_CSV, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            titles.append(toks(r.get("title", "")))
    # inverted index on rare tokens for fast jaccard pruning
    df = {}
    for i, t in enumerate(titles):
        for w in t:
            df[w] = df.get(w, 0) + 1
    inv = {}
    for i, t in enumerate(titles):
        for w in t:
            if df[w] <= 300:            # rare tokens only
                inv.setdefault(w, []).append(i)
    return titles, inv

def prior_sim(tt, inv, titles, cap=60):
    cand = {}
    for w in tt:
        for i in inv.get(w, ())[:20]:
            cand[i] = cand.get(i, 0) + 1
    if not cand: return 0.0
    best = 0.0
    for i in sorted(cand, key=cand.get, reverse=True)[:cap]:
        et = titles[i]
        if et:
            inter = len(tt & et)
            uni = len(tt | et)
            if uni and inter / uni > best: best = inter / uni
    return best

# ------------------------------------------------------------- compose -----
def compose(lane, base, ctx, mech, twist_idx, caps, combo):
    rng = random.Random((combo * 2654435761) & 0xFFFFFFFF)
    ctx_full, ctx_short, artifact = ctx
    tag = MECH_TAG[mech["id"]]
    if lane == "W":
        pat = PAT_BY_ID[base]
        use_mech_t = rng.random() < 0.5
        src = rng.choice(mech["templates"]) if use_mech_t else rng.choice(pat["angles"])
        title = re.sub(r"\s+", " ", src.format(c=ctx_short)).strip(" ,.")
        title = title[0].upper() + title[1:] + f" \u2014 {tag}"
        pitch = (f"{mech['name']}: {mech['desc']}. Winner-DNA insight - {pat.get('note','')}. "
                 f"Applied to {ctx_full}, where {artifact} become decisions, not paperwork. "
                 f"Stack: {' + '.join(CAP_NAME[c] for c in caps[:3])}. Novel architecture, not another chatbot. {TWISTS[twist_idx]}.")
    else:
        dom, lens_name, lens_desc = U_LENS_BY_KEY[base]
        s = lens_name.replace("-", " ")
        t = rng.choice(U_TITLE_T).format(s=s, c=ctx_short)
        title = re.sub(r"\s+", " ", t)
        title = title[0].upper() + title[1:] + f" \u2014 {tag}"
        lead = lens_desc[0].upper() + lens_desc[1:]
        pitch = (f"{lead}. Built on {mech['name']} - {mech['desc']}. For {ctx_full}. "
                 f"Stack: {' + '.join(CAP_NAME[c] for c in caps[:3])}. Novel architecture, not another chatbot. {TWISTS[twist_idx]}.")
    return title[:120], pitch[:460]

U_TITLE_T = ["{s} for {c}", "the {s} bench for {c}", "{c} run through a {s}",
             "{s}, wired into {c}", "the {s} engine behind {c}"]

def pick_caps(rng, mech, base, lane):
    if lane == "W":
        pool = mech["caps"] if rng.random() < 0.6 else PAT_BY_ID[base]["caps"]
    else:
        pool = mech["caps"] if rng.random() < 0.6 else U_LENS_BY_KEY[base][0]["caps"]
    caps = list(rng.choice(pool))
    if rng.random() < 0.30:
        extra = rng.choice([c for c in ["W", "S", "I", "V", "SAM", "SO", "G"] if c not in caps])
        caps = caps + [extra]
    return caps

def score(combo, lane, base, mech, caps, ctx_short):
    rng = random.Random((combo * 40503 + 7919) & 0xFFFFFFFF)
    tc, ta = TIER_BOOST[mech["tier"]]
    fam = FAM_WEIGHT[mech["fam"]]
    if lane == "W":
        p = PAT_BY_ID[base]
        feas0, wow0, amb0, impact0 = p.get("feas", 7), p.get("wow", 8), p.get("amb", 8), p.get("impact", 8)
    else:
        d = U_LENS_BY_KEY[base][0]
        feas0, wow0, amb0, impact0 = d.get("feas", 6), d.get("wow", 8.5), d.get("amb", 9), d.get("impact", 7.5)
    creativity = min(10, 4.2 + tc * fam + rng.uniform(-0.5, 0.5))
    ambition = min(10, amb0 * 0.72 + 0.9 * (len(caps) >= 3) + ta * fam + rng.uniform(-0.4, 0.4))
    works = max(1, min(10, feas0 + (0.5 if len(caps) <= 3 else -0.3) + rng.uniform(-0.7, 0.7)))
    work_real = min(10, impact0 * 0.9 + ctx_boost(ctx_short) + 1.2 * (mech["fam"] in ("GEO", "MoRBE")) + rng.uniform(-0.5, 0.5))
    meta = min(10, 3.4 + 1.25 * len(caps) + (1.2 if any(c in ("SAM", "SO", "G", "W") for c in caps) else 0) + rng.uniform(-0.4, 0.4))
    fit = min(10, 7.6 + rng.uniform(-0.7, 0.7))
    wow = min(10, wow0 + rng.uniform(-0.6, 0.6))
    total = (creativity * 0.14 + ambition * 0.11 + works * 0.16 + work_real * 0.20 +
             meta * 0.12 + fit * 0.08 + wow * 0.19) * 10
    return dict(score_total=round(total, 1), creativity=round(creativity, 1),
                ambition=round(ambition, 1), works=round(works, 1),
                work_real=round(work_real, 1), meta=round(meta, 1), fit=round(fit, 1),
                wow=round(wow, 1))

# ---------------------------------------------------------------- main -----
PAT_BY_ID = {p["id"]: p for p in ALL_W_PATTERNS}
U_LENS_BY_KEY = {}
for d in ALL_U_DOMAINS:
    for ln, ld in d["lenses"]:
        U_LENS_BY_KEY[f"{d['id']}-{ln}"] = (d, ln, ld)
W_BASES = sorted(PAT_BY_ID)
U_BASES = sorted(U_LENS_BY_KEY)
N_CTX, N_MECH, N_TW = len(ALL_CTX), len(ALL_MECHS), len(TWISTS)

print(f"lane W bases={len(W_BASES)} lane U bases={len(U_BASES)} ctx={N_CTX} mechs={N_MECH} twists={N_TW}")

def decode(combo, lane, n_base):
    t = combo % N_TW; c = combo // N_TW
    m = c % N_MECH; c = c // N_MECH
    b = c % n_base
    ctx = c // n_base          # exact mixed-radix recovery, < N_CTX
    return b, m, t, ctx

def lane_combos(lane, count):
    """LCG walk over (base, mech, ctx, twist) space -> unique combos."""
    n_base = len(W_BASES) if lane == "W" else len(U_BASES)
    L = n_base * N_MECH * N_CTX * N_TW
    a, cstep = 1103515245, 12345
    # ensure stride coprime with L: bump a until gcd(a,L)==1
    from math import gcd
    while gcd(a, L) != 1:
        a += 2
    combos = (np.arange(count, dtype=np.int64) * a + cstep) % L
    assert len(np.unique(combos)) == count, f"collision in lane {lane}"
    return combos, n_base, L

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    prior_titles, prior_inv = load_prior()
    print(f"prior pool titles: {len(prior_titles)}")

    heap = []          # (score, lane, combo)
    pool_rows = []     # audit rows for the 2M
    stats = {}
    for lane in ("W", "U"):
        combos, n_base, L = lane_combos(lane, ENUM_PER_LANE)
        stats[f"lattice_{lane}"] = L
        print(f"[{lane}] lattice={L:,} enumerating {ENUM_PER_LANE:,} unique points")
        # expand EXPAND_PER_LANE scored candidates: stride-sample the enum space
        step = max(1, ENUM_PER_LANE // EXPAND_PER_LANE)
        sub = combos[::step][:EXPAND_PER_LANE]
        bases = np.array(W_BASES if lane == "W" else U_BASES)
        mechs = ALL_MECHS
        for i in range(len(sub)):
            combo = int(sub[i])
            b_i, m_i, t_i, c_idx = decode(combo, lane, n_base)
            base, mech = str(bases[b_i]), mechs[m_i]
            rng = random.Random((combo * 2246822519) & 0xFFFFFFFF)
            caps = pick_caps(rng, mech, base, lane)
            ctx_short = ALL_CTX[c_idx][1]
            sc = score(combo, lane, base, mech, caps, ctx_short)
            s = sc["score_total"]
            pool_rows.append((lane, combo, s, sc["work_real"], sc["wow"]))
            item = (s, lane, combo)
            if len(heap) < TOP_MATERIALIZE:
                heapq.heappush(heap, item)
            elif s > heap[0][0]:
                heapq.heapreplace(heap, item)
        print(f"[{lane}] expanded {len(sub):,} scored candidates; heap={len(heap)}")

    with gzip.open(f"{DL}/hackathon_ideas_round6_pool2M.csv.gz", "wt", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["lane", "combo", "score_total", "work_real", "wow"])
        w.writerows(pool_rows)
    print(f"pool audit written: {len(pool_rows):,} rows")

    # ---- materialize top ~60k, dedupe vs prior, diversity caps ----
    top = sorted(heap, reverse=True)
    mech_cap, pat_cap, region_cap = 260, 220, 700
    mech_n, pat_n, reg_n = {}, {}, {}
    finalists = []
    for s, lane, combo in top:
        if len(finalists) >= FINAL_N: break
        n_base = len(W_BASES) if lane == "W" else len(U_BASES)
        b_i, m_i, t_i, c_idx = decode(combo, lane, n_base)
        base = str(np.array(W_BASES if lane == "W" else U_BASES)[b_i])
        mech = ALL_MECHS[m_i]
        ctx = ALL_CTX[c_idx]
        if mech_n.get(mech["id"], 0) >= mech_cap: continue
        if pat_n.get(base, 0) >= pat_cap: continue
        reg = REGION.get(ctx[1], "R3R4")
        if reg_n.get(reg, 0) >= region_cap: continue
        rng = random.Random((combo * 2246822519) & 0xFFFFFFFF)
        caps = pick_caps(rng, mech, base, lane)
        title, pitch = compose(lane, base, ctx, mech, t_i, caps, combo)
        tt = toks(title)
        if prior_sim(tt, prior_inv, prior_titles) > 0.72: continue
        if any(len(tt & ft) / max(1, len(tt | ft)) > 0.82 for _, _, _, ft, _ in finalists[-800:]): continue
        sc = score(combo, lane, base, mech, caps, ctx[1])
        mech_n[mech["id"]] = mech_n.get(mech["id"], 0) + 1
        pat_n[base] = pat_n.get(base, 0) + 1
        reg_n[reg] = reg_n.get(reg, 0) + 1
        finalists.append((lane, base, combo, tt, dict(
            lane=lane, base=base, mech=mech["id"], mech_fam=mech["fam"], mech_tier=mech["tier"],
            title=title, pitch=pitch, domain=ctx[0], domain_short=ctx[1],
            region=REGION.get(ctx[1], "r3r4"), artifact=ctx[2],
            models="+".join(CAP_SHORT[c] for c in caps), twist=TWISTS[t_i], **sc)))

    cols = ["lane","base","mech","mech_fam","mech_tier","title","pitch","domain","domain_short",
            "region","artifact","models","twist","score_total","creativity","ambition","works",
            "work_real","meta","fit","wow"]
    with open(f"{DL}/hackathon_ideas_round6_top5000.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for _, _, _, _, r in sorted(finalists, key=lambda x: -x[4]["score_total"]):
            w.writerow({k: r.get(k, "") for k in cols})
    with open(f"{OUT_DIR}/round6_top5000.jsonl", "w", encoding="utf-8") as f:
        for _, _, _, _, r in sorted(finalists, key=lambda x: -x[4]["score_total"]):
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    stats.update(finalists=len(finalists), enumerated=2 * ENUM_PER_LANE,
                 expanded=2 * EXPAND_PER_LANE, prior_pool=len(prior_titles),
                 mech_spread=len(mech_n), pattern_spread=len(pat_n),
                 region_spread=len(reg_n))
    json.dump(stats, open(f"{OUT_DIR}/LATTICE_STATS.json", "w"), indent=1)
    print("STATS:", json.dumps(stats))
    fam = {}
    for _, _, _, _, r in finalists: fam[r["mech_fam"]] = fam.get(r["mech_fam"], 0) + 1
    print("family spread:", fam)
    print(f"ROUND-6 TOP {len(finalists)} -> {OUT_DIR}/round6_top5000.jsonl")
