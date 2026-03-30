# New Session Bootstrap Prompt

Copy/paste this into a fresh Copilot session:

Read `CLAUDE.md`, `.ai/LEAD_PROMPT.md`, `.ai/HANDOFF_CONTEXT.md`, `.ai/sprint_ledger.json`, `.ai/SPRINT_REQUIREMENTS.md`, and all files in `agents/`. Then:
1. Summarize the current project state.
2. Identify whether a sprint is active.
3. List any blockers or missing inputs.
4. Recommend the exact next command or next sprint action.

If a sprint is active, continue from the ledger state. If no sprint is active, stay in template mode and wait for sprint requirements.
