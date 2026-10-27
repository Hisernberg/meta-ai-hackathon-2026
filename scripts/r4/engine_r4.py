# -*- coding: utf-8 -*-
"""Round-4 idea engine: 10k winner-DNA lane (W) + 10k user-profile lane (U).
- dedupes vs the 10,568-idea grand pool (inverted-index Jaccard, fast)
- anti-project filter (updated Participant Guide)
- scores with the NEW Stage-2 rubric (Impact .30 / Meta .25 / Tech .20 / Demo .25)
- emits: round4 CSV, merged grand corpus, lane-comparison stats, top-150 shortlist
"""
import csv, json, os, random, re, sys

sys.path.insert(0, "/home/z/my-project/scripts/r3")
sys.path.insert(0, "/home/z/my-project/scripts/r4")
from arch_r4 import (ARCHS, ARCH_BY_ID, HARNESS, HARNESS_BY_ID, CAP_NAME,
                     anti_check, ctx_banned, score_idea_r4)
from corpora_r4 import DNA_R4, PROFILE_R4, W_CONTEXTS_R4, CTX_BOOST
from winner_dna import WINNER_DNA, W_CONTEXTS
from profile_domains import PROFILE_DOMAINS

GRAND_CSV = "/home/z/my-project/download/hackathon_ideas_grand_corpus_10568.csv"
OUT_CSV   = "/home/z/my-project/download/hackathon_ideas_round4.csv"
GRAND_OUT = "/home/z/my-project/download/hackathon_ideas_grand_corpus_r4.csv"
OUT_DIR   = "/home/z/my-project/ideation/round4"

TARGET_W, TARGET_U = 10000, 10000
LENS_BLOCK = {"technique-breakdown", "highlight-loom"}   # sports-adjacent (banned family)

# ---------------------------------------------------------------- dedupe index
_tok = re.compile(r"[a-z0-9]+")
def toks(s): return frozenset(_tok.findall(s.lower()))

class Dedupe:
    def __init__(self):
        self.index = {}          # token -> set(ids)
        self.titles = {}         # id -> tokenset
        self.fp = set()          # fingerprints
    def add_existing(self, tid, title):
        t = toks(title)
        self.titles[tid] = t
        for w in t: self.index.setdefault(w, set()).add(tid)
    def near(self, title, thr):
        t = toks(title)
        cand = set()
        for w in t:
            bucket = self.index.get(w)
            if bucket:
                cand |= bucket if len(bucket) <= 80 else set(list(bucket)[:80])
        for cid in cand:
            et = self.titles[cid]
            j = len(t & et) / len(t | et)
            if j > thr: return True
        return False
    def add_new(self, tid, title, fp):
        t = toks(title)
        self.titles[tid] = t
        for w in t: self.index.setdefault(w, set()).add(tid)
        self.fp.add(fp)

# ---------------------------------------------------------------- text rendering
ARCH_VERB = {
 "A01": "war-games every move", "A02": "routes each call to the right expert",
 "A03": "thinks in masks and manifolds", "A04": "buys autonomy with evidence",
 "A05": "imagines before it acts", "A06": "demands receipts per step",
 "A07": "forges its own tools", "A08": "banks every solved task",
 "A09": "races cheap experts, exits early", "A10": "lets claims compete on a blackboard",
 "A11": "cross-examines its own verdicts", "A12": "probes its own conclusions",
 "A13": "remembers by object, not by text", "A14": "aligns runs to specs by transport",
 "A15": "shares work across a hypergraph", "A16": "fine-tunes itself on the spot",
 "A17": "sets its own curriculum", "A18": "runs a twin ahead of reality",
 "A19": "searches what machines did", "A20": "addresses the world region by region",
 "A21": "binds pixel, timestamp and utterance", "A22": "climbs the model cascade on doubt",
 "A23": "grows data where it fails", "A24": "writes the tests first",
 "A25": "auctions every task", "A26": "hires a swarm on a budget",
}
T_TPL = ["{a} · {arch}", "{c} via {arch}", "{arch} take on {c}",
         "{c}, {arch} edition", "{arch} for {c}", "{arch} plays {c}"]
def cap_txt(caps):
    names = []
    for c in caps:
        n = CAP_NAME[c]
        n = (n.replace("muse-", "Muse ").replace("spark-open-1026", "Spark Open (open weights)")
              .replace("wonder-1.0", "Wonder").replace("spark-1.3", "Spark")
              .replace("image-1.0", "Image").replace("voice-transcribe-1.0", "Voice")
              .replace("sam-3.1", "SAM 3.1").replace("glimmer", "Glimmer"))
        names.append(n)
    return " + ".join(names)

def title_case(s):
    return re.sub(r"\s+", " ", s).strip(" ,.-").capitalize()

def compose(rng, lane, lens, pat, ctx, arch, harness, caps):
    ctx_full, ctx_s, artifact = ctx
    arch_name = arch["name"].replace("-", " ")
    angle = rng.choice(pat["angles"]).format(c=ctx_s)
    tpl = T_TPL[rng.randrange(len(T_TPL))]
    title = tpl.format(a=title_case(angle), c=ctx_s, arch=arch_name)
    mech = arch["mech"][0].upper() + arch["mech"][1] + arch["mech"][2:]
    if lane == "W":
        pitch = (f"{pat['transform']}. For {ctx_full}: {mech}. "
                 f"Orchestration: {harness['name'].replace('-',' ')} — {harness['note']}. "
                 f"Stack: {cap_txt(caps)}.")
    else:
        pain = rng.choice(pat.get("pains", ["the work nobody has time to check"]))
        hook = rng.choice(pat.get("conf_hooks", ["applied ML"]))
        pitch = (f"{lens_desc_map[(lens)]}. Built for {ctx_full} — fixes: {pain}. {mech}. "
                 f"Orchestration: {harness['name'].replace('-',' ')} ({harness['note']}). "
                 f"Stack: {cap_txt(caps)}. Conference hook: {hook}.")
    return title, pitch[:500]

lens_desc_map = {}

def norm_pat(p, old=False):
    """give old r3 patterns the r4-required fields"""
    q = dict(p)
    if old:
        q["impact"] = min(9.0, 5.2 + 0.25 * p.get("wow", 7))
        q["users"] = ["operators", "team leads"]
        q["visual"] = p.get("wow", 0) >= 8
    q.setdefault("users", ["operators"])
    q.setdefault("visual", False)
    return q

def main():
    rng = random.Random(20261)
    os.makedirs(OUT_DIR, exist_ok=True)
    dd = Dedupe()
    n_exist = 0
    with open(GRAND_CSV, newline="", encoding="utf-8") as f:
        for i, r in enumerate(csv.DictReader(f)):
            dd.add_existing(("old", i), r.get("title", ""))
            n_exist += 1
    print(f"existing pool loaded: {n_exist}")

    # ---------------- prepare pattern/context pools (banned filtered) ----------------
    w_pats = [norm_pat(p, old=True) for p in WINNER_DNA] + list(DNA_R4)
    w_ctxs = [c for c in W_CONTEXTS if not ctx_banned(c[0])] + list(W_CONTEXTS_R4)
    u_domains = list(PROFILE_DOMAINS) + list(PROFILE_R4)
    u_pats = []   # flattened lenses as patterns
    for d in u_domains:
        for (ln, desc) in d["lenses"]:
            if ln in LENS_BLOCK: continue
            lens_desc_map[(d["id"], ln)] = desc
            u_pats.append(dict(id=f"{d['id']}-{ln}", name=ln, lens_key=(d["id"], ln),
                               domain_id=d["id"], angles=[f"{ln.replace('-',' ')} for {{c}}"],
                               caps=d["caps"],
                               feas=d["feas"], wow=d["wow"],
                               impact=d.get("impact", min(9.0, 5.0 + 0.28 * d["wow"])),
                               amb=d["amb"], users=[c[0] for c in d["contexts"][:2]],
                               visual=d.get("wow", 0) >= 8,
                               pains=d.get("pains", []), conf_hooks=d.get("conf_hooks", []),
                               theme=d.get("theme", "world")))
    u_ctxs = []
    for d in u_domains:
        u_ctxs += [c for c in d["contexts"] if not ctx_banned(c[0])]
    # dedupe contexts by short name
    seen = set(); w_ctxs = [c for c in w_ctxs if not (c[1] in seen or seen.add(c[1]))]
    seen = set(); u_ctxs = [c for c in u_ctxs if not (c[1] in seen or seen.add(c[1]))]
    print(f"pools: W pats={len(w_pats)} ctxs={len(w_ctxs)} | U pats={len(u_pats)} ctxs={len(u_ctxs)}")

    rows = []
    def gen_lane(lane, target, pats, ctxs):
        made, guard = 0, 0
        while made < target and guard < target * 40:
            guard += 1
            pat = pats[guard % len(pats)] if rng.random() < 0.5 else rng.choice(pats)
            ctx = ctxs[guard % len(ctxs)] if rng.random() < 0.5 else rng.choice(ctxs)
            arch = ARCHS[guard % len(ARCHS)] if rng.random() < 0.45 else rng.choice(ARCHS)
            harness = HARNESS[(guard * 7 + 3) % len(HARNESS)] if rng.random() < 0.5 else rng.choice(HARNESS)
            caps = list(rng.choice(pat["caps"]))
            if rng.random() < 0.30:
                extra = rng.choice([c for c in ["S","V","I","SAM","G","SO","W"] if c not in caps])
                caps.append(extra)
            if rng.random() < 0.25:  # swap harness for spread
                harness = rng.choice([h for h in HARNESS if h["id"] != harness["id"]])
            fp = (pat["id"], arch["id"], ctx[1], "+".join(caps))
            if fp in dd.fp: continue
            title, pitch = compose(rng, lane, pat.get("lens_key", ("", pat["name"])),
                                   pat, ctx, arch, harness, caps)
            lab = anti_check(title + " " + pitch)
            if lab: continue
            if ctx_banned(ctx[0]): continue
            boost = CTX_BOOST.get(ctx[1], 1 if lane == "W" else 1)
            sc = score_idea_r4(rng, pat, arch, harness, caps, boost, len(pat["users"]))
            row = dict(round=4, lane=lane, lens=pat["id"],
                       pattern=pat["name"], arch=arch["name"], arch_id=arch["id"],
                       harness=harness["name"], harness_id=harness["id"],
                       title=title, pitch=pitch, theme=pat.get("theme", "world"),
                       domain=ctx[0], models="+".join(CAP_NAME[c] for c in caps),
                       users="; ".join(pat["users"])[:120],
                       **{k: sc[k] for k in ("impact","meta_tooling","tech","demo","total","days")},
                       open_weight=sc["flags"]["open_weight"], agentic=sc["flags"]["agentic"],
                       creative=sc["flags"]["creative"], viral=sc["flags"]["viral"])
            if dd.near(title, 0.82): continue
            dd.add_new((lane, guard), title, fp)
            rows.append(row); made += 1
            if made % 2000 == 0: print(f"  lane {lane}: {made}")
        return made

    mw = gen_lane("W", TARGET_W, w_pats, w_ctxs)
    mu = gen_lane("U", TARGET_U, u_pats, u_ctxs)

    cols = ["round","lane","lens","pattern","arch","arch_id","harness","harness_id",
            "title","pitch","theme","domain","models","users",
            "impact","meta_tooling","tech","demo","total","days",
            "open_weight","agentic","creative","viral"]
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
        for r in sorted(rows, key=lambda x: -x["total"]): w.writerow(r)

    # ---------------- merged grand corpus ----------------
    old_cols = ["round","lens","title","pitch","theme","domain","models","wow","feas",
                "score_total","creativity","ambition","works","work_real","meta","fit","days","flag"]
    union = cols + ["wow","feas","score_total","creativity","ambition","works","work_real","meta","fit","flag"]
    with open(GRAND_CSV, newline="", encoding="utf-8") as f, open(GRAND_OUT, "w", newline="", encoding="utf-8") as g:
        rd = csv.DictReader(f); gw = csv.DictWriter(g, fieldnames=union); gw.writeheader()
        for r in rd: gw.writerow({k: r.get(k, "") for k in union})
        for r in sorted(rows, key=lambda x: -x["total"]): gw.writerow({k: r.get(k, "") for k in union})

    # ---------------- lane comparison stats ----------------
    def stats(lane):
        sub = [r for r in rows if r["lane"] == lane]
        if not sub: return {}
        ax = lambda k: sum(r[k] for r in sub) / len(sub)
        return dict(n=len(sub), avg_total=round(ax("total"),2), avg_impact=round(ax("impact"),2),
                    avg_meta=round(ax("meta_tooling"),2), avg_tech=round(ax("tech"),2),
                    avg_demo=round(ax("demo"),2),
                    pct_ow=round(100*sum(r["open_weight"] for r in sub)/len(sub),1),
                    pct_agentic=round(100*sum(r["agentic"] for r in sub)/len(sub),1),
                    pct_viral=round(100*sum(r["viral"] for r in sub)/len(sub),1))
    lane_stats = {"W": stats("W"), "U": stats("U")}
    with open(f"{OUT_DIR}/lane_stats.json", "w") as f: json.dump(lane_stats, f, indent=1)
    print("lane stats:", json.dumps(lane_stats, indent=1))

    # ---------------- shortlist: diversity-capped top 150 ----------------
    SL = 150
    cand = [r for r in rows if r["days"] <= 8 and r["demo"] >= 7.0]
    cand.sort(key=lambda r: -r["total"])
    picked, per_pat, per_arch, per_pair, per_lane = [], {}, {}, {}, {"W":0,"U":0}
    for r in cand:
        if per_lane[r["lane"]] >= SL // 2: continue
        if per_pat.get(r["pattern"], 0) >= 4: continue
        if per_arch.get(r["arch"], 0) >= 6: continue
        if per_pair.get((r["pattern"], r["arch"]), 0) >= 1: continue
        picked.append(r)
        per_pat[r["pattern"]] = per_pat.get(r["pattern"], 0) + 1
        per_arch[r["arch"]] = per_arch.get(r["arch"], 0) + 1
        per_pair[(r["pattern"], r["arch"])] = 1
        per_lane[r["lane"]] += 1
        if len(picked) >= SL: break
    with open(f"{OUT_DIR}/shortlist150.json", "w") as f:
        json.dump(picked, f, indent=1)
    print(f"round-4 generated: W={mw} U={mu} total={len(rows)}; shortlist={len(picked)}")
    print(f"files: {OUT_CSV}\n       {GRAND_OUT}\n       {OUT_DIR}/shortlist150.json")

if __name__ == "__main__":
    main()
