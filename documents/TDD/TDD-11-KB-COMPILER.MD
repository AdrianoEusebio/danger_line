# 🧪 TDD-11: KB Compiler (raw/ → wiki/)

## Caso de Uso
O KB Compiler processa dados brutos da pasta `raw/` e gera/atualiza artigos estruturados na pasta `wiki/`, mantendo index e changelog.

## Pré-condições
- Provider de IA disponível
- Pasta `raw/` existe e contém pelo menos 1 arquivo
- Pasta `wiki/` existe (pode estar vazia)

## Testes

### T-11.1: Compilação incremental — novo conceito
- **Input**: Novo arquivo em `raw/analyses/2026-05-04_auth_py.md`
- **Pre-cond**: Wiki não tem artigo sobre auth
- **Expected**: Novo artigo criado em `wiki/architecture/auth_system.md`
- **Validação**: Artigo existe, contém frontmatter YAML com `compiled_from`, `tags`, `related`

### T-11.2: Compilação incremental — conceito existente
- **Input**: Novo arquivo em `raw/solutions/2026-05-05_fix_auth.md`
- **Pre-cond**: Wiki já tem `wiki/architecture/auth_system.md`
- **Expected**: Artigo existente ATUALIZADO com nova informação, não duplicado
- **Validação**: `last_compiled` atualizado, conteúdo expandido, artigo único

### T-11.3: Compilação full — rebuild completo
- **Input**: Comando `compile_knowledge(full=True)`
- **Pre-cond**: raw/ tem 10 arquivos, wiki/ tem 5 artigos
- **Expected**: Wiki reconstruído por completo, todos os artigos re-compilados
- **Validação**: Todos artigos recriados, backlinks regenerados, index.md atualizado

### T-11.4: Index.md atualizado após compilação
- **Input**: Compilação incremental com 1 novo artigo
- **Expected**: `wiki/index.md` contém referência ao novo artigo
- **Validação**: `index.md` contém `[[novo_artigo]]` na categoria correta

### T-11.5: Changelog registra ações
- **Input**: Compilação de qualquer tipo
- **Expected**: `wiki/changelog.md` registra a ação com timestamp
- **Validação**: Última entrada no changelog corresponde à ação realizada

### T-11.6: Frontmatter YAML válido
- **Input**: Artigo compilado
- **Expected**: Frontmatter contém campos obrigatórios
- **Validação**: `title`, `compiled_from`, `last_compiled`, `tags`, `related`, `confidence` presentes

### T-11.7: [[Wikilinks]] gerados automaticamente
- **Input**: Artigo sobre auth menciona "error handling" — artigo `[[Error Handling]]` existe
- **Expected**: Link `[[Error Handling]]` inserido automaticamente no artigo
- **Validação**: Artigo contém `[[Error Handling]]` e o artigo referenciado tem backlink

### T-11.8: raw/ vazio — noop
- **Input**: `compile_knowledge()` com raw/ vazio
- **Expected**: Nenhuma alteração no wiki, log de "nothing to compile"
- **Validação**: Wiki inalterado, changelog não registra ação

## Diagrama de Fluxo

```mermaid
flowchart TD
    START([compile_knowledge]) --> MODE{Full ou Incremental?}
    MODE -->|Incremental| SCAN_NEW[Scan: novos arquivos em raw/]
    MODE -->|Full| SCAN_ALL[Scan: todos arquivos em raw/]
    
    SCAN_NEW --> EMPTY{raw/ tem novos?}
    EMPTY -->|Não| NOOP[Log: nothing to compile]
    EMPTY -->|Sim| FOREACH[Para cada arquivo novo]
    
    SCAN_ALL --> FOREACH
    
    FOREACH --> EXTRACT[IA extrai conceitos-chave]
    EXTRACT --> EXISTS{Artigo existe no wiki?}
    EXISTS -->|Sim| MERGE[Merge: atualizar artigo]
    EXISTS -->|Não| CREATE[Criar novo artigo]
    
    MERGE --> LINK[Auto-gerar [[wikilinks]]]
    CREATE --> LINK
    LINK --> INDEX[Atualizar index.md]
    INDEX --> LOG[Registrar no changelog.md]
    LOG --> END([Compilação completa])
    NOOP --> END
```
