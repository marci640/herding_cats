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
- If assumptions require TPM review, execution pauses at `HITL_PENDING`
- Resume only after `approved-by-tpm` label is present
- On resume, latest `.ai/ACTIVE_ASSUMPTIONS.md` from the remote branch is synced locally before Transformer continues
- Original sprint requirements remain the business source of intent; Architect and Auditor validate alignment against them.
- Transformer should remain contract-only (`schema.yml` + approved assumptions) to prevent interpretation drift.
- Upstream readiness issues must be resolved before full `dbt run`/`dbt test`

### 4) Continue after pause

Use `continue` (or `continue sprint`) after you apply TPM label or fix blockers. The lead prompt re-checks gate conditions and proceeds from the correct phase.

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
| Run DevOps only | `execute #file:agents/04_devops.md` |

## Command Cheat Sheet

| Action | Command |
|---|---|
| Initialize sprint | `Read #file:.ai/LEAD_PROMPT.md and CLAUDE.md. Initialize sprint from .ai/SPRINT_REQUIREMENTS.md.` |
| Run full sprint | `Read #file:.ai/LEAD_PROMPT.md and CLAUDE.md. Run full sprint.` |
| Continue after HITL/blocker | `continue sprint` |
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

### Example Prompts

- *"Read Jira ticket SCRUM-1 and generate sprint requirements for `.ai/SPRINT_REQUIREMENTS.md`."*
- *"Search Confluence for today's meeting notes and validate them against the current sprint requirements."*
- *"Update Jira task SCRUM-1 with current sprint progress, blockers, and status."*
- *"Publish the sprint wrap-up outputs (requirements and summary) to the `sprint_docs` folder in Confluence."*

## Troubleshooting: Where to Look

| What | File |
|---|---|
| Current sprint state | `.ai/sprint_ledger.json` |
| Project standards | `CLAUDE.md` |
| Workflow & orchestration rules | `.ai/LEAD_PROMPT.md` |
| Agent behavior | `agents/` |

> **TPM Tip:** If Copilot drifts on SQL behavior, say: *"Use CLAUDE.md as source of truth."*
