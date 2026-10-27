# -*- coding: utf-8 -*-
"""Final-16 selection for the round-3 arena (documented rule):
   LLM triage order -> remove same-lens near-duplicates (keep 1 per flavor) ->
   family cap 3 -> inject defending champion Ustad (S139) as protected seed ->
   fill remaining slots in triage order. Writes round3/top16.json for judge_r3.mjs."""
import json

DIR = "/home/z/my-project/hackathon-repo/ideation/round3"
top40 = json.load(open(f"{DIR}/top40.json"))
short = {r["sid"]: r for r in json.load(open(f"{DIR}/shortlist.json"))}

def flavor(lens):
    p = lens.split("-")
    if lens.startswith("W-"): return f"W-{p[1]}"
    if lens.startswith("U-"): return f"U-{p[1]}-{p[2] if len(p) > 2 else ''}"
    return lens

picked, seen_flavor, fam = [], set(), {}
for x in top40:
    r = x["r"]; fl = flavor(r["lens"])
    if fl in seen_flavor: continue          # near-duplicate flavor (same lens, diff context)
    key2 = "-".join(fl.split("-")[:2])
    if fam.get(key2, 0) >= 3: continue
    seen_flavor.add(fl)
    fam[key2] = fam.get(key2, 0) + 1
    picked.append(r)
    if len(picked) == 15: break

# protected seed: defending champion
ustad = short["S139"]
if not any(r["sid"] == "S139" for r in picked):
    picked.append(ustad)

for i, r in enumerate(picked):
    r["total"] = 0  # arena fallback order neutral
json.dump(picked, open(f"{DIR}/top16.json", "w"), indent=1)
print(f"final 16 locked -> {DIR}/top16.json")
for i, r in enumerate(picked):
    print(f"{i+1:2d}. [{r['sid']}] {r['title'][:60]} | {r['lens']} | {r['theme']} | r{r['round']}")
