# 🧠 IDEIA 1 — Obsidian como Knowledge Engine (Agnóstico)

## 1. O Vault como Banco de Dados Vivo
O Obsidian é o repositório central de inteligência. A integração é projetada para ser **independente da IDE**, funcionando via sistema de arquivos e Local REST API.

## 2. Ecossistema de Plugins Sinergistas
Para extrair o máximo valor, o sistema se apoia nestes plugins do Obsidian:
1.  **Local REST API**: Permite que qualquer interface (MCP, CLI ou Script) interaja com o conhecimento.
2.  **Dataview**: Gera dashboards dinâmicos (ex: "Lista de todos os Playbooks de Backend").
3.  **Templater**: Padroniza a criação de notas de acordo com o contexto ativo (Frontend/Backend).
4.  **Tag Wrangler**: Organiza as especialidades através de tags hierárquicas.
5.  **Graph Analysis**: Para visualizar e analisar a conexão entre soluções de diferentes projetos.
6.  **Advanced URI**: Para permitir que o sistema envie comandos de navegação profunda para o Obsidian.

## 3. Estrutura de Pastas (Multi-Brain Architecture)
O vault é organizado para suportar múltiplos contextos conectados:
- `00_Core_Library/`: Conhecimento universal (padrões de projeto, clean code).
- `01_Backend/`: Contexto especializado em APIs, bancos de dados e performance.
- `02_Frontend/`: Contexto especializado em UI/UX, frameworks e estado.
- `03_Infrastructure/`: Contexto de deploy, docker e cloud.
- `🐞 BugTracker/`: Repositório global de erros e soluções higienizadas.

## 4. Integração com o Core
O Módulo Obsidian (`src/modules/obsidian/`) garante que a IA tenha acesso ao contexto certo no momento certo, injetando wikilinks e metadados que facilitam a navegação tanto para a IA quanto para o desenvolvedor humano.

---
> **Status**: Sincronizado com a nova arquitetura agnóstica. Removida lógica de pastas por projeto local.
