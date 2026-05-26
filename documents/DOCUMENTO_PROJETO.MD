# 📖 DOCUMENTO DE PROJETO — DANGER LINE v5.0 (DragonScale MCP Edition)

## Ecossistema MCP para Knowledge Base Portátil no Obsidian

---

## 1. Visão Estratégica

### 1.1 O Sistema
O **Danger Line v5.0** opera como um **Servidor MCP (Model Context Protocol)** robusto e portátil. Ele atua como uma interface de alta velocidade que conecta a inteligência baseada na IDE (**Antigravity**) ao banco de dados em Markdown do desenvolvedor (**Obsidian Vault**).

Ao fundir o design leve e portátil com os poderosos conceitos de estruturação de conhecimento do `claude-obsidian`, o Danger Line traz consistência semântica à documentação de projetos de forma headless, multiplataforma (Windows e Linux) e direta no File System (DFS).

### 1.2 Princípios Fundamentais
1. **Foco Único (MCP-Nativo):** Todas as ações são orquestradas via ferramentas (Tools) e recursos (Resources) ativados de forma passiva ou ativa pela IDE.
2. **Portabilidade Absoluta:** Lógica implementada em Python puro. Sem shell scripts ou dependências Unix rígidas, garantindo funcionamento idêntico no Windows.
3. **Gerenciamento de Contexto Semântico:** Uso de identificadores exclusivos, análise de grafos de links e detecção de similaridade local para otimizar tokens e evitar redundâncias.
4. **Acoplamento Inteligente ao Workspace:** Leitura silenciosa de diretórios de projetos ativos para carregamento automático de diretrizes de codificação locais.

---

## 2. Arquitetura do Sistema

### 2.1 Diagrama de Arquitetura v5.0 (Modular)

```mermaid
graph TD
    subgraph "Cliente (IDE)"
        IDE["IDE Antigravity (IA Assistente)"]
    end

    subgraph "Servidor MCP (Danger Line v5.0)"
        MCP["🔌 Módulo MCP (FastMCP Tools/Resources)"]
        
        subgraph "Core Orchestrator"
            ENGINE["🧠 KnowledgeEngine"]
        end

        subgraph "Subcomponentes Core (Python)"
            LINT["🔍 Linter Engine (Órfãos, Links Mortos)"]
            DS["🐉 DragonScale Memory (Folds, Endereços, Cosseno)"]
            PARSE["📝 MarkdownBuilder (YAML + Tags de Densidade)"]
        end

        subgraph "Obsidian Engine"
            VAULT["📓 VaultManager (DFS Lock-Safe)"]
        end
    end

    subgraph "Persistência Local"
        FILE["🗂️ Arquivos Markdown (*.md)"]
    </subgraph>

    IDE <-->|Model Context Protocol| MCP
    MCP <--> ENGINE
    ENGINE <--> DS
    ENGINE <--> LINT
    ENGINE <--> PARSE
    ENGINE <--> VAULT
    VAULT <-->|Leitura/Escrita Direta DFS| FILE
```

---

## 3. Detalhamento dos Módulos

### 3.1 Módulo MCP (fastmcp)
Ponto de entrada de comandos e recursos para a IDE. Contém:
* **Tools:** `query_kb` (busca textual e de tags), `commit_knowledge` (gravação de manuais), `commit_bugfix` (gravação de correções), `explore_graph` (navegação em teia de links) e o novo `lint_kb` (validação de integridade).
* **Resources:** `obsidian://overview` (visão geral do vault) e `obsidian://project-rules` (regras específicas de código do projeto ativo).

### 3.2 Core Orchestrator & Subcomponentes (Python)
* **KnowledgeEngine:** Gerencia o fluxo de gravação e as correlações (ex: afinidade de stack de projetos e links bidirecionais).
* **Linter Engine:** Auditor local que varre o vault em busca de páginas sem saída/entrada (órfãs), links markdown apontando para notas inexistentes e metadados corrompidos.
* **DragonScale Memory Engine:**
  * *Folds Manager:* Realiza summarization/rollup de logs de alterações no Python.
  * *Address Allocator:* Controla sequenciadores de ID únicos (`address: c-NNNNNN`) com concorrência segura em arquivos locais (`.vault-meta/address-counter.txt`).
  * *Semantic Tiling:* Calcula embeddings locais de notas via Ollama (`nomic-embed-text`) e roda verificação de similaridade de cosseno para evitar notas idênticas.
* **MarkdownBuilder:** Codifica e decodifica o cabeçalho YAML Frontmatter e o corpo das notas Markdown, aplicando tags automáticas de granularidade (`contexto/rascunho`, `contexto/medio`, `contexto/profundo`) com base no tamanho do corpo.

### 3.3 Módulo Obsidian (VaultManager)
Abstração de E/S direta baseada na biblioteca `pathlib`.
* Realiza a persistência local lock-safe (garantida por travas no Python como `portalocker` para prevenir colisões no Windows).
* Encontra caminhos de notas globais, listas de diretórios dinâmicos e consultas rápidas por tags normalizadas.

---

## 4. Glossário do Projeto

| Termo | Definição |
|-------|-----------|
| **DragonScale Memory** | Conjunto de mecanismos avançados de estruturação de conhecimento portados do claude-obsidian para melhorar integridade, histórico e similaridade semântica. |
| **Direct File System (DFS)** | Acesso de leitura/gravação direto ao disco rígido local do usuário sem intermediários como APIs REST de rede ou plugins ativos. |
| **Deterministic Addresses** | Números sequenciais estáveis e persistentes associados aos arquivos markdown para identificá-los de forma única independentemente de renomeações no vault. |
| **Semantic Tiling** | Processo matemático de comparação por similaridade de cosseno de embeddings de textos para marcar notas conceitualmente equivalentes. |
| **Log Folds** | Agrupamento e condensação incremental de logs cronológicos de alterações em resumos de alto nível. |
