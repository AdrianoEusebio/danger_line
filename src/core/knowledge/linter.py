"""
WikiLinter — Health checks do wiki compilado.

Dois modos:
    lint_quick(): automático — apenas STALE + MISSING (barato)
    lint_full():  manual/hot-update — todos os 4 checks (completo)

TDD: TDD-12-KB-LINTER.MD
"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from pathlib import Path

from providers.base import ProviderChain
from storage.models import LintReport
from storage.wiki_store import WikiStore

logger = logging.getLogger(__name__)


class WikiLinter:
    """Verifica saúde do wiki. Nunca modifica arquivos."""

    LINT_PROMPT = """\
You are a knowledge base health checker.
Analyze the wiki articles provided and report:
1. INCONSISTENCIES: conflicting information between articles or with the code
2. MISSING: topics/modules that should have articles but don't
3. STALE: articles that may be outdated (code changed significantly)
4. CONNECTIONS: potential [[wikilinks]] between unrelated articles that should be linked

RESPOND JSON ONLY:
{
  "issues": [{"type": "INCONSISTENCY|STALE", "article": "slug", "detail": "..."}],
  "suggestions": [{"type": "MISSING|CONNECTION", "topic": "...", "detail": "..."}],
  "health_score": 0.0-1.0
}"""

    def __init__(
        self,
        provider_chain: ProviderChain,
        wiki_store: WikiStore,
        project_path: Path,
        stale_threshold_days: int = 30,
    ):
        self._chain = provider_chain
        self._wiki = wiki_store
        self._project = project_path
        self._stale_threshold = stale_threshold_days

    async def lint_quick(self) -> LintReport:
        """
        Lint rápido — apenas STALE + MISSING.
        Disparado automaticamente a cada N compilações.
        """
        logger.info("WikiLinter: running lint_quick (auto)")
        # TODO: Implementar checks rápidos sem LLM (baseado em timestamps)
        return LintReport(health_score=1.0)

    async def lint_full(self) -> LintReport:
        """
        Lint completo — todos os 4 checks.
        Disparado manualmente via MCP tool lint_wiki().
        """
        logger.info("WikiLinter: running lint_full (manual hot-update)")
        articles = self._wiki.get_all_articles()

        if not articles:
            return LintReport(
                health_score=0.0,
                suggestions=[{
                    "type": "EMPTY_WIKI",
                    "topic": "wiki",
                    "detail": "Wiki has no articles. Run compile_knowledge first.",
                    "action": "run_compile",
                }],
            )

        # TODO: Implementar chamada ao LLM com artigos
        return LintReport(health_score=1.0)

    def format_report(self, report: LintReport) -> str:
        """Formata o LintReport para exibição no terminal."""
        lines = [
            f"🔍 WIKI LINT REPORT — Health Score: {report.health_score:.0%}",
            "─" * 55,
        ]

        issues_by_type: dict[str, list] = {}
        for issue in report.issues:
            issues_by_type.setdefault(issue["type"], []).append(issue)

        if "INCONSISTENCY" in issues_by_type:
            for i in issues_by_type["INCONSISTENCY"]:
                lines.append(f"⚠️  INCONSISTENCY [{i['article']}]: {i['detail']}")

        if "STALE" in issues_by_type:
            for i in issues_by_type["STALE"]:
                lines.append(f"⏰  STALE [{i['article']}]: {i['detail']}")

        for sug in report.suggestions:
            if sug["type"] == "MISSING":
                lines.append(f"📋  MISSING: {sug['topic']} — {sug['detail']}")
            elif sug["type"] == "CONNECTION":
                lines.append(f"🔗  CONNECTION: {sug['detail']}")
            elif sug["type"] == "EMPTY_WIKI":
                lines.append(f"📭  EMPTY WIKI: {sug['detail']}")

        if not report.issues and not report.suggestions:
            lines.append("✅  Wiki is healthy — no issues found.")

        return "\n".join(lines)
