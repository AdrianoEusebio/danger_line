# 🚀 ROADMAP TDD — DANGER LINE (Refatoração 4.0)

Este documento dita a construção baseada na nova arquitetura unificada e simplificada, focada em classes base (Default Classes) e exclusividade do ecossistema MCP.

---

## 🟢 FASE 1: Limpeza e Fundação Base [CONCLUÍDO]
- [x] **Limpeza de Módulos Legados**: Deletar módulos internos de providers (Groq/Gemini), classificação de estrelas, Context Manager e Sanitizer.
- [x] **Ajuste da Estrutura de Diretórios**: Definir o padrão `/src/modules/mcp/` e `/src/modules/obsidian/`.
- [x] **Atualização das Dependências**: Reduzir bibliotecas do `requirements.txt` / `pyproject.toml` removendo LangChain ou APIs pesadas; focando apenas no FastMCP e utilitários.

## 🟡 FASE 2: Engine do Obsidian (Classes Reutilizáveis) [CONCLUÍDO]
- [x] **Classe `ObsidianVaultManager`**: Desenvolver classe padrão que resolve o path do vault e lida de forma segura com acesso I/O de diretórios.
- [x] **Classe `MarkdownBuilder` / Parser**: Utilitário dedicado para gerar templates consistentes com Frontmatter YAML e formatação amigável para o app do Obsidian.
- [x] **Lógica de Busca Simples**: Sistema rápido para varrer o vault por tags ou títulos que a IDE requisitar.

## 🛡️ FASE 3: Interface MCP Enxuta e "Graph Explore" [CONCLUÍDO]
- [x] **Implementar Tool `query_kb(query, tags)`**: Expõe a lógica de busca do Obsidian (baseada em **Tags Semânticas - Ideia A**), retornando arquivos consolidados e formatados.
- [x] **Implementar Tool `commit_knowledge`**: Interface para a IA criar e atualizar manuais/bugs no Obsidian com validação rigorosa e YAML obrigatório.
- [x] **Implementar Tool `explore_graph` (Ideia B)**: Tool MCP capaz de ler wikilinks de uma nota raiz e retornar o resumo da teia de conhecimento conectada.
- [x] **Implementar Project Rules via Resources (Ideia C)**: Expor dinamicamente diretrizes de projetos como um resource MCP baseado na pasta local aberta do desenvolvedor.

## 🔄 FASE 4: Testes Unitários e Validação E2E [CONCLUÍDO]
- [x] Testar se o `MarkdownBuilder` gera as anotações do jeito esperado, não quebrando o formato do Obsidian (ex: espaços indevidos no Frontmatter).
- [x] Mockar a IDE usando o Inspector do FastMCP para validar as queries de escrita e leitura de forma isolada (validado via script de testes E2E).
- [x] Adotar o fluxo "no-magic": garantir que se der algum erro, os logs do MCP informem claramente a IA de forma acionável.

---

## 📈 Progresso Geral: [ 100% ]
*(Atualizado após a execução bem-sucedida de todas as fases)*
