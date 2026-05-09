# Danger Line Knowledge Base Rules

The AI MUST follow these rules when working in this workspace:

1. **KB-First Research**: Before proposing a solution to any bug or architectural challenge, the AI MUST use `danger-line.query_kb` to search for existing patterns or playbooks in the Obsidian Knowledge Base.
2. **Proactive Capture**: After any successful implementation of a complex fix or a new design pattern, the AI MUST offer to save this knowledge using `danger-line.commit_knowledge`.
3. **Context Awareness**: The AI SHOULD monitor the current work context (Backend vs Frontend) and suggest using `danger-line.switch_brain` if it detects a mismatch.
4. **Sanitization Compliance**: All data sent to the KB MUST pass through the internal Sanitizer (automatically handled by the MCP tool, but the AI should remain vigilant).
5. **Agnostic Excellence**: The AI should maintain the project's agnostic and modular philosophy, ensuring no project-specific code leaks into the core Danger Line logic.
