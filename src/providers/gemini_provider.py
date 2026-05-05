"""
GeminiProvider — Provider de fallback (Gemini Flash).

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


class GeminiProvider(BaseProvider):
    """Provider Google Gemini Flash — fallback do Groq."""

    DEFAULT_MODEL = "gemini-2.0-flash"

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        super().__init__(ProviderConfig(name=ProviderName.GEMINI))
        self._api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self._model = model or self.DEFAULT_MODEL
        self._client = None  # Lazy init

    def _get_client(self):
        if self._client is None:
            import google.generativeai as genai  # type: ignore
            genai.configure(api_key=self._api_key)
            self._client = genai.GenerativeModel(self._model)
        return self._client

    async def is_available(self) -> bool:
        return bool(self._api_key and self._api_key != "your-gemini-api-key-here")

    async def complete(self, request: CompletionRequest) -> CompletionResponse:
        client = self._get_client()
        full_prompt = f"{request.system}\n\n{request.prompt}" if request.system else request.prompt

        response = client.generate_content(full_prompt)

        return CompletionResponse(
            content=response.text,
            provider=ProviderName.GEMINI,
            # Gemini free tier não expõe token count de forma consistente
            input_tokens=0,
            output_tokens=0,
        )
