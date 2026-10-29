// Round-4 funnel: 20k fresh ideas -> top 24 finalists.
//   A heuristic prefilter (score_total caps) -> 240
//   B LLM triage: 12 batched calls (20/call) 240 -> 80
//   C LLM deep:   10 batched calls (8/call)   80 -> 24
// Resumable under hackathon-repo/ideation/round4/. On persistent 429 the batch
// falls back to heuristic rank (disclosed in results).
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import fs from "node:fs";
const run = promisify(execFile);
const DIR = "/home/z/my-project/hackathon-repo/ideation/round4";
const sleep = ms => new Promise(r => setTimeout(r, ms));
const j = p => { try { return JSON.parse(fs.readFileSync(p, "utf8")); } catch { return null; } };
const save = (p, o) => fs.writeFileSync(p, JSON.stringify(o, null, 1));

const SYSTEM = `You are the head judge of the Meta Global AI Developer Hackathon 2026 (round-4 mega battle). 7 build days left, solo builder, $150 Meta API credits + $100 Modal + $100 Baseten.
TRACK: indie — judged on creativity, technical ambition, WHETHER IT WORKS (each one third). Rubric: Impact 30%, Use of Meta AI Tooling 25%, Technical Depth 20%, Demo 25%.
THEMES: world = Build for Your World | frontier = Push the Frontier.
HARD RULES: idea must be NEW (not a clone of a famous product; generic hackathon apps are anti-projects) and a REAL WORK use case (named user, concrete artifact, defensible time/money saved). Round-4 ideas all embody a NOVEL AGENT ARCHITECTURE (mixture of world agents, role-based experts, geometry-aware segmentation/embeddings, verifiable harnesses) — reward ideas where the architecture is load-bearing (it is WHY the product wins), not decoration.
MODELS (exact ids): muse-wonder-1.0 (1M ctx, computer use, subagents) | muse-spark-1.3 | muse-image-1.0 | muse-voice-transcribe-1.0 | sam-3.1 (segment/track anything in image+video) | muse-spark-open (open weights; Baseten hosting/fine-tune) | muse-glimmer (small, Apache-2.0, self-host). Modal = serverless GPUs + sandboxes. Baseten = open-weight serving.
HARD CONSTRAINTS: demoable live in 90 seconds; buildable by 1 person in <=7 days; no from-scratch frontier training (fine-tuning open weights OK); no robot hardware; no medical diagnosis; no surveillance/face-recognition of non-consenting people.
Judge like a skeptical senior Meta engineer: penalize vague data stories, hidden human labor, legality gray zones, anything that will not survive a live demo. Reward: named worker + concrete artifact + visible wow + honest scope + architectures nobody has productized.`;

async function callZai(user, tag, retries = 5) {
  for (let i = 1; i <= retries; i++) {
    const tmp = `/tmp/zai_r4_${tag.replace(/\W/g, "_")}.json`;
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
const line = (i, x) => `#${i} [${x.lane}/${x.mech}] "${x.title}" — ${x.pitch.slice(0, 210)}`;

(async () => {
  const all = j(`${DIR}/round4_all.jsonl`) || fs.readFileSync(`${DIR}/round4_all.jsonl`, "utf8")
    .trim().split("\n").map(l => JSON.parse(l));
  console.log(`loaded ${all.length} round-4 ideas`);
  all.forEach((x, i) => { x.idx = i; x.id = `R4-${String(i).padStart(5, "0")}`; });

  // ---- A. heuristic prefilter -> 240 ----
  let pre = j(`${DIR}/prefilter.json`);
  if (!pre) {
    const byMech = {}, byDomain = {};
    const sorted = [...all].sort((a, b) => b.score_total - a.score_total);
    pre = [];
    for (const x of sorted) {
      if (pre.length >= 240) break;
      if ((byMech[x.mech] || 0) >= 16) continue;
      if ((byDomain[x.domain] || 0) >= 4) continue;
      byMech[x.mech] = (byMech[x.mech] || 0) + 1;
      byDomain[x.domain] = (byDomain[x.domain] || 0) + 1;
      pre.push(x);
    }
    save(`${DIR}/prefilter.json`, pre);
  }
  console.log(`prefilter: ${pre.length}`);

  // ---- B. LLM triage 240 -> 80 ----
  let triage = j(`${DIR}/triage_scores.json`);
  if (!triage) {
    triage = { scores: {}, fallback: [] };
    const B = 20;
    for (let b = 0; b < Math.ceil(pre.length / B); b++) {
      const batch = pre.slice(b * B, (b + 1) * B);
      const tag = `tri_${b}`;
      const listing = batch.map((x, i) => line(i, x)).join("\n");
      const prompt = `${listing}\n\nScore EACH idea 0-10 for "should survive to the deep round" = novelty of the architecture x real-work credibility x live-demo wow. Anti-projects (generic chatbots/RAG wrappers/health advice) = 0-2. Return STRICT JSON: {"scores":[{"i":0,"s":7.5,"why":"<=8 words"},...]}`;
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
      await sleep(3000);
    }
    // fill fallbacks with heuristic rank
    pre.forEach((x, i) => { if (!triage.scores[x.id]) triage.scores[x.id] = { s: 10 - (i / pre.length) * 4, why: "heuristic-fallback" }; });
    save(`${DIR}/triage_scores.json`, triage);
  }
  const afterTriage = [...pre].sort((a, b) => (triage.scores[b.id]?.s ?? 0) - (triage.scores[a.id]?.s ?? 0)).slice(0, 80);
  console.log(`after triage: ${afterTriage.length}`);

  // ---- C. LLM deep 80 -> 24 ----
  let deep = j(`${DIR}/deep_scores.json`);
  if (!deep) {
    deep = { items: {}, fallback: [] };
    const B = 8;
    for (let b = 0; b < Math.ceil(afterTriage.length / B); b++) {
      const batch = afterTriage.slice(b * B, (b + 1) * B);
      const tag = `deep_${b}`;
      const listing = batch.map((x, i) => line(i, x)).join("\n");
      const prompt = `${listing}\n\nFor EACH idea return 5 axes 0-10: novelty (architecture genuinely new & load-bearing), real (named user + artifact + saved time/money), wow (90-second live demo spectacle), build (feasible solo in 7 days; 10 = trivial), meta (creative depth of Meta model/Modal/Baseten use). Return STRICT JSON: {"scores":[{"i":0,"nov":8,"real":7,"wow":9,"build":6,"meta":8,"note":"<=10 words"},...]}`;
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
      await sleep(3000);
    }
    save(`${DIR}/deep_scores.json`, deep);
  }
  const ranked = Object.values(deep.items).sort((a, b) => b.total - a.total);
  const top24 = ranked.slice(0, 24).map(r => r.it);
  save(`${DIR}/finalists24.json`, top24.map(x => ({ ...x, deep: deep.items[x.id] })));
  console.log(`FINALISTS24 (${deep.fallback.length} fallback batches):`);
  top24.forEach((x, i) => console.log(`  ${i + 1}. ${x.id} [${x.lane}/${x.mech}] ${(deep.items[x.id]?.total ?? 0).toFixed(2)} ${x.title.slice(0, 72)}`));
})();
