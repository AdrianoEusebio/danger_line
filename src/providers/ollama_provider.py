"""
OllamaProvider — Provider local de fallback offline.

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


class OllamaProvider(BaseProvider):
    """Provider Ollama — fallback offline/local."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
    ):
        super().__init__(ProviderConfig(name=ProviderName.OLLAMA, timeout_seconds=60))
        self._base_url = base_url or os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self._model = model or os.getenv("OLLAMA_MODEL", "gemma4:e4b")
        self._client = None  # Lazy init

    def _get_client(self):
        if self._client is None:
            import ollama  # type: ignore
            self._client = ollama.AsyncClient(host=self._base_url)
        return self._client

    async def is_available(self) -> bool:
        """Verifica se o Ollama está rodando localmente."""
        try:
            import httpx
            async with httpx.AsyncClient(timeout=3) as http:
                resp = await http.get(f"{self._base_url}/api/tags")
                return resp.status_code == 200
        except Exception:
            return False

    async def complete(self, request: CompletionRequest) -> CompletionResponse:
        client = self._get_client()
        messages = []
        if request.system:
            messages.append({"role": "system", "content": request.system})
        messages.append({"role": "user", "content": request.prompt})

        response = await client.chat(
            model=self._model,
            messages=messages,
            options={"temperature": request.temperature},
        )

        content = response["message"]["content"] if isinstance(response, dict) else response.message.content

        return CompletionResponse(
            content=content,
            provider=ProviderName.OLLAMA,
            input_tokens=response.get("prompt_eval_count", 0) if isinstance(response, dict) else 0,
            output_tokens=response.get("eval_count", 0) if isinstance(response, dict) else 0,
        )
