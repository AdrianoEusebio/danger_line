from src.modules.obsidian.vault_manager import VaultManager
from src.modules.obsidian.markdown_parser import MarkdownBuilder
from src.shared.logger import logger

class KnowledgeEngine:
    """The central orchestrator that manages the KB pipeline."""
    
    def __init__(self):
        self.vault = VaultManager()

    async def capture_pattern(self, name: str, content: str, tags: list = None, project: str = "Global", folder: str = None) -> bool:
        """Saves a technical pattern directly to the vault under the project's folder."""
        try:
            logger.info(f"Saving new pattern: {name} in project: {project}")
            
            metadata = {
                "type": "Pattern",
                "project": project,
                "category": "technical-pattern",
                "tags": ["pattern", project.lower()] + (tags or [])
            }
            body = f"""# 🧠 Pattern: {name}

## Context
Captured logic.

## Implementation Details
{content}
"""
            final_note = MarkdownBuilder.build(metadata, body)
            return self.vault.save_note(project, name, final_note)
            
        except Exception as e:
            logger.error(f"Error saving pattern: {e}")
            return False

    async def register_project(self, name: str, path: str, stack: list, description: str) -> bool:
        """Creates or updates a Project Master Card in the vault, with Stack Affinity cross-linking."""
        try:
            logger.info(f"Registering project master card: {name}")
            
            # Stack similarity cross-linking
            related_projects = []
            stack_lower = {s.lower().strip() for s in stack}
            
            existing_cards = self.vault.list_notes("🗂️ Projects")
            for card_name in existing_cards:
                proj_name = card_name[:-3] if card_name.endswith(".md") else card_name
                if proj_name.lower() == name.lower():
                    continue
                    
                card_content = self.vault.read_note("🗂️ Projects", card_name)
                if card_content:
                    card_meta, card_body = MarkdownBuilder.parse(card_content)
                    card_stack = card_meta.get("stack", [])
                    if isinstance(card_stack, list):
                        card_stack_lower = {s.lower().strip() for s in card_stack}
                        if stack_lower.intersection(card_stack_lower):
                            # Stack match!
                            related_projects.append(proj_name)
                            
                            # Update existing card to link to the new project
                            link_str = f"[[{name}]]"
                            if link_str not in card_body:
                                new_card_body = card_body.rstrip()
                                if "## 🔗 Related Projects" not in new_card_body:
                                    new_card_body += f"\n\n## 🔗 Related Projects\n- {link_str}"
                                else:
                                    new_card_body = new_card_body.replace(
                                        "## 🔗 Related Projects",
                                        f"## 🔗 Related Projects\n- {link_str}"
                                    )
                                updated_note = MarkdownBuilder.build(card_meta, new_card_body)
                                self.vault.save_note("🗂️ Projects", proj_name, updated_note)

            metadata = {
                "type": "ProjectCard",
                "project": name,
                "path": path,
                "stack": stack,
                "status": "active"
            }
            
            body = f"""# 🗂️ Project Master Card: {name}

## 📝 Description
{description}

## 🏗️ Architecture & Stack
- **Primary Stack:** {', '.join(stack)}
- **Path:** `{path}`
"""

            if related_projects:
                body += "\n## 🔗 Related Projects\n"
                for p in related_projects:
                    body += f"- [[{p}]]\n"

            body += f"""
## 🧠 Knowledge Landscape
- [[Patterns - {name}]]
- [[Specs - {name}]]
- [[Bugfixes - {name}]]

> [!TIP]
> Use o plugin Dataview para listar notas automaticamente aqui.
"""
            final_note = MarkdownBuilder.build(metadata, body)
            return self.vault.save_note("🗂️ Projects", name, final_note)
            
        except Exception as e:
            logger.error(f"Error registering project: {e}")
            return False

    async def capture_bugfix(self, error_log: str, solution: str, project: str = "Global") -> bool:
        """Saves a bugfix playbook directly to the vault under the project's folder."""
        try:
            logger.info(f"Saving bugfix for project: {project}")
            
            metadata = {
                "type": "Bugfix",
                "project": project,
                "error_code": error_log[:50] + "...",
                "tags": ["bugfix", project.lower()]
            }
            body = f"""# 🐞 Bugfix Playbook: {error_log[:50]}...

## Problem Analysis
{error_log} detected in {project}.

## 🔧 Solution (Playbook)
{solution}

## Prevention
- [ ] Add check for X
- [ ] Update config Y
"""
            final_note = MarkdownBuilder.build(metadata, body)
            return self.vault.save_note(project, f"fix-{project}", final_note)
            
        except Exception as e:
            logger.error(f"Error saving bugfix: {e}")
            return False

# Singleton
knowledge_engine = KnowledgeEngine()
