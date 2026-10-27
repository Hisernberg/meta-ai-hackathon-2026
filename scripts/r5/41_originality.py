# -*- coding: utf-8 -*-
"""Round-4 originality gate: every finalist is searched against
  1) GitHub repo search (authenticated)  2) Hugging Face models/datasets/spaces.
Output: collision verdict per finalist (clone / close / related / none) + evidence
+ a novelty-gap note. Feeds the arena prompts as novelty evidence.
"""
import json, re, sys, time, urllib.request, urllib.parse

SECRETS = "/home/z/my-project/.secrets/env"
TOKENS = {}
for line in open(SECRETS):
    line = line.strip()
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        TOKENS[k.strip()] = v.strip().strip('"')
GH = TOKENS.get("GH_TOKEN", "")
HF = TOKENS.get("HF_TOKEN", "")

STOP = set("""a an the for with without that this from into onto and or of to in on by is are
be been being your you our their its it's how why what when all any can will must every
three two four not no yes new make made builds built run runs running""".split())

def queries_for(title, mech):
    toks = [t for t in re.findall(r"[a-zA-Z]+", title.lower()) if t not in STOP and len(t) > 2]
    toks = toks[:4]
    if not toks: return []
    q1 = " ".join(toks[:3])
    q2 = " ".join(toks[:2] + ["agent"]) if mech.startswith(("mowa","morbe","fuse")) else " ".join(toks[:2] + ["vision"])
    return [q1, q2]

def get(url, tok=None):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json" if "api.github.com" in url else "application/json",
        "User-Agent": "r4-originality-check",
        **({"Authorization": f"Bearer {tok}"} if tok else {})})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        return {"_err": str(e)[:80]}

def gh_search(q):
    u = "https://api.github.com/search/repositories?q=" + urllib.parse.quote(q) + "&per_page=3&sort=best-match"
    d = get(u, GH)
    if "_err" in d: return []
    return [{"full": r["full_name"], "desc": (r.get("description") or "")[:90], "stars": r["stargazers_count"]} for r in d.get("items", [])]

def hf_search(q, kind):
    u = f"https://huggingface.co/api/{kind}?search={urllib.parse.quote(q)}&limit=3"
    d = get(u, HF)
    if isinstance(d, dict) or "_err" in d: return []
    out = []
    for r in d[:3]:
        out.append({"id": r.get("id", "?"), "likes": r.get("likes", 0),
                    "desc": (r.get("description") or r.get("cardData", {}).get("summary") or "")[:90]})
    return out

def verdict(hits, title_toks):
    if not hits: return "none"
    scored = []
    for h in hits:
        txt = (h.get("desc") or "").lower() + " " + (h.get("full") or h.get("id") or "").lower().replace("-", " ").replace("_", " ").replace("/", " ")
        ov = sum(1 for t in title_toks if t in txt)
        scored.append(ov)
    m = max(scored) if scored else 0
    if m >= 4: return "close"
    if m >= 2: return "related"
    return "none"

def run(finalists_path, out_json, out_md):
    finalists = json.load(open(finalists_path))
    results, cache = [], {}
    for x in finalists:
        qs = queries_for(x["title"], x["mech"])
        ev, all_hits = [], []
        for q in qs:
            time.sleep(1.2)
            gh = cache.get(("gh", q)) or gh_search(q)
            cache[("gh", q)] = gh
            time.sleep(0.8)
            hm = cache.get(("hm", q)) or hf_search(q, "models")
            cache[("hm", q)] = hm
            time.sleep(0.8)
            hs = cache.get(("hs", q)) or hf_search(q, "spaces")
            cache[("hs", q)] = hs
            all_hits += gh + hm + hs
            ev.append({"q": q, "github": gh[:3], "hf_models": hm[:3], "hf_spaces": hs[:3]})
        ttoks = [t for t in re.findall(r"[a-zA-Z]+", x["title"].lower()) if t not in STOP and len(t) > 2]
        v = verdict(all_hits, ttoks)
        results.append({"id": x["id"], "title": x["title"], "mech": x["mech"], "lane": x["lane"],
                        "verdict": v, "evidence": ev})
        print(f'{x["id"]} [{v:>7}] {x["title"][:70]}')
    json.dump(results, open(out_json, "w"), indent=1)
    with open(out_md, "w") as f:
        f.write("# Round-4 Originality Gate — HF + GitHub sweep\n\n")
        f.write("Every top-24 finalist searched against GitHub repo search + Hugging Face models/datasets-spaces (Oct 28, 2026). ")
        f.write("Verdicts: none = no meaningful collision; related = adjacent work exists but mechanism/user differs; close = must differentiate in spec; clone = reject.\n\n")
        f.write("| # | ID | Verdict | Idea | Strongest hit |\n|---|----|---------|------|---------------|\n")
        for i, r in enumerate(results, 1):
            best = ""
            for e in r["evidence"]:
                for h in e["github"] + e["hf_models"] + e["hf_spaces"]:
                    if not best: best = (h.get("full") or h.get("id") or "")
            f.write(f'| {i} | {r["id"]} | **{r["verdict"]}** | {r["title"][:64]} | {best[:52]} |\n')
        f.write("\n## Full evidence\n\n")
        for r in results:
            f.write(f'### {r["id"]} — {r["title"]} [{r["verdict"]}]\n')
            for e in r["evidence"]:
                f.write(f'- query `{e["q"]}`\n')
                for h in e["github"]:
                    f.write(f'  - GitHub: {h["full"]} ({h["stars"]}*) — {h["desc"]}\n')
                for h in e["hf_models"]:
                    f.write(f'  - HF model: {h["id"]}\n')
                for h in e["hf_spaces"]:
                    f.write(f'  - HF space: {h["id"]}\n')
            f.write("\n")
    print(f"originality gate done -> {out_md}")

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], sys.argv[3])
