# 📋 FICHA TÉCNICA — DANGER LINE v5.0 (DragonScale MCP Edition)

---

## Identificação do Projeto

| Campo | Valor |
|---|---|
| **Nome** | Danger Line |
| **Tipo** | Servidor MCP nativo portátil |
| **Versão** | 5.0.0 (DragonScale MCP Edition) |
| **Linguagem Principal** | Python 3.11+ |
| **Licença** | Privada |
| **Autor** | Adrian |
| **Vault Obsidian** | `C:/Users/Adriano/Desktop/PROJETOS/danger_line/storage/brainline` |

---

## Requisitos de Software

| Dependência | Versão | Obrigatório | Justificativa |
|---|---|---|---|
| **Python** | 3.11+ | ✅ Sim | Execução portátil do servidor e lógica. |
| **Ollama** | latest | ✅ Sim (Opcional) | Utilizado para gerar embeddings locais (`nomic-embed-text`) para detecção de duplicidades. |
| **Obsidian** | 1.5+ | ✅ Sim | Visualizador e editor humano do cérebro digital (Wiki). |
| **Antigravity IDE** | latest | ✅ Sim | Ambiente cliente que consome as tools e resources do MCP. |

---

## Stack Tecnológica Portátil (Python Puro)

Para garantir máxima portabilidade no Windows e Linux, todas as travas e operações do sistema operacional foram portadas para bibliotecas Python nativas, eliminando scripts shell (`flock` Unix).

| Biblioteca | Versão | Função | Justificativa |
|---|---|---|---|
| **fastmcp** | latest | Servidor MCP | Criação ágil e tipada de tools e resources. |
| **portalocker** | latest | Trava de Arquivos | Permite o uso de locks exclusivos (`flock`) de concorrência tanto no Windows quanto no Linux de forma nativa e portátil. |
| **ollama** | latest | API de Embeddings | Comunicação com o serviço local do Ollama para processamento semântico. |
| **pathlib / re** | Standard | E/S e Regex | Utilitários do sistema para navegação de diretórios e extração de wikilinks. |
| **pytest / pytest-asyncio**| latest | Testes Unitários | Automação e assincronia na validação da integridade de escrita/leitura. |

---

## Requisitos Funcionais

| ID | Requisito | Descrição | Módulo |
|---|---|---|---|
| **RF-01** | Processar comandos MCP | Expor ferramentas de consulta e escrita (`query_kb`, `commit_knowledge`, `commit_bugfix`, `explore_graph`, `lint_kb`). | MCP |
| **RF-02** | Leitura/Escrita DFS | Acessar arquivos Markdown diretamente no disco do usuário de forma assíncrona e lock-safe. | Obsidian (VaultManager) |
| **RF-03** | Auto-Tag de Densidade | Injetar tags de densidade de contexto (`contexto/rascunho`, `contexto/medio`, `contexto/profundo`) com base no tamanho do corpo. | Core (MarkdownBuilder) |
| **RF-04** | Afinidade de Projetos | Mapear similaridade de stack técnico de projetos e criar links bidirecionais automáticos. | Core (KnowledgeEngine) |
| **RF-05** | Linter de Wiki | Rastrear links mortos, notas órfãs e inconsistências estruturais no frontmatter YAML. | Core (Linter) |
| **RF-06** | Endereços Únicos | Alocar IDs sequenciais estáveis (`c-NNNNNN`) no YAML frontmatter, vinculados em `.manifest.json`. | Core (DragonScale Address) |
| **RF-07** | Similaridade Semântica| Comparar similaridade de cosseno de embeddings locais para identificar duplicações conceituais de notas. | Core (Semantic Tiling) |
| **RF-08** | Folds de Log | Agrupar e resumir logs de alteração cronológicos para otimização de busca. | Core (Folds Manager) |
| **RF-09** | Hot Cache de Sessão | Gerar arquivo rotativo `wiki/hot.md` para resumos instantâneos da IDE. | Core (Hot Cache) |

---

## Estrutura de Diretórios Proposta

```
Danger_line/
├── src/
│   ├── main.py                 # Ponto de entrada do servidor MCP
│   ├── core/
│   │   ├── engine.py           # Orquestrador central (KnowledgeEngine)
│   │   ├── linter.py           # [NOVO] Linter de integridade do vault
│   │   └── dragonscale.py      # [NOVO] Mecanismos DragonScale (Address, Folds, Tiling, Scorer)
│   ├── modules/
│   │   ├── mcp/
│   │   │   └── server.py       # Handlers, Tools e Resources do FastMCP
│   │   └── obsidian/
│   │       ├── vault_manager.py# Manipulação E/S, Locks (portalocker) e Buscas
│   │       └── markdown_parser.py# Construtor/Parser de YAML frontmatter e body
│   └── shared/
│       ├── config.py           # Configurações de diretórios, API URLs e níveis de Log
│       └── logger.py           # Setup de logs padronizados UTF-8
├── documents/                  # Documentação arquitetural
├── tests/                      # Suite de testes pytest
│   ├── test_engine.py
│   ├── test_vault_manager.py
│   ├── test_markdown_parser.py
│   └── test_dragonscale.py     # [NOVO] Testes dos motores DragonScale
├── pyproject.toml
└── .env
```
