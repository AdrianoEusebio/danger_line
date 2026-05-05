"""
FeedbackLoop — Filed Back: outputs bons retornam ao raw/ para enriquecer o wiki.

TDD: TDD-13-KB-QA-FILED-BACK.MD
"""
from __future__ import annotations

import logging
from pathlib import Path

from storage.markdown_store import MarkdownStore
from storage.models import SolutionResult

logger = logging.getLogger(__name__)


class FeedbackLoop:
    """
    Garante que soluções de qualidade (aprovadas pela IA premium ou pelo alvará)
    retornem ao raw/ para serem compiladas no wiki.

    É o mecanismo de "compound learning" do sistema.
    """

    def __init__(self, store: MarkdownStore):
        self._store = store

    def file_back_solution(self, solution: SolutionResult) -> Path:
        """
        Salva solução aprovada em raw/solutions/.
        O KB Compiler a processará na próxima compilação incremental.

        Returns:
            Path do arquivo criado em raw/solutions/
        """
        path = self._store.save_solution(solution)
        logger.info("FeedbackLoop: filed back solution for '%s' → %s", solution.filename, path)
        return path

    def file_back_batch_review(self, items: list[dict], batch_number: int) -> Path:
        """
        Salva batch review (alvará) da IA premium em raw/reviews/.

        Args:
            items: Lista de itens revisados (cada item tem filename, status, notes)
            batch_number: Número sequencial do batch
        """
        path = self._store.save_review(items, batch_number)
        logger.info(
            "FeedbackLoop: filed back batch review #%d (%d items) → %s",
            batch_number, len(items), path,
        )
        return path
