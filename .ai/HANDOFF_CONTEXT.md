# Handoff Context

## Purpose
Copilot-first ETL platform template using dbt + DuckDB + Airflow orchestrated by a Technical PM through specialized agent personas.

## How It Works

### Sprint Lifecycle
Phases: **0 (Init) → 1 (Architect) → 1.5 (Assumptions) → 2 (Transformer) → 3 (Auditor) → 4 (DevOps) → Wrap-up**

- `ACTIVE_JIRA_ID` in `.env` is the sprint ID and branch name. A sprint can cover multiple Jira issues; a Jira issue can span multiple sprints.
- Phase 0 verifies the environment and initializes the sprint safely. Requirements work begins only after the TPM explicitly says `requirements ready`.
- Two HITL gates use Confluence as the collaboration surface:
  - **Requirements** (Human-Led): `ready` → `generated` → loop → `approved`
  - **Assumptions** (AI-Led): `generated` → `ready` → loop → `approved`
- Four state commands: `requirements ready`, `requirements approved`, `assumptions ready`, `assumptions approved`.
- Ledger tracks `requirements_state` and `assumptions_state` (`null` → `generated` → `approved`).
- Git checkpoints are allowed only after explicit TPM approval commands.
- For in-progress assumptions, Confluence and the linked PR are the review source of truth until approval.

### Confluence Model
- Pages split into `TEAM INPUT` (human-owned, never overwritten) and `AI OUTPUT` (fully replaced on each `generated` pass).
- Discovery: search `CONFLUENCE_SPACE` (from `.env`) by page type + `ACTIVE_JIRA_ID`.
- Every publish appends a `## Changelog` entry via `update-page`.
- Confluence version conflicts should trigger an automatic re-fetch and retry before surfacing an error.
- Publishing is non-blocking — if MCP is unavailable, the sprint continues.

### Key Contracts
- `schema.yml` + approved assumptions = implementation contract.
- Transformer reads only `schema.yml`, never raw requirements.
- Assumptions use 5-item format: `Ambiguity/Gap`, `Decision`, `Rationale`, `Implementation Impact`, `TPM Action`.
- Virtual environment only: `venv/bin/python`, `venv/bin/pip`, `venv/bin/dbt`.

## Environment
- Python 3.11, dbt-core 1.11.7, dbt-duckdb 1.10.1, DuckDB 1.4.4
- MSSQL community extension (cached at `~/.duckdb/extensions/v1.4.4/osx_arm64/`)
- Atlassian MCP in `.vscode/mcp.json` (14 tools, official `atlassian-mcp`)

## Read Order
1. `CLAUDE.md` — project standards
2. `.ai/LEAD_PROMPT.md` — orchestration rules
3. `.ai/sprint_ledger.json` — current state
4. `.ai/SPRINT_REQUIREMENTS.md` — active requirements
5. `agents/` — worker personas

## Bootstrap Prompt
```
Read CLAUDE.md, .ai/LEAD_PROMPT.md, .ai/HANDOFF_CONTEXT.md, .ai/sprint_ledger.json, .ai/SPRINT_REQUIREMENTS.md, and all files in agents/. Then:
1. Summarize the current project state.
2. Identify whether a sprint is active.
3. List any blockers or missing inputs.
4. Recommend the next action.
```
