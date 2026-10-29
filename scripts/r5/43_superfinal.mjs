// ROUND-5 SUPERFINAL: Nuskha (R3/R5 council champion) vs Thikana (R4 bracket champion).
// Full official rulebook context (Participant Guide pasted by user, Oct 28).
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import fs from "node:fs";
const run = promisify(execFile);
const DIR = "/home/z/my-project/hackathon-repo/ideation/round5";
const sleep = ms => new Promise(r => setTimeout(r, ms));
const j = p => { try { return JSON.parse(fs.readFileSync(p, "utf8")); } catch { return null; } };
const save = (p, o) => fs.writeFileSync(p, JSON.stringify(o, null, 1));

const SYSTEM = `You are the FINAL judging panel chair of the Meta Global AI Developer Hackathon 2026. Official rubric (0-10 each): Impact 30% (real-world potential, who benefits, fits a problem statement) | Use of Meta AI Tooling 25% (creative, beyond basic integration, surprising capabilities) | Technical Depth & Execution 20% (sound engineering, real craft) | Demo 25% (working, impressive, holds up live, genuinely cool video). Stage-1 pass/fail: must reasonably fit a theme (Build for Your World / Push the Frontier) AND reasonably use Meta Model API and/or open-weight models.
ANTI-PROJECTS (auto-fail): generic ideas seen across hackathons — AI medical advice, basic RAG, simple image analyzers, AI-for-education chatbots, job screeners, nutrition coaches, personality analyzers, sports analyzers, political/war content. Rules: public repo, new work only, demo must highlight what was built during the event.
Bonus prizes exist: Most Viral ($20K), Best Build on Open Weights ($10K), Community Vote ($10K), Best Agentic Use-Case ($5K), Best Creative Build ($5K).
Solo builder, 7 days left, $150 Meta API + $100 Modal + $100 Baseten credits. Judge like a skeptical senior Meta engineer: no hidden human labor, no legality gray zones, no demo fragility. Reward: named user + concrete artifact + visible wow + honest scope + novel architecture that is load-bearing.`;

const NUSKHA = {
  id: "NUSKHA", rounds: "R3 champion (beat Ustad among 10,568) | R5: survived hardest heat, council 25/30 UNANIMOUS #1 vs 20,000 fresh architecture-first challengers",
  title: "Nuskha — every methods section, runnable",
  pitch: `Turns a research paper's methods section into a runnable recipe (env, data, seeds, commands, expected outputs); flags every missing/ambiguous step ("seed unstated; split unspecified — Fig. 3 irreproducible as written"); executes step-by-step in Modal sandboxes behind a gated role-expert bench (Mixture of Role-based Experts: Ingestion -> Auditor -> Executor -> Reconciler; Glimmer gates escalate to Spark); reconciles reproduced figures with a NUMERIC mask-geometry score + three-ladder consistency (line/step/paper); risky verdicts signed by 2-of-3 verifier quorum with evidence pointers; deterministic replay; output = one-page quorum-signed Reproduction Receipt (verified/mismatch/not-runnable per claim). Graceful dry-run fallback = demo cannot die.
Users: grad students (70% of researchers have failed to reproduce an experiment — Nature survey), research-engineering freelancers invoicing against receipts, journal clubs, OSS maintainers.
Stack: Wonder 1M-ctx whole-paper read (cost-aware router: Spark-first, Wonder on uncertainty), Spark+vision reconciliation, Glimmer self-hosted gates on Modal (Best Open Weights eligible), Spark Open on Baseten as LoRA-tuned recipe grader (Best Agentic eligible), Image for receipt callouts. Theme: Push the Frontier (1M-ctx + computer use + sandboxes are load-bearing).
Originality sweep: GitHub+HF search found no clone (AI Scientist=auto-research, PaperBench=eval, neither verifies one paper's methods for a human before they sink a week).`,
};
const THIKANA = {
  id: "THIKANA", rounds: "R4 champion (bracket 64->1, 87.1 final) + council 4/5 first votes vs 20,000 challengers",
  title: "Thikana — the physical world, addressable (solar fleet memory)",
  pitch: `Turns routine site photos into a living, region-addressed memory of a solar rooftop fleet: SAM 3.1 segments every panel, rail, cable run and inverter into queryable visual addresses ("what changed in region 3 since the last monsoon?"); a hierarchical role-crew of agents closes the whole loop — commissioning checklist -> fault ticket -> field fix -> re-verification of the same region — and every verdict ships with receipts (masks, timestamps, prior evidence, confidence). Retrieval walks a geometry-aware mask-manifold embedding (masks as priors, geodesic-style ranking) — segment-as-index architecture.
Users: EPC O&M engineers (5-200 sites, 300 photos/visit, no comparison baseline), fleet owners ("is site 12 getting worse or is it the monsoon?"), field technicians (voice-first briefing, fixes re-verified), inspectors/lenders (exportable dossier, every claim carries mask+timestamp).
Context: Bangladesh rooftop-solar boom under net-metering; commissioning photo documentation required; O&M is a decade-long obligation with no photo-first tooling; existing tools are one-shot defect classifiers or heavyweight enterprise suites.
Stack: SAM 3.1 (segmentation core), Spark (change reasoning, voice briefing), Voice Transcribe (hands-busy field), Glimmer edge triage, Spark Open on Baseten, Image for briefs. Theme: Push the Frontier ("understand and control a physical system" verbatim). Originality sweep: 146/150 arena-eligible original, 0 collisions.`,
};

async function callZai(user, tag, retries = 5) {
  for (let i = 1; i <= retries; i++) {
    const tmp = `/tmp/zai_sf_${tag.replace(/\W/g, "_")}.json`;
    try {
      await run("/usr/local/bin/z-ai", ["chat", "-p", user, "-s", SYSTEM, "-o", tmp], { timeout: 420000 });
      const d = JSON.parse(fs.readFileSync(tmp, "utf8"));
      fs.rmSync(tmp, { force: true });
      return d?.choices?.[0]?.message?.content ?? "";
    } catch (e) {
      console.log(`  retry ${i} [${tag}]: ${String(e.message || e).slice(0, 80)}`);
      fs.rmSync(tmp, { force: true });
      await sleep(14000 * i);
    }
  }
  return "";
}
const grab = (t) => { if (!t) return null;
  let s = t.trim().replace(/^```(json)?/i, "").replace(/```$/g, "").trim();
  const a = s.indexOf("{"), b = s.lastIndexOf("}");
  if (a === -1 || b <= a) return null;
  try { return JSON.parse(s.slice(a, b + 1)); } catch { return null; } };

(async () => {
  const card = x => `### ${x.id} — ${x.title}\nProvenance: ${x.rounds}\n${x.pitch}`;
  let sf = j(`${DIR}/superfinal.json`);
  if (!sf) {
    const prompt = `SUPERFINAL — the two multi-round champions of a 30,568-idea battle meet. Pick the ONE project to build for the $1M hackathon.\n\n${card(NUSKHA)}\n\n${card(THIKANA)}\n\nScore BOTH on the four rubric axes (impact/meta/tech/demo, 0-10). Consider: which survives a LIVE 90-second demo better; which has the stronger "Use of Meta AI Tooling" story; which is more clearly NEW vs the anti-project list; which fits Push the Frontier / Build for Your World better; demo-video virality; solo-buildability in 7 days.\nReturn STRICT JSON: {"nuskha":{"impact":0,"meta":0,"tech":0,"demo":0,"total":0},"thikana":{...same...},"winner":"nuskha|thikana","margin":"<=15 words","why":"<=40 words","virality_pick":"...","risk_note":"<=25 words"}`;
    let out = grab(await callZai(prompt, "head"));
    if (!out) { await sleep(8000); out = grab(await callZai(prompt + "\nJSON only.", "head2")); }
    sf = { head: out || "FAILED" };
    save(`${DIR}/superfinal.json`, sf);
  }
  console.log("HEAD-TO-HEAD:", JSON.stringify(sf.head));
  // 3-persona mini council for depth
  const personas = [
    "a Meta research scientist who values technical depth and honest scope",
    "a hackathon judge who has watched 500 demo videos die live",
    "the Meta API product manager who wants capabilities that surprise even the model team"];
  sf.council = sf.council || [];
  for (let p = sf.council.length; p < personas.length; p++) {
    const prompt = `You are ${personas[p]}. Two champions meet; rank them for the FINAL build decision and score 0-10 on impact, meta-tooling creativity, technical depth, live-demo survival.\n\n### NUSKHA — ${NUSKHA.title}\n${NUSKHA.pitch}\n\n### THIKANA — ${THIKANA.title}\n${THIKANA.pitch}\n\nReturn STRICT JSON: {"scores":{"nuskha":{"impact":0,"meta":0,"tech":0,"demo":0,"total":0},"thikana":{...}},"winner":"nuskha|thikana","one_line":"<=20 words"}`;
    const out = grab(await callZai(prompt, `c_${p}`));
    if (out) { sf.council.push({ persona: personas[p], verdict: out }); save(`${DIR}/superfinal.json`, sf); }
    await sleep(3000);
  }
  const tally = { nuskha: 0, thikana: 0 };
  if (sf.head?.winner) tally[sf.head.winner]++;
  for (const c of sf.council) if (c.verdict?.winner) tally[c.verdict.winner]++;
  sf.tally = tally;
  save(`${DIR}/superfinal.json`, sf);
  console.log("SUPERFINAL TALLY:", JSON.stringify(tally));
})();
