# 🐉 ESPECIFICAÇÃO DRAGONSCALE MEMORY (Python/MCP)

Este documento especifica a portabilidade e adaptação dos mecanismos de gerenciamento e estruturação de conhecimento do `claude-obsidian` para a arquitetura portátil e robusta em Python do **Danger Line v5.0**.

---

## Mecanismo 1: Fold Operator (Rollup de Logs)

O histórico cronológico de transações (`wiki/log.md`) cresce indefinidamente a cada gravação. O **Fold Operator** agrupa e condensa as últimas `2^k` entradas do log em resumos analíticos adicionais de alto nível salvos na pasta `/wiki/folds/`.

### Especificação da Implementação:
1. **Identificador Determinístico:** Cada fold recebe um nome de arquivo estável baseado no seu intervalo temporal e quantidade de logs:
   `fold-k{K}-from-{DATA_INICIAL}-to-{DATA_FINAL}-n{COUNT}.md`
2. **Imutabilidade e Adição:** O compactador lê os logs, extrai os principais temas abordados e gera o resumo. Ele **não deleta** os logs originais (append-only); apenas consolida a informação para acelerar buscas analíticas futuras.
3. **Escrita no Python:** Implementado em `src/core/dragonscale.py` na classe `FoldsManager`.

---

## Mecanismo 2: Deterministic Page Addresses (Endereços Estáveis)

Para evitar a quebra de links no Obsidian e referências soltas em reestruturações de pastas ou renomeações de notas, cada página conceitual recebe um identificador serial permanente em seu YAML frontmatter.

```yaml
---
tipo: concept
title: "Autenticação OAuth2"
address: c-000042
---
```

### Especificação da Implementação:
1. **Controle de Concorrência Multiplataforma (Windows/Linux):**
   * Em sistemas Unix, usa-se o comando `flock`. Para garantir a portabilidade completa no Windows, utilizamos a biblioteca Python **`portalocker`** para obter travas de arquivo exclusivas e seguras ao ler/incrementar o arquivo `.vault-meta/address-counter.txt`.
2. **Manifesto de Mapeamento:**
   * O mapeamento entre caminhos físicos e endereços é armazenado no arquivo `.raw/.manifest.json` na chave `address_map`:
     ```json
     {
       "address_map": {
         "wiki/concepts/Autenticacao.md": "c-000042"
       }
     }
     ```
   * **Regra de Reuso:** Se um arquivo for renomeado ou re-ingerido, a classe `AddressAllocator` consulta o manifesto e herda o mesmo ID, em vez de alocar um ID novo.

---

## Mecanismo 3: Semantic Tiling (Prevenção de Duplicidades)

O linter semântico compara o conteúdo das notas para identificar notas com conceitos quase idênticos salvas sob títulos diferentes, alertando a IDE.

### Especificação da Implementação:
1. **Integração HTTP Local com Ollama:**
   * O Danger Line faz requisições POST para o serviço local do Ollama (`http://127.0.0.1:11434/api/embeddings`) utilizando o modelo `nomic-embed-text` para computar vetores de 768 dimensões para o corpo de cada nota Markdown.
2. **Cache Incremental com Hash de Conteúdo:**
   * Para evitar custos computacionais redundantes de re-embeddings, guardamos os vetores calculados em `.vault-meta/tiling-cache.json` com a chave hash `sha256(model + body)`. Alterações em metadados do YAML não invalidam o cache.
3. **Cálculo Matemático de Cosseno:**
   * O script calcula a similaridade de cosseno de todos os pares de notas ativas:
     $$\text{similarity} = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|}$$
   * **Banda de Erro ($\ge 0.90$):** Considerado duplicata óbvia. Gera erro e bloqueio preventivo antes de persistir a escrita.
   * **Banda de Revisão ($0.80 - 0.90$):** Considerado sobreposição parcial de ideias. Sugere revisão de mesclagem humana.

---

## Mecanismo 4: Boundary-First Autoresearch (Grafo de Conexões)

Mapeia a topologia da base de conhecimento gerada pelas relações de links internos do Obsidian (`[[wikilinks]]`).

### Especificação da Implementação:
1. **Construção do Grafo:**
   * Varre a pasta `/wiki` extraindo os links com a regex `\[\[([^\]|]+)(?:\|[^\]]+)?\]\]` e cria uma representação de grafo direcionado na memória.
2. **Fórmula de Pontuação de Fronteira:**
   * Para cada página $p$, o Danger Line calcula o score da fronteira do conhecimento:
     $$\text{boundary\_score}(p) = (\text{out\_degree}(p) - \text{in\_degree}(p)) \times \text{recency\_weight}(p)$$
   * **Significado:** Uma página com alto score aponta para muitas páginas/conceitos sugeridos (grau de saída alto), mas foi pouco referenciada por outras notas consolidadas (grau de entrada baixo). Isso indica um tópico periférico que precisa de pesquisa ativa e aprofundamento.
   * O resultado é exposto como uma lista ordenada que a IDE pode consumir para preencher gaps no cérebro digital de forma autônoma.
