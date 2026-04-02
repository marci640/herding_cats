# Handoff Context

## Purpose
This repository is a reusable **Copilot-first ETL platform template** built from the operating patterns proven in the `coding_cats` project.

## What a New Session Should Assume
- This repo is a **template**, not an active business implementation.
- Keep the orchestration model intact: **Architect → HITL → Transformer → Auditor → DevOps**.
- Keep the existing governance intact unless the user explicitly changes it:
  - DuckDB remains the default local database.
  - dbt remains the transformation framework.
  - Airflow remains the orchestration target.
  - `snake_case` naming, PK tests, and `processed_at` timestamp standards remain in force.
- Treat repo files as the source of truth; do **not** rely on prior chat memory.

## Durable Lessons Carried Forward
- Requirements are the **business source of intent**.
- `schema.yml` + approved assumptions are the **implementation contract**.
- Transformer should remain **contract-only** and should not interpret raw requirements.
- Assumptions must be concrete and executable:
  1. `Ambiguity/Gap`
  2. `Decision (Proposed Default)`
  3. `Rationale`
  4. `Implementation Impact`
  5. `TPM Action`
- PR links to Confluence `assumptions` page as the canonical review surface (not PR body).
- Use the project virtual environment only: `venv/bin/python`, `venv/bin/pip`, `venv/bin/dbt`.

## Confluence Integration
- **Page structure per sprint:** `sprints/SCRUM-N/` with two pages:
  - `requirements` — authored and edited by TPM/stakeholders only
  - `assumptions` — initial draft by agent, edited by both agent and stakeholders
- **Version tracking:** When Confluence content is read into the process, the consuming file (`SPRINT_REQUIREMENTS.md` or `ACTIVE_ASSUMPTIONS.md`) includes a `Confluence Source: <page_title> v<N> — <URL>` header line.
- **Publishing:** All Confluence writes go through Devin (04_devops.md Mode 3). If MCP is unavailable, the sprint continues — publishing is non-blocking.

## What Was Intentionally Removed in This Template
- Business/domain-specific SQL models
- Seed data and source-specific attachments
- Source contracts such as `models/sources.yml`
- Historical sprint archives and sprint-specific checkpoint artifacts
- Business-specific scoring logic, enums, thresholds, and mappings

## What Must Be Supplied Per New Project or Sprint
- Sprint requirements in `.ai/SPRINT_REQUIREMENTS.md`
- Real staging/intermediate SQL models
- Real schema contracts in `dbt_project/models/**/schema.yml`
- Any source/seed definitions required by the implementation
- Any project-specific DAG refinements beyond the generic seed/run/test skeleton

## Recommended Read Order for Fresh Sessions
1. `CLAUDE.md`
2. `.ai/LEAD_PROMPT.md`
3. `.ai/HANDOFF_CONTEXT.md`
4. `.ai/sprint_ledger.json`
5. `.ai/SPRINT_REQUIREMENTS.md`
6. `agents/` (all agent files)

## New Session Bootstrap
Copy/paste this into a fresh Copilot session:

```
Read CLAUDE.md, .ai/LEAD_PROMPT.md, .ai/HANDOFF_CONTEXT.md, .ai/sprint_ledger.json, .ai/SPRINT_REQUIREMENTS.md, and all files in agents/. Then:
1. Summarize the current project state.
2. Identify whether a sprint is active.
3. List any blockers or missing inputs.
4. Recommend the exact next command or next sprint action.

If a sprint is active, continue from the ledger state. If no sprint is active, stay in template mode and wait for sprint requirements.
```

## Environment
- Python 3.11, dbt-core 1.11.7, dbt-duckdb 1.10.1, DuckDB 1.4.4
- MSSQL community extension works on DuckDB 1.4.4 (cached at `~/.duckdb/extensions/v1.4.4/osx_arm64/`)
- MSSQL connection via on-run-start hooks in `dbt_project.yml`
- Atlassian MCP configured in `.vscode/mcp.json` (14 tools)

## Recent Process Changes (This Session)
- **LEAD_PROMPT.md** consolidated from 217→167 lines across multiple passes
- **Confluence version tracking:** Provenance lives in consuming files (header line), not in the ledger
- **Devin Mode 3** simplified to single `publish` action (~15 lines, down from ~40)
- **Removed:** `requirements` page (unnecessary — assumptions already surface misinterpretation)
- **Removed:** `add-info-bar` and `update` Confluence actions (dead code)
- **Simplified prompts:** Blocker + requirements-revised prompts no longer require IDs (agent derives from context)
- **Assumptions Format Consistency:** Enforced the full 5-item format (including `Ambiguity/Gap`) across `01_architect.md` and `LEAD_PROMPT.md` to prevent generation gaps.
- **Resolved Assumptions Formatting:** Added a strict rule to `01_architect.md` to ensure carried-forward/resolved assumptions retain their exact original 5-item structure (only updating the `TPM Action` field), rather than summarizing into an "Original Issue / Resolution" format.
