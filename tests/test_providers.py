"""
TDD-03: Provider Chain (Fallback)
Referência: documents/TDD/TDD-03-PROVIDER-CHAIN.MD
"""
import pytest
from providers.base import ProviderChain, CompletionRequest, ProviderName
from providers.groq_provider import GroqProvider

class TestProviderChain:
    """T-03.x — Chain de fallback entre providers."""

    async def test_03_1_groq_primary_success(self, mock_groq_provider):
        """T-03.1: Groq disponível deve ser usado como primário."""
        chain = ProviderChain([mock_groq_provider])
        request = CompletionRequest(prompt="Olá")
        
        response = await chain.complete(request)
        
        assert response.provider == ProviderName.GROQ
        assert mock_groq_provider.complete.called

    async def test_03_2_fallback_to_gemini_when_groq_fails(
        self, mock_unavailable_provider, mock_gemini_provider
    ):
        """T-03.2: Falha do Groq deve acionar Gemini como fallback."""
        chain = ProviderChain([mock_unavailable_provider, mock_gemini_provider])
        request = CompletionRequest(prompt="Olá")
        
        response = await chain.complete(request)
        
        assert response.provider == ProviderName.GEMINI
        assert mock_gemini_provider.complete.called

    async def test_03_3_all_providers_unavailable_raises_error(
        self, mock_unavailable_provider
    ):
        """T-03.3: Todos providers indisponíveis deve retornar erro claro."""
        chain = ProviderChain([mock_unavailable_provider])
        request = CompletionRequest(prompt="Olá")
        
        with pytest.raises(RuntimeError, match="PROVIDER_UNAVAILABLE"):
            await chain.complete(request)
