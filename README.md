# 🔴 DANGER LINE v2

> Sistema administrativo e assistente com IA base para buscas e resumos — otimizador de tokens para IAs premium.

---

## O que é

O **Danger Line** é uma camada de pré-processamento inteligente que usa IAs gratuitas (Groq, Gemini Flash) para analisar, classificar e resumir código **antes** de enviar apenas o essencial para sua IA paga. O resultado é uma economia de **50-70% de tokens** sem perda de qualidade.

```
Você → Danger Line (IA gratuita) → Contexto otimizado → Antigravity (IA premium)
```

Além disso, o sistema constrói um **Knowledge Base pessoal** (método Karpathy) que aprende com cada análise, tornando respostas futuras mais rápidas e baratas.

---

## Funcionalidades

| Funcionalidade | Descrição |
|---------------|-----------|
| 🔍 **Análise de código** | Analisa arquivos e projetos com IA base gratuita |
| ⭐ **Classificação 1-3★** | Decide automaticamente se o problema precisa de IA premium |
| 📝 **Contexto otimizado** | Gera super-prompts compactos para a IA premium |
| 📚 **Knowledge Base** | Wiki compilada que lembra análises e soluções anteriores |
| 🔌 **MCP Server** | Integração nativa com Antigravity IDE |
| 📊 **Dashboard** | Painel de métricas de economia de tokens no terminal |

---

## Pré-requisitos

| Dependência | Versão | Obrigatório |
|-------------|--------|-------------|
| Python | 3.11+ | ✅ |
| uv | latest | ✅ |
| Obsidian | 1.5+ | ✅ (IDE do Knowledge Base) |
| Antigravity IDE | latest | ⬜ (para MCP) |
| Ollama | 0.5+ | ⬜ (para LLM local offline) |

---

## Instalação

```bash
# 1. Clonar o repositório
git clone <repo-url>
cd Danger_line

# 2. Instalar dependências com uv
uv sync

# 3. Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas chaves:
# GROQ_API_KEY=...
# OBSIDIAN_VAULT_PATH=C:/Users/adria/OneDrive/Documentos/Danger_line/Danger Line
```

---

## Configuração do MCP no Antigravity

Edite `C:\Users\adria\.gemini\antigravity\mcp_config.json`:

```json
{
  "mcpServers": {
    "danger-line": {
      "command": "python",
      "args": ["src/mcp/server.py"],
      "cwd": "C:/path/to/Danger_line"
    }
  }
}
```

> [!TIP]
> Use o campo `cwd` para definir a raiz do projeto. O sistema carregará automaticamente o arquivo `.env` da raiz, não sendo mais necessário passar as chaves de API diretamente no JSON.

Reinicie o Antigravity. O sistema detecta as tools automaticamente.

---

## Configurar um Projeto

Ao usar o Danger Line em um projeto pela primeira vez:

```
# Via MCP (no Antigravity):
"Registre o projeto em C:/MeuProjeto"

# O sistema automaticamente:
# 1. Cria uma pasta segura em Danger_line/storage/MeuProjeto_hash/ (Zero Footprint no seu projeto!)
# 2. Gera config.toml e AGENT.md no storage centralizado
# 3. Faz scan inicial (~3000 tokens, único)
# 4. Cria Project Card no Obsidian vault
```

Sua estrutura de pastas original permanece **limpa**. Todos os dados ficam em:
`Danger_line/storage/{nome_projeto}_{hash}/`

```
storage/MeuProjeto_hash/
├── .gitignore
├── AGENT.md        ← instruções customizadas para o compilador
├── config.toml     ← configurações do projeto
├── raw/            ← dados brutos (append-only, não editar)
└── cache/          ← cache de análises (gerado automaticamente)
```

> Ver `documents/TEMPLATE_AGENTE.MD` para o template do `AGENT.md`.

---

## Uso via MCP (Antigravity)

Uma vez configurado, use naturalmente no Antigravity:

```
"Analise o bug no auth.py"
→ Danger Line analisa, classifica como 2★, gera contexto otimizado

"Qual é a arquitetura do módulo de pagamentos?"
→ Danger Line consulta o Knowledge Base, retorna contexto rico

"Mostre as métricas de economia desta semana"
→ Danger Line exibe tokens economizados, KB coverage, wiki health
```

---

## Uso via CLI

```bash
# Analisar um arquivo
uv run python src/main.py analyze src/auth.py

# Ver painel de métricas
uv run python src/main.py dashboard

# Compilar Knowledge Base manualmente
uv run python src/main.py compile

# Lint do wiki (hot-update)
uv run python src/main.py lint
```

---

## Estrutura do Projeto

```
Danger_line/
├── src/
│   ├── main.py                 # Entry point CLI
│   ├── cli/                    # Interface terminal
│   ├── core/
│   │   ├── analyzer.py         # Análise de código
│   │   ├── classifier.py       # Classificação 1-3★
│   │   ├── summarizer.py       # Resumos otimizados
│   │   ├── prompt_builder.py   # Super-prompts
│   │   └── knowledge/          # Knowledge Base (Karpathy)
│   │       ├── compiler.py
│   │       ├── qa_engine.py
│   │       ├── linter.py
│   │       ├── indexer.py
│   │       ├── linker.py
│   │       └── feedback.py
│   ├── providers/              # Groq, Gemini, Ollama
│   ├── storage/                # Markdown, Obsidian, Cache
│   ├── mcp/                    # MCP Server (FastMCP)
│   └── metrics/                # Token Tracker
├── documents/                  # Documentação arquitetural
│   └── TDD/                    # Test-driven design (13 TDDs)
├── tests/                      # Testes automatizados
├── pyproject.toml
└── .env
```

---

## Documentação Técnica

| Documento | Conteúdo |
|-----------|----------|
| [RESUMO_PROJETO.MD](documents/RESUMO_PROJETO.MD) | Visão executiva |
| [FICHA_TECNICA.MD](documents/FICHA_TECNICA.MD) | Stack, requisitos, riscos |
| [DOCUMENTO_PROJETO.MD](documents/DOCUMENTO_PROJETO.MD) | Arquitetura completa |
| [IDEIA-1 a IDEIA-6](documents/) | Detalhamento de cada feature |
| [API_CONTRACT.MD](documents/API_CONTRACT.MD) | Contrato das MCP tools |
| [TEMPLATE_AGENTE.MD](documents/TEMPLATE_AGENTE.MD) | Template do AGENT.md |
| [TDD/](documents/TDD/) | 13 TDDs, 89+ testes |

---

## Licença

Privada — uso pessoal.
