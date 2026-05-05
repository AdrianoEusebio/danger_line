"""
PromptBuilder — Constrói super-prompts otimizados para IAs premium.

TDD: TDD-05-SUMMARIZER.MD | API_CONTRACT.MD
"""
from __future__ import annotations

from storage.models import AnalysisResult

class PromptBuilder:
    """Monta o contexto final para a IA de alta performance."""

    HEADER = "### CONTEXT ARCHITECTURE — DANGER LINE AGENT ###"
    FOOTER = "### END OF CONTEXT — PROCEED WITH SOLUTION ###"

    @staticmethod
    def build_super_prompt(
        problem: str,
        analyses: list[AnalysisResult],
        wiki_context: str = ""
    ) -> str:
        """
        Combina o problema, análises de arquivos e contexto do KB em um prompt denso.
        """
        sections = [PromptBuilder.HEADER]

        # 1. Wiki Context (Conhecimento Prévio)
        if wiki_context and wiki_context != "NOT_FOUND":
            sections.append("## KNOWLEDGE BASE CONTEXT (Patterns & Known Bugs)")
            sections.append(wiki_context)

        # 2. File Analyses (O essencial de cada arquivo)
        sections.append("## PROJECT COMPONENTS ANALYSIS")
        for analysis in analyses:
            sections.append(f"### FILE: {analysis.filepath}")
            sections.append(analysis.summary_for_ai)
            if analysis.issues:
                sections.append("Detected potential issues: " + ", ".join(analysis.issues))

        # 3. The Problem
        sections.append("## TARGET PROBLEM / TASK")
        sections.append(problem)

        sections.append(PromptBuilder.FOOTER)

        return "\n\n".join(sections)
