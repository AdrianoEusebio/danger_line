"""
Bootstrap — Inicialização de novos projetos no sistema.

Implementa a Opção C Híbrido:
1. Scan estrutura
2. Project Card profundo
3. Análise de 5 arquivos-chave

TDD: TDD-13-KB-QA-FILED-BACK.MD | TDD-11-KB-COMPILER.MD
"""
from __future__ import annotations

import logging
from pathlib import Path

from filesystem.scanner import ProjectScanner
from .project_card import ProjectCardEngine
from core.analyzer import CodeAnalyzer
from storage.obsidian import ObsidianIntegration
from storage.cache import AnalysisCache
from storage.markdown_store import MarkdownStore
from providers.base import ProviderChain

logger = logging.getLogger(__name__)

class ProjectBootstrap:
    """Configura um projeto novo para uso com o Danger Line."""

    def __init__(
        self, 
        provider_chain: ProviderChain,
        obsidian: ObsidianIntegration
    ):
        self.chain = provider_chain
        self.obsidian = obsidian
        self.card_engine = ProjectCardEngine(provider_chain)

    async def register(self, project_path: Path) -> dict:
        """
        Registra o projeto e executa o scan inicial.
        """
        logger.info(f"Registering new project: {project_path}")
        
        # 1. Criar estrutura danger_line/
        dl_path = project_path / "danger_line"
        dl_path.mkdir(exist_ok=True)
        
        # Inicializar storage local
        cache = AnalysisCache(dl_path / "cache")
        store = MarkdownStore(dl_path)
        analyzer = CodeAnalyzer(self.chain, cache, store)
        scanner = ProjectScanner(project_path)

        # 2. Scan Estrutura
        tree = scanner.get_tree(depth=2)
        
        # 3. Analisar 5 arquivos-chave (Investimento de tokens)
        key_files = scanner.find_key_files(count=5)
        analyses = []
        for f in key_files:
            try:
                analysis = await analyzer.analyze(f)
                analyses.append(analysis)
            except Exception as e:
                logger.warning(f"Failed to analyze key file {f}: {e}")

        # 4. Gerar Project Card profundo
        structure_info = f"FILE TREE:\n{tree}\n\nKEY FILES ANALYZED:\n"
        for a in analyses:
            structure_info += f"- {a.filepath}: {a.summary_for_ai[:200]}...\n"

        card_content = await self.card_engine.generate(project_path.name, structure_info)
        
        # 5. Salvar Card no Obsidian
        self.obsidian.save_project_card(project_path.name, card_content)

        return {
            "project": project_path.name,
            "tree": tree,
            "files_analyzed": len(analyses),
            "card_saved": True
        }
