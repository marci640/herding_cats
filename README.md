# Herding Cats - Agile Agentic Data Pipeline Project

## Project Vision

A **Technical PM** orchestrates a data engineering lifecycle using **GitHub Copilot**. The TPM manages sprints by providing specialized context to Copilot, which acts as a Data Architect, dbt Developer, QA Engineer, or DevOps Engineer on demand.

---

## The Structure

* **`CLAUDE.md`**: Project standards (naming, SQL style, testing).
* **`.ai/LEAD_PROMPT.md`**: Orchestration rules and phase sequencing.
* **`.ai/sprint_ledger.json`**: Sprint state machine (single source of truth).
* **`agents/`**: Role-specific worker personas.

---

## Running Sprints

> **Convention:** `ACTIVE_JIRA_ID` in `.env` is the sprint ID, branch name, and Confluence lookup key. A sprint can cover work across multiple Jira issues, and a Jira issue may span multiple sprints.

### Phase 0: Init

`Initialize sprint from .env` → verifies environment, fetches requirements from Confluence, drafts `SPRINT_REQUIREMENTS.md`. Halts for `requirements approved`.

### Phases 1–4: Build

**Phase 1 (Architect)** → `schema.yml` + assumptions → **Phase 1.5 (Assumptions gate)** → halts for `assumptions approved` → **Phase 2 (Transformer)** → SQL from contract → **Phase 3 (Auditor)** → `dbt test` → **Phase 4 (DevOps)** → DAG validation.

### Two Confluence Workflows

Both use pages split into `TEAM INPUT` (human-owned) and `AI OUTPUT` (agent-managed, fully replaced on each pass). Every publish appends a `## Changelog` entry.

**Requirements (Human-Led):** `ready` → `generated` → *(loop)* → `approved`
- Human seeds notes on Confluence → `requirements ready` → AI structures draft → team reviews → loop or `requirements approved`.

**Assumptions (AI-Led):** `generated` → `ready` → *(loop)* → `approved`
- Architect generates assumptions → AI publishes + opens PR → team answers in `TEAM INPUT` → `assumptions ready` → AI regenerates → loop or `assumptions approved` (requires `approved-by-tpm` label).

### Wrap-up

Archives sprint artifacts to `docs/archive/`, promotes permanent rules to `CLAUDE.md`, resets ledger and `SPRINT_REQUIREMENTS.md`.

## Command Cheat Sheet

| Action | Command |
|---|---|
| Initialize sprint | `Read #file:.ai/LEAD_PROMPT.md and CLAUDE.md. Initialize sprint from .env.` |
| Run full sprint | `Read #file:.ai/LEAD_PROMPT.md and CLAUDE.md. Run full sprint.` |
| Requirements updated on Confluence | `requirements ready` |
| Lock requirements | `requirements approved` |
| Assumptions answered on Confluence | `assumptions ready` |
| Lock assumptions | `assumptions approved` |
| Continue after blocker | `continue sprint` |
| Wrap up | `Use #file:.ai/LEAD_PROMPT.md to execute the Sprint Wrap-Up.` |
| Reset | `Use #file:.ai/LEAD_PROMPT.md to execute Sprint Reset Protocol.` |

## Atlassian MCP Setup

1. Generate API token at [id.atlassian.com](https://id.atlassian.com/manage-profile/security/api-tokens).
2. Configure `.vscode/mcp.json`:
   ```json
   "atlassian": {
     "command": "/opt/homebrew/bin/npx",
     "type": "stdio",
     "args": ["-y", "atlassian-mcp@latest"],
     "env": {
       "ATLASSIAN_BASE_URL": "https://your-site.atlassian.net",
       "ATLASSIAN_API_TOKEN": "YOUR_TOKEN",
       "ATLASSIAN_USERNAME": "your-email@example.com"
     }
   }
   ```
   Also set `ACTIVE_JIRA_ID` and `CONFLUENCE_SPACE` in `.env`.
3. Restart VS Code → check OUTPUT panel for "Discovered N tools."

## Troubleshooting

| What | File |
|---|---|
| Current sprint state | `.ai/sprint_ledger.json` |
| Project standards | `CLAUDE.md` |
| Orchestration rules | `.ai/LEAD_PROMPT.md` |
| Agent behavior | `agents/` |
| Session handoff | `.ai/HANDOFF_CONTEXT.md` |
