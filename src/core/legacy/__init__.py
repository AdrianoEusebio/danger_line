"""
Código legado do Danger Line v1.

Mantido para referência e reaproveitamento de lógica.
NÃO importar diretamente — use os módulos em src/core/ e src/providers/.

Componentes reaproveitáveis (ver DOCUMENTO_PROJETO.MD §9.1):
    - agente.py      → lógica de loop → src/core/agent.py
    - ia.py          → OllamaProvider → src/providers/ollama_provider.py
    - ferramentas.py → tools map → src/mcp/server.py
    - gerador.py     → PromptBuilder → src/core/prompt_builder.py
"""
