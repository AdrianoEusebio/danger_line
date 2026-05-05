# 🧪 TDD-13: KB Q&A Engine + Filed Back

## Caso de Uso
O Q&A Engine responde perguntas consultando o wiki compilado. O Filed Back loop garante que soluções de qualidade retornem ao raw/ para enriquecer o wiki.

## Pré-condições
- Provider de IA disponível
- Wiki existe e contém artigos compilados
- Indexer funcionando para busca por relevância

## Testes — Q&A Engine

### T-13.1: Query com match exato no wiki
- **Input**: `query_knowledge("authentication system")`
- **Pre-cond**: Wiki tem `[[Authentication System]]`
- **Expected**: Resposta com conteúdo do artigo, source citado
- **Validação**: `result.answer` contém informações do artigo, `result.sources` contém `[[Authentication System]]`

### T-13.2: Query sem match — NOT_FOUND
- **Input**: `query_knowledge("blockchain integration")`
- **Pre-cond**: Wiki não tem artigo sobre blockchain
- **Expected**: `result.answer == "NOT_FOUND"`, `result.sources == []`
- **Validação**: Não inventa informação, retorna NOT_FOUND honestamente

### T-13.3: Query com múltiplos artigos relevantes
- **Input**: `query_knowledge("error handling in auth")`
- **Pre-cond**: Wiki tem `[[Authentication System]]` e `[[Error Handling]]`
- **Expected**: Resposta sintetiza informações de AMBOS artigos
- **Validação**: `result.sources` contém ambos artigos, resposta é coerente

### T-13.4: Query para classificação — enriquecer contexto do classifier
- **Input**: `query("Known bugs or patterns related to: race condition on API")`
- **Pre-cond**: Wiki tem `[[Race Condition - Token Refresh]]` com solução
- **Expected**: Resposta inclui bug conhecido + solução aplicada
- **Validação**: Resposta referencia o bug, inclui detalhes da solução

### T-13.5: Indexer seleciona artigos relevantes (não manda tudo)
- **Input**: Wiki com 50 artigos, query sobre "auth"
- **Expected**: Indexer seleciona apenas 3-5 artigos mais relevantes para o prompt
- **Validação**: Prompt enviado ao provider contém ≤ 5 artigos, tokens < 3000

## Testes — Filed Back Loop

### T-13.6: Solução da IA potente vai para raw/
- **Input**: IA potente resolveu problema de auth com solução aprovada
- **Expected**: Arquivo criado em `raw/solutions/2026-05-04_fix_auth.md`
- **Validação**: Arquivo existe, contém problema + solução + metadata

### T-13.7: Alvará da IA potente vai para raw/
- **Input**: IA potente emitiu batch review aprovando 5 soluções
- **Expected**: Arquivo criado em `raw/reviews/2026-05-04_batch_01.md`
- **Validação**: Arquivo existe, contém todos os 5 itens revisados

### T-13.8: Filed Back trigger compilação incremental
- **Input**: Nova solução salva em raw/ via filed back
- **Expected**: KB Compiler é notificado e compila incrementalmente
- **Validação**: Wiki atualizado com informação da nova solução

### T-13.9: Filed Back não duplica informação
- **Input**: Mesma solução salva duas vezes via filed back
- **Expected**: raw/ contém dois arquivos (append-only), mas wiki MERGE não duplica
- **Validação**: Wiki tem um único artigo com informação consolidada

### T-13.10: Project Card gerado no primeiro scan
- **Input**: `get_project_card(project="NovoProjeto")` — projeto sem card
- **Expected**: Project Card auto-gerado com resumo, stack, métricas iniciais
- **Validação**: Card contém seções: Resumo, Stack, Especificações, Métricas KB (zeradas)

## Diagrama de Fluxo

```mermaid
flowchart TD
    subgraph "Q&A Engine"
        Q_START([query_knowledge]) --> INDEX[Indexer busca artigos relevantes]
        INDEX --> FOUND{Artigos encontrados?}
        FOUND -->|Sim| PROMPT[Montar prompt com artigos selecionados]
        FOUND -->|Não| NOT_FOUND[Retornar NOT_FOUND]
        PROMPT --> AI[IA Base sintetiza resposta]
        AI --> CITE[Incluir [[sources]]  na resposta]
        CITE --> Q_RESULT([QAResult])
        NOT_FOUND --> Q_RESULT
    end

    subgraph "Filed Back Loop"
        FB_START([Solução recebida]) --> QUALITY{Qualidade?}
        QUALITY -->|Aprovada pelo alvará| SAVE_RAW[Salvar em raw/solutions/]
        QUALITY -->|Review batch| SAVE_REVIEW[Salvar em raw/reviews/]
        SAVE_RAW --> NOTIFY[Notificar KB Compiler]
        SAVE_REVIEW --> NOTIFY
        NOTIFY --> COMPILE[Compilação incremental]
        COMPILE --> MERGE{Conceito existe?}
        MERGE -->|Sim| UPDATE[Merge no artigo existente]
        MERGE -->|Não| CREATE[Criar novo artigo]
        UPDATE --> DONE([Wiki atualizado])
        CREATE --> DONE
    end
```
