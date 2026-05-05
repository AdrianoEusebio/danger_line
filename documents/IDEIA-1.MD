# 💡 IDEIA 1 — Modelo de IA Gratuito como Base do Sistema

## Conceito

O sistema deve operar com uma IA gratuita como motor principal, delegando para a IA paga apenas quando necessário. A IA base é responsável por análises, classificações e resumos — tarefas que não exigem o poder computacional de modelos premium.

## Providers Disponíveis

### Groq (Recomendado como Primary)
- **API gratuita** com rate limits generosos (~500K tokens/dia no Llama 8B)
- **Velocidade extrema**: inference em hardware LPU, ~10x mais rápido que GPT
- **Modelos disponíveis**: Llama 3.1 8B (rápido), Llama 3.3 70B (preciso)
- **Sem custo** e sem cartão de crédito

### Gemini Flash (Fallback Cloud)
- **API gratuita** com ~1M tokens/dia
- **Google AI Studio** para chave de API
- **Modelo**: Gemini 2.0 Flash — boa capacidade de análise de código
- **Vantagem**: Janela de contexto enorme (1M tokens)

### Ollama / LLM Local (Fallback Offline)
- **Modelo atual**: `gemma4:e4b` — muito limitado em contexto
- **Problema**: Janela de contexto pequena (~4K tokens), respostas lentas
- **Uso viável**: Apenas para tarefas extremamente simples (classificação binária, extração de keywords)

## Integração com Antigravity

**SIM, é possível integrar diretamente!** Via MCP (Model Context Protocol):

1. O Danger Line roda como um **MCP Server** usando FastMCP
2. O Antigravity se conecta via `mcp_config.json`
3. O Gemini (que o Antigravity usa) pode chamar as tools do Danger Line
4. Resultado: **O Antigravity É a IA potente**, e o Danger Line é o assistente que prepara contexto

Isso significa que ao usar o Antigravity com o MCP do Danger Line configurado, o Gemini 2.5 (ou Claude) terá acesso direto às análises otimizadas do sistema.

## Passos Técnicos

### Passo 1: Configurar Provider Abstraction
```python
# src/providers/base.py
from abc import ABC, abstractmethod

class AIProvider(ABC):
    @abstractmethod
    async def complete(self, prompt: str, system: str = "") -> str: ...
    
    @abstractmethod
    async def is_available(self) -> bool: ...
    
    @abstractmethod
    def get_token_count(self, text: str) -> int: ...
```

### Passo 2: Implementar Groq Provider
```python
# src/providers/groq_provider.py
from groq import Groq

class GroqProvider(AIProvider):
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.1-8b-instant"  # rápido para classificação
```

### Passo 3: Implementar Gemini Flash Provider
```python
# src/providers/gemini_provider.py
import google.generativeai as genai

class GeminiFlashProvider(AIProvider):
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.0-flash")
```

### Passo 4: Implementar Chain of Fallback
```python
# src/providers/chain.py
class ProviderChain:
    def __init__(self):
        self.providers = [
            GroqProvider(),
            GeminiFlashProvider(),
            OllamaProvider(),
        ]
    
    async def complete(self, prompt, system=""):
        for provider in self.providers:
            if await provider.is_available():
                return await provider.complete(prompt, system)
        raise NoProviderAvailableError()
```

### Passo 5: Sobre a LLM Local
A LLM local (`gemma4:e4b`) pode ser usada na lógica de forma limitada:
- **Chunking**: Dividir o código em pedaços de ~2K tokens
- **Classificação binária**: "É erro de sintaxe? SIM/NÃO" (prompts curtos)
- **Extração de keywords**: Não requer contexto grande
- **Cache de respostas**: Evitar reprocessar o mesmo código

> **Veredicto**: Usar Groq como primary, Gemini Flash como fallback, Ollama apenas para tarefas offline muito simples.

---

## Riscos e Mitigações

| Risco | Mitigação |
|-------|-----------|
| Rate limit do Groq | Fallback automático para Gemini Flash |
| Ollama muito lento | Usar apenas para cache warmup e classificação |
| API keys expostas | `.env` + nunca commitar chaves |
