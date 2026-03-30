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
- PR body should point reviewers to `.ai/ACTIVE_ASSUMPTIONS.md` as the source of truth rather than duplicating assumptions.
- Use the project virtual environment only: `venv/bin/python`, `venv/bin/pip`, `venv/bin/dbt`.

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
6. `agents/01_architect.md`
7. `agents/02_transformer.md`
8. `agents/03_auditor.md`
9. `agents/04_devops.md`

## Current Template State
- `active_sprint` should remain `null` until a new sprint is started.
- `dbt_project/` is a skeleton only.
- `dags/dbt_pipeline_dag.py` is a generic Airflow/dbt orchestration skeleton.
