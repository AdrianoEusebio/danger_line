# 📋 FICHA TÉCNICA — DANGER LINE

---

## Identificação do Projeto

| Campo                   | Valor                                                        |
| -------------------------| --------------------------------------------------------------|
| **Nome**                | Danger Line                                                  |
| **Tipo**                | MCP Server nativo                                            |
| **Versão**              | 4.0.0 (Simplificação Arquitetural)                           |
| **Linguagem Principal** | Python 3.11+                                                 |
| **Licença**             | Privada                                                      |
| **Autor**               | Adrian                                                       |
| **Vault Obsidian**      | `C:/Users/adria/OneDrive/Documentos/Danger_line/Danger Line` |

---

## Arquitetura Base

O sistema é focado exclusivamente em duas responsabilidades centrais, implementadas via classes reutilizáveis:

### 1. Módulo MCP (Comunicação IDE)
- **Função**: Expor as capacidades do sistema via Model Context Protocol para a IDE (Antigravity).
- **Framework**: `FastMCP`.
- **Foco Técnico**: Código enxuto; converte comandos da IA em chamadas para as classes de negócio internas.

### 2. Módulo Obsidian (Knowledge Engine)
- **Função**: Operações diretas de leitura/escrita no disco local (DFS).
- **Foco Técnico**: Baseado em classes genéricas para manipulação segura de arquivos Markdown. Garante consistência de formatação (YAML frontmatter, wikilinks).

---

## Requisitos de Software

| Dependência | Versão | Obrigatório |
|-------------|--------|-------------|
| Python | 3.11+ | ✅ Sim |
| uv | latest | ✅ Sim |
| Obsidian | 1.5+ | ✅ Sim |
| Antigravity IDE | latest | ✅ Sim |

---

## Stack Tecnológica Simplificada

A eliminação de APIs de terceiros (LLMs) e middlewares (APIs REST) reduz as dependências ao estritamente necessário.

| Componente | Tecnologia | Justificativa |
|-----------|------------|---------------|
| Runtime | Python 3.11+ | Facilidade de manutenção e ecossistema MCP. |
| MCP Framework | `FastMCP` | Padrão robusto para servidores MCP. |
| File System | Módulo `pathlib` e I/O padrão | Interação direta e rápida com o Obsidian sem depender de plugins REST do aplicativo. |
| Package Manager | `uv` | Velocidade e determinismo no ambiente. |

---

## Requisitos Funcionais

| ID | Requisito | Módulo |
|----|-----------|--------|
| RF-01 | Receber e processar comandos via protocolo MCP. | MCP |
| RF-02 | Escrever arquivos Markdown padronizados no diretório do Obsidian. | Obsidian |
| RF-03 | Realizar leitura de conteúdo (busca/pesquisa) de padrões no Obsidian. | Obsidian |
| RF-04 | Garantir formatação segura de metadados em novos arquivos. | Core/Shared |

---

## Estrutura de Diretórios Proposta (Classes Defaults)

```
Danger_line/
├── src/
│   ├── main.py                 # Inicia o servidor FastMCP
│   ├── modules/
│   │   ├── mcp/                # Handlers e rotas MCP
│   │   │   └── server.py
│   │   └── obsidian/           # Lógica do Knowledge Engine
│   │       ├── vault_manager.py  # Classe padrão de gestão do diretório local
│   │       └── markdown_parser.py# Classe padrão para parser e escrita segura de MD
│   ├── core/                   # Integração entre módulos e lógica principal
│   └── shared/                 # Configurações globais e utilitários
├── documents/                  # Documentação arquitetural simplificada
├── pyproject.toml
└── .env
```
