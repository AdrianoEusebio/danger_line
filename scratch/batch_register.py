import os
import subprocess
from pathlib import Path

projects_dir = Path(r"c:\Users\adria\OneDrive\Área de Trabalho\PROJETOS")
cli_path = Path(r"c:\Users\adria\OneDrive\Área de Trabalho\PROJETOS\Danger_line\src\main.py")

projects = [p for p in projects_dir.iterdir() if p.is_dir()]

print(f"Found {len(projects)} projects. Starting batch registration...")

for project in projects:
    print(f"\n--- Processing: {project.name} ---")
    try:
        # Usando a venv ou python do sistema conforme configurado
        result = subprocess.run(
            ["python", str(cli_path), "register", str(project.resolve())], 
            capture_output=True, 
            text=True,
            encoding="utf-8"
        )
        if result.returncode == 0:
            print(f"SUCCESS: {project.name} registered.")
        else:
            print(f"ERROR registering {project.name}:")
            print(result.stderr)
            print(result.stdout)
    except Exception as e:
        print(f"CRITICAL ERROR for {project.name}: {e}")

print("\nBatch registration finished.")
