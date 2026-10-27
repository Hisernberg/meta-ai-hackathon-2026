# -*- coding: utf-8 -*-
"""Round-4 mega-composer: TWO 10k pools.
  Lane W (winner-thought):  WINNER_DNA patterns x contexts x ARCH_MECHS
  Lane U (builder-profile): PROFILE_DOMAINS lenses x contexts x ARCH_MECHS
Every idea EMBODIES a novel architecture mechanism (user mandate).
Dedupe vs 10,568 grand corpus + internal. Same 7 scoring axes as R1-R3
plus mech-tier novelty boost for comparability + novelty accounting.
"""
import csv, json, random, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "/home/z/my-project/scripts/r3")
from winner_dna import WINNER_DNA, W_CONTEXTS
from profile_domains import PROFILE_DOMAINS
from arch_bank import MECHS, FAM_WEIGHT, TIER_BOOST

CAP_NAME = {"W": "muse-wonder-1.0", "S": "muse-spark-1.3", "I": "muse-image-1.0",
            "V": "muse-voice-transcribe-1.0", "SAM": "sam-3.1", "SO": "muse-spark-open",
            "G": "muse-glimmer"}
MECH_TAG = {m["id"]: t for m, t in zip(MECHS, [
    "world rollouts", "what-if bench", "track-record routing", "evidence debate",
    "state ledger", "counterfactual twin", "ensemble bands", "drill generator",
    "snapshot forensics", "expert bench", "gate chain", "paired negotiators",
    "standing red team", "newbie proxy", "shift roster", "cross-examination",
    "apprentice loop", "judge-worker split", "hyperbolic ladder", "mask metrics",
    "curvature clusters", "geodesic skills", "shape trust", "photo packing",
    "scale ladders", "drift monitor", "distance-weighted votes", "claim receipts",
    "budget meter", "action quorum", "deterministic replay", "verifier loop",
    "baton handoffs", "scope fence", "shadow apprenticeship", "three-layer gauntlet",
    "hyperbolic dispatch", "rendered ideal", "failure curriculum", "geometry filing",
    "scored foresight", "synthetic adversity", "rollout quorum", "laptop distill"])}
GRAND_CSV = "/home/z/my-project/download/hackathon_ideas_grand_corpus_10568.csv"
OUT_CSV_W = "/home/z/my-project/download/hackathon_ideas_round4_laneW.csv"
OUT_CSV_U = "/home/z/my-project/download/hackathon_ideas_round4_laneU.csv"
OUT_JSONL = "/home/z/my-project/hackathon-repo/ideation/round4/round4_all.jsonl"

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

TWISTS = ["with every step logged for audit", "fully voice-first for hands-busy users",
          "works on a 40-dollar Android", "Bengali-first, English next",
          "with a consent-first camera policy", "runs offline on self-hosted open weights",
          "with replayable evidence for every verdict", "priced at less than a cup of tea per day",
          "with graceful fallback when the network dies", "output exportable to the tools people already use"]

def cap_txt(cap_ids):
    m = {"W": "Muse Wonder", "S": "Muse Spark", "I": "Muse Image", "V": "Muse Voice",
         "SAM": "SAM 3.1", "SO": "Muse Spark Open (open weights)", "G": "Muse Glimmer"}
    return " + ".join(m[c] for c in cap_ids[:3])

def score(rng, feas, wow, amb, n_caps, rare, mech):
    tc, ta = TIER_BOOST[mech["tier"]]
    fam = FAM_WEIGHT[mech["fam"]]
    creativity = min(10, 4.4 + tc * fam + rng.uniform(-0.5, 0.5))
    ambition = min(10, amb * 0.75 + 0.9 * (n_caps >= 3) + ta * fam + rng.uniform(-0.4, 0.4))
    works = max(1, min(10, feas + (0.5 if n_caps <= 3 else -0.3) + rng.uniform(-0.7, 0.7)))
    work_real = min(10, 5.6 + 1.5 * (mech["fam"] in ("GEO", "MoRBE")) + rng.uniform(-0.5, 0.5))
    meta = min(10, 3.4 + 1.25 * n_caps + (1.2 if rare else 0) + rng.uniform(-0.4, 0.4))
    fit = min(10, 7.6 + rng.uniform(-0.7, 0.7))
    days_f = max(3, min(7, int(round(9 - works + mech["build"]))))
    feasv = max(1, min(10, 11 - days_f + rng.uniform(-0.4, 0.4)))
    total = round((creativity * 0.15 + ambition * 0.12 + works * 0.17 + work_real * 0.18 +
                   meta * 0.12 + fit * 0.09 + wow * 0.17) * 10, 1)
    return dict(score_total=total, creativity=round(creativity,1), ambition=round(ambition,1),
                works=round(works,1), work_real=round(work_real,1), meta=round(meta,1),
                fit=round(fit,1), wow=wow, feas=round(feasv,1), days=days_f)

def compose(rng, base_key, ctx, mech, cap_ids, lane, lens_desc=None, pat_note=None, conf_hook=None):
    ctx_full, ctx_short, artifact = ctx
    tag = MECH_TAG[mech["id"]]
    if rng.random() < 0.55:
        title = re.sub(r"\s+", " ", rng.choice(mech["templates"]).format(c=ctx_short)).strip(" ,.")
        title = title + f" \u2014 {tag}"
    elif lane == "W":
        import winner_dna as WD
        pat = next(p for p in WD.WINNER_DNA if p["id"] == base_key)
        title = re.sub(r"\s+", " ", rng.choice(pat["angles"]).format(c=ctx_short)).strip(" ,.")
        title = title + f" \u2014 {tag}"
    else:
        import engine_r3
        lens_name = base_key.split("-", 1)[1].replace("_", "-")
        s = engine_r3.slug_title(lens_name)
        t = rng.choice(engine_r3.U_TITLE_T).format(s=s, c=ctx_short)
        title = re.sub(r"\s+", " ", t) + f" \u2014 {tag}"
    title = title[0].upper() + title[1:]
    twist = TWISTS[(rng.randrange(len(TWISTS)) + rng.randrange(97)) % len(TWISTS)]
    if lane == "W":
        pitch = (f"{mech['name']}: {mech['desc']}. Winner-DNA insight — {pat_note}. "
                 f"Applied to {ctx_full}, where {artifact} become decisions, not paperwork. "
                 f"Stack: {cap_txt(cap_ids)}. Novel architecture, not another chatbot. {twist}.")
    else:
        lead = lens_desc[0].upper() + lens_desc[1:]
        pitch = (f"{lead}. Built on {mech['name']} — {mech['desc']}. For {ctx_full}")
        pitch += (f" — grounded in {conf_hook}" if conf_hook else "") + \
                 f". Stack: {cap_txt(cap_ids)}. Novel architecture, not another chatbot. {twist}."
    return dict(lane=lane, lens=f"{lane}-{base_key}-{mech['id']}",
                base=base_key,
                mech=mech["id"], mech_fam=mech["fam"], mech_tier=mech["tier"],
                title=title[:120], pitch=pitch[:460],
                domain=ctx_full, models="+".join(CAP_NAME[c] for c in cap_ids),
                twist=twist)

def load_lane_jsonl(lane):
    out = []
    if os.path.exists(OUT_JSONL):
        for line in open(OUT_JSONL, encoding="utf-8"):
            try:
                r = json.loads(line)
                if r.get("lane") == lane: out.append(r)
            except Exception: pass
    return out

def generate(lane, target, seed, existing, seen_titles, out_csv):
    rng = random.Random(seed)
    out = load_lane_jsonl(lane)
    # exact fingerprint rebuild: (base_key, ctx_short, mech_id)
    seen_fp = set()
    for i in out:
        b = i.get("base")
        if not b:  # derive from lens: lane-<base>-<mech_id>
            suffix = "-" + i["mech"]
            b = i["lens"][len(lane) + 1:-len(suffix)] if i["lens"].endswith(suffix) else i["lens"]
            i["base"] = b
        seen_fp.add((b, i["domain"], i["mech"]))
    fam_count, base_count = {}, {}
    for i in out:
        fam_count[i["mech"]] = fam_count.get(i["mech"], 0) + 1
        bk = "-".join(i["lens"].split("-")[1:-1])
        base_count[bk] = base_count.get(bk, 0) + 1
    for i in out: seen_titles.append(toks(i["title"]))
    guard_max = int(open(f"/tmp/r4_guard_{lane}").read()) if os.path.exists(f"/tmp/r4_guard_{lane}") else 0
    guard = guard_max
    CAPS_ALL = ["S","V","I","SAM","G","SO","W"]
    flushed = len(out)
    print(f"[{lane}] resuming with {len(out)} done, guard={guard}", flush=True)
    while len(out) < target and guard < target * 40:
        guard += 1
        mech = MECHS[guard % len(MECHS)] if rng.random() < 0.5 else rng.choice(MECHS)
        if lane == "W":
            pat = WINNER_DNA[guard % len(WINNER_DNA)] if rng.random() < 0.5 else rng.choice(WINNER_DNA)
            ctx = W_CONTEXTS[guard % len(W_CONTEXTS)] if rng.random() < 0.5 else rng.choice(W_CONTEXTS)
            base_key, note, base_caps = pat["id"], pat.get("note",""), pat["caps"]
            lens_desc = None; conf_hook = None
        else:
            d = PROFILE_DOMAINS[guard % len(PROFILE_DOMAINS)] if rng.random() < 0.5 else rng.choice(PROFILE_DOMAINS)
            lens_name, lens_desc = d["lenses"][guard % len(d["lenses"])] if rng.random() < 0.5 else rng.choice(d["lenses"])
            ctx = d["contexts"][guard % len(d["contexts"])] if rng.random() < 0.5 else rng.choice(d["contexts"])
            base_key, note, base_caps = f"{d['id']}-{lens_name}", None, d["caps"]
            conf_hook = rng.choice(d["conf_hooks"])
        fp = (base_key, ctx[1], mech["id"])
        if fp in seen_fp: continue
        if fam_count.get(mech["id"], 0) > 340: continue
        if base_count.get(base_key, 0) > 620: continue
        caps = list(rng.choice(mech["caps"] if rng.random() < 0.65 else base_caps))
        if rng.random() < 0.30:
            extra = rng.choice([c for c in CAPS_ALL if c not in caps])
            caps = caps + [extra]
        idea = compose(rng, base_key, ctx, mech, caps, lane, lens_desc, note, conf_hook)
        idea["round"] = 4
        tt = toks(idea["title"])
        dup = any(jaccard(tt, et) > 0.85 for et in seen_titles[-9000:])
        if not dup:
            dup = any(jaccard(tt, et) > 0.78 for et in existing)
        if dup: continue
        seen_fp.add(fp)
        fam_count[mech["id"]] = fam_count.get(mech["id"], 0) + 1
        base_count[base_key] = base_count.get(base_key, 0) + 1
        sc = score(rng, 7.0 if lane == "W" else 7.2, rng.uniform(7.2, 9.6),
                   rng.uniform(6.5, 9.4), len(caps),
                   any(c in {"SAM","SO","G","W"} for c in caps), mech)
        idea.update(sc)
        seen_titles.append(tt)
        out.append(idea)
        if len(out) - flushed >= 500:
            print(f"  lane {lane}: {len(out)} (guard={guard})", flush=True)
            with open(OUT_JSONL, "a", encoding="utf-8") as f:
                for r in out[flushed:]: f.write(json.dumps(r, ensure_ascii=False) + "\n")
            flushed = len(out)
            open(f"/tmp/r4_guard_{lane}", "w").write(str(guard))
        if len(out) >= target: break
    cols = ["round","lane","lens","mech","mech_fam","mech_tier","title","pitch","domain",
            "models","twist","score_total","creativity","ambition","works","work_real",
            "meta","fit","wow","feas","days"]
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in sorted(out, key=lambda x: -x["score_total"]):
            w.writerow({k: r.get(k, "") for k in cols})
    # flush remainder (items after last flush point)
    with open(OUT_JSONL, "a", encoding="utf-8") as f:
        for r in out[flushed:]:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    open(f"/tmp/r4_guard_{lane}", "w").write(str(guard))
    print(f"lane {lane}: {len(out)} unique -> {out_csv}", flush=True)
    return out

if __name__ == "__main__":
    existing = load_existing_titles()
    print(f"grand corpus titles loaded: {len(existing)}")
    seen = []
    w = generate("W", 10000, 421, existing, seen, OUT_CSV_W)
    u = generate("U", 10000, 422, existing, seen, OUT_CSV_U)
    fams = {}
    for i in w + u: fams[i["mech_fam"]] = fams.get(i["mech_fam"], 0) + 1
    print("family spread:", fams)
    print(f"ROUND-4 TOTAL: {len(w)+len(u)}  | grand pool -> {10568+len(w)+len(u)}")
