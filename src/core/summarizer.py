"""
Summarizer — Transforma código bruto em resumos otimizados.

Gera dois outputs:
1. Summary for AI: Denso, técnico, focado em dependências e lógica.
2. Summary for Human: Markdown elegante para visualização no Obsidian.

TDD: TDD-05-SUMMARIZER.MD
"""
from __future__ import annotations

import logging
from providers.base import CompletionRequest, ProviderChain

logger = logging.getLogger(__name__)

SUMMARIZER_SYSTEM_PROMPT = """\
You are a technical code architect. Your task is to summarize the provided code file.
You must provide two distinct summaries.

1. AI SUMMARY:
- Technical and dense.
- List all imports and key dependencies.
- Describe the core responsibility of the file.
- List main classes and functions with their signatures.
- Highlight complex logic or potential side effects.

2. HUMAN SUMMARY:
- Clean Markdown.
- Use emojis for readability.
- Sections: Overview, Key Components, and Technical Notes.

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:
===AI_START===
[AI summary here]
===AI_END===
===HUMAN_START===
[Human summary here]
===HUMAN_END===
"""

class CodeSummarizer:
    """Gera resumos técnicos e legíveis de arquivos de código."""

    def __init__(self, provider_chain: ProviderChain):
        self._chain = provider_chain

    async def summarize(self, filename: str, content: str) -> tuple[str, str]:
        """
        Resume o conteúdo de um arquivo.
        Returns: (summary_for_ai, summary_for_human)
        """
        request = CompletionRequest(
            prompt=f"FILENAME: {filename}\n\nCONTENT:\n{content}",
            system=SUMMARIZER_SYSTEM_PROMPT,
            max_tokens=2048,
            temperature=0.2,
        )

        try:
            response = await self._chain.complete(request)
            raw = response.content

            ai_summary = self._extract_section(raw, "AI_START", "AI_END")
            human_summary = self._extract_section(raw, "HUMAN_START", "HUMAN_END")

            return ai_summary, human_summary
        except Exception as e:
            logger.error(f"Summarizer failed for {filename}: {e}")
            return f"Error summarizing file: {e}", f"### ❌ Erro na análise de {filename}\nNão foi possível gerar o resumo."

    def _extract_section(self, text: str, start_marker: str, end_marker: str) -> str:
        try:
            start = text.find(f"==={start_marker}===") + len(f"==={start_marker}===")
            end = text.find(f"==={end_marker}===")
            return text[start:end].strip()
        except Exception:
            return "Section not found."
