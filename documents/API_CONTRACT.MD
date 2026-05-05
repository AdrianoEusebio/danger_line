# 📄 API CONTRACT — MCP Tools

> Contrato formal das tools expostas via MCP pelo Danger Line v2.
> Todas as tools são `async`. Erros retornam string com prefixo `ERROR:`.

---

## Convenções

```
Input types:  str, int, bool, list[str]
Output type:  str (sempre — MCP retorna texto)
Error format: "ERROR: {code} — {message}"
Path safety:  todos os paths são validados contra o workspace configurado
```

---

## Tools de Análise

### `analyze_file`

```
Descrição : Analisa um arquivo de código e retorna resumo otimizado para IA.
            Salva automaticamente em cache e raw/.

Parâmetros:
  path: str         — Path relativo ao workspace (ex: "src/auth.py")

Retorno: str
  Resumo estruturado EN com seções:
  - FILE INFO (language, size, dependencies)
  - ARCHITECTURE (patterns, responsibilities)
  - KEY FUNCTIONS (list)
  - ISSUES DETECTED (if any)
  - CLASSIFICATION HINT (estimated difficulty)

Erros:
  ERROR: PATH_OUTSIDE_WORKSPACE — path não está dentro do workspace
  ERROR: FILE_NOT_FOUND        — arquivo não existe
  ERROR: PROVIDER_UNAVAILABLE  — nenhum provider de IA disponível

Efeitos colaterais:
  ✅ Cria/atualiza cache em danger_line/cache/{hash}.json
  ✅ Append em danger_line/raw/analyses/{date}_{filename}.md
  ✅ Incrementa compile_count (pode disparar lint_quick automático)
```

---

### `analyze_project`

```
Descrição : Mapeia e analisa a estrutura de um projeto completo.
            Usado no scan inicial (Opção C Híbrido: estrutura + card + 5 arquivos-chave).

Parâmetros:
  path  : str  — Path do projeto (default: workspace atual)
  depth : int  — Profundidade do scan (default: 2, max: 5)
  full  : bool — Se True, analisa os 5 arquivos-chave em profundidade (~3000 tokens)

Retorno: str
  - PROJECT OVERVIEW (name, language, framework, file count)
  - DIRECTORY STRUCTURE (árvore filtrada)
  - KEY FILES (5 arquivos mais centrais identificados)
  - DEPENDENCIES (principais deps detectadas)
  - INITIAL ASSESSMENT (complexidade geral)

Erros:
  ERROR: PATH_OUTSIDE_WORKSPACE
  ERROR: NOT_A_DIRECTORY       — path não é uma pasta
  ERROR: PROVIDER_UNAVAILABLE

Efeitos colaterais:
  ✅ Gera Project Card no Obsidian vault (se full=True)
  ✅ Cria estrutura danger_line/ no projeto (se não existir)
```

---

## Tools de Classificação

### `classify_problem`

```
Descrição : Classifica a dificuldade de um problema (1-3★).
            Consulta o KB (wiki) antes de classificar para possível reclassificação.

Parâmetros:
  description : str       — Descrição do problema em linguagem natural
  files       : list[str] — Arquivos relevantes (opcional, melhora precisão)

Retorno: str (JSON)
  {
    "difficulty": 1 | 2 | 3,
    "confidence": 0.0-1.0,
    "category": "syntax|logic|architecture|performance|security|config",
    "reasoning": "...",
    "wiki_match": "[[Article Name]]" | null,
    "recommended_action": "resolve_locally|ask_user|escalate"
  }

Erros:
  ERROR: PROVIDER_UNAVAILABLE
  ERROR: INVALID_DESCRIPTION  — descrição vazia ou muito curta (<10 chars)

Efeitos colaterais:
  ✅ Consulta wiki via Q&A Engine (leitura apenas)
  ✅ Registra classificação em danger_line/raw/classifications/
```

---

### `get_optimized_context`

```
Descrição : Gera um super-prompt otimizado para envio à IA premium.
            Combina análise de arquivos + contexto do KB + problema do usuário.

Parâmetros:
  problem : str       — Problema ou pergunta do usuário
  files   : list[str] — Arquivos relevantes para incluir no contexto

Retorno: str
  Super-prompt formatado seguindo o padrão:
  ### CONTEXT ARCHITECTURE — DANGER LINE AGENT ###
  ... (ver DOCUMENTO_PROJETO.MD §4.2)

Erros:
  ERROR: PROVIDER_UNAVAILABLE
  ERROR: CONTEXT_TOO_LARGE — contexto excede limite seguro (>50K chars)

Efeitos colaterais:
  ✅ Pode chamar analyze_file internamente (com cache)
  ✅ Consulta wiki via Q&A Engine
```

---

## Tools de Knowledge Base

### `compile_knowledge`

```
Descrição : Compila os dados brutos de raw/ em artigos wiki estruturados.

Parâmetros:
  full : bool — Se True, re-compila tudo. Se False (default), apenas novos arquivos.

Retorno: str
  COMPILATION REPORT:
  - Articles created: N
  - Articles updated: N
  - Links generated: N
  - Time elapsed: Xs
  - Tokens used: N

Erros:
  ERROR: PROVIDER_UNAVAILABLE
  ERROR: RAW_EMPTY             — nada para compilar
  ERROR: COMPILATION_PARTIAL   — compilação falhou após N artigos (com rollback)

Efeitos colaterais:
  ✅ Cria/atualiza artigos em Obsidian vault/projects/{project}/wiki/
  ✅ Atualiza index.md e changelog.md
  ✅ Incrementa compile_count (pode disparar lint_quick)
  ⚠️ Em caso de falha: rollback automático, wiki mantido em estado anterior
```

---

### `query_knowledge`

```
Descrição : Realiza Q&A sobre o wiki compilado do projeto.

Parâmetros:
  query   : str — Pergunta em linguagem natural
  project : str — Nome do projeto (default: workspace atual)

Retorno: str
  ANSWER: {resposta sintetizada dos artigos relevantes}
  SOURCES: [[Artigo1]], [[Artigo2]]
  
  Ou: "NOT_FOUND: No relevant articles found for this query."

Erros:
  ERROR: PROVIDER_UNAVAILABLE
  ERROR: WIKI_EMPTY — wiki não tem artigos compilados ainda

Efeitos colaterais:
  Nenhum — operação de leitura apenas
```

---

### `lint_wiki`

```
Descrição : Executa health check completo do wiki (hot-update manual).
            Roda todos os 4 checks: INCONSISTENCY, MISSING, STALE, CONNECTION.

Parâmetros:
  project : str — Nome do projeto (default: workspace atual)

Retorno: str
  🔍 WIKI LINT REPORT — Health Score: X%
  ⚠️  INCONSISTENCY: {N issues}
  📋  MISSING: {N suggestions}
  ⏰  STALE: {N articles}
  🔗  CONNECTION: {N suggestions}
  
  DETAILS: [lista de issues e sugestões]

Erros:
  ERROR: PROVIDER_UNAVAILABLE
  ERROR: WIKI_EMPTY

Efeitos colaterais:
  Nenhum — operação de leitura apenas (nunca modifica o wiki)
```

---

### `get_project_card`

```
Descrição : Retorna o Project Card do projeto. Se não existir, gera um novo
            (deep scan, ~3000 tokens, salvo no Obsidian).

Parâmetros:
  project : str — Nome do projeto (default: workspace atual)

Retorno: str
  Conteúdo do Project Card em Markdown:
  - Resumo, Stack, Especificações Técnicas
  - Bugs Conhecidos, Métricas KB

Erros:
  ERROR: PROVIDER_UNAVAILABLE — apenas se precisar gerar (card não existe)
  ERROR: PROJECT_NOT_FOUND    — projeto não registrado no sistema

Efeitos colaterais:
  ✅ Se card não existe: gera e salva em Obsidian vault
  ✅ Se card existe: retorna sem custo de tokens
```

---

### `get_known_patterns`

```
Descrição : Lista patterns de código detectados no wiki do projeto.

Parâmetros:
  project  : str — Nome do projeto (default: workspace atual)
  category : str — Filtro opcional ("auth|error|performance|...")

Retorno: str
  Lista de patterns com links para artigos do wiki:
  - [[Repository Pattern]] — detectado em 5 módulos
  - [[Error Boundary]] — detectado em 3 módulos

Efeitos colaterais:
  Nenhum — leitura apenas
```

---

### `get_known_bugs`

```
Descrição : Lista bugs conhecidos e soluções do wiki do projeto.

Parâmetros:
  project : str  — Nome do projeto (default: workspace atual)
  status  : str  — Filtro: "open|resolved|all" (default: "all")

Retorno: str
  Lista de bugs com status e link para artigo:
  🔴 [bug-001] Race condition on token refresh — [[Race Condition - Token Refresh]]
  ✅ [bug-002] Missing validation on /users — resolved 2026-05-01

Efeitos colaterais:
  Nenhum — leitura apenas
```

---

## Tools de Métricas

### `get_metrics`

```
Descrição : Retorna métricas completas de tokens e Knowledge Base da sessão atual.

Parâmetros:
  period : str — "session|week|month|all" (default: "session")

Retorno: str
  TOKEN METRICS:
  - Saved: N tokens (X%)
  - Base AI (Groq): N tokens
  - Premium AI: N tokens
  - Estimated without DL: N tokens

  DISTRIBUTION:
  - 1★: N problems (X%)
  - 2★: N problems (X%)
  - 3★: N problems (X%)

  KNOWLEDGE BASE:
  - Articles: N
  - Knowledge Score: X%
  - KB Hits: N
  - Wiki Health: X% (last lint: date)

Efeitos colaterais:
  Nenhum — leitura apenas
```

---

## Tools de Configuração

### `set_workspace`

```
Descrição : Define ou troca o workspace ativo.

Parâmetros:
  path : str — Path absoluto do projeto

Retorno: str
  "Workspace set to: {path}
   Project: {project_name}
   KB Status: {articles} articles, {score}% coverage"

Erros:
  ERROR: PATH_NOT_FOUND    — diretório não existe
  ERROR: NOT_A_DIRECTORY

Efeitos colaterais:
  ✅ Atualiza workspace no config da sessão
  ✅ Carrega AGENT.md do projeto (se existir)
```

---

## Códigos de Erro Completos

| Código | Descrição |
|--------|-----------|
| `PATH_OUTSIDE_WORKSPACE` | Path tenta sair do workspace (path traversal) |
| `FILE_NOT_FOUND` | Arquivo não encontrado |
| `NOT_A_DIRECTORY` | Path é arquivo, não pasta |
| `PROJECT_NOT_FOUND` | Projeto não registrado |
| `PROVIDER_UNAVAILABLE` | Nenhuma IA base disponível (Groq, Gemini, Ollama) |
| `CONTEXT_TOO_LARGE` | Contexto gerado excede limite seguro |
| `RAW_EMPTY` | Pasta raw/ vazia, nada para compilar |
| `WIKI_EMPTY` | Wiki sem artigos compilados |
| `COMPILATION_PARTIAL` | Compilação falhou parcialmente (rollback aplicado) |
| `INVALID_DESCRIPTION` | Input muito curto ou vazio |
