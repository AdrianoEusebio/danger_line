# 📋 TEMPLATE — AGENT.md

> **Este é o template oficial do `AGENT.md`** que deve ser copiado para a pasta `danger_line/` de cada projeto.
> O arquivo será lido pelo KB Compiler como contexto em linguagem natural.
>
> ⚠️ Configurações estruturadas (números, paths, flags) vão em `config.toml`, não aqui.

---

## Como usar

1. Copie este template para `SeuProjeto/danger_line/AGENT.md`
2. Substitua os campos marcados com `[...]`
3. Remova as seções que não se aplicam
4. Quanto mais específico, melhor será a compilação do KB

---

# AGENT.md — [Nome do Projeto]

> Instruções customizadas para o KB Compiler do Danger Line.
> Este arquivo é injetado diretamente no contexto do LLM durante a compilação.

## Identidade do Projeto

```
Nome: [Nome do projeto]
Tipo: [Web App / Game / API / CLI / Library / ...]
Stack principal: [Ex: Python + FastAPI + PostgreSQL]
Estágio: [Desenvolvimento ativo / Manutenção / Legado]
```

## Foco de Compilação

> Diga ao compilador **o que importa** neste projeto.

Ao analisar e compilar o Knowledge Base deste projeto, priorize:

- **[Módulo ou tema 1]**: [Por quê é importante. Ex: "O sistema de auth — é o mais crítico e mais quebra"]
- **[Módulo ou tema 2]**: [Ex: "Performance das queries — temos problemas recorrentes aqui"]
- **[Módulo ou tema 3]**: [Ex: "Integração com a API externa X — documentação fraca, propenso a bugs"]

## Contexto Técnico

> Informações que a IA precisa saber que não são óbvias pelo código.

```
Decisões arquiteturais importantes:
- [Ex: "Usamos async em todo o core, nunca misturar com código síncrono"]
- [Ex: "O banco tem índices customizados — não alterar queries sem verificar"]
- [Ex: "Frontend e backend compartilham tipos via schema.ts gerado"]

Padrões do projeto:
- [Ex: "Todos os serviços seguem Repository Pattern"]
- [Ex: "Erros são sempre CustomError com código e contexto"]

Armadilhas conhecidas:
- [Ex: "O módulo X tem estado global — cuidado com race conditions"]
- [Ex: "A lib Y tem bug na versão atual, usamos workaround em utils/patch.ts"]
```

## O que NÃO documentar

> Evite poluir o wiki com informações irrelevantes.

- [Ex: "Ignorar arquivos de migração antigos em db/migrations/legacy/"]
- [Ex: "Não documentar scripts de seed, são temporários"]
- [Ex: "Ignorar todo o diretório docs/ — está desatualizado"]

## Estilo de Documentação

> Como os artigos do wiki devem ser escritos para este projeto.

```
Idioma dos artigos: [PT-BR / EN]
Nível de detalhe: [Alto (incluir exemplos de código) / Médio / Baixo (só overview)]
Formato preferido: [Seguir padrão ADR / Livre / C4 Model]
```

## Bugs Conhecidos (Inicial)

> Liste bugs conhecidos para o wiki começar rico. Remova quando resolvidos.

- `[bug-001]`: [Descrição breve] — [status: aberto/investigando/workaround aplicado]
- `[bug-002]`: [Descrição breve] — [status]

## Referências Externas

> Links que o compilador deve considerar como contexto adicional.

- Documentação oficial: [URL ou N/A]
- Repositório de referência: [URL ou N/A]
- ADRs externos: [URL ou N/A]

---

## Exemplo Preenchido

```markdown
# AGENT.md — Ribeirinho Express

## Identidade do Projeto
Nome: Ribeirinho Express
Tipo: Game (Godot 4)
Stack principal: GDScript + Godot 4.3
Estágio: Desenvolvimento ativo

## Foco de Compilação
- **Sistema de física de carga**: É o mais complexo, tem pressão + gravidade + destruição
- **Sistema de barcos**: Spawning dinâmico com 3 docas — propenso a bugs de estado
- **CargoGrid**: Lógica de validação de pedidos — regras complexas de suporte físico

## Contexto Técnico
Decisões importantes:
- "Gravitational logic roda em _physics_process, não _process"
- "Cada boat instance tem seu próprio CargoGrid isolado"
- "Pressure é calculada de cima para baixo, nunca bottom-up"

Armadilhas:
- "Boat spawning fora da tela usa posição Y negativa — não confundir com bug"

## O que NÃO documentar
- Ignorar assets/ (imagens, sons) — não relevante para o KB
- Ignorar project.godot e arquivos de config do editor

## Bugs Conhecidos
- [bug-001]: Boat às vezes não detecta ordem completa — status: investigando
```
