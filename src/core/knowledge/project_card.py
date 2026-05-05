"""
ProjectCardEngine — Gera o "RG" do projeto no Obsidian.

TDD: TDD-13-KB-QA-FILED-BACK.MD
"""
from __future__ import annotations

import logging
from providers.base import CompletionRequest, ProviderChain

logger = logging.getLogger(__name__)

PROJECT_CARD_PROMPT = """\
You are a software architect. Generate a high-level Project Card for the provided codebase structure.
The card must be in Markdown and include:
- 📋 Overview: What this project does.
- 🔧 Tech Stack: Detected languages and frameworks.
- 🏗️ Architecture: Brief description of the project structure.
- 🐛 Known Issues: (Leave empty if none provided).
- 📊 KB Stats: (Placeholder for metrics).

Be concise but professional. Use English."""

class ProjectCardEngine:
    """Gera documentação estruturada do projeto para humanos."""

    def __init__(self, provider_chain: ProviderChain):
        self._chain = provider_chain

    async def generate(self, project_name: str, structure_info: str) -> str:
        """
        Gera o conteúdo do Project Card.
        structure_info: deve conter a árvore de arquivos e dependências detectadas.
        """
        request = CompletionRequest(
            prompt=f"PROJECT: {project_name}\n\nSTRUCTURE:\n{structure_info}",
            system=PROJECT_CARD_PROMPT,
            max_tokens=2048,
            temperature=0.3,
        )

        try:
            response = await self._chain.complete(request)
            return response.content
        except Exception as e:
            logger.error(f"ProjectCard generation failed: {e}")
            return f"# Project Card: {project_name}\n\nError generating card: {e}"
