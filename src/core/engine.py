from src.modules.obsidian.vault_manager import VaultManager
from src.modules.obsidian.markdown_parser import MarkdownBuilder
from src.shared.logger import logger

class KnowledgeEngine:
    """The central orchestrator that manages the KB pipeline."""
    
    def __init__(self):
        self.vault = VaultManager()

    async def capture_pattern(self, name: str, content: str, tags: list = None, project: str = "Global", folder: str = "🧩 Padrões") -> bool:
        """Saves a technical pattern directly to the vault."""
        try:
            logger.info(f"Saving new pattern: {name}")
            
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

## 🔗 Related
- [[Project Master Card: {project}]]
"""
            final_note = MarkdownBuilder.build(metadata, body)
            return self.vault.save_note(folder, name, final_note)
            
        except Exception as e:
            logger.error(f"Error saving pattern: {e}")
            return False

    async def register_project(self, name: str, path: str, stack: list, description: str) -> bool:
        """Creates or updates a Project Master Card in the vault."""
        try:
            logger.info(f"Registering project master card: {name}")
            
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
        """Saves a bugfix playbook directly to the vault."""
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
            return self.vault.save_note("🐞 BugTracker", f"fix-{project}", final_note)
            
        except Exception as e:
            logger.error(f"Error saving bugfix: {e}")
            return False

# Singleton
knowledge_engine = KnowledgeEngine()
