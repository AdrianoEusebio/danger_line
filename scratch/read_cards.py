import os
import sys
import io
from pathlib import Path

# Force UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

vault_projects = Path(r"C:\Users\adria\OneDrive\Documentos\Danger_line\Danger Line\projects")

for project_dir in vault_projects.iterdir():
    if project_dir.is_dir():
        card_path = project_dir / f"{project_dir.name}.md"
        if card_path.exists():
            print(f"=== PROJECT: {project_dir.name} ===")
            print(card_path.read_text(encoding="utf-8"))
            print("\n" + "="*40 + "\n")
