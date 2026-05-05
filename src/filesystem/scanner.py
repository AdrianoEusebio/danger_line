"""
Scanner — Exploração de diretórios e identificação de arquivos-chave.

TDD: TDD-11-KB-COMPILER.MD
"""
from __future__ import annotations

import os
from pathlib import Path

class ProjectScanner:
    """Explora o sistema de arquivos para mapear o projeto."""

    IGNORE_DIRS = {
        "node_modules", "venv", ".git", "__pycache__", 
        ".pytest_cache", ".vscode", ".idea", "dist", "build",
        "danger_line"  # Ignorar nossa própria pasta de dados
    }

    def __init__(self, workspace_path: Path):
        self.root = workspace_path

    def get_tree(self, depth: int = 2) -> str:
        """Retorna uma representação em texto da árvore de arquivos."""
        lines = [f"📁 {self.root.name}/"]
        self._build_tree_lines(self.root, 1, depth, lines)
        return "\n".join(lines)

    def _build_tree_lines(self, path: Path, current_depth: int, max_depth: int, lines: list[str]):
        if current_depth > max_depth:
            return

        try:
            items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
            for i, item in enumerate(items):
                if item.name in self.IGNORE_DIRS:
                    continue
                
                is_last = (i == len(items) - 1)
                prefix = "    " * (current_depth - 1) + ("└── " if is_last else "├── ")
                
                icon = "📁" if item.is_dir() else "📄"
                lines.append(f"{prefix}{icon} {item.name}")
                
                if item.is_dir():
                    self._build_tree_lines(item, current_depth + 1, max_depth, lines)
        except PermissionError:
            pass

    def find_key_files(self, count: int = 5) -> list[Path]:
        """Identifica arquivos centrais do projeto (main, index, server, etc)."""
        key_patterns = ["main", "index", "app", "server", "core", "agent", "manage"]
        found = []

        # 1. Buscar na raiz
        for item in self.root.iterdir():
            if item.is_file() and any(p in item.stem.lower() for p in key_patterns):
                found.append(item)

        # 2. Buscar em pastas comuns (src/, lib/, scripts/)
        for sub in ["src", "lib", "scripts", "core"]:
            sub_path = self.root / sub
            if sub_path.exists() and sub_path.is_dir():
                for item in sub_path.iterdir():
                    if item.is_file() and any(p in item.stem.lower() for p in key_patterns):
                        found.append(item)

        # Limitar e retornar
        return found[:count]
