"""
GroqProvider — Provider primário de IA base.

Modelos:
    - llama-3.1-8b-instant  (classificação rápida)
    - llama-3.3-70b-versatile (análise profunda)

TDD: TDD-03-PROVIDER-CHAIN.MD | TDD-14-ERROR-RECOVERY.MD
"""
from __future__ import annotations

import os
from typing import Optional

from .base import (
    BaseProvider,
    CompletionRequest,
    CompletionResponse,
    ProviderConfig,
    ProviderName,
)


class GroqProvider(BaseProvider):
    """Provider Groq usando a API oficial."""

    DEFAULT_MODEL = "llama-3.3-70b-versatile"
    FAST_MODEL = "llama-3.1-8b-instant"

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        super().__init__(ProviderConfig(name=ProviderName.GROQ))
        self._api_key = api_key or os.getenv("GROQ_API_KEY", "")
        self._model = model or self.DEFAULT_MODEL
        self._client = None  # Lazy init

    def _get_client(self):
        if self._client is None:
            from groq import AsyncGroq  # type: ignore
            self._client = AsyncGroq(api_key=self._api_key)
        return self._client

    async def is_available(self) -> bool:
        return bool(self._api_key and self._api_key != "your-groq-api-key-here")

    async def complete(self, request: CompletionRequest) -> CompletionResponse:
        client = self._get_client()
        messages = []
        if request.system:
            messages.append({"role": "system", "content": request.system})
        messages.append({"role": "user", "content": request.prompt})

        response = await client.chat.completions.create(
            model=self._model,
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            timeout=self.config.timeout_seconds,
        )

        return CompletionResponse(
            content=response.choices[0].message.content or "",
            provider=ProviderName.GROQ,
            input_tokens=response.usage.prompt_tokens if response.usage else 0,
            output_tokens=response.usage.completion_tokens if response.usage else 0,
        )
