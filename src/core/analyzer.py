"""
CodeAnalyzer — O coração da análise de arquivos do Danger Line.

Coordena:
1. Cache (evita chamadas desnecessárias)
2. Summarizer (gera os resumos via IA base)
3. MarkdownStore (persiste na camada raw/ para o KB)

TDD: TDD-01-ANALISE-ARQUIVO.MD
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from storage.cache import AnalysisCache
from storage.markdown_store import MarkdownStore
from storage.models import AnalysisResult
from .summarizer import CodeSummarizer
from providers.base import ProviderChain

logger = logging.getLogger(__name__)

class CodeAnalyzer:
    """Responsável por processar arquivos individuais e gerar resultados estruturados."""

    def __init__(
        self, 
        provider_chain: ProviderChain,
        cache: Optional[AnalysisCache] = None,
        store: Optional[MarkdownStore] = None
    ):
        self._summarizer = CodeSummarizer(provider_chain)
        self._cache = cache
        self._store = store

    async def analyze(self, file_path: Path) -> AnalysisResult:
        """
        Analisa um arquivo, usando cache se disponível.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # 1. Tentar Cache
        if self._cache:
            cached_data = self._cache.get(file_path)
            if cached_data:
                logger.info(f"Cache hit for {file_path}")
                # Nota: Em um sistema real, reconstruiríamos o AnalysisResult completo aqui
                # ou retornaríamos o cache se ele for suficiente.
                # Para o v2, se houver cache, retornamos o que temos.
                return AnalysisResult(
                    file_hash=cached_data["file_hash"],
                    filename=file_path.name,
                    filepath=str(file_path),
                    language=cached_data["language"],
                    summary_for_ai="[CACHED] " + cached_data.get("summary_for_ai", ""),
                    summary_for_human="[CACHED] " + cached_data.get("summary_for_human", ""),
                    difficulty=cached_data["difficulty"],
                    provider_used="cache"
                )

        # 2. Cache Miss ou Cache Desativado -> Analisar com IA
        logger.info(f"Analyzing {file_path} with AI...")
        content = file_path.read_text(encoding="utf-8", errors="replace")
        
        # Gerar hash
        file_hash = AnalysisCache.compute_hash(file_path)
        
        # Chamar Summarizer
        summary_ai, summary_human = await self._summarizer.summarize(file_path.name, content)
        
        # Criar resultado (difficulty 2 como default para análise inicial)
        result = AnalysisResult(
            file_hash=file_hash,
            filename=file_path.name,
            filepath=str(file_path),
            language=self._detect_language(file_path),
            summary_for_ai=summary_ai,
            summary_for_human=summary_human,
            difficulty=2,  # Será refinado pelo Classifier se necessário
            provider_used="base_ai"
        )

        # 3. Salvar (Cache + Raw Store)
        if self._cache:
            self._cache.set(file_path, result)
        
        if self._store:
            self._store.save_analysis(result)

        return result

    def _detect_language(self, path: Path) -> str:
        ext = path.suffix.lower()
        mapping = {
            ".py": "python",
            ".gd": "gdscript",
            ".js": "javascript",
            ".ts": "typescript",
            ".tsx": "react/typescript",
            ".jsx": "react/javascript",
            ".go": "go",
            ".rs": "rust",
            ".md": "markdown"
        }
        return mapping.get(ext, "unknown")
