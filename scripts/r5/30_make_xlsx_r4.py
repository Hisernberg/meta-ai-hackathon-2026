# -*- coding: utf-8 -*-
"""Round-4 deliverable workbook: ideas dataset + battle audit trail."""
import json, csv
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

DIR = "/home/z/my-project/hackathon-repo/ideation/round4"
OUT = "/home/z/my-project/download/Round4_Ideas_Dataset.xlsx"

HDR = Font(bold=True, color="FFFFFF")
FILL = PatternFill("solid", fgColor="1F3864")
WRAP = Alignment(wrap_text=True, vertical="top")

def sheet(wb, name, rows, widths=None, max_rows=None):
    ws = wb.create_sheet(name)
    if not rows: return
    ws.append(rows[0])
    for c in ws[1]: c.font, c.fill = HDR, FILL
    for r in (rows[1:] if not max_rows else rows[1:max_rows]):
        ws.append([str(v)[:500] if v is not None else "" for v in r])
    for i, col in enumerate(ws.columns, 1):
        w = (widths or {}).get(i, 18)
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row: c.alignment = WRAP
    ws.freeze_panes = "A2"

wb = Workbook(); wb.remove(wb.active)

sheet(wb, "README", [
 ["Meta Global AI Developer Hackathon 2026 — Round-4 Battle of Ideas (Oct 28, 2026)"],
 ["Team blackbox (solo: navi12 / Nabid Nur) — Indie track"],
 [],
 ["Pool this round: 10,568 (R1-R3) + 20,000 new R4 ideas = 30,568 unique ideas total."],
 ["R4 lanes: 10,000 winner-thought lane (Devpost/CV winner-DNA patterns) + 10,000 builder-profile lane"],
 ["(models, images, videos, ML/DS, research, conference-level ideas — the builder's own thought process)."],
 ["Every R4 idea embodies a NOVEL mechanism from the architecture bank:"],
 ["  MoWA (mixture of world agents) | MoRBE (mixture of role-based experts) | GEO (geometry-aware"],
 ["  segmentation/embedding optimization) | HARNESS (verifiable agentic harness) | FUSION (combos)."],
 [],
 ["Funnel: heuristic prefilter 240 -> LLM triage 80 (0 fallback batches) -> LLM deep 24 finalists"],
 ["-> HF+GitHub originality sweep on all 24 (0 clones: 11 none / 12 related / 1 close)"],
 ["-> Grand arena: 24 + incumbent Nuskha seeded hardest path; bracket -> council of 5 personas."],
 [],
 ["VERDICT: NUSKHA re-confirmed champion — council 25/30, unanimous #1 from all 5 personas."],
 ["Challengers: R4-08143 scale-ladder claims-to-model 14 pts | R4-12533 geodesic skills 9 | R4-01930 mask-metrics 7."],
 ["Nuskha V4 spec upgraded with: gate chain, quorum receipts, mask-geometry reconciliation,"],
 ["three-ladder consistency, cost-aware router. Build spec: CHAMPION_V4.md; forms: FORMS_READY_V4.md."],
], {1: 110})

# lane samples (top 400 each by score for readability; full CSVs in download/)
def lane_rows(path, cap):
    rows = [["rank","lane","mech","mech_fam","tier","title","pitch","domain","models","score","days"]]
    with open(path, newline="", encoding="utf-8") as f:
        for i, r in enumerate(csv.DictReader(f)):
            if i >= cap: break
            rows.append([i+1, r["lane"], r["mech"], r["mech_fam"], r["mech_tier"],
                         r["title"], r["pitch"], r["domain"], r["models"],
                         r["score_total"], r["days"]])
    return rows

sheet(wb, "LaneW_top400", lane_rows("/home/z/my-project/download/hackathon_ideas_round4_laneW.csv", 400),
      {1:6,3:20,6:44,7:60,8:24,9:34,10:8})
sheet(wb, "LaneU_top400", lane_rows("/home/z/my-project/download/hackathon_ideas_round4_laneU.csv", 400),
      {1:6,3:20,6:44,7:60,8:24,9:34,10:8})

# finalists 24 + originality
fin = json.load(open(f"{DIR}/finalists24.json"))
orig = {o["id"]: o["verdict"] for o in json.load(open(f"{DIR}/originality.json"))}
rows = [["rank","id","lane","mech","deep_total","title","originality_verdict"]]
for i, x in enumerate(fin, 1):
    rows.append([i, x["id"], x["lane"], x["mech"], x["deep"]["total"], x["title"], orig.get(x["id"], "none")])
sheet(wb, "Finalists24", rows, {2:11,3:7,4:22,5:11,6:60,7:17})

# arena trail
res = json.load(open(f"{DIR}/R4_RESULT.json"))
rows = [["stage","winner","details"]]
rows.append(["R1 heats (5x5, top2 adv)", "10 advanced", "; ".join(
    ["h0: R3-CHAMP+R4-10763 (Nuskha seeded vs top-4 scorers)", "h1: R4-18271+R4-11515", "h2: R4-01930+R4-01249",
     "h3: R4-12533+R4-13369", "h4: R4-08143+R4-09098"])])
rows.append(["R2 heats", "4 advanced", "h0: R3-CHAMP+R4-01930 | h1: R4-08143+R4-12533"])
rows.append(["Semis", "2 advanced", "semi0: R4-01930 8.2 > Nuskha 7.5 (attack-mode upset) | semi1: R4-08143 8.2 > R4-12533 7.5"])
rows.append(["Grand final (bracket)", "R4-08143", "8.7 vs R4-01930 8.1 — bracket champion"])
rows.append(["Council of 5 (final verdict)", "NUSKHA (R3-CHAMP)", "25/30 unanimous #1; R4-08143 14, R4-12533 9, R4-01930 7"])
rows.append(["FINAL CHAMPION", "NUSKHA", "3rd consecutive battle win (R2, R3, R4); spec: CHAMPION_V4.md"])
for p in res.get("council", []):
    rows.append(["council persona", p["persona"][:48], p.get("line", "")])
sheet(wb, "Arena_trail", rows, {1:30,2:34,3:80})

# originality evidence summary
rows = [["id","title","verdict"]]
for o in json.load(open(f"{DIR}/originality.json")):
    rows.append([o["id"], o["title"], o["verdict"]])
sheet(wb, "Originality_sweep", rows, {1:11,2:70,3:11})

wb.save(OUT)
print("saved", OUT)
