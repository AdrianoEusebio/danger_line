# 📋 FICHA TÉCNICA — DANGER LINE v2

---

## Identificação do Projeto

| Campo | Valor |
|-------|-------|
| **Nome** | Danger Line v2 |
| **Tipo** | Sistema Administrativo + Assistente IA |
| **Versão** | 2.0.0 (planejamento) |
| **Linguagem Principal** | Python 3.11+ |
| **Licença** | Privada |
| **Autor** | Adrian |
| **Repositório** | Local — `Danger_line/` |

---

## Requisitos de Sistema

### Hardware Mínimo
| Recurso | Mínimo | Recomendado |
|---------|--------|-------------|
| RAM | 4 GB | 8 GB |
| Disco | 500 MB | 2 GB (com LLM local) |
| CPU | 2 cores | 4 cores |
| GPU | Não necessário | NVIDIA 4GB+ VRAM (se usar LLM local) |

### Software
| Dependência | Versão | Obrigatório |
|-------------|--------|-------------|
| Python | 3.11+ | ✅ Sim |
| uv | latest | ✅ Sim |
| Docker | 24.0+ | ⬜ Opcional |
| Ollama | 0.5+ | ⬜ Opcional (para LLM local) |
| Obsidian | 1.5+ | ✅ Sim (IDE do Knowledge Base) |
| Antigravity IDE | latest | ⬜ Opcional (para MCP) |

---

## Stack Tecnológica

### Core
| Componente | Tecnologia | Justificativa |
|-----------|------------|---------------|
| Runtime | Python 3.11+ | Ecossistema rico para IA, tipagem forte |
| Package Manager | `uv` | Velocidade superior ao pip, padrão moderno |
| CLI Framework | `rich` + `click` | Terminal rico, autocomplete, help automático |
| MCP Framework | `FastMCP` (via `mcp[cli]`) | Integração nativa com Antigravity/Gemini |

### IA Base (Gratuita)
| Provider | Modelo | Tokens/Dia (Free) | Uso |
|----------|--------|--------------------|-----|
| Groq | Llama 3.1 8B | ~500K TPD | Análise rápida, classificação |
| Groq | Llama 3.3 70B | ~100K TPD | Análise profunda, resumos |
| Gemini | Flash 2.0 | ~1M TPD | Fallback, análise de código |
| Ollama | gemma4:e4b | Ilimitado (local) | Offline, tarefas leves |

### IA Potente (Paga — via terceiros)
| Provider | Modelo | Integração |
|----------|--------|------------|
| Antigravity | Gemini Pro / Claude | MCP Server → tools |
| Gemini CLI | Gemini 2.5 | Subprocess / MCP |

### Armazenamento
| Tipo | Tecnologia | Formato |
|------|------------|---------|
| Análises | Markdown files | `.md` com frontmatter YAML |
| Cache | JSON local | `.json` |
| Configuração | `.env` + `config.toml` | Variáveis de ambiente |
| Vault (opcional) | Obsidian | Markdown + wikilinks |

---

## Requisitos Funcionais

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-01 | Analisar estrutura de projetos (árvore, dependências) | 🔴 Alta |
| RF-02 | Gerar resumos otimizados para IA (em inglês, com prompts negativos) | 🔴 Alta |
| RF-03 | Classificar problemas por dificuldade (1-3★) | 🔴 Alta |
| RF-04 | Delegar problemas 2-3★ para IA potente com contexto otimizado | 🔴 Alta |
| RF-05 | Solicitar confirmação do usuário para problemas 2★ | 🟡 Média |
| RF-06 | Painel de controle com métricas de tokens | 🟡 Média |
| RF-07 | Funcionar como MCP Server para Antigravity | 🟡 Média |
| RF-08 | Funcionar como CLI standalone | 🟡 Média |
| RF-09 | Armazenar análises em Markdown (Obsidian-compatible) | 🟡 Média |
| RF-10 | Gerar documentação técnica e diagramas | 🟢 Baixa |
| RF-11 | IA potente avaliar e melhorar as análises do sistema | 🟢 Baixa |
| RF-12 | Compilar Knowledge Base a partir de dados brutos (raw/ → wiki/) | 🔴 Alta |
| RF-13 | Q&A Engine: consultar wiki compilado para enriquecer contexto | 🔴 Alta |
| RF-14 | Linting do wiki: detectar inconsistências, dados faltando | 🟡 Média |
| RF-15 | Gerar Project Card automático ao registrar projeto novo | 🟡 Média |
| RF-16 | Filed Back: soluções boas da IA potente retornam ao wiki | 🟡 Média |

## Requisitos Não-Funcionais

| ID | Requisito | Métrica |
|----|-----------|---------|
| RNF-01 | Tempo de resposta da IA base | < 10 segundos |
| RNF-02 | Economia mínima de tokens | > 40% vs uso direto |
| RNF-03 | Suporte a projetos multilinguagem | Python, JS/TS, PHP, Go |
| RNF-04 | Análises geradas em inglês (padrão IA) | 100% output para IA em EN |
| RNF-05 | Documentação para humanos em PT-BR | Markdown técnico |
| RNF-06 | Uptime do MCP server | 99% durante sessão |

---

## Estrutura de Diretórios (Planejada)

```
Danger_line/
├── src/
│   ├── main.py                 # Entry point
│   ├── cli/
│   │   ├── interface.py        # CLI rica com Rich
│   │   └── dashboard.py        # Painel de métricas
│   ├── core/
│   │   ├── agent.py            # Agente orquestrador
│   │   ├── classifier.py       # Classificador de dificuldade (1-3★)
│   │   ├── analyzer.py         # Análise de código
│   │   ├── summarizer.py       # Gerador de resumos otimizados
│   │   ├── prompt_builder.py   # Construtor de prompts para IA potente
│   │   └── knowledge/          # 🆕 Knowledge Base (Karpathy)
│   │       ├── compiler.py     # raw/ → wiki/ (Compile)
│   │       ├── qa_engine.py    # Q&A sobre o wiki
│   │       ├── linter.py       # Health checks do wiki
│   │       ├── indexer.py      # Auto-linking + summaries
│   │       ├── linker.py       # [[wikilinks]] cross-references
│   │       └── feedback.py     # Filed Back loop
│   ├── providers/
│   │   ├── base.py             # Interface base para providers
│   │   ├── groq_provider.py    # Groq API
│   │   ├── gemini_provider.py  # Gemini Flash
│   │   ├── ollama_provider.py  # LLM local
│   │   └── external.py         # IA potente (subprocess/MCP)
│   ├── storage/
│   │   ├── markdown_store.py   # Salvamento em MD (cache + raw)
│   │   ├── obsidian.py         # Integração Obsidian (obrigatório)
│   │   ├── wiki_store.py       # 🆕 Wiki storage (leitura/escrita)
│   │   └── cache.py            # Cache de análises
│   ├── mcp/
│   │   └── server.py           # MCP Server (FastMCP)
│   └── metrics/
│       ├── token_tracker.py    # Rastreamento de tokens
│       └── reporter.py         # Relatórios de economia
├── documents/                  # Documentação do projeto
├── tests/                      # Testes automatizados
├── docker/
│   └── Dockerfile
├── docker-compose.yml
├── pyproject.toml              # Configuração do projeto (uv)
├── .env
└── README.md
```

---

## Métricas de Sucesso

| Métrica | Meta |
|---------|------|
| Economia de tokens da IA paga | > 50% |
| Precisão da classificação de dificuldade | > 80% |
| Tempo médio para análise de arquivo | < 5s |
| Cobertura de testes | > 70% |
| Knowledge Score após 1 semana de uso | > 40% |
| KB Hits (consultas evitaram análise completa) | > 30% das consultas |

---

## Riscos Identificados

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Rate limit do Groq free tier | Alto | Média | Fallback para Gemini Flash / Ollama |
| LLM local muito fraca para classificação | Médio | Alta | Usar Groq como primary, Ollama como fallback offline |
| MCP não suportado no Antigravity | Alto | Baixa | Já confirmado: suporte via `mcp_config.json` |
| Contexto da LLM local acaba rápido | Médio | Alta | Chunking + resumos incrementais |
| Wiki desatualizado (KB stale) | Médio | Média | Linting periódico + detecção de mudanças |
| Custo de compilação do KB | Baixo | Média | Usar IA base (Groq) para compilar, não a potente |
| Wiki muito grande para context window | Médio | Baixa | Indexer seleciona apenas artigos relevantes |
