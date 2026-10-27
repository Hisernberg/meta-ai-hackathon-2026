// Round-3 Battle of Ideas: LLM funnel + arena over the 10,568-idea pool.
// Stages (all resumable under hackathon-repo/ideation/round3/):
//   A triage: 140 -> top 40 (24 batched calls)
//   B deep:   40  -> top 16 (40 calls, 5 axes, Indie-weighted)
//   C arena:  16 -> 8 -> 4 -> 2 -> 1 (15 attack calls)
//   D council: 5 personas rank the final 4 (5 calls)
// Defending champion Ustad (r2) is seeded with the hardest path.
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import fs from "node:fs";
const run = promisify(execFile);
const DIR = "/home/z/my-project/hackathon-repo/ideation/round3";
const sleep = ms => new Promise(r => setTimeout(r, ms));
const j = p => { try { return JSON.parse(fs.readFileSync(p, "utf8")); } catch { return null; } };
const save = (p, o) => fs.writeFileSync(p, JSON.stringify(o, null, 1));

const SYSTEM = `You are the head judge of the Meta Global AI Developer Hackathon 2026 grand idea arena. 10 build days left, solo builder, $150 Meta API credits + $100 Modal + $100 Baseten, $1M prizes.
TRACK: indie — judged on creativity, technical ambition, WHETHER IT WORKS (each one third).
THEMES: world = Build for Your World (problem the builder knows firsthand) | frontier = Push the Frontier (new machine capability).
HARD RULES: idea must be NEW (not a clone of a famous product) and a REAL WORK use case (named user, concrete artifact, defensible time/money saved).
MODELS (exact ids): muse-wonder-1.0 (1M ctx, computer use, subagents) | muse-spark-1.3 | muse-image-1.0 | muse-voice-transcribe-1.0 | sam-3.1 (segment/track anything in image+video) | muse-spark-open (open weights; Baseten hosting/fine-tune) | muse-glimmer (small, Apache-2.0, self-host).
Modal = serverless GPUs + sandboxes. Baseten = open-weight serving.
HARD CONSTRAINTS: demoable live in 90 seconds; buildable by 1 person in <=7 days; no from-scratch frontier training (fine-tuning open weights is OK); no robot hardware; no autonomous medical diagnosis (assistive OK); no surveillance or face-recognition of non-consenting people.
Judge like a skeptical senior Meta engineer: penalize vague data stories, hidden human labor, legality gray zones, and anything that will not survive a live demo. Reward: named worker + concrete artifact + visible wow + honest scope.`;

const WEIGHTS = { c: 0.18, a: 0.16, w: 0.26, r: 0.26, m: 0.14 }; // Indie-weighted

async function callZai(user, tag, retries = 6) {
  for (let i = 1; i <= retries; i++) {
    const tmp = `/tmp/zai_r3_${tag.replace(/\W/g, "_")}.json`;
    try {
      await run("/usr/local/bin/z-ai", ["chat", "-p", user, "-s", SYSTEM, "-o", tmp], { timeout: 420000 });
      const d = JSON.parse(fs.readFileSync(tmp, "utf8"));
      fs.rmSync(tmp, { force: true });
      return d?.choices?.[0]?.message?.content ?? "";
    } catch (e) {
      console.log(`  retry ${i}/${retries} [${tag}]: ${String(e.message || e).slice(0, 100)}`);
      fs.rmSync(tmp, { force: true });
      await sleep(15000 * i);
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
const entry = (r, full = true) => {
  const m = String(r.models || "").replace(/muse-/g, "").replace(/-1\.0|-1\.3/g, "");
  let e = `[${r.sid}] ${r.title} — theme:${r.theme}`;
  if (full) e += `\npitch: ${r.pitch}\ndomain: ${r.domain} | stack: ${m} | heuristic:${r.score_total} | round:${r.round}`;
  return e;
};

// ---------- Stage A: triage ----------
async function triage(short) {
  const dir = `${DIR}/triage`; fs.mkdirSync(dir, { recursive: true });
  const batches = [];
  for (let i = 0; i < short.length; i += 6) batches.push(short.slice(i, i + 6));
  let done = 0;
  for (let bi = 0; bi < batches.length; bi++) {
    const out = `${dir}/batch_${String(bi).padStart(2, "0")}.json`;
    if (j(out)) { done++; continue; }
    const list = batches[bi].map(r => entry(r, false)).join("\n");
    const user = `Score each idea 1-10 for champion potential (creativity + real work use + whether it will actually work solo). 6 ideas:\n${list}\nReturn ONLY JSON: {"scores":[{"sid":"Sxxx","s":1-10,"why":"<=10 words"}]}`;
    const o = grab(await callZai(user, `t${bi}`));
    if (o?.scores?.length) { save(out, o.scores); done++; console.log(`triage ${done}/${batches.length}`); }
    await sleep(1200);
  }
  const all = batches.flatMap((_, bi) => j(`${dir}/batch_${String(bi).padStart(2, "0")}.json`) || []);
  const byId = Object.fromEntries(short.map(r => [r.sid, r]));
  const ranked = all.filter(x => byId[x.sid]).map(x => ({ ...x, r: byId[x.sid] }))
    .sort((a, b) => b.s - a.s).slice(0, 40);
  save(`${DIR}/top40.json`, ranked);
  console.log(`triage done: ${all.length} scored, top40 kept`);
  return ranked;
}

// ---------- Stage B: deep score ----------
async function deep(ranked) {
  const dir = `${DIR}/deep`; fs.mkdirSync(dir, { recursive: true });
  for (const r of ranked) {
    const out = `${dir}/item_${r.sid}.json`;
    if (j(out)) continue;
    const user = `Score this hackathon idea on 5 axes (1-10): c=creativity, a=technical ambition, w=whether it works solo in 7 days, r=real work use case strength, m=how deeply it uses Meta models. Be a harsh skeptic; 7 is a strong score.\n\n${entry(r)}\n\nReturn ONLY JSON: {"sid":"${r.sid}","c":0,"a":0,"w":0,"r":0,"m":0,"verdict":"<=22 words"}`;
    const o = grab(await callZai(user, `d${r.sid}`));
    if (o && o.c) { o.total = +(o.c * WEIGHTS.c + o.a * WEIGHTS.a + o.w * WEIGHTS.w + o.r * WEIGHTS.r + o.m * WEIGHTS.m).toFixed(2); save(out, o); console.log(`deep ${r.sid}: ${o.total}`); }
    await sleep(6000);
  }
  const scoredAll = () => ranked.map(r => ({ ...r, ...j(`${dir}/item_${r.sid}.json`) })).filter(x => x.total);
  let scored = scoredAll();
  for (let pass = 0; pass < 4 && scored.length < ranked.length; pass++) {
    console.log(`deep pass ${pass + 1}: ${scored.length}/${ranked.length} scored — retrying missing`);
    await sleep(20000);
    for (const r of ranked.filter(x => !j(`${dir}/item_${x.sid}.json`))) {
      const user = `Score this hackathon idea on 5 axes (1-10): c=creativity, a=technical ambition, w=whether it works solo in 7 days, r=real work use case strength, m=how deeply it uses Meta models. Be a harsh skeptic; 7 is a strong score.\n\n${entry(r)}\n\nReturn ONLY JSON: {"sid":"${r.sid}","c":0,"a":0,"w":0,"r":0,"m":0,"verdict":"<=22 words"}`;
      const o = grab(await callZai(user, `d${r.sid}`));
      if (o && o.c) { o.total = +(o.c * WEIGHTS.c + o.a * WEIGHTS.a + o.w * WEIGHTS.w + o.r * WEIGHTS.r + o.m * WEIGHTS.m).toFixed(2); save(`${dir}/item_${r.sid}.json`, o); console.log(`deep ${r.sid}: ${o.total}`); }
      await sleep(9000);
    }
    scored = scoredAll();
  }
  // diversity cap: <=3 per family in top 16
  const famCount = {};
  const top16 = [];
  for (const x of scored) {
    const fam = String(x.r?.lens || x.lens || "").split("-").slice(0, 2).join("-");
    if ((famCount[fam] || 0) >= 3) continue;
    famCount[fam] = (famCount[fam] || 0) + 1;
    top16.push(x);
    if (top16.length === 16) break;
  }
  save(`${DIR}/top16.json`, top16);
  console.log(`deep done. top16 families:`, Object.keys(famCount).length);
  return top16;
}

// ---------- Stage C: arena ----------
const BRACKET = [[0, 15], [7, 8], [4, 11], [3, 12], [2, 13], [5, 10], [6, 9], [1, 14]];
async function arena(top16) {
  const dir = `${DIR}/arena`; fs.mkdirSync(dir, { recursive: true });
  let round = top16;
  let level = 4; // 16 -> 8
  while (round.length > 1) {
    const next = [];
    const pairs = round.length === 16 ? BRACKET : round.map((_, i) => [i, i + 1]).filter(([a]) => a % 2 === 0);
    for (const [ai, bi] of pairs) {
      if (bi === undefined) { next.push(round[ai]); continue; }
      const A = round[ai], B = round[bi];
      const out = `${dir}/L${level}_${A.sid}_vs_${B.sid}.json`;
      let res = j(out);
      if (!res) {
        const user = `ARENA MATCH. Two hackathon ideas. Attack each one's weakest point (one line each), then pick the winner for the Meta Global AI Developer Hackathon indie track (creativity/ambition/whether-it-works each 1/3; must be NEW + real work use case).\n\nIDEA A:\n${entry(A)}\n\nIDEA B:\n${entry(B)}\n\nReturn ONLY JSON: {"attackA":"<=14 words","attackB":"<=14 words","winner":"A|B","why":"<=18 words"}`;
        const o = grab(await callZai(user, `a${A.sid}${B.sid}`));
        if (o && (o.winner === "A" || o.winner === "B")) { res = { ...o, A: A.sid, B: B.sid }; save(out, res); }
        else { res = { A: A.sid, B: B.sid, winner: (A.total ?? 0) >= (B.total ?? 0) ? "A" : "B", why: "score fallback" }; save(out, res); }
        await sleep(6000);
      }
      console.log(`L${level}: ${A.sid} vs ${B.sid} -> ${res.winner} (${res.why})`);
      next.push(res.winner === "A" ? A : B);
    }
    round = next; level = level / 2;
  }
  save(`${DIR}/champion.json`, round[0]);
  console.log(`ARENA CHAMPION: ${round[0].sid} — ${round[0].title}`);
  return round[0];
}

// ---------- Stage D: council ----------
const PERSONAS = [
  ["pragmatist", "A pragmatic judge who has watched 500 demos die: only belief in 7-day solo builds counts."],
  ["meta-maximalist", "A Meta models maximalist: ideas must need Muse Wonder/SAM 3.1/Voice/Image/Open-weights deeply, not cosmetically."],
  ["showman", "A demo-day showman: the 90-second wow is everything; boring-but-useful loses."],
  ["auditor", "A rules auditor: new (not a clone), real work use case, consent/legality, honest scope."],
  ["user-standin", "Stand-in for the builder: loves building models, images, videos, ML engineering, data science, research and top-conference-level work — which idea would he proud to build and defend?"],
];
async function council(final4) {
  const dir = `${DIR}/council`; fs.mkdirSync(dir, { recursive: true });
  const list = final4.map((r, i) => `#${i + 1} ${entry(r)}`).join("\n\n");
  for (const [pid, pdesc] of PERSONAS) {
    const out = `${dir}/${pid}.json`;
    if (j(out)) continue;
    const user = `You are the ${pid} judge: ${pdesc}\nRank these 4 finalists best-to-worst for winning the hackathon:\n\n${list}\n\nReturn ONLY JSON: {"ranking":["1","2","3","4"],"why":"<=16 words"} (use the # numbers)`;
    const o = grab(await callZai(user, `c${pid}`));
    if (o?.ranking) { save(out, o); console.log(`${pid}: ${o.ranking.join(">")}`); }
    await sleep(6000);
  }
  const votes = PERSONAS.map(([pid]) => j(`${dir}/${pid}.json`)).filter(Boolean);
  const pts = {};
  for (const v of votes) v.ranking.forEach((n, i) => { pts[n] = (pts[n] || 0) + (4 - i); });
  const board = { votes, points: pts };
  save(`${DIR}/council_board.json`, board);
  const order = Object.entries(pts).sort((a, b) => b[1] - a[1]);
  console.log(`COUNCIL POINTS:`, order.map(([n, p]) => `#${n}:${p}pts`).join(" "));
  return order;
}

// ---------- main ----------
const short = j(`${DIR}/shortlist.json`);
if (!short) { console.error("missing shortlist.json"); process.exit(1); }
const top40 = j(`${DIR}/top40.json`) || await triage(short);
const top16 = j(`${DIR}/top16.json`) || await deep(top40);
const champ = j(`${DIR}/champion.json`) || await arena(top16);
const councilRes = j(`${DIR}/council_board.json`) || null;
const final4 = councilRes ? null : await currentFinal4(top16);
async function currentFinal4(top16) { // reconstruct final 4 from arena files
  const dir = `${DIR}/arena`;
  const files = fs.readdirSync(dir).filter(f => f.startsWith("L2_"));
  const winners = files.map(f => j(`${dir}/${f}`)).filter(Boolean)
    .map(r => r.winner === "A" ? r.A : r.B);
  return top16.filter(r => winners.includes(r.sid)).length === 4
    ? top16.filter(r => winners.includes(r.sid)) : top16.slice(0, 4);
}
if (!councilRes) { const order = await council(final4); save(`${DIR}/result.json`, { champion: champ.sid, title: champ.title, council: order }); }
else save(`${DIR}/result.json`, { champion: champ.sid, title: champ.title, council: Object.entries(councilRes.points) });
console.log("ALL STAGES COMPLETE");
