# 💡 IDEIA 2 — Direcionamento a Pasta Específica + MCP Server

## Conceito

O sistema será direcionado a uma **pasta/workspace específica**, podendo funcionar de duas formas:
1. **MCP Server**: Integrado diretamente ao Antigravity como uma ferramenta nativa
2. **CLI Standalone**: Linkado a um workspace para uso independente

## MCP Server — A Melhor Opção

### O que é MCP?

O **Model Context Protocol** é um protocolo padronizado (tipo "USB-C para IAs") que permite que LLMs acessem ferramentas externas de forma segura. Quando configurado:

- O Antigravity vê as tools do Danger Line como **ferramentas nativas**
- Pode chamá-las automaticamente quando achar relevante
- O Danger Line roda como um processo separado, comunicando via `stdio`

### Como Funciona na Prática

```
Usuário no Antigravity: "Analise o bug no auth.py do meu projeto"
         │
         ▼
Antigravity (Gemini/Claude): "Vou usar a tool analyze_file do Danger Line"
         │
         ▼
Danger Line MCP Server: Analisa com Groq → Retorna contexto otimizado
         │
         ▼
Antigravity: Usa o contexto otimizado para resolver o problema
```

### Configuração do Workspace

O MCP Server recebe o `WORKSPACE_PATH` como variável de ambiente, definindo qual pasta ele analisa.

## Passos Técnicos

### Passo 1: Criar MCP Server com FastMCP
```python
# src/mcp/server.py
from mcp.server.fastmcp import FastMCP
import os

mcp = FastMCP("DangerLine")
WORKSPACE = os.getenv("WORKSPACE_PATH", ".")

@mcp.tool()
def analyze_file(path: str) -> str:
    """Analyze a source code file and return an optimized summary for AI consumption.
    
    Args:
        path: Relative path to the file within the workspace
    """
    full_path = os.path.join(WORKSPACE, path)
    # ... análise com IA base
    return optimized_context

@mcp.tool()
def analyze_project(depth: int = 3) -> str:
    """Map and analyze the entire project structure.
    
    Args:
        depth: How deep to traverse the directory tree
    """
    # ... mapear projeto
    return project_summary

@mcp.tool()
def classify_problem(description: str, files: list[str] = []) -> str:
    """Classify a coding problem by difficulty (1-3 stars).
    
    Args:
        description: Description of the problem
        files: Relevant file paths
    """
    # ... classificar com IA base
    return classification_result

@mcp.tool()
def get_metrics() -> str:
    """Get token usage metrics and savings report."""
    return metrics_report

if __name__ == "__main__":
    mcp.run()
```

### Passo 2: Configurar no Antigravity
```json
// ~/.gemini/antigravity/mcp_config.json
{
  "mcpServers": {
    "danger-line": {
      "command": "uv",
      "args": [
        "run",
        "--directory", "C:/Users/adria/OneDrive/Área de Trabalho/PROJETOS/Danger_line",
        "python", "src/mcp/server.py"
      ],
      "env": {
        "GROQ_API_KEY": "gsk_...",
        "WORKSPACE_PATH": "C:/Users/adria/OneDrive/Área de Trabalho/PROJETOS/MeuProjeto"
      }
    }
  }
}
```

### Passo 3: CLI como Alternativa
Para uso sem Antigravity:
```bash
# Linkar a um workspace
python src/main.py --workspace "C:/path/to/project"

# Ou definir via .env
WORKSPACE_PATH=C:/path/to/project
```

### Passo 4: Suporte Multi-Workspace
```python
# Permitir trocar workspace em runtime
@mcp.tool()
def set_workspace(path: str) -> str:
    """Change the workspace directory the system analyzes.
    
    Args:
        path: Absolute path to the new workspace
    """
    global WORKSPACE
    WORKSPACE = path
    return f"Workspace changed to: {path}"
```

### Passo 5: Testar com MCP Inspector
```bash
# Instalar e testar antes de conectar ao Antigravity
uv run mcp dev src/mcp/server.py
```

---

## Comparação: MCP vs CLI

| Aspecto | MCP Server | CLI Standalone |
|---------|------------|----------------|
| Integração | Nativa com Antigravity | Manual via terminal |
| UX | Transparente, automática | Requer copiar/colar contexto |
| Flexibilidade | Limitado aos tools definidos | Interface livre |
| Economia de tokens | Máxima (fluxo direto) | Boa (manual) |
| Setup | Configurar `mcp_config.json` | Apenas rodar o script |

> **Recomendação**: Implementar **ambos**. O MCP Server como uso principal e o CLI como ferramenta de debugging e uso standalone.
