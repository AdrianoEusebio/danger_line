import re
from datetime import datetime
from typing import Dict, Any, Tuple

class MarkdownBuilder:
    """A reusable utility to parse and build Markdown files with YAML frontmatter."""

    @staticmethod
    def build(metadata: Dict[str, Any], content: str) -> str:
        """Generates a markdown string with frontmatter and body."""
        # Calculate density tag based on body content length
        body_len = len(content)
        if body_len < 500:
            density_tag = "contexto/rascunho"
        elif body_len < 2000:
            density_tag = "contexto/medio"
        else:
            density_tag = "contexto/profundo"

        # Update metadata tags
        tags = metadata.get("tags", [])
        if not isinstance(tags, list):
            tags = [tags] if tags else []
        if density_tag not in tags:
            tags = list(tags) + [density_tag]
        metadata["tags"] = tags

        # Ensure project link is in the content
        project = metadata.get("project")
        if project and metadata.get("type") != "ProjectCard":
            legacy_link = f"[[Project Master Card: {project}]]"
            if legacy_link in content:
                content = content.replace(legacy_link, f"[[{project}]]")
            elif f"[[{project}]]" not in content:
                content = content.rstrip() + f"\n\n## 🔗 Relacionado\n- [[{project}]]"

        lines = ["---"]
        for key, value in metadata.items():
            if isinstance(value, list):
                # Format lists as YAML flow style: [a, b, c]
                items = [f'"{v}"' if ',' in str(v) or ' ' in str(v) else str(v) for v in value]
                lines.append(f"{key}: [{', '.join(items)}]")
            else:
                lines.append(f"{key}: {value}")
        if "date" not in metadata:
            lines.append(f"date: {datetime.now().strftime('%Y-%m-%d')}")
        lines.append("---")
        lines.append("")
        lines.append(content.strip())
        return "\n".join(lines)

    @staticmethod
    def parse(content: str) -> Tuple[Dict[str, Any], str]:
        """Parses a markdown string, returning its metadata dict and the body content."""
        metadata = {}
        body = content
        
        # Match frontmatter block: starting and ending with ---
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
        if match:
            frontmatter_text = match.group(1)
            body = match.group(2)
            
            for line in frontmatter_text.splitlines():
                if ":" in line:
                    key, val = line.split(":", 1)
                    key = key.strip()
                    val = val.strip()
                    
                    # Parse flow-style lists: [val1, val2]
                    if val.startswith("[") and val.endswith("]"):
                        items_str = val[1:-1]
                        if items_str:
                            val = [item.strip().strip('"').strip("'") for item in items_str.split(",")]
                        else:
                            val = []
                    metadata[key] = val
                    
        return metadata, body.strip()
