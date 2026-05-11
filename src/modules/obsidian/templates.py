from datetime import datetime

class KBTemplate:
    """Standardized templates for KB notes."""
    
    @staticmethod
    def get_frontmatter(metadata: dict) -> str:
        """Generates YAML frontmatter from a dictionary."""
        lines = ["---"]
        for key, value in metadata.items():
            if isinstance(value, list):
                value_str = f"[{', '.join(value)}]"
            else:
                value_str = str(value)
            lines.append(f"{key}: {value_str}")
        lines.append(f"date: {datetime.now().strftime('%Y-%m-%d')}")
        lines.append("---")
        return "\n".join(lines)

    @staticmethod
    def project_master_card(name: str, path: str, stack: list, description: str) -> str:
        metadata = {
            "type": "ProjectCard",
            "project": name,
            "path": path,
            "stack": stack,
            "status": "active"
        }
        frontmatter = KBTemplate.get_frontmatter(metadata)
        body = f"""
# 🗂️ Project Master Card: {name}

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

## 🛠️ Active Contexts
- #backend
- #frontend
"""
        return f"{frontmatter}\n{body}"

    @staticmethod
    def atomic_pattern(name: str, project: str, brain: str, context: str, content: str) -> str:
        metadata = {
            "type": "Pattern",
            "project": project,
            "brain": brain,
            "category": "technical-pattern"
        }
        frontmatter = KBTemplate.get_frontmatter(metadata)
        body = f"""
# 🧠 Pattern: {name}

## Context
{context}

## Implementation Details
{content}

## 🔗 Related
- [[Project Master Card: {project}]]
"""
        return f"{frontmatter}\n{body}"

    @staticmethod
    def bugfix_playbook(error: str, project: str, brain: str, solution: str) -> str:
        metadata = {
            "type": "Bugfix",
            "project": project,
            "brain": brain,
            "error_code": error
        }
        frontmatter = KBTemplate.get_frontmatter(metadata)
        body = f"""
# 🐞 Bugfix Playbook: {error}

## Problem Analysis
{error} detected in {project}.

## 🔧 Solution (Playbook)
{solution}

## Prevention
- [ ] Add check for X
- [ ] Update config Y
"""
        return f"{frontmatter}\n{body}"
