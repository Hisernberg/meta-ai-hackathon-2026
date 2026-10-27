// Round-4 GRAND ARENA: 24 finalists + defending champion Nuskha (R3) seeded
// with the hardest path. Heats -> semis -> grand final + council of 5.
//   R1: 5 heats of 5 -> top 2 each = 10
//   R2: 2 heats of 5 -> top 2 each = 4
//   R3: 2 semis (1v1v1v1 ranked) -> top 2... actually 4 -> 2 (two matches of 2)
//   R4: grand final 2 -> 1 CHAMPION. Council of 5 personas re-ranks final 4.
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import fs from "node:fs";
const run = promisify(execFile);
const DIR = "/home/z/my-project/hackathon-repo/ideation/round4";
const sleep = ms => new Promise(r => setTimeout(r, ms));
const j = p => { try { return JSON.parse(fs.readFileSync(p, "utf8")); } catch { return null; } };
const save = (p, o) => fs.writeFileSync(p, JSON.stringify(o, null, 1));

const SYSTEM = `You are the head judge of the Meta Global AI Developer Hackathon 2026 — round-4 GRAND ARENA. 7 build days left, solo builder, $150 Meta API credits + $100 Modal + $100 Baseten.
TRACK: indie — creativity, technical ambition, WHETHER IT WORKS (each one third). Rubric: Impact 30%, Meta Tooling 25%, Technical Depth 20%, Demo 25%.
HARD RULES: NEW (not a clone; generic hackathon apps are anti-projects: no basic RAG, no simple image analyzers, no health/medical advice, no surveillance, no job screeners) + REAL WORK use case (named user, concrete artifact, defensible time/money saved). Novel agent architecture (mixture of world agents / role-based experts / geometry-aware segmentation or embeddings / verifiable harnesses) must be LOAD-BEARING.
MODELS: muse-wonder-1.0 (1M ctx, computer use, subagents) | muse-spark-1.3 | muse-image-1.0 | muse-voice-transcribe-1.0 | sam-3.1 | muse-spark-open (open weights, Baseten) | muse-glimmer (small, Apache-2.0, self-host). Modal = serverless GPUs + sandboxes.
CONSTRAINTS: 90-second live demo; solo-buildable in <=7 days; no robot hardware; no from-scratch frontier training.
Judge like a skeptical senior Meta engineer. Kill: vague data stories, hidden human labor, legality gray zones, demo fragility. Reward: named worker + concrete artifact + visible wow + honest scope + architecture nobody has productized.`;

async function callZai(user, tag, retries = 5) {
  for (let i = 1; i <= retries; i++) {
    const tmp = `/tmp/zai_r4a_${tag.replace(/\W/g, "_")}.json`;
    try {
      await run("/usr/local/bin/z-ai", ["chat", "-p", user, "-s", SYSTEM, "-o", tmp], { timeout: 420000 });
      const d = JSON.parse(fs.readFileSync(tmp, "utf8"));
      fs.rmSync(tmp, { force: true });
      return d?.choices?.[0]?.message?.content ?? "";
    } catch (e) {
      console.log(`  retry ${i}/${retries} [${tag}]: ${String(e.message || e).slice(0, 90)}`);
      fs.rmSync(tmp, { force: true });
      await sleep(14000 * i);
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

const NUSKHA = {
  id: "R3-CHAMP", lane: "INCUMBENT", mech: "fuse:recipe-exec",
  title: "Nuskha — paper methods -> runnable recipe, executed in Modal sandboxes",
  pitch: "Turn any research paper's methods section into a numbered recipe a grad student can actually run: parameter extraction, missing-steps audit (what the paper omits), environment provisioning in Modal sandboxes, execution with logged artifacts, figure reconciliation (does the remade figure match the published one), and a signed Reproduction Receipt. Stack: Wonder (1M ctx) reads the paper, Spark plans, Glimmer drafts sandbox code, Modal executes, Spark Open on Baseten grades similarity. Push the Frontier. Defending champion from round 3 (beat 10,568 ideas).",
  orig: "related", deep: { total: 8.5 }
};

const card = (x, i) => `#${i} (${x.id}) "${x.title}" — ${x.pitch.slice(0, 330)}` +
  (x.orig && x.orig !== "none" ? ` [originality sweep: ${x.orig} adjacent work exists]` : " [originality sweep: clean]");

async function match(tag, cands, n) {
  const listing = cands.map((x, i) => card(x, i)).join("\n\n");
  const prompt = `HEAT — rank these ${cands.length} ideas. Return STRICT JSON:
{"ranking":[{"i":0,"score":8.2,"kill":"main weakness <=12 words"}...],"top":${n},"why_final":"<=25 words"}
Score 0-10 on: novelty-of-architecture x real-work credibility x 90s-demo wow x solo-buildability-in-7-days x Meta-stack depth. ${n} advance.\n\n${listing}`;
  let out = grab(await callZai(prompt, tag));
  if (!out?.ranking) { // one retry with stricter instruction
    await sleep(8000);
    out = grab(await callZai(prompt + "\nReturn ONLY the JSON object.", tag + "b"));
  }
  if (!out?.ranking) return null;
  const ranked = out.ranking.filter(r => cands[r.i]).slice(0, cands.length);
  return { tag, verdict: out, order: ranked.map(r => ({ cand: cands[r.i], score: r.score, kill: r.kill })) };
}

(async () => {
  const finalists = j(`${DIR}/finalists24.json`);
  const orig = j(`${DIR}/originality.json`) || [];
  const omap = Object.fromEntries(orig.map(o => [o.id, o.verdict]));
  const pool = finalists.map(x => ({ ...x, orig: omap[x.id] || "none" }));
  // hardest path: Nuskha + the top-4 deep scorers in heat 1
  const sorted = [...pool].sort((a, b) => (b.deep?.total || 0) - (a.deep?.total || 0));
  const heat1 = [NUSKHA, ...sorted.slice(0, 4)];
  const rest = sorted.slice(4);
  const heats = [heat1];
  for (let i = 0; i < rest.length; i += 5) heats.push(rest.slice(i, i + 5));
  console.log(`R1 heats: ${heats.map(h => h.length).join(", ")}`);

  // ---- Round 1 ----
  let r1 = j(`${DIR}/arena_r1.json`);
  if (!r1) {
    r1 = [];
    for (let h = 0; h < heats.length; h++) {
      const res = await match(`r1_h${h}`, heats[h], 2);
      if (!res) { console.log(`HEAT ${h} FAILED`); return; }
      r1.push(res); save(`${DIR}/arena_r1.json`, r1);
      console.log(`R1 h${h}: adv=[${res.order.slice(0, 2).map(o => o.cand.id).join(", ")}]`);
      await sleep(3000);
    }
  }
  let adv2 = r1.flatMap(res => res.order.slice(0, 2).map(o => o.cand));
  console.log(`advancing to R2: ${adv2.length}`);
  // ensure Nuskha track
  const nuskhaAlive = adv2.some(x => x.id === "R3-CHAMP");

  // ---- Round 2: 2 heats of 5 ----
  const h2a = adv2.slice(0, 5), h2b = adv2.slice(5);
  let r2 = j(`${DIR}/arena_r2.json`);
  if (!r2) {
    r2 = [];
    for (let h = 0; h < 2; h++) {
      const res = await match(`r2_h${h}`, h === 0 ? h2a : h2b, 2);
      if (!res) { console.log(`R2 HEAT ${h} FAILED`); return; }
      r2.push(res); save(`${DIR}/arena_r2.json`, r2);
      console.log(`R2 h${h}: adv=[${res.order.slice(0, 2).map(o => o.cand.id).join(", ")}]`);
      await sleep(3000);
    }
  }
  const adv4 = r2.flatMap(res => res.order.slice(0, 2).map(o => o.cand));
  console.log(`SEMIFINALISTS: ${adv4.map(x => x.id).join(", ")}`);

  // ---- Semis: 2 matches of 2 ----
  let r3s = j(`${DIR}/arena_semis.json`);
  if (!r3s) {
    r3s = [];
    for (let m = 0; m < 2; m++) {
      const pair = adv4.slice(m * 2, m * 2 + 2);
      const res = await match(`semi_${m}`, pair, 1);
      if (!res) { console.log(`SEMI ${m} FAILED`); return; }
      r3s.push(res); save(`${DIR}/arena_semis.json`, r3s);
      console.log(`SEMI ${m}: win=${res.order[0].cand.id}`);
      await sleep(3000);
    }
  }
  const final2 = r3s.map(res => res.order[0].cand);
  console.log(`GRAND FINAL: ${final2.map(x => x.id).join(" vs ")}`);

  // ---- Grand final ----
  let gf = j(`${DIR}/arena_grand_final.json`);
  if (!gf) {
    gf = await match("grand_final", final2, 1);
    if (!gf) { console.log("GRAND FINAL FAILED"); return; }
    save(`${DIR}/arena_grand_final.json`, gf);
  }
  const champ = gf.order[0].cand;
  console.log(`\n*** ROUND-4 ARENA CHAMPION: ${champ.id} — ${champ.title} ***`);

  // ---- Council of 5 over final 4 ----
  const final4 = adv4;
  let council = j(`${DIR}/council_board.json`);
  if (!council) {
    const personas = [
      "a skeptical Meta research scientist who has seen 10,000 demos fail",
      "a hackathon judge optimizing for the Demo 25% rubric slot",
      "an infrastructure engineer at Modal who costs out GPU-minutes",
      "the target user (a busy practitioner in the idea's domain)",
      "a VC who funds AI tools and hates toys"];
    council = [];
    for (let p = 0; p < personas.length; p++) {
      const listing = final4.map((x, i) => card(x, i)).join("\n\n");
      const prompt = `You are ${personas[p]}. Rank these 4 ideas for the FINAL. Return STRICT JSON: {"votes":[{"i":0,"pts":5},...4 items, points 5/3/2/1 unique],"one_line":"why <=20 words"}\n\n${listing}`;
      const out = grab(await callZai(prompt, `council_${p}`));
      if (out?.votes?.length) council.push({ persona: personas[p], votes: out.votes, line: out.one_line });
      save(`${DIR}/council_board.json`, council);
      await sleep(3000);
    }
  }
  const tally = {};
  for (const c of council) for (const v of c.votes) {
    const cand = final4[v.i]; if (!cand) continue;
    tally[cand.id] = (tally[cand.id] || 0) + (v.pts || 0);
  }
  console.log("COUNCIL TALLY:", JSON.stringify(tally));
  save(`${DIR}/R4_RESULT.json`, {
    champion: champ, grand_final: gf, council, tally,
    semifinalists: adv4, nuskha_alive: adv4.some(x => x.id === "R3-CHAMP") && champ.id === "R3-CHAMP",
    nuskha_eliminated_at: nuskhaAlive ? null : (r2.some(h => h.order.slice(0, 2).some(o => o.cand.id === "R3-CHAMP")) ? "semi" : "r2")
  });
  console.log("DONE");
})();
