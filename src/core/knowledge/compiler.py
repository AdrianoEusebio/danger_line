"""
KB Compiler — Transforma raw/ em artigos wiki estruturados.

Pipeline: raw/analyses/ + raw/solutions/ + raw/reviews/ → wiki/*.md

TDD: TDD-11-KB-COMPILER.MD
"""
from __future__ import annotations

import logging
from pathlib import Path

from providers.base import ProviderChain
from storage.wiki_store import WikiStore

logger = logging.getLogger(__name__)


class KBCompiler:
    """
    Compila dados brutos (raw/) em artigos wiki (wiki/).

    Modos:
        - incremental: apenas arquivos raw/ não compilados ainda
        - full: reconstrói todo o wiki
    """

    COMPILE_PROMPT = """\
You are a knowledge base article compiler.
Given raw analysis/solution data, create a structured wiki article.

Requirements:
- Write in English
- Use [[wikilinks]] to reference related concepts
- Include frontmatter YAML with: title, compiled_from, last_compiled, tags, related, confidence
- Structure: Overview → Key Concepts → Implementation Details → Known Issues → Related

RESPOND WITH THE COMPLETE MARKDOWN ARTICLE ONLY."""

    def __init__(self, provider_chain: ProviderChain, wiki_store: WikiStore, raw_path: Path):
        self._chain = provider_chain
        self._wiki = wiki_store
        self._raw = raw_path
        self.compile_count: int = 0

    async def compile_incremental(self) -> dict:
        """
        Compila arquivos de raw/analyses/ para o wiki/.
        """
        raw_analyses = self._raw / "raw" / "analyses"
        if not raw_analyses.exists():
            return {"error": "raw/analyses folder not found"}

        new_files = list(raw_analyses.glob("*.md"))
        created = 0
        
        for file in new_files:
            # Slug baseada no nome original do arquivo (removendo data prefix)
            # Ex: 2026-05-05_auth_py.md -> auth_py
            slug = "_".join(file.stem.split("_")[1:])
            
            if self._wiki.article_exists(slug):
                continue
                
            content = file.read_text(encoding="utf-8")
            
            # No v2 real, aqui chamaríamos a IA para fundir múltiplas análises.
            # No v2 core agora, transformamos a análise bruta em artigo formatado.
            article_content = f"# {slug.replace('_', '.')}\n\n"
            article_content += f"**Compiled from**: {file.name}\n\n"
            article_content += content.split("## For AI")[0] # Pega o frontmatter e título
            
            if "## For Human" in content:
                article_content += "## Overview\n" + content.split("## For Human")[1]

            self._wiki.write_article(slug, article_content)
            created += 1

        self.compile_count += created
        return {"articles_created": created, "articles_updated": 0, "links_generated": 0}

    async def compile_full(self) -> dict:
        """Reconstrói todo o wiki do zero."""
        # TODO: Implementar
        logger.info("KBCompiler: full compile triggered")
        return {"articles_created": 0, "articles_updated": 0, "links_generated": 0}

    def should_lint(self, lint_interval: int) -> bool:
        """Retorna True se é hora de rodar lint_quick automático."""
        return lint_interval > 0 and self.compile_count % lint_interval == 0
