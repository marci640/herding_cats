# 😺 Herding Cats - Agile Agentic Data Pipeline Project

## Project Vision

This project demonstrates how a **Technical PM** orchestrates a complex data engineering lifecycle using **GitHub Copilot**. Instead of writing line-by-line code, the TPM manages a "Sprint" by providing specialized context to Copilot, ensuring it acts as a Data Architect, dbt Developer, or QA Engineer on demand.

---

## The Structure

The project is designed to be **"Copilot-Native."** It uses hidden and specialized folders to feed Copilot the exact context it needs for each phase.

* **`.ai/LEAD_PROMPT.md`**: The master instructions for the Copilot chat session.
* **`agents/`**: Role-specific instructions you "attach" to your Copilot Chat.
* **`CLAUDE.md`**: Copilot naturally reads this to understand your coding standards (Naming conventions, SQL style, etc.).

---

## Running Sprints (Detailed Workflow)

### 1) Prepare the sprint contract

> **Convention: 1 Sprint = 1 Epic.** In agentic workflows, AI agents compress development velocity enough that a full Epic (e.g., a complete feature or pipeline) can ship in a single sprint timebox. This project enforces a 1:1 mapping: the **Jira Epic ID** (`SCRUM-N`) is the **branch name**, the **sprint ID**, and the **ledger key**. Sub-tasks live under the epic in Jira but the sprint identity is always the epic.

Before chat execution, fill `.ai/SPRINT_REQUIREMENTS.md` completely:
- business rules
- transformation logic
- model/source changes
- execution prerequisites
- acceptance criteria

Keep `CLAUDE.md` in repo root so Copilot applies project standards automatically.

### 2) Initialize sprint state (Phase 0 gate)

Run initialization once per sprint. This syncs requirements into the ledger and verifies environment readiness before any implementation begins.

Expected outcomes:
1. `active_sprint` is written in `.ai/sprint_ledger.json`
2. environment checks run (Python/dbt/adapter/dependencies)
3. status moves to active execution state

### 3) Execute Architect → HITL → Transformer → Auditor → DevOps

The orchestrator enforces sequencing and quality gates:
- Architect writes/updates technical contract (`schema.yml`)
- Assumptions gate opens PR when assumptions exist
- Transformer implements SQL from contract
- Auditor validates compile + tests
- DevOps validates DAG syntax and coverage

Important gate behavior:
- If assumptions require TPM review, they are published to **Confluence** (`sprints/SCRUM-N/assumptions`) as the canonical review surface. Non-technical stakeholders can edit there.
- The GitHub PR links to the Confluence page and carries the approval signal (`approved-by-tpm` label).
- Resume only after `approved-by-tpm` label is present on the PR.
- On resume, the agent fetches the latest assumptions from Confluence (not the PR body) and syncs locally before continuing.
- Original sprint requirements remain the business source of intent; Architect and Auditor validate alignment against them.
- Transformer should remain contract-only (`schema.yml` + approved assumptions) to prevent interpretation drift.
- Upstream readiness issues must be resolved before full `dbt run`/`dbt test`

### 4) Continue after pause

Use `continue` (or `continue sprint`) after you apply TPM label or fix blockers. The lead prompt re-checks gate conditions and proceeds from the correct phase.

**Mid-sprint re-entry:** If a blocker is resolved or requirements change on Confluence during HITL, use the dedicated re-entry prompts (see Command Cheat Sheet) to re-run the Architect with fresh discovery.

### 5) Wrap up before merge

Wrap-up archives sprint artifacts, promotes permanent rules, updates ledger history, and resets `.ai/SPRINT_REQUIREMENTS.md` for the next sprint.

Outputs include:
- `docs/archive/sprint_[N]/sprint_[N]_requirements.md`
- `docs/archive/sprint_[N]/sprint_[N]_summary.md`
- `active_sprint: null` in ledger

## Advanced: Individual Phase Execution

For debugging or running a single phase in isolation:

| Action | Command |
|---|---|
| Run Architect only | `run #file:agents/01_architect.md` |
| Run Transformer only | `run #file:agents/02_transformer.md` |
| Run Auditor only | `audit via #file:agents/03_auditor.md` |
| Run DevOps (env/DAG) | `execute #file:agents/04_devops.md` |

## Command Cheat Sheet

| Action | Command |
|---|---|
| Draft requirements from Jira + Confluence | *"Read the current branch name, fetch the matching Jira epic, and read the `requirements` page from `sprints/SCRUM-N/` in Confluence. Draft `.ai/SPRINT_REQUIREMENTS.md` from both."* |
| Initialize sprint | `Read #file:.ai/LEAD_PROMPT.md and CLAUDE.md. Initialize sprint from .ai/SPRINT_REQUIREMENTS.md.` |
| Run full sprint | `Read #file:.ai/LEAD_PROMPT.md and CLAUDE.md. Run full sprint.` |
| Continue after HITL/blocker | `continue sprint` |
| Blocker resolved (re-run Architect) | *"Blocker resolved. Re-run Phase 1 from discovery."* |
| Requirements revised on Confluence | *"Requirements updated. Re-run from Phase 1."* |
| Wrap up sprint | `Use #file:.ai/LEAD_PROMPT.md to execute the Sprint Wrap-Up.` |
| Reset current sprint | `Use #file:.ai/LEAD_PROMPT.md to execute Sprint Reset Protocol.` |

## New Session Handoff

All durable context — lessons, bootstrap prompt, and template state — lives in `.ai/HANDOFF_CONTEXT.md`.

## Atlassian MCP Integration

This project leverages the **Model Context Protocol (MCP)** to bridge GitHub Copilot with Jira and Confluence. This allows for seamless technical project management and automated documentation directly within the IDE.

### Key Capabilities

| Feature | For Data Engineers (Technical) | For TPMs (Orchestration) |
|---|---|---|
| **Jira (Read/Write)** | Fetch requirements for new resources or dbt models directly from tickets. | Create "Technical Debt" tickets when Copilot identifies code smells during refactors. |
| **Confluence (Read)** | Reference ADRs to ensure data pipelines follow established team standards. | Audit repositories against Project Specs on Confluence to identify missing features. |
| **Confluence (Write)** | Automatically generate "Deployment Guides" based on the `README.md` and code changes. | Update "Sprint Progress" pages with summaries of daily code commits. |

### Setup Instructions

1. **Generate API Token:** Create a Personal Access Token at [id.atlassian.com](https://id.atlassian.com/manage-profile/security/api-tokens).
2. **Configure MCP Server:** Add the Atlassian server to `.vscode/mcp.json`:
   ```json
   "atlassian": {
     "command": "/opt/homebrew/bin/npx",
     "type": "stdio",
     "args": ["atlassian-mcp@latest"],
     "env": {
       "PATH": "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin",
       "ATLASSIAN_BASE_URL": "https://your-site.atlassian.net",
       "ATLASSIAN_API_TOKEN": "YOUR_TOKEN",
       "ATLASSIAN_USERNAME": "your-email@example.com"
     }
   }
   ```
3. **Verify Connection:** Restart VS Code, then check the OUTPUT panel (dropdown: "MCP: atlassian") for "Discovered N tools."

### Ad-Hoc Prompts

These are contextual — use when the situation calls for it, not every sprint.

| Use Case | Prompt |
|---|---|
| **HITL reconciliation** | *"Search Confluence for today's meeting notes and reconcile any decisions against `.ai/ACTIVE_ASSUMPTIONS.md`."* |
| **Status sync to Jira** | *"Read `.ai/sprint_ledger.json` and update Jira task SCRUM-1 with current phase, blockers, and status."* |

## Troubleshooting: Where to Look

| What | File |
|---|---|
| Current sprint state | `.ai/sprint_ledger.json` |
| Project standards | `CLAUDE.md` |
| Workflow & orchestration rules | `.ai/LEAD_PROMPT.md` |
| Agent behavior | `agents/` |

> **TPM Tip:** If Copilot drifts on SQL behavior, say: *"Use CLAUDE.md as source of truth."*
