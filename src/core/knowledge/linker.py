"""
Linker — Cross-references e wikilinks entre artigos.

TDD: TDD-11-KB-COMPILER.MD | TDD-15-CROSS-PROJECT.MD
"""
from __future__ import annotations

from storage.wiki_store import WikiStore


class WikiLinker:
    """Gerencia [[wikilinks]] e cross-project promotion."""

    def __init__(self, wiki_store: WikiStore):
        self._wiki = wiki_store

    def get_backlinks(self, slug: str) -> list[str]:
        """Retorna lista de artigos que linkam para o slug dado."""
        import re
        articles = self._wiki.get_all_articles()
        backlinks = []
        for article_slug, content in articles.items():
            if article_slug == slug:
                continue
            if re.search(rf"\[\[{re.escape(slug)}\]\]", content, re.IGNORECASE):
                backlinks.append(article_slug)
        return backlinks

    def count_backlinks(self) -> dict[str, int]:
        """Retorna contagem de backlinks para cada artigo."""
        articles = self._wiki.get_all_articles()
        counts = {slug: 0 for slug in articles}
        for backlinks_target in articles:
            for bl in self.get_backlinks(backlinks_target):
                counts[bl] = counts.get(bl, 0) + 1
        return counts

    def is_global_candidate(self, content: str, confidence_threshold: float = 0.9) -> bool:
        """
        Verifica se um artigo é candidato para promoção ao KB global.
        Requer que confidence no frontmatter seja >= threshold.
        """
        # TODO: Parse frontmatter confidence
        return False
