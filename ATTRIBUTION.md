# Attribution & Licenses

Every bundled skill is open source. This pack only re-organizes them; all credit and
upstream development belongs to the original authors. Licenses: MIT unless noted.

## Bundled from your uploads

| Skill(s) | Source repository | Author |
|---|---|---|
| arena | github.com/[arena-skill] (uploaded as `arena-skill-main.zip`) | arena-skill |
| taste-skill | github.com/Leonxlnx/taste-skill | Leonxlnx |
| ponytail, ponytail-review, ponytail-audit | github.com/DietrichGebert/ponytail | DietrichGebert |
| diagram-design | github.com/cathrynlavery/diagram-design | cathrynlavery |
| idea-refine, interview-me, spec-driven-development, planning-and-task-breakdown, constraint-driven-development, context-engineering, incremental-implementation, test-driven-development, api-and-interface-design, source-driven-development, debugging-and-error-recovery, performance-optimization, security-and-hardening, frontend-ui-engineering, browser-testing-with-devtools, code-review-and-quality, doubt-driven-development, shipping-and-launch | github.com/addyosmani/agent-skills | Addy Osmani |
| docx, pdf, pptx, xlsx, theme-factory, canvas-design, image-enhancer, webapp-testing, skill-creator, mcp-builder, changelog-generator | via github.com/ComposioHQ/awesome-claude-skills; docx/pdf/pptx/xlsx/theme-factory/canvas-design/mcp-builder/skill-creator originate from github.com/anthropics/skills | ComposioHQ / Anthropic |

## Researched but not bundled (see INSTALL-MORE.md)

| Repository | What it is | Why not bundled |
|---|---|---|
| github.com/anthropics/skills | Official Anthropic skill catalog + plugin marketplace | Core skills already included via awesome-claude-skills; install as marketplace for updates |
| github.com/paperclipai/paperclip | Platform for managing teams of AI agents (Skill Studio, evals, versioning) | It's a runtime platform, not a copyable skill folder |
| github.com/nexu-io/open-design | Collaborative AI design agent workspace, 100+ design skills, 151 design systems | Desktop app / MCP install, not plain skill folders |
| github.com/tt-a1i/archify | Interactive HTML diagram generator (architecture, workflow, sequence, ERD...) | One-command install; grab it, it complements diagram-design |
| github.com/K-Dense-AI/scientific-agent-skills | 177 validated science skills + 100+ scientific databases (bio, chem, medicine, materials) | 177 skills would dwarf this pack; install selectively per project domain |
| github.com/morluto/rea (uploaded `rea-main.zip`) | "Reverse Engineer Anything" MCP — binaries, Electron, .NET, runtime | 6,400+ file Node platform installed via `npx rea-agents setup`; only relevant for RE/security projects |

## Additional high-quality collections found during research

| Repository | What it is |
|---|---|
| github.com/obra/superpowers | Jesse Vincent's full dev methodology (285K+ stars): brainstorming, writing-plans, systematic-debugging, verification-before-completion |
| github.com/mattpocock/skills | Matt Pocock's "Skills for Real Engineers": grill-me, to-spec, to-tickets, tdd, diagnosing-bugs, domain-modeling |
| github.com/vercel-labs/agent-skills | Deploy-to-Vercel + agent-browser + web-design-guidelines + react-best-practices |
| github.com/VoltAgent/awesome-agent-skills | Curated index of 1,000+ skills — the discovery layer for anything else you need |
| www.skills.sh | The open skills ecosystem/registry (`npx skills add owner/repo`) |

## Custom content

`skills/00-hackathon-rubric/` was authored for this pack from the official hackathon
page, Meta developer docs (dev.meta.ai), Meta Connect 2026 recap, and press coverage.
Facts (pricing, models, dates) verified Oct 27, 2026; re-check the Official Rules page
for submission requirements before final submission.
