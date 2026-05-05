"""
Provider Base — Interface abstrata para todos os providers de IA.

Implementações:
    - GroqProvider  (src/providers/groq_provider.py)
    - GeminiProvider (src/providers/gemini_provider.py)
    - OllamaProvider (src/providers/ollama_provider.py)

TDD: TDD-03-PROVIDER-CHAIN.MD
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ProviderName(str, Enum):
    GROQ = "groq"
    GEMINI = "gemini"
    OLLAMA = "ollama"


@dataclass
class ProviderConfig:
    name: ProviderName
    timeout_seconds: int = 30
    max_retries: int = 1


@dataclass
class CompletionRequest:
    prompt: str
    system: str = ""
    max_tokens: int = 4096
    temperature: float = 0.1


@dataclass
class CompletionResponse:
    content: str
    provider: ProviderName
    input_tokens: int = 0
    output_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens


class BaseProvider(ABC):
    """Interface abstrata para todos os providers de IA base."""

    def __init__(self, config: ProviderConfig):
        self.config = config

    @property
    def name(self) -> ProviderName:
        return self.config.name

    @abstractmethod
    async def is_available(self) -> bool:
        """Verifica se o provider está disponível."""
        ...

    @abstractmethod
    async def complete(self, request: CompletionRequest) -> CompletionResponse:
        """Envia prompt e retorna resposta."""
        ...


class ProviderChain:
    """
    Chain of Responsibility para providers.
    Tenta cada provider em ordem até um responder com sucesso.

    Ordem padrão: Groq → Gemini → Ollama

    TDD: TDD-03-PROVIDER-CHAIN.MD
    """

    def __init__(self, providers: list[BaseProvider]):
        if not providers:
            raise ValueError("At least one provider is required")
        self._providers = providers

    async def complete(self, request: CompletionRequest) -> CompletionResponse:
        """Tenta cada provider em ordem, fazendo fallback em caso de falha."""
        last_error: Optional[Exception] = None

        for provider in self._providers:
            try:
                if not await provider.is_available():
                    continue
                return await provider.complete(request)
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                continue

        raise RuntimeError(
            f"ERROR: PROVIDER_UNAVAILABLE — All providers failed. "
            f"Last error: {last_error}"
        )
