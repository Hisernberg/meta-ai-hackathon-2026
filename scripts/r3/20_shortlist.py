# -*- coding: utf-8 -*-
"""Round-3: merge grand pool (7,868) + round-3 (2,700) -> 10,568; select a capped,
diverse shortlist of 140 for the LLM arena. Defending champion Ustad is seeded in."""
import csv, json, os
from collections import Counter

GRAND = "/home/z/my-project/download/hackathon_ideas_grand_corpus_7868.csv"
R3 = "/home/z/my-project/download/hackathon_ideas_round3.csv"
OUT_DIR = "/home/z/my-project/hackathon-repo/ideation/round3"
os.makedirs(OUT_DIR, exist_ok=True)

def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

grand, r3 = load(GRAND), load(R3)
pool = grand + r3
merged_path = "/home/z/my-project/download/hackathon_ideas_grand_corpus_10568.csv"
with open(merged_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(pool[0].keys()))
    w.writeheader()
    for r in pool:
        w.writerow({k: r.get(k, "") for k in pool[0].keys()})
print(f"merged pool: {len(pool)} -> {merged_path}")

# shortlist: greedy by score_total with caps
CAP_FAMILY, CAP_DOMAIN = 12, 6
fam, dom = Counter(), Counter()
short, rest = [], []
for r in sorted(pool, key=lambda x: -float(x["score_total"] or 0)):
    lens = r.get("lens", "")
    family = lens.split("-")[1] if lens.startswith(("W-", "U-")) else "legacy"
    if fam[family] >= CAP_FAMILY or dom[r["domain"]] >= CAP_DOMAIN:
        rest.append(r); continue
    fam[family] += 1; dom[r["domain"]] += 1
    short.append(r)
    if len(short) >= 139: break

# seed the defending champion (round-2 winner) for the hardest path
ustad = dict(lens="champion-r2", title="Ustad — film a job once, get a living SOP",
             pitch="Street-food stall chains film one job on a phone; it becomes an illustrated SOP "
                   "with checkpoints, a trainee quiz from generated wrong-step scenes, and an "
                   "expert-approval loop. Muse Spark video + Voice + SAM 3.1 + Muse Image.",
             theme="world", domain="street food stall chains",
             models="muse-spark-1.3+muse-voice-transcribe-1.0+sam-3.1+muse-image-1.0",
             score_total="84.0", round="2")
short.append(ustad)

for i, r in enumerate(short):
    r["sid"] = f"S{i:03d}"
with open(f"{OUT_DIR}/shortlist.json", "w", encoding="utf-8") as f:
    json.dump([{k: r.get(k, "") for k in ("sid", "lens", "title", "pitch", "theme",
                "domain", "models", "score_total", "round")} for r in short], f, indent=1)
print(f"shortlist: {len(short)} (families={len(fam)}) -> {OUT_DIR}/shortlist.json")
print("family spread:", dict(fam.most_common(12)))
