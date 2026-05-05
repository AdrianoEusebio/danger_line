"""
TDD-02: Classificação por Estrelas (com Knowledge Base)
Referência: documents/TDD/TDD-02-CLASSIFICACAO-ESTRELAS.MD
"""
import pytest
import json
from core.classifier import DifficultyClassifier
from storage.models import Classification
from providers.base import CompletionResponse, ProviderName
from unittest.mock import AsyncMock

class TestClassifier:
    """T-02.x — Classificação de dificuldade 1-3★."""

    async def test_02_1_classify_syntax_error(self, mock_chain):
        """T-02.1: Erro simples deve ser classificado via IA."""
        classifier = DifficultyClassifier(mock_chain)
        
        # Mockando a resposta da IA para o Classifier
        mock_chain._providers[0].complete = AsyncMock(return_value=CompletionResponse(
            content='{"difficulty": 1, "confidence": 0.95, "reasoning": "Simple syntax error", "category": "syntax", "wiki_match": null}',
            provider=ProviderName.GROQ
        ))

        result = await classifier.classify("Missing semicolon in javascript")
        
        assert result.difficulty == 1
        assert result.category == "syntax"
        assert result.recommended_action == "resolve_locally"

    async def test_02_7_invalid_ai_response_defaults_to_2_star(self, mock_chain):
        """T-02.7: Resposta inválida da IA deve defaultar para 2★."""
        classifier = DifficultyClassifier(mock_chain)
        
        mock_chain._providers[0].complete = AsyncMock(return_value=CompletionResponse(
            content='invalid json',
            provider=ProviderName.GROQ
        ))

        result = await classifier.classify("Some complex problem")
        assert result.difficulty == 2 # Default fallback
