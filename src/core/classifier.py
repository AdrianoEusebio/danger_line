"""
DifficultyClassifier — Classifica problemas em 1-3★.

Consulta o KB (wiki) antes de classificar para possível reclassificação.
Se o wiki tem solução para um pattern similar, rebaixa a dificuldade.

TDD: TDD-02-CLASSIFICACAO-ESTRELAS.MD
"""
from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING

from providers.base import CompletionRequest, ProviderChain
from storage.models import Classification

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

CLASSIFICATION_PROMPT = """\
You are a code difficulty classifier. Classify the difficulty as:

1★ SIMPLE: syntax errors, missing imports, typos, config, OR known pattern in wiki
2★ MODERATE: logic bugs, small refactors, <3 files involved
3★ COMPLEX: architecture changes, performance, security, multi-module

IMPORTANT: If WIKI_CONTEXT contains a similar solved bug or pattern, DOWNGRADE difficulty.
- Exact match → difficulty 1
- Partial match (similarity note) → downgrade by 1 level, set partial_match flag

RESPOND WITH VALID JSON ONLY:
{"difficulty": N, "confidence": 0.0-1.0, "reasoning": "...", "category": "syntax|logic|architecture|performance|security|config", "wiki_match": "ArticleName or null"}"""


class DifficultyClassifier:
    """
    Classifica a dificuldade de um problema (1-3★).
    Integra com Q&A Engine do KB para reclassificação.
    """

    def __init__(self, provider_chain: ProviderChain):
        self._chain = provider_chain

    async def classify(
        self,
        problem: str,
        code_context: str = "",
        wiki_context: str = "",
    ) -> Classification:
        """
        Classifica o problema. Consulta o wiki antes de classificar.

        Args:
            problem: Descrição do problema
            code_context: Trecho de código relevante (opcional)
            wiki_context: Resultado do Q&A Engine sobre o wiki (opcional)
        """
        if not problem or len(problem.strip()) < 10:
            return Classification(
                difficulty=2,
                confidence=0.5,
                reasoning="Description too short to classify",
                category="unknown",
            )

        prompt_parts = [f"PROBLEM: {problem}"]
        if code_context:
            prompt_parts.append(f"CODE CONTEXT:\n{code_context}")
        if wiki_context and wiki_context != "NOT_FOUND":
            prompt_parts.append(f"WIKI_CONTEXT (known bugs/patterns):\n{wiki_context}")

        request = CompletionRequest(
            prompt="\n\n".join(prompt_parts),
            system=CLASSIFICATION_PROMPT,
            max_tokens=512,
            temperature=0.0,
        )

        try:
            response = await self._chain.complete(request)
            raw = response.content.strip()

            # Extrair JSON mesmo se vier com markdown code block
            if "```" in raw:
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]

            data = json.loads(raw)
            difficulty = int(data.get("difficulty", 2))

            if difficulty not in (1, 2, 3):
                raise ValueError(f"Invalid difficulty: {difficulty}")

            return Classification(
                difficulty=difficulty,
                confidence=float(data.get("confidence", 0.5)),
                reasoning=data.get("reasoning", ""),
                category=data.get("category", "unknown"),
                wiki_match=data.get("wiki_match"),
                recommended_action=self._recommended_action(difficulty),
            )

        except (json.JSONDecodeError, KeyError, ValueError) as exc:
            logger.warning("Classifier: invalid AI response, defaulting to 2★. Error: %s", exc)
            return Classification(
                difficulty=2,
                confidence=0.3,
                reasoning=f"Failed to parse AI response, defaulted to 2★. Raw: {exc}",
                category="unknown",
            )

    @staticmethod
    def _recommended_action(difficulty: int) -> str:
        return {1: "resolve_locally", 2: "ask_user", 3: "escalate"}.get(difficulty, "ask_user")
