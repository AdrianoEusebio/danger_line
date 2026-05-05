"""
WikiStore — Leitura e escrita do wiki compilado.

O wiki nunca é escrito diretamente pelo usuário —
apenas pelo KB Compiler (src/core/knowledge/compiler.py).

TDD: TDD-11-KB-COMPILER.MD | TDD-12-KB-LINTER.MD
"""
from __future__ import annotations

from pathlib import Path


class WikiStore:
    """Interface de leitura/escrita do wiki compilado."""

    def __init__(self, wiki_path: Path):
        self.wiki_path = wiki_path
        self.wiki_path.mkdir(parents=True, exist_ok=True)

    def get_all_articles(self) -> dict[str, str]:
        """Retorna todos os artigos: {slug: conteúdo}."""
        articles = {}
        for file in self.wiki_path.rglob("*.md"):
            articles[file.stem] = file.read_text(encoding="utf-8")
        return articles

    def get_article(self, slug: str) -> str | None:
        """Retorna conteúdo de um artigo pelo slug, ou None."""
        for file in self.wiki_path.rglob(f"{slug}.md"):
            return file.read_text(encoding="utf-8")
        return None

    def write_article(self, slug: str, content: str, category: str = "") -> Path:
        """Escreve (cria ou atualiza) um artigo no wiki."""
        if category:
            folder = self.wiki_path / category
            folder.mkdir(parents=True, exist_ok=True)
        else:
            folder = self.wiki_path

        article_path = folder / f"{slug}.md"
        article_path.write_text(content, encoding="utf-8")
        return article_path

    def article_exists(self, slug: str) -> bool:
        return any(self.wiki_path.rglob(f"{slug}.md"))

    def count_articles(self) -> int:
        return len(list(self.wiki_path.rglob("*.md")))

    def get_index(self) -> str:
        """Retorna conteúdo do index.md, ou string vazia."""
        index = self.wiki_path / "index.md"
        return index.read_text(encoding="utf-8") if index.exists() else ""

    def write_index(self, content: str) -> None:
        (self.wiki_path / "index.md").write_text(content, encoding="utf-8")

    def snapshot_hashes(self) -> dict[str, str]:
        """Retorna hash de cada arquivo — usado para detectar modificações pelo Linter."""
        import hashlib
        hashes = {}
        for file in self.wiki_path.rglob("*.md"):
            hashes[str(file)] = hashlib.md5(file.read_bytes()).hexdigest()
        return hashes
