# -*- coding: utf-8 -*-
"""Round-4 novelty verification (HF + GitHub) and battle arena.
Usage:
  python3 novelty_arena_r4.py novelty   # checks shortlist150 against HF + GitHub
  python3 novelty_arena_r4.py arena     # runs bracket on novelty survivors -> final8
Checkpointed; safe to re-run (skips already-checked ideas).
"""
import json, os, sys, time, random, urllib.parse, urllib.request

sys.path.insert(0, "/home/z/my-project/scripts/r4")
OUT_DIR = "/home/z/my-project/ideation/round4"
SHORTLIST = f"{OUT_DIR}/shortlist150.json"
NOVELTY = f"{OUT_DIR}/novelty.json"
ARENA = f"{OUT_DIR}/arena_bracket.json"
FINAL8 = f"{OUT_DIR}/final8.json"

STOP = set("""the for and with that this via edition take plays a an of to on by at in as is
are be it its from into your you our we they their for not new""".split())

def toks(s):
    import re
    return set(re.findall(r"[a-z0-9]+", s.lower()))

def load_env():
    p = "/home/z/my-project/.secrets/env"
    if os.path.exists(p):
        for line in open(p):
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

def http_json(url, headers, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.loads(r.read().decode("utf-8", "ignore"))
        except Exception as e:
            code = getattr(e, "code", None)
            if code in (403, 429) and i < tries - 1:
                time.sleep(8 + 6 * i); continue
            if i < tries - 1: time.sleep(2); continue
            return None
    return None

def query_tokens(title, extra=""):
    ws = [w for w in toks(title + " " + extra) if w not in STOP and len(w) > 2]
    ws = sorted(ws, key=lambda w: -len(w))
    return ws[:4]

def jacc(a, b):
    a, b = toks(a), toks(b)
    return len(a & b) / len(a | b) if (a and b) else 0.0

def novelty():
    load_env()
    gh_tok = os.environ.get("GH_TOKEN", "")
    hf_tok = os.environ.get("HF_TOKEN", "")
    ideas = json.load(open(SHORTLIST))
    done = {}
    if os.path.exists(NOVELTY):
        done = json.load(open(NOVELTY))
    gh_headers = {"Accept": "application/vnd.github+json", "User-Agent": "r4-novelty-check"}
    if gh_tok: gh_headers["Authorization"] = f"Bearer {gh_tok}"
    hf_headers = {"User-Agent": "r4-novelty-check"}
    if hf_tok: hf_headers["Authorization"] = f"Bearer {hf_tok}"

    for n, idea in enumerate(ideas):
        key = idea["title"]
        if key in done:
            continue
        qt = query_tokens(idea["title"], idea.get("pattern", ""))
        qg = urllib.parse.quote(" ".join(qt[:4]))
        qh = urllib.parse.quote(" ".join(qt[:3]))
        best, near = 0.0, 0
        hits = []
        # GitHub repositories
        gh = http_json(f"https://api.github.com/search/repositories?q={qg}&per_page=5&sort=best-match", gh_headers)
        time.sleep(2.2)
        if gh is None:
            gh_failed = True
        else:
            gh_failed = False
            for it in (gh.get("items") or [])[:5]:
                j = jacc(idea["title"] + " " + idea.get("arch", ""), (it.get("full_name") or "") + " " + (it.get("description") or ""))
                best = max(best, j)
                if j >= 0.40: near += 1
                if j >= 0.40: hits.append(f"GH:{it.get('full_name')}({j:.2f})")
        # HF models + spaces
        for kind in ("models", "spaces"):
            hf = http_json(f"https://huggingface.co/api/{kind}?search={qh}&limit=5", hf_headers)
            time.sleep(0.35)
            if isinstance(hf, list):
                for it in hf[:5]:
                    j = jacc(idea["title"] + " " + idea.get("arch", ""), (it.get("id") or "") + " " + (it.get("description") or "") if kind == "spaces" else (it.get("id") or ""))
                    best = max(best, j)
                    if j >= 0.40:
                        near += 1
                        hits.append(f"HF:{it.get('id')}({j:.2f})")
        if gh_failed and best == 0.0:
            verdict, penalty = "check_failed", -2.0
        elif best >= 0.62 or near >= 3:
            verdict, penalty = "collision", -100.0
        elif best >= 0.45 or near >= 2:
            verdict, penalty = "near-collision", -4.0
        elif near == 1:
            verdict, penalty = "thin-ice", -1.5
        else:
            verdict, penalty = "original", +2.0
        done[key] = dict(verdict=verdict, penalty=penalty, best=round(best, 3),
                         near=near, hits=hits[:6])
        if n % 10 == 0:
            print(f"[{n+1}/{len(ideas)}] {key[:52]} -> {verdict} ({best:.2f})")
            json.dump(done, open(NOVELTY, "w"), indent=1)
    json.dump(done, open(NOVELTY, "w"), indent=1)
    vs = {}
    for v in done.values(): vs[v["verdict"]] = vs.get(v["verdict"], 0) + 1
    print("novelty verdicts:", vs)

def battle(a, b, rng):
    """pairwise arena battle under the NEW rubric; returns winner dict"""
    ka = (a["final"], a["demo"], a["impact"], a["tech"], -a["days"],
          a["nov"]["penalty"], rng.uniform(0, 0.4))
    kb = (b["final"], b["demo"], b["impact"], b["tech"], -b["days"],
          b["nov"]["penalty"], rng.uniform(0, 0.4))
    return a if ka > kb else b

def arena():
    ideas = json.load(open(SHORTLIST))
    nov = json.load(open(NOVELTY))
    pool = []
    for r in ideas:
        v = nov.get(r["title"])
        if not v or v["verdict"] == "collision": continue
        x = dict(r); x["nov"] = v
        x["final"] = round(r["total"] + v["penalty"], 2)
        pool.append(x)
    pool.sort(key=lambda x: -x["final"])
    field = pool[:64]
    rng = random.Random(77)
    rounds = ["R64", "R32", "R16", "QF", "SF", "FINAL"]
    hist = []
    cur = field
    snap = {}
    for rd in rounds:
        # 1v-N seeding so top seeds meet late
        seeded = []
        n = len(cur)
        for i in range(n // 2):
            seeded += [cur[i], cur[n - 1 - i]]
        if n % 2: seeded.append(cur[n // 2])
        nxt = []
        for i in range(0, len(seeded) - 1, 2):
            w = battle(seeded[i], seeded[i + 1], rng)
            nxt.append(w)
            hist.append(dict(round=rd,
                             a=f"{seeded[i]['title'][:60]}[{seeded[i]['lane']}|{seeded[i]['final']}]",
                             b=f"{seeded[i+1]['title'][:60]}[{seeded[i+1]['lane']}|{seeded[i+1]['final']}]",
                             winner=f"{w['title'][:60]}[{w['lane']}]"))
        if len(seeded) % 2 == 1: nxt.append(seeded[-1])
        cur = nxt
        if len(cur) == 8: snap["8"] = cur[:]
        if len(cur) == 4: snap["4"] = cur[:]
        if len(cur) == 2: snap["2"] = cur[:]
        print(f"{rd}: {len(cur)} left; leader: {cur[0]['title'][:60]} [{cur[0]['lane']}] {cur[0]['final']}")
    f8 = snap.get("8", cur[:1])
    json.dump(dict(champion=cur[0], final2=snap.get("2", []), semifinalists=snap.get("4", []),
                   finalists8=f8, matches=hist),
              open(ARENA, "w"), indent=1)
    json.dump(f8, open(FINAL8, "w"), indent=1)
    lanes = {}
    for c in f8: lanes[c["lane"]] = lanes.get(c["lane"], 0) + 1
    print(f"CHAMPION: {cur[0]['title']} [{cur[0]['lane']}] final={cur[0]['final']}")
    print("final-8 lane mix:", lanes)
    for i, c in enumerate(f8, 1):
        print(f"  {i}. ({c['final']:5.1f}) {c['title'][:70]} | arch={c['arch'][:34]} | {c['nov']['verdict']}")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "novelty"
    if mode == "novelty": novelty()
    elif mode == "arena": arena()
    else: print("usage: novelty|arena")
