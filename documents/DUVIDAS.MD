# ❓ DÚVIDAS — DANGER LINE v2

## Índice
1. [Dúvidas Simples](#1-dúvidas-simples)
2. [Dúvidas Técnicas](#2-dúvidas-técnicas)
3. [Dúvidas Arquiteturais](#3-dúvidas-arquiteturais)
4. [Dúvidas do Usuário (respondidas)](#4-dúvidas-do-usuário)
5. [Dúvidas em Aberto](#5-dúvidas-em-aberto)

---

## 1. Dúvidas Simples

### D-01: Qual gerenciador de pacotes usar?
**R**: `uv` — é o padrão moderno para Python, mais rápido que pip, suporta `pyproject.toml`, e é o recomendado pelo ecossistema MCP.

### D-02: O código deve ser em português ou inglês?
**R**: **Código em inglês** (variáveis, funções, classes, comentários técnicos). **Documentação para humanos em PT-BR**. Outputs para IA sempre em inglês.

### D-03: Preciso de um banco de dados?
**R**: Não inicialmente. Markdown files + JSON para cache e métricas são suficientes. SQLite pode ser adicionado depois se necessário para buscas complexas.

### D-04: Posso usar o sistema sem Antigravity?
**R**: Sim. O CLI standalone funciona independentemente. O MCP Server é uma camada extra.

---

## 2. Dúvidas Técnicas

### D-05: Como o MCP Server se comunica com o Antigravity?
**R**: Via `stdio` (standard input/output). O Antigravity inicia o processo Python e se comunica via streams. Não precisa de porta de rede, não precisa de HTTP.

### D-06: O MCP Server roda constantemente ou sob demanda?
**R**: O Antigravity inicia o processo quando necessário e o mantém vivo durante a sessão. Quando o Antigravity fecha, o processo encerra.

### D-07: Como estimar tokens sem acesso à API de tokenização?
**R**: Regra de ~4 caracteres por token (para modelos de linguagem inglesa). Para cálculos mais precisos, usar a lib `tiktoken` (OpenAI) ou estimativas dos providers.

### D-08: O Groq tem SDK oficial em Python?
**R**: Sim. `pip install groq` — API compatível com OpenAI, muito simples de usar.

### D-09: Como lidar com rate limiting do Groq?
**R**: Implementar retry com backoff exponencial + fallback automático para Gemini Flash quando o rate limit é atingido (HTTP 429).

### D-10: O FastMCP suporta async?
**R**: Sim. Tools podem ser async functions normais. O FastMCP lida com o event loop.

---

## 3. Dúvidas Arquiteturais

### D-11: Provider Chain vs Router — qual padrão usar?
**R**: **Chain of Responsibility** com fallback. O primeiro provider disponível atende. Se falhar, passa para o próximo. Simples e eficaz.

### D-12: Como o classifier será calibrado sem dados reais?
**R**: Iniciar com few-shot examples hardcoded. Conforme o sistema é usado e a IA potente emite alvarás, os exemplos são enriquecidos. É um sistema que melhora com uso.

### D-13: O review buffer deve ter limite de tamanho?
**R**: Sim. Máximo de ~20 itens ou ~5000 tokens no batch. Se exceder, enviar automaticamente ou perguntar ao usuário.

### D-14: Como separar o contexto do MCP do CLI?
**R**: O core engine (analyzer, classifier, summarizer) é compartilhado. MCP e CLI são apenas interfaces diferentes para o mesmo core. Padrão **Ports & Adapters**.

### D-15: O que acontece se nenhum provider estiver disponível?
**R**: O sistema opera em modo **offline degradado**: pode fazer mapeamento de projetos, extração de dependências (regex), e cache lookup — tudo sem IA. Apenas análise e classificação ficam indisponíveis.

### D-16: Como integrar o Knowledge Base (Karpathy) sem duplicar funcionalidade com o cache/storage existente?
**R**: O Knowledge Base Karpathy opera em **nível diferente** do cache. O cache armazena análises individuais de arquivos; o KB compila e interliga conhecimento de múltiplas análises, criando uma "memória de longo prazo" do projeto. São complementares, não redundantes.

### D-17: O Knowledge Base deve ser por projeto ou global?
**R**: **Ambos**. Cada projeto tem seu KB local (`.danger_line/wiki/`), e existe um KB global (`~/.danger_line/global_wiki/`) que acumula patterns e aprendizados cross-project. A decisão de o que promover de local para global é feita pelo sistema.

---

## 4. Dúvidas do Usuário (Respondidas)

### D-U1: Docker — devemos usar? Qual a melhor alternativa?

**Devemos usar?** Para desenvolvimento local e MCP, **NÃO**. Docker adiciona complexidade desnecessária:
- Volume mounting do Windows é lento e problemático
- MCP usa `stdio`, que complica com Docker
- Ollama precisa de `host.docker.internal`, mais uma camada

**Quando usar Docker?**
- Deploy em servidor remoto
- CI/CD para testes automatizados
- Distribuição para terceiros

**Melhor alternativa para dev local**: `uv` (gerencia venv automaticamente) + rodar Python diretamente.

---

### D-U2: LLM Local — como usar e devemos usar?

**Sua LLM (gemma4:e4b)**: Muito limitada (~4K contexto). Não é viável como provider principal.

**Como usar na lógica**:
- ✅ Classificação binária (sim/não) com prompts curtos
- ✅ Extração de keywords de código
- ✅ Fallback offline de último recurso
- ❌ Análise de código completa
- ❌ Geração de resumos

**Devemos usar?** Como **terceiro fallback** (após Antigravity/Gemini Flash e Groq). Nunca como primary.

---

### D-U3: Entendimento de cada ideia — ATUALIZADO

| Ideia | Entendimento | Status |
|-------|-------------|--------|
| **Ideia 1** (IA gratuita) | 100% ✅ | **Prioridade definida**: 1º Gemini Flash (Antigravity), 2º Groq, 3º LLM local |
| **Ideia 2** (MCP) | 100% ✅ | **Confirmado**: MCP é o caminho. Pasta/CLI somente como fallback |
| **Ideia 3** (Análise/Resumo) | 95% ✅ | **Esclarecido**: Padrão para IA = boas práticas de prompt. Padrão para humano = doc técnica. Análise sempre padrão IA. Resumo adapta conforme destino |
| **Ideia 4** (Estrelas) | 100% ✅ | **Esclarecido**: 1★ = automático. 2-3★ = manual em termos de **permissão** (entendimento do usuário), não complexidade |
| **Ideia 5** (Painel) | 100% ✅ | **Definido**: Histórico temporal, dividido por semana |
| **Ideia 6** (Karpathy KB) | 🔄 Rascunho | Ver `IDEIA-6.MD` — base de conhecimento pessoal compilada por IA |

---

### D-U4: Melhor arquitetura para o projeto?

**Recomendação: Ports & Adapters (Hexagonal) simplificada**

```
src/
├── core/          ← DOMÍNIO (puro, sem dependências externas)
│   ├── analyzer.py
│   ├── classifier.py
│   ├── summarizer.py
│   ├── prompt_builder.py
│   └── knowledge/     ← NOVO: Knowledge Base (Karpathy)
│       ├── compiler.py
│       ├── linker.py
│       └── indexer.py
├── providers/     ← ADAPTERS de saída (implementações de IA)
│   ├── base.py    ← Interface abstrata
│   ├── groq.py
│   ├── gemini.py
│   └── ollama.py
├── storage/       ← ADAPTERS de persistência
│   ├── markdown.py
│   ├── cache.py
│   └── wiki.py        ← NOVO: Wiki storage (Karpathy)
├── mcp/           ← PORT de entrada (MCP)
│   └── server.py
├── cli/           ← PORT de entrada (CLI)
│   ├── interface.py
│   └── dashboard.py
└── metrics/       ← Cross-cutting concern
    └── tracker.py
```

**Por quê?** Core isolado, fácil trocar providers, fácil adicionar interfaces (REST API, web, etc.).

---

### D-U5: Como integrar internamente no Antigravity como MCP?

1. Criar o MCP Server com FastMCP (`src/mcp/server.py`)
2. Editar `C:\Users\adria\.gemini\antigravity\mcp_config.json`
3. Adicionar a configuração do servidor
4. Reiniciar o Antigravity
5. O Gemini/Claude agora tem acesso às tools do Danger Line

O Antigravity **automaticamente** detecta e usa as tools quando relevante.

---

### D-U6: O que dá pra reaproveitar do projeto antigo?

| Componente | % Reaproveitável | Ação |
|-----------|------------------|------|
| `leitor.py` | 70% | Refatorar nomes para inglês |
| `obsidian.py` | 80% | Manter como storage adapter |
| `ferramentas.py` | 50% | Migrar para @mcp.tool() |
| `ia.py` | 60% | Abstrair em OllamaProvider |
| `gerador.py` | 40% | Reescrever com novo formato EN |
| `agente.py` | 30% | Loop útil, regex frágil |
| `ia_externa.py` | 10% | Substituir por MCP |
| `interface.py` | 50% | Manter Rich, adicionar Click |

---

### D-U7: Nível do prompt e como melhorar?

**Nível**: 7/10 — **Acima da média** para um usuário técnico.

**Pontos fortes**:
- ✅ Dividiu em sub-ideias numeradas (facilita o parsing da IA)
- ✅ Deu contexto do problema original e por que mudou
- ✅ Pediu deliverables específicos (documentos nomeados)
- ✅ Fez perguntas direcionadas ao final
- ✅ Indicou constraints técnicas (LLM fraca, Obsidian, etc.)

**O que melhorar para próximos prompts**:
1. **Separar contexto de pedido**: Primeiro explique O QUÊ quer, depois o PORQUÊ. O prompt mistura os dois
2. **Usar Markdown no prompt**: Headers (`##`), listas (`-`), e negrito ajudam a IA a parsear
3. **Definir prioridades explícitas**: "P0: MCP Server, P1: Classificador, P2: Dashboard"
4. **Ser explícito sobre formato de saída**: "Responda em tabela", "Use diagramas Mermaid"
5. **Prompt negativo**: Adicionar "NÃO faça X" ajuda a evitar respostas genéricas
6. **Numerar os deliverables separadamente do contexto**: O pedido dos documentos ficou misturado com as ideias
7. **Especificar escopo do TDD**: "N testes por caso de uso" ou "focar em happy path + edge cases"

---

## 5. Decisões Tomadas (Últimas)

- [x] **Obsidian**: ✅ Obrigatório — peça fundamental do sistema, IDE de visualização do wiki
- [x] **Groq API Key**: ✅ Usuário já tem conta
- [x] **KB Scope**: ✅ Pasta global com subpastas por projeto (multi-project)
- [x] **KB Format**: ✅ `[[wikilinks]]` estilo Obsidian
- [x] **Compilação KB**: ✅ Modo **B+ Balanceado** (detalhes abaixo)

### Decisão: Compilação KB — Modo B+ Balanceado

**Para IA**: Tudo é salvo automaticamente (append-only). Cada análise, classificação e solução vai para `raw/` e é compilado em contexto otimizado EN.

**Para Humano**: O sistema gera um **Project Card** automaticamente quando um projeto novo é registrado. O card contém:
- 📋 Resumo do projeto (o que é, stack, arquitetura)
- 🔧 Especificações técnicas (dependências, padrões)
- 🐛 Bugs conhecidos (cresce incrementalmente com uso)
- 📊 Métricas (cobertura do KB, último scan)

**O card evolui**: Updates incrementais conforme o projeto é usado. O humano nunca precisa pedir resumo — ele aparece automaticamente no Obsidian.

**O que NÃO polui o Obsidian**: Prompts intermediários crus da IA ficam em `raw/`, acessíveis mas não expostos na wiki visível.

## 5b. Decisões Tomadas (Rodada 2)

- [x] **Obsidian Vault**: ✅ Usar o vault existente (`C:/Users/adria/OneDrive/Documentos/Danger_line/Danger Line`)
- [x] **Project Card profundidade**: ✅ Profundo (~3000 tokens) — melhor base = melhor economia futura
- [x] **AGENT.md + pasta local**: ✅ Criar pasta `danger_line/` dentro de cada projeto com AGENT.md e todos os dados locais do KB

### Decisão: Pasta `danger_line/` por projeto

Cada projeto terá uma pasta local:
```
MeuProjeto/
├── src/
├── ...
└── danger_line/               # Pasta local do Danger Line
    ├── AGENT.md               # Instruções customizadas para o compilador
    ├── raw/                   # Dados brutos append-only
    │   ├── analyses/
    │   ├── classifications/
    │   ├── solutions/
    │   └── reviews/
    ├── cache/                 # Cache de análises
    │   └── {file_hash}.json
    └── config.toml            # Config local do projeto
```

O wiki compilado fica no **vault global do Obsidian** (não na pasta do projeto), porque:
- O Obsidian precisa de acesso direto para visualizar
- O wiki global permite cross-project learning
- A pasta local guarda só dados brutos + cache

---

## 5c. Decisões Tomadas (Rodada 3 — Final)

- [x] **Wiki inicial**: ✅ Opção C Híbrido — scan de estrutura + Project Card profundo + 5 arquivos-chave (~3000 tokens, 1x por projeto)
- [x] **lint_wiki**: ✅ **Automático + hot-update manual** — roda automaticamente a cada N compilações, mas existe `lint_wiki(force=True)` como MCP tool para rodar sob demanda

### Decisão: Wiki Inicial — Opção C Híbrido

Fluxo ao registrar um projeto novo:
```
1. Scan de estrutura     → árvore de arquivos, deps, configs  (~500 tokens)
2. Project Card profundo → resumo, stack, arquitetura          (~1500 tokens)
3. 5 arquivos-chave      → os mais centrais (main, index, etc) (~1000 tokens)
─────────────────────────────────────────────────────────────────────────────
   Total: ~3000 tokens (investimento único) → wiki começa útil
   Depois: incrementa a cada análise no uso normal
```

### Decisão: lint_wiki — Automático + Hot-update

| Modo | Trigger | Escopo |
|------|---------|--------|
| **Automático** | A cada 10 compilações (configurável via AGENT.md) | Checks rápidos: stale + missing |
| **Hot-update** | `lint_wiki()` via MCP tool (sob demanda) | Full lint: todos os checks |

```python
# MCP tools expostas
@mcp.tool()
async def lint_wiki() -> str:
    """Force a full wiki health check (hot-update). Use when you suspect
    the wiki is outdated or after a major code refactor."""
    return await linter.lint_full()

# Automático: dispara após N compilações
async def compile_incremental(...):
    ...
    self.compile_count += 1
    if self.compile_count % self.config.lint_interval == 0:  # default: 10
        await self.linter.lint_quick()  # apenas stale + missing
```

---

## 6. Dúvidas em Aberto

> ✅ **Todas as dúvidas foram respondidas!** O projeto está com arquitetura totalmente definida e pronto para a fase de implementação.

### Próximos passos sugeridos:
1. Setup do ambiente (`uv`, `pyproject.toml`)
2. Implementar `src/core/knowledge/compiler.py` (KB Compiler)
3. Implementar `src/mcp/server.py` com as tools definidas
4. Configurar o vault do Obsidian e a pasta `danger_line/` no primeiro projeto
