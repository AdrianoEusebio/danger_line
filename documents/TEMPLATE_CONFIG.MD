# 📋 TEMPLATE — config.toml

> Schema e template do arquivo `config.toml` que vai em cada projeto, dentro de `danger_line/config.toml`.
> Este arquivo é lido diretamente pelo Python (sem LLM). Para instruções em linguagem natural, use `AGENT.md`.

---

## Schema Completo

```toml
# =============================================================================
# DANGER LINE — Configuração do Projeto
# Gerado automaticamente em: danger_line/config.toml
# =============================================================================

[project]
# Nome do projeto (preenchido automaticamente no primeiro scan)
name = "NomeDoProjeto"

# Path absoluto do projeto
path = "C:/Users/adria/OneDrive/Área de Trabalho/PROJETOS/NomeDoProjeto"

# Linguagem(ns) principal(is) detectada(s)
language = ["python"]           # Exemplos: ["python"], ["gdscript"], ["typescript", "python"]

# Framework detectado (ou "none")
framework = "fastapi"           # Exemplos: "fastapi", "godot4", "nextjs", "none"

# Data do primeiro registro (ISO 8601)
registered_at = "2026-05-05T00:00:00"

# Data da última análise
last_analyzed = "2026-05-05T00:00:00"

# =============================================================================
[knowledge_base]
# =============================================================================

# Intervalo de compilações até disparar lint_quick automático (default: 10)
lint_interval = 10

# Profundidade do scan inicial (Opção C Híbrido)
# "quick" = estrutura + card + 5 arquivos (~3000 tokens, 1x)
# "full"  = todos os arquivos (alto custo inicial)
initial_scan_depth = "quick"

# Número de arquivos-chave para analisar no scan inicial
key_files_count = 5

# Tempo máximo (dias) antes de um artigo ser considerado "stale"
stale_threshold_days = 30

# =============================================================================
[providers]
# =============================================================================

# Provider primário para este projeto
# "groq" | "gemini" | "ollama" | "auto" (segue a chain padrão)
primary = "auto"

# Modelo preferido do Groq para análises profundas deste projeto
groq_model_deep = "llama-3.3-70b-versatile"

# Modelo preferido do Groq para classificação rápida
groq_model_fast = "llama-3.1-8b-instant"

# =============================================================================
[compilation]
# =============================================================================

# Arquivos e pastas a IGNORAR durante análise e compilação
# Padrões glob — adicionados ao .gitignore implícito do scanner
ignore = [
    "node_modules/",
    "__pycache__/",
    "*.pyc",
    ".git/",
    "dist/",
    "build/",
    "*.min.js",
    "migrations/legacy/",    # Exemplo: ignorar migrations antigas
]

# Arquivos prioritários — analisados primeiro e com mais profundidade
priority_files = [
    # Exemplos — substitua pelos arquivos mais importantes do seu projeto:
    # "src/main.py",
    # "src/core/agent.py",
    # "src/mcp/server.py",
]

# Extensões de arquivo a incluir na análise
include_extensions = [
    ".py", ".ts", ".js", ".tsx", ".jsx",
    ".go", ".rs", ".gd",              # GDScript (Godot)
    ".md",                             # Documentação inline
]

# =============================================================================
[metrics]
# =============================================================================

# Contagem de compilações desde o último lint (persistido entre sessões)
compile_count = 0

# Total de análises realizadas neste projeto
total_analyses = 0

# Total de KB hits (wiki evitou análise completa)
total_kb_hits = 0

# Data do último lint
last_lint = ""
```

---

## Campos Obrigatórios vs Opcionais

| Campo | Obrigatório | Default | Descrição |
|-------|:-----------:|---------|-----------|
| `project.name` | ✅ | — | Preenchido no primeiro scan |
| `project.path` | ✅ | — | Preenchido no primeiro scan |
| `knowledge_base.lint_interval` | ❌ | `10` | Compilações entre lints automáticos |
| `knowledge_base.initial_scan_depth` | ❌ | `"quick"` | Profundidade do scan inicial |
| `knowledge_base.stale_threshold_days` | ❌ | `30` | Dias para artigo ser stale |
| `providers.primary` | ❌ | `"auto"` | Provider padrão do projeto |
| `compilation.ignore` | ❌ | `[]` | Paths a ignorar |
| `compilation.priority_files` | ❌ | `[]` | Arquivos analisados primeiro |
| `metrics.compile_count` | ✅ | `0` | Persistido automaticamente |

---

## Exemplo Preenchido — Ribeirinho Express (Godot)

```toml
[project]
name = "Ribeirinho Express"
path = "C:/Users/adria/OneDrive/Área de Trabalho/PROJETOS/RibeirinoExpress"
language = ["gdscript"]
framework = "godot4"
registered_at = "2026-05-05T00:00:00"
last_analyzed = "2026-05-05T00:00:00"

[knowledge_base]
lint_interval = 5        # Projeto ativo — lint mais frequente
initial_scan_depth = "quick"
key_files_count = 5
stale_threshold_days = 14  # Código muda rápido, stale em 2 semanas

[providers]
primary = "auto"
groq_model_deep = "llama-3.3-70b-versatile"
groq_model_fast = "llama-3.1-8b-instant"

[compilation]
ignore = [
    ".godot/",
    "*.import",
    "*.uid",
    "assets/audio/",
    "assets/art/",
]
priority_files = [
    "scripts/cargo_grid.gd",
    "scripts/boat_controller.gd",
    "scripts/dock_manager.gd",
    "scripts/physics_engine.gd",
    "scripts/game_manager.gd",
]
include_extensions = [".gd", ".md"]

[metrics]
compile_count = 0
total_analyses = 0
total_kb_hits = 0
last_lint = ""
```
