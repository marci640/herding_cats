# TPM Quickstart

## What this repo is
A reusable Copilot-first ETL platform template using:
- dbt for transformations
- DuckDB for local development
- Airflow for orchestration
- Role-based AI workflow: Architect → HITL → Transformer → Auditor → DevOps

## Read these first
1. `CLAUDE.md`
2. `.ai/LEAD_PROMPT.md`
3. `.ai/HANDOFF_CONTEXT.md`
4. `.ai/SPRINT_REQUIREMENTS.md`

## Standard startup command
Use this in a fresh Copilot session:

`Read #file:.ai/LEAD_PROMPT.md and CLAUDE.md. Initialize sprint from .ai/SPRINT_REQUIREMENTS.md.`

## Before starting a sprint
Make sure you have:
- completed `.ai/SPRINT_REQUIREMENTS.md`
- a working virtual environment at `venv/`
- dependencies installed from `requirements.txt`
- any needed seeds/sources defined for the sprint

## Important operating rules
- Requirements = business intent
- `schema.yml` + approved assumptions = implementation contract
- Transformer should not interpret raw requirements
- Use only `venv/bin/python`, `venv/bin/pip`, `venv/bin/dbt`
- If assumptions exist, wait for TPM approval before implementation continues

## Useful commands
- Initialize sprint: `Read #file:.ai/LEAD_PROMPT.md and CLAUDE.md. Initialize sprint from .ai/SPRINT_REQUIREMENTS.md.`
- Run sprint: `Read #file:.ai/LEAD_PROMPT.md and CLAUDE.md. Run full sprint.`
- Continue after HITL: `continue sprint`
- Wrap up: `Use #file:.ai/LEAD_PROMPT.md to execute the Sprint Wrap-Up.`
- Reset sprint: `Use #file:.ai/LEAD_PROMPT.md to execute Sprint Reset Protocol.`

## Where to look when something is wrong
- Current state: `.ai/sprint_ledger.json`
- Project rules: `CLAUDE.md`
- Workflow rules: `.ai/LEAD_PROMPT.md`
- Agent behavior: `agents/`
- New-session bootstrap: `.ai/NEW_SESSION_PROMPT.md`
