# ❓ DÚVIDAS — DANGER LINE (Refatoração 4.0)

## 1. Dúvidas sobre a Nova Estrutura Obsidian

### Q-01: Sem os "múltiplos cérebros" de Backend/Frontend, como a IA acha a coisa certa?
**R**: Confiamos na inteligência sistêmica da IA da IDE (Antigravity). Quando ela pesquisa `query_kb("autenticação backend")`, nós apenas precisamos ter arquivos e nomes bem organizados. A IA atual consegue entender o contexto global sem precisar ser forçada a uma "caixa" de stack.

### Q-02: Como vamos lidar com metadados?
**R**: A ideia é criar uma classe `MarkdownBuilder` reutilizável que force sempre a injeção de propriedades consistentes (Data, Autor, Tags) no Frontmatter do YAML, garantindo que tudo fique localizável tanto para scripts futuros quanto para o usuário via Dataview.

## 2. Novas Ideias para o Futuro Próximo

### Ideia A: Tags Semânticas em vez de Pastas Rígidas
Em vez de depender de diretórios físicos engessados, podemos colocar quase todas as anotações em diretórios de nível superior (ex: `/Notas`) e abusar do sistema de propriedades do Obsidian. A IA escreve `#backend`, `#auth`, `#bugfix` nos arquivos, permitindo cruzamentos incríveis no Graph View.

### Ideia B: Ferramenta de "Graph Explore" via MCP
Em vez de só ler arquivos, e se o Danger Line pudesse extrair os links dentro de um documento Markdown específico e dizer à IA quais outras anotações estão fortemente ligadas a ele? O Danger Line processa a regex `\[\[(.*?)\]\]` e cria um mapa mental instantâneo para o Antigravity navegar.

### Ideia C: Regras por Projetos (Project-specific Rules)
Se o Danger Line já gerencia o Obsidian do desenvolvedor, podemos armazenar no Obsidian regras como: "No projeto `XPTO`, não utilize `for` loops, utilize `.map()`". O Danger Line poderia exportar um resource MCP automático, então sempre que a IA entra na pasta do projeto XPTO, ela lê o resource associado.

## 3. Próximos Passos de Decisão

- [ ] Validar se precisamos manter a limpeza de dados sensíveis (Sanitizer) internamente, ou apenas pedir via system-prompt para o Antigravity não registrar chaves e senhas no Obsidian.
- [ ] Construir as classes fundamentais `ObsidianVaultManager` (para manipulação de arquivos) no diretório `/src/modules/obsidian/`.
- [ ] Definir o template estrito do YAML gerado quando usarmos a tool `commit_knowledge`.
