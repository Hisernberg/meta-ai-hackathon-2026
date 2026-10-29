// Round-6 funnel: 5,000 worldwide-lattice finalists -> 32 deep-scored.
//   A. balanced prefilter 5000 -> 300 (mech/family/region caps, lane mix)
//   B. LLM triage 300 -> 90  (12 batches x 25)
//   C. LLM deep   90  -> 32  (6 batches x 15, 5 axes)
// Resumable under hackathon-repo/ideation/round6/. Fallback = heuristic rank (disclosed).
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import fs from "node:fs";
const run = promisify(execFile);
const DIR = "/home/z/my-project/hackathon-repo/ideation/round6";
const sleep = ms => new Promise(r => setTimeout(r, ms));
const j = p => { try { return JSON.parse(fs.readFileSync(p, "utf8")); } catch { return null; } };
const jl = p => fs.readFileSync(p, "utf8").trim().split("\n").map(l => JSON.parse(l));
const save = (p, o) => fs.writeFileSync(p, JSON.stringify(o, null, 1));

const SYSTEM = `You are the head judge of the Meta Global AI Developer Hackathon 2026 - round-6 WORLDWIDE battle (ideas mined from 10,000,000 lattice points seeded by global hackathon winners 2025-26). 6 build days left, solo builder (ML/research background, loves images+video+models), $150 Meta API credits + $100 Modal + $100 Baseten.
TRACK: indie. OFFICIAL RUBRIC: Impact 30%, Use of Meta AI Tooling 25%, Technical Depth & Execution 20%, Demo 25%.
HARD RULES: idea must be NEW (no clones; anti-projects = generic chatbots, basic RAG, simple image analyzers, health/medical advice, surveillance, job screeners, sports coaching, politics) and a REAL WORK use case (named user, concrete artifact, defensible time/money saved). Every idea embodies a NOVEL AGENT ARCHITECTURE (mixture of world agents, role-based expert parliaments, geometry-aware segmentation/embeddings, verifiable harnesses like undo-ledgers/attestations/auctions) - the architecture must be LOAD-BEARING, not decoration.
MODELS (exact ids): muse-wonder-1.0 (1M ctx, computer use, subagents) | muse-spark-1.3 | muse-image-1.0 | muse-voice-transcribe-1.0 | sam-3.1 (segment/track anything, image+video) | muse-spark-open (open weights; Baseten `+"`meta-models/muse-spark-open-1026`"+`) | muse-glimmer (30B Apache-2.0 self-host). Modal = serverless GPUs + sandboxes.
CONSTRAINTS: demoable live in 90 seconds; solo-buildable in <=6 days; no robot hardware; no from-scratch frontier training (fine-tune OK).
Judge like a skeptical senior Meta engineer: reward named worker + concrete artifact + visible wow + honest scope + worldwide story (works Dhaka-to-Detroit), punish vague data stories, hidden human labor, legality gray zones, demo fragility.`;

async function callZai(user, tag, retries = 5) {
  for (let i = 1; i <= retries; i++) {
    const tmp = `/tmp/zai_r6_${tag.replace(/\W/g, "_")}.json`;
    try {
      await run("/usr/local/bin/z-ai", ["chat", "-p", user, "-s", SYSTEM, "-o", tmp], { timeout: 420000 });
      const d = JSON.parse(fs.readFileSync(tmp, "utf8"));
      fs.rmSync(tmp, { force: true });
      return d?.choices?.[0]?.message?.content ?? "";
    } catch (e) {
      console.log(`  retry ${i}/${retries} [${tag}]: ${String(e.message || e).slice(0, 90)}`);
      fs.rmSync(tmp, { force: true });
      await sleep(12000 * i);
    }
  }
  return "";
}
const grab = (text) => {
  if (!text) return null;
  let s = text.trim().replace(/^```(json)?/i, "").replace(/```$/g, "").trim();
  const a = s.indexOf("{"), b = s.lastIndexOf("}");
  if (a === -1 || b <= a) return null;
  try { return JSON.parse(s.slice(a, b + 1)); } catch { return null; }
};
const line = (i, x) => `#${i} [${x.lane}/${x.mech_fam}:${x.mech}] "${x.title}" - ${x.pitch.slice(0, 200)}`;

(async () => {
  const all = jl(`${DIR}/round6_top5000.jsonl`);
  console.log(`loaded ${all.length} round-6 ideas`);
  all.forEach((x, i) => { x.idx = i; x.id = `R6-${String(i).padStart(5, "0")}`; });

  // ---- A. balanced prefilter 5000 -> 300 ----
  let pre = j(`${DIR}/prefilter.json`);
  if (!pre) {
    const sorted = [...all].sort((a, b) => b.score_total - a.score_total);
    const mechC = {}, famC = {}, regC = {}, domC = {}, laneC = { W: 0, U: 0 };
    pre = [];
    for (const x of sorted) {
      if (pre.length >= 300) break;
      if ((mechC[x.mech] || 0) >= 9) continue;
      if ((famC[x.mech_fam] || 0) >= 70) continue;
      if ((regC[x.region] || 0) >= 40) continue;
      if ((domC[x.domain] || 0) >= 3) continue;
      if (laneC[x.lane] >= 165) continue;
      mechC[x.mech] = (mechC[x.mech] || 0) + 1;
      famC[x.mech_fam] = (famC[x.mech_fam] || 0) + 1;
      regC[x.region] = (regC[x.region] || 0) + 1;
      domC[x.domain] = (domC[x.domain] || 0) + 1;
      laneC[x.lane]++;
      pre.push(x);
    }
    save(`${DIR}/prefilter.json`, pre);
  }
  console.log(`prefilter: ${pre.length} (lane mix W=${pre.filter(x => x.lane === "W").length} U=${pre.filter(x => x.lane === "U").length})`);

  // ---- B. LLM triage 300 -> 90 ----
  let triage = j(`${DIR}/triage_scores.json`);
  if (!triage) {
    triage = { scores: {}, fallback: [] };
    const B = 25;
    for (let b = 0; b < Math.ceil(pre.length / B); b++) {
      const batch = pre.slice(b * B, (b + 1) * B);
      const tag = `tri_${b}`;
      const listing = batch.map((x, i) => line(i, x)).join("\n");
      const prompt = `${listing}\n\nScore EACH idea 0-10 for "should survive to the deep round" = novelty of the architecture x real-work credibility x live-demo wow x worldwide credibility. Anti-projects = 0-2. Return STRICT JSON: {"scores":[{"i":0,"s":7.5,"why":"<=8 words"},...]}`;
      const txt = await callZai(prompt, tag);
      const out = grab(txt);
      if (out?.scores?.length) {
        for (const r of out.scores) {
          const it = batch[r.i];
          if (it && typeof r.s === "number") triage.scores[it.id] = { s: r.s, why: String(r.why || "").slice(0, 60) };
        }
      } else { triage.fallback.push(tag); }
      console.log(`triage batch ${b + 1}/${Math.ceil(pre.length / B)} ok=${!!out} fallback=${triage.fallback.length}`);
      save(`${DIR}/triage_scores.json`, triage);
      await sleep(2500);
    }
    pre.forEach((x, i) => { if (!triage.scores[x.id]) triage.scores[x.id] = { s: 10 - (i / pre.length) * 4, why: "heuristic-fallback" }; });
    save(`${DIR}/triage_scores.json`, triage);
  }
  const afterTriage = [...pre].sort((a, b) => (triage.scores[b.id]?.s ?? 0) - (triage.scores[a.id]?.s ?? 0)).slice(0, 90);
  console.log(`after triage: ${afterTriage.length}`);

  // ---- C. LLM deep 90 -> 32 ----
  let deep = j(`${DIR}/deep_scores.json`);
  if (!deep) {
    deep = { items: {}, fallback: [] };
    const B = 15;
    for (let b = 0; b < Math.ceil(afterTriage.length / B); b++) {
      const batch = afterTriage.slice(b * B, (b + 1) * B);
      const tag = `deep_${b}`;
      const listing = batch.map((x, i) => line(i, x)).join("\n");
      const prompt = `${listing}\n\nFor EACH idea return 5 axes 0-10: novelty (architecture genuinely new & load-bearing), real (named user + artifact + saved time/money), wow (90-second live demo spectacle), build (feasible solo in 6 days; 10 = trivial), meta (creative depth of Meta model/Modal/Baseten use). Return STRICT JSON: {"scores":[{"i":0,"nov":8,"real":7,"wow":9,"build":6,"meta":8,"note":"<=10 words"},...]}`;
      const txt = await callZai(prompt, tag);
      const out = grab(txt);
      if (out?.scores?.length) {
        for (const r of out.scores) {
          const it = batch[r.i];
          if (it && [r.nov, r.real, r.wow, r.build, r.meta].every(v => typeof v === "number")) {
            const total = r.nov * 0.28 + r.real * 0.26 + r.wow * 0.2 + r.build * 0.12 + r.meta * 0.14;
            deep.items[it.id] = { it, nov: r.nov, real: r.real, wow: r.wow, build: r.build, meta: r.meta, total: +(total).toFixed(2), note: String(r.note || "").slice(0, 70) };
          }
        }
      } else { deep.fallback.push(tag); }
      console.log(`deep batch ${b + 1}/${Math.ceil(afterTriage.length / B)} ok=${!!out} have=${Object.keys(deep.items).length}`);
      save(`${DIR}/deep_scores.json`, deep);
      await sleep(2500);
    }
    save(`${DIR}/deep_scores.json`, deep);
  }
  const ranked = Object.values(deep.items).sort((a, b) => b.total - a.total);
  const top32 = ranked.slice(0, 32).map(r => ({ ...r.it, deep: deep.items[r.it.id] }));
  save(`${DIR}/finalists32.json`, top32);
  console.log(`FINALISTS32 (${deep.fallback.length} fallback batches):`);
  top32.forEach((x, i) => console.log(`  ${i + 1}. ${x.id} [${x.lane}/${x.mech}] ${(x.deep?.total ?? 0).toFixed(2)} ${x.title.slice(0, 70)}`));
})();
