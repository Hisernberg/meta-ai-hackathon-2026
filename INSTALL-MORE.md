# Install More — one-liners for the repos not bundled

Run these from your terminal. `npx skills add owner/repo` works with Claude Code,
Codex, Cursor, Gemini CLI and most hosts (skills.sh ecosystem).

## Directly useful for the hackathon

```bash
# Interactive HTML diagrams (architecture / sequence / ERD as shareable HTML)
npx skills add tt-a1i/archify -g

# Official Anthropic catalog (document-skills, artifacts-builder, brand-guidelines...)
/plugin marketplace add anthropics/skills          # Claude Code
npx skills add anthropics/skills                    # other hosts

# Design direction for app screens + pages (trending alternative to taste-skill)
npx skills add uizze.sh/ui-taste                    # see skills.sh for exact slug

# Vercel deployment + browser automation + UI review guidelines
npx skills add vercel-labs/agent-skills

# Full engineering methodology (brainstorm → plan → TDD → debug → verify)
/plugin install superpowers@claude-plugins-official # Claude Code
npx skills add obra/superpowers-skills              # other hosts

# Matt Pocock's engineer workflow skills (grill-me → to-spec → to-tickets → implement)
npx skills add mattpocock/skills
```

## Pick per project domain (only if your entry needs it)

```bash
# Science-heavy "Push the Frontier" entry (bio/chem/materials/medicine):
npx skills add K-Dense-AI/scientific-agent-skills    # then install ONLY the
                                                     # skills your domain needs
# Security / reverse-engineering entry:
npx rea-agents setup                                 # REA MCP (binaries, Electron, .NET)

# Design workspace with 100+ design skills + design systems (desktop app):
# macOS/Windows: download from https://open-design.ai
# into coding agent:  od mcp install claude
```

## Discovery indexes — when you need a skill that isn't here

- https://skills.sh — open registry + leaderboard (`npx skills add owner/repo`)
- https://github.com/VoltAgent/awesome-agent-skills — 1,000+ curated skills
- https://awesomeskill.ai — searchable marketplace with descriptions
- https://github.com/ComposioHQ/awesome-claude-skills — includes 1,000+ SaaS-automation
  skills via Composio/Rube MCP (Gmail, Slack, Notion, GitHub, Apify...) — useful if
  your project needs to take actions in external services

## Rule of thumb

Install skills **when your agent demonstrably fails at something you repeat** — not
speculatively. A lean pack of 10 skills you actually trigger beats 200 you never do.
