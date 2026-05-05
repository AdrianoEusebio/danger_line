"""
ObsidianIntegration — Sincronização com o vault do Obsidian.

Obsidian é a IDE de visualização do Knowledge Base.
O wiki compilado fica no vault, o raw/ fica no projeto.

TDD: TDD-06-STORAGE-CACHE.MD
"""
from __future__ import annotations

import shutil
from pathlib import Path


class ObsidianIntegration:
    """Sincroniza wiki compilado com o vault do Obsidian."""

    def __init__(self, vault_path: str | Path):
        self.vault_path = Path(vault_path)
        if not self.vault_path.exists():
            raise FileNotFoundError(
                f"ERROR: Obsidian vault not found at '{vault_path}'. "
                f"Please ensure Obsidian is installed and the vault path is correct "
                f"in your .env file (OBSIDIAN_VAULT_PATH)."
            )
        self.projects_folder = self.vault_path / "projects"
        self.global_folder = self.vault_path / "global"

        # Garantir estrutura base
        self._init_vault_structure()

    def _init_vault_structure(self) -> None:
        """Inicializa estrutura mínima do vault se não existir."""
        (self.projects_folder).mkdir(exist_ok=True)
        (self.global_folder / "patterns").mkdir(parents=True, exist_ok=True)
        (self.global_folder / "lessons").mkdir(parents=True, exist_ok=True)

        global_index = self.global_folder / "index.md"
        if not global_index.exists():
            global_index.write_text(
                "# Global Knowledge Base\n\n"
                "Cross-project patterns and lessons learned.\n\n"
                "## Patterns\n\n## Lessons\n",
                encoding="utf-8",
            )

    def save_project_card(self, project_name: str, card_content: str) -> Path:
        """Salva Project Card no vault."""
        project_folder = self.projects_folder / project_name
        project_folder.mkdir(exist_ok=True)

        card_path = project_folder / f"{project_name}.md"
        card_path.write_text(card_content, encoding="utf-8")
        return card_path

    def sync_wiki_to_vault(self, project_name: str, wiki_source: Path) -> int:
        """
        Sincroniza wiki compilado do projeto para o vault.
        Retorna número de arquivos sincronizados.
        """
        dest = self.projects_folder / project_name / "wiki"
        dest.mkdir(parents=True, exist_ok=True)

        count = 0
        for file in wiki_source.rglob("*.md"):
            relative = file.relative_to(wiki_source)
            target = dest / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, target)
            count += 1

        return count

    def get_project_card(self, project_name: str) -> str | None:
        """Retorna conteúdo do Project Card existente, ou None se não existir."""
        card_path = self.projects_folder / project_name / f"{project_name}.md"
        if card_path.exists():
            return card_path.read_text(encoding="utf-8")
        return None

    def get_wiki_articles(self, project_name: str) -> dict[str, str]:
        """Retorna todos os artigos do wiki como {nome: conteúdo}."""
        wiki_path = self.projects_folder / project_name / "wiki"
        if not wiki_path.exists():
            return {}

        articles = {}
        for file in wiki_path.rglob("*.md"):
            articles[file.stem] = file.read_text(encoding="utf-8")
        return articles
