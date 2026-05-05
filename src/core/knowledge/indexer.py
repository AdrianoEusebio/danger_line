"""
Indexer — Auto-linking e summaries para o wiki.

TDD: TDD-11-KB-COMPILER.MD
"""
from __future__ import annotations

import re
from storage.wiki_store import WikiStore


class WikiIndexer:
    """Gera e mantém o index.md + auto-linking entre artigos."""

    def __init__(self, wiki_store: WikiStore):
        self._wiki = wiki_store

    def generate_index(self, articles: dict[str, str]) -> str:
        """Gera o conteúdo do index.md a partir dos artigos existentes."""
        # TODO: Categorizar artigos automaticamente
        lines = ["# Wiki Index\n", f"Total articles: {len(articles)}\n"]
        for slug in sorted(articles.keys()):
            lines.append(f"- [[{slug}]]")
        return "\n".join(lines)

    def extract_potential_links(self, content: str, all_slugs: list[str]) -> list[str]:
        """
        Detecta menções de conceitos no conteúdo que poderiam virar [[wikilinks]].
        Retorna lista de slugs mencionados mas não linkados.
        """
        existing_links = set(re.findall(r"\[\[([^\]]+)\]\]", content))
        potential = []
        for slug in all_slugs:
            name = slug.replace("_", " ")
            if name.lower() in content.lower() and slug not in existing_links:
                potential.append(slug)
        return potential

    def inject_wikilinks(self, content: str, links_to_add: list[str]) -> str:
        """Injeta [[wikilinks]] para conceitos detectados no conteúdo."""
        # TODO: Implementar injeção inteligente (não duplicar, não quebrar código)
        return content
