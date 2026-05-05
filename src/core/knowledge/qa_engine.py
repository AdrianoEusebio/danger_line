"""
WikiQA — Q&A Engine sobre o wiki compilado.

TDD: TDD-13-KB-QA-FILED-BACK.MD
"""
from __future__ import annotations

from providers.base import CompletionRequest, ProviderChain
from storage.models import QAResult
from storage.wiki_store import WikiStore


class WikiQA:
    """Responde perguntas consultando o wiki compilado."""

    QA_PROMPT = """\
You are a knowledge base query engine.
Answer the question using ONLY information from the wiki articles provided.
If the answer is not in the wiki, respond exactly: NOT_FOUND
Always cite the source article with [[wikilinks]] at the end of your answer."""

    MAX_ARTICLES_IN_PROMPT = 5  # Indexer seleciona os mais relevantes

    def __init__(self, provider_chain: ProviderChain, wiki_store: WikiStore):
        self._chain = provider_chain
        self._wiki = wiki_store

    def _select_relevant(self, query: str, articles: dict[str, str]) -> dict[str, str]:
        """Seleciona os artigos mais relevantes para a query (simples: keyword match)."""
        query_words = set(query.lower().split())
        scored = []
        for slug, content in articles.items():
            score = sum(1 for word in query_words if word in content.lower())
            scored.append((score, slug, content))
        scored.sort(reverse=True)
        return {slug: content for _, slug, content in scored[: self.MAX_ARTICLES_IN_PROMPT]}

    async def query(self, question: str) -> QAResult:
        """Consulta o wiki e retorna resposta com fontes."""
        all_articles = self._wiki.get_all_articles()

        if not all_articles:
            return QAResult(answer="NOT_FOUND", not_found=True)

        relevant = self._select_relevant(question, all_articles)

        articles_text = "\n\n---\n\n".join(
            f"ARTICLE [[{slug}]]:\n{content}" for slug, content in relevant.items()
        )

        request = CompletionRequest(
            prompt=f"QUESTION: {question}\n\nWIKI ARTICLES:\n{articles_text}",
            system=self.QA_PROMPT,
            max_tokens=1024,
            temperature=0.0,
        )

        response = await self._chain.complete(request)
        answer = response.content.strip()

        if answer == "NOT_FOUND":
            return QAResult(answer="NOT_FOUND", not_found=True)

        # Extrair [[wikilinks]] citados na resposta
        import re
        sources = re.findall(r"\[\[([^\]]+)\]\]", answer)

        return QAResult(answer=answer, sources=sources, not_found=False)
