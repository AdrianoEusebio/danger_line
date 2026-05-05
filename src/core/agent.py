"""
AgentOrchestrator — O cérebro do Danger Line.

Coordena o fluxo de ponta a ponta:
1. Recebe arquivo/problema
2. Consulta o Wiki (Q&A)
3. Analisa o arquivo (Analyzer)
4. Classifica a dificuldade (Classifier)
5. Gera o Super-Prompt (PromptBuilder)
6. Registra métricas (TokenTracker)

TDD: TDD-08-ORQUESTRADOR.MD
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from .analyzer import CodeAnalyzer
from .classifier import DifficultyClassifier
from .prompt_builder import PromptBuilder
from core.knowledge.qa_engine import WikiQA
from core.knowledge.feedback import FeedbackLoop
from metrics.token_tracker import TokenTracker
from providers.base import ProviderChain
from storage.cache import AnalysisCache
from storage.markdown_store import MarkdownStore

logger = logging.getLogger(__name__)

class AgentOrchestrator:
    """Orquestra todos os componentes para resolver uma tarefa."""

    def __init__(
        self,
        provider_chain: ProviderChain,
        cache: AnalysisCache,
        store: MarkdownStore,
        wiki_qa: WikiQA,
        tracker: TokenTracker
    ):
        self.chain = provider_chain
        self.analyzer = CodeAnalyzer(provider_chain, cache, store)
        self.classifier = DifficultyClassifier(provider_chain)
        self.wiki_qa = wiki_qa
        self.tracker = tracker
        self.builder = PromptBuilder()

    async def process_task(self, problem: str, file_path: Path) -> dict:
        """
        Executa o fluxo completo para um problema em um arquivo.
        """
        logger.info(f"Processing task for {file_path}")
        
        # 1. Consulta ao Knowledge Base (O que já sabemos?)
        wiki_context = await self.wiki_qa.query(problem)
        if not wiki_context.not_found:
            self.tracker.record_kb_hit()

        # 2. Análise Técnica (O que o arquivo faz?)
        analysis = await self.analyzer.analyze(file_path)
        if analysis.provider_used == "cache":
            self.tracker.record_cache_hit()
        
        # 3. Classificação (Quem deve resolver?)
        # Passamos o wiki_context para o classifier decidir se rebaixa a estrela
        classification = await self.classify(problem, analysis.summary_for_ai, wiki_context.answer)
        self.tracker.record_problem(classification.difficulty)

        # 4. Construção do Super-Prompt
        super_prompt = self.builder.build_super_prompt(
            problem=problem,
            analyses=[analysis],
            wiki_context=wiki_context.answer if not wiki_context.not_found else ""
        )

        # 5. Estimativa de economia (simples: prompt bruto vs otimizado)
        raw_estimate = len(problem) + file_path.stat().st_size
        self.tracker.record_raw_estimate(raw_estimate // 4) # estimativa grosseira de tokens

        return {
            "classification": classification,
            "analysis": analysis,
            "super_prompt": super_prompt,
            "wiki_match": wiki_context.sources if not wiki_context.not_found else []
        }

    async def classify(self, problem: str, code_summary: str, wiki_context: str) -> any:
        return await self.classifier.classify(problem, code_summary, wiki_context)
