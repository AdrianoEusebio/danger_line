# 🚀 ROADMAP TDD — DANGER LINE (Refatoração v5.0)

Este documento dita o plano de construção modular baseado na arquitetura v5.0 (DragonScale MCP Edition), focada em portabilidade máxima de lógica para Python e testes unitários automatizados.

---

## 🟢 FASE 1: Limpeza e Fundação Base [CONCLUÍDO]
- [x] **Limpeza de Módulos Legados**: Deletar providers, classificação de estrelas, Context Manager e Sanitizer.
- [x] **Ajuste da Estrutura de Diretórios**: Definir o padrão `/src/modules/mcp/` e `/src/modules/obsidian/`.
- [x] **Atualização das Dependências**: Reduzir bibliotecas focando no FastMCP e utilitários básicos.

## 🟢 FASE 2: Engine do Obsidian (Classes Reutilizáveis) [CONCLUÍDO]
- [x] **Classe `ObsidianVaultManager`**: Desenvolver classe padrão que resolve o path do vault e lida de forma segura com acesso I/O de diretórios.
- [x] **Classe `MarkdownBuilder` / Parser**: Utilitário dedicado para gerar templates consistentes com Frontmatter YAML e formatação de metadados.
- [x] **Lógica de Busca Simples**: Sistema rápido para varrer o vault por tags ou títulos que a IDE requisitar.

## 🟢 FASE 3: Interface MCP Enxuta e "Graph Explore" [CONCLUÍDO]
- [x] **Implementar Tool `query_kb(query, tags)`**: Expõe a lógica de busca do Obsidian baseada em Tags Semânticas, retornando notas consolidadas de 500 caracteres.
- [x] **Implementar Tool `commit_knowledge`**: Interface para a IA criar e atualizar manuais/bugs no Obsidian com validação rigorosa e YAML obrigatório.
- [x] **Implementar Tool `explore_graph`**: Rastreia todos os wikilinks de uma nota de partida gerando um resumo de conexões.
- [x] **Implementar Project Rules via Resources**: Expor dinamicamente diretrizes de projetos como um resource MCP baseado na pasta local ativa.

## 🟢 FASE 4: Testes Unitários e Validação E2E [CONCLUÍDO]
- [x] Testar se o `MarkdownBuilder` gera as anotações sem corromper metadados ou wikilinks.
- [x] Mockar chamadas MCP usando ferramentas de teste para validar as queries de escrita e leitura de forma isolada.
- [x] Adotar fluxo de logs acionáveis de erro no MCP.

## 🟡 FASE 5: Linter de Integridade e Hot Cache (Portados) [A FAZER]
- [ ] **Classe `Linter` (`src/core/linter.py`)**: Implementar algoritmo para detectar links mortos (`[[Nota]]` apontando para arquivo inexistente), páginas órfãs (sem backlinks) e metadados ausentes no YAML.
- [ ] **Tool MCP `lint_kb`**: Criar interface MCP que roda o linter e exporta o relatório de integridade estruturada em `wiki/meta/lint-report-YYYY-MM-DD.md`.
- [ ] **Módulo `Hot Cache`**: Implementar no orquestrador a escrita/sincronização do arquivo `wiki/hot.md` com os metadados das 10 últimas interações de forma rotativa para economia de tokens.
- [ ] **Testes de Integridade (`tests/test_linter.py`)**: Validar a detecção lógica de órfãos e referências quebradas com arquivos mockados em diretórios temporários.

## 🟡 FASE 6: DragonScale Memory Core em Python [A FAZER]
- [ ] **Portar Sequenciador de Endereços (`c-NNNNNN`)**: Implementar alocação de IDs em Python puro dentro do orquestrador de gravação. Usar a biblioteca `portalocker` para travar `.vault-meta/address-counter.txt` de forma segura no Windows e Linux.
- [ ] **Portar Linter Semântico de Cosseno (Tiling)**: Escrever módulo Python que conecta via HTTP com a API local do Ollama (`nomic-embed-text`) para computar embeddings das notas e calcular similaridade de cosseno de pares de páginas, rejeitando duplicidades semânticas em tempo de gravação.
- [ ] **Portar Grafo de Fronteira (Boundary Scorer)**: Implementar a fórmula `(out_degree - in_degree) * recency_weight` para identificar as notas periféricas e listar agendas de pesquisa.
- [ ] **Portar Compactador de Logs (Folds)**: Implementar rollup de alteração de logs em resumos no diretório `/wiki/folds/` a partir do histórico acumulado.
- [ ] **Testes Unitários da Memória (`tests/test_dragonscale.py`)**: Garantir estabilidade de concorrência com travas, cálculos de cosseno e geração de grafos matemáticos.

---

## 📈 Progresso Geral: [ 66% ]
*(Atualizado com a inclusão das Fases 5 e 6 de evolução de portabilidade)*
