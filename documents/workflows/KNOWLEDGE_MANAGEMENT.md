# Workflow: Knowledge Management (Danger Line)

This workflow ensures the AI correctly utilizes the Obsidian Knowledge Base via MCP.

## Trigger
- When an error is encountered.
- When a new feature or architectural pattern is implemented.
- When the user asks "What do we know about X?".

## Steps

### 1. Research Phase
- **Check KB**: Before suggesting a fix, run `query_kb(query="topic")`.
- **Analyze Context**: Use the returned notes to align the solution with established patterns.

### 2. Implementation Phase
- Apply the solution following the KB's "Specs" or "Playbooks".
- If a conflict arises between current code and KB, flag it to the user.

### 3. Distillation Phase (Post-Fix)
- **Sanitize**: Ensure no secrets are in the solution.
- **Commit**: Run `commit_knowledge(raw_data="solution/logs", name="Title", note_type="Bugfix/Pattern")`.
- **Link**: Mention related notes to create a semantic web in Obsidian.

## Rules
- Always use English for the `raw_data` sent to `commit_knowledge`.
- Always verify the active brain using `get_active_brain` before committing.
