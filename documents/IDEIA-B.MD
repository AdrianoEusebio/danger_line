# 🕸️ IDEIA B — Graph Explore (Mapa Mental via MCP)

## 1. O Contexto Oculto no Obsidian
O maior trunfo do Obsidian não são as anotações isoladas, mas sim como elas se conectam através dos `[[wikilinks]]`. Uma nota sobre "Padrão de Autenticação" pode ter links para "Configuração do JWT" e "Middleware de Segurança". 

Atualmente, se a IA ler a primeira nota, ela vê que os links existem, mas não sabe o que há dentro deles.

## 2. A Nova Ferramenta MCP: `explore_graph`
A proposta é criar uma nova tool no FastMCP chamada `explore_graph(nota_origem, profundidade)`.

### O Fluxo:
1. A IA da IDE encontra um wikilink interessante: `[[Middleware de Segurança]]`.
2. Em vez de ler nota por nota, ela chama a tool `explore_graph("Padrão de Autenticação", profundidade=1)`.
3. O **Danger Line** abre a nota raiz, extrai todos os wikilinks usando Expressões Regulares (`\[\[(.*?)\]\]`), abre essas notas referenciadas, e monta um resumo condensado.
4. Ele retorna para a IA uma "árvore mental" instantânea:
   - "Essa nota se conecta a X (que fala sobre Y) e Z (que fala sobre W)".

## 3. Valor Gerado
A IA da IDE ganha a capacidade humana de "pular de link em link" de forma programática. Ela entende o contexto periférico do projeto sem consumir tokens absurdos lendo todos os arquivos de uma vez.

---
> **Status:** Pronta para implementação. Requer adição de uma nova tool ao servidor FastMCP e lógica de parser de Regex no módulo do Obsidian.
