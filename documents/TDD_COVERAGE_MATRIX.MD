# 📊 Matriz de Cobertura — TDD × Módulos

> Mapa de quais TDDs cobrem quais módulos de `src/`. Garante que nenhum módulo vai para produção sem testes definidos.
>
> **Status**: ✅ Coberto | ⚠️ Parcial | ❌ Sem cobertura

---

## Mapa Completo

| Módulo (`src/`) | TDD Principal | TDDs Adicionais | Status |
|-----------------|:-------------:|:---------------:|:------:|
| `core/analyzer.py` | TDD-01 | TDD-08, TDD-10 | ✅ |
| `core/classifier.py` | TDD-02 | TDD-08, TDD-10 | ✅ |
| `core/summarizer.py` | TDD-05 | TDD-08 | ✅ |
| `core/prompt_builder.py` | TDD-05 | TDD-04 | ✅ |
| `core/agent.py` | TDD-08 | TDD-02, TDD-04 | ✅ |
| `core/knowledge/compiler.py` | TDD-11 | TDD-06, TDD-14 | ✅ |
| `core/knowledge/qa_engine.py` | TDD-13 | TDD-02, TDD-04 | ✅ |
| `core/knowledge/linter.py` | TDD-12 | TDD-14 | ✅ |
| `core/knowledge/indexer.py` | TDD-11 | TDD-13 | ✅ |
| `core/knowledge/linker.py` | TDD-11 | TDD-15 | ✅ |
| `core/knowledge/feedback.py` | TDD-13 | TDD-06, TDD-11 | ✅ |
| `providers/base.py` | TDD-03 | TDD-14 | ✅ |
| `providers/groq_provider.py` | TDD-03 | TDD-14 | ✅ |
| `providers/gemini_provider.py` | TDD-03 | TDD-14 | ✅ |
| `providers/ollama_provider.py` | TDD-03 | TDD-14 | ✅ |
| `storage/markdown_store.py` | TDD-06 | TDD-13, TDD-14 | ✅ |
| `storage/obsidian.py` | TDD-06 | TDD-15 | ✅ |
| `storage/wiki_store.py` | TDD-11 | TDD-12, TDD-15 | ✅ |
| `storage/cache.py` | TDD-06 | TDD-14 | ✅ |
| `mcp/server.py` | TDD-04 | TDD-10, TDD-14 | ✅ |
| `cli/interface.py` | TDD-09 | — | ✅ |
| `cli/dashboard.py` | TDD-09 | TDD-07 | ✅ |
| `metrics/token_tracker.py` | TDD-07 | TDD-04 | ✅ |
| `metrics/reporter.py` | TDD-07 | TDD-09 | ✅ |
| `main.py` | TDD-08 | TDD-09 | ✅ |

---

## Mapa Reverso — TDD → Módulos

| TDD | Módulos cobertos |
|-----|-----------------|
| **TDD-01** | `core/analyzer.py` |
| **TDD-02** | `core/classifier.py`, `core/knowledge/qa_engine.py` |
| **TDD-03** | `providers/base.py`, `providers/groq_provider.py`, `providers/gemini_provider.py`, `providers/ollama_provider.py` |
| **TDD-04** | `mcp/server.py`, `core/agent.py` |
| **TDD-05** | `core/summarizer.py`, `core/prompt_builder.py` |
| **TDD-06** | `storage/markdown_store.py`, `storage/obsidian.py`, `storage/cache.py` |
| **TDD-07** | `metrics/token_tracker.py`, `metrics/reporter.py` |
| **TDD-08** | `core/agent.py`, `main.py` |
| **TDD-09** | `cli/interface.py`, `cli/dashboard.py` |
| **TDD-10** | `mcp/server.py` (security), `core/analyzer.py` (edge cases) |
| **TDD-11** | `core/knowledge/compiler.py`, `core/knowledge/indexer.py`, `core/knowledge/linker.py`, `storage/wiki_store.py` |
| **TDD-12** | `core/knowledge/linter.py` |
| **TDD-13** | `core/knowledge/qa_engine.py`, `core/knowledge/feedback.py` |
| **TDD-14** | `providers/base.py`, `storage/markdown_store.py`, `core/knowledge/compiler.py` (error paths) |
| **TDD-15** | `core/knowledge/linker.py`, `storage/obsidian.py`, `storage/wiki_store.py` |

---

## Cobertura por Camada

| Camada | Módulos | Cobertos | % |
|--------|:-------:|:--------:|:-:|
| Core — Processing | 5 | 5 | 100% |
| Core — Knowledge Base | 6 | 6 | 100% |
| Providers | 4 | 4 | 100% |
| Storage | 4 | 4 | 100% |
| MCP | 1 | 1 | 100% |
| CLI | 2 | 2 | 100% |
| Metrics | 2 | 2 | 100% |
| **Total** | **24** | **24** | **100%** |

---

## Como Manter Esta Matriz

Ao criar um novo módulo em `src/`:
1. Adicionar uma linha na tabela com status `❌`
2. Criar ou associar um TDD existente
3. Atualizar o status para `⚠️` após escrever os testes
4. Atualizar para `✅` após testes passando
