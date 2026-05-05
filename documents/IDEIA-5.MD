# 💡 IDEIA 5 — Painel de Controle via Terminal

## Conceito

O sistema terá um **dashboard no terminal** mostrando métricas em tempo real:
- % de tokens economizados vs uso direto
- Tokens gastos na IA base vs IA potente
- Distribuição de problemas por estrelas
- Análise da IA potente sobre qualidade e sugestões de melhoria
- **Métricas do Knowledge Base** (artigos, cobertura, health, KB hits)

## Layout do Painel

```
╔══════════════════════════════════════════════════════════╗
║              🔴 DANGER LINE — PAINEL DE CONTROLE        ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  📊 ECONOMIA DE TOKENS                                   ║
║  ┌────────────────────────────────────────┐               ║
║  │ Economizados:  12,450 tokens  (62%)   │               ║
║  │ ████████████████████░░░░░░░░░░░░░░░░  │               ║
║  └────────────────────────────────────────┘               ║
║                                                          ║
║  💰 CONSUMO                                              ║
║  ├─ IA Base (Groq):     3,200 tokens                    ║
║  ├─ IA Potente:         4,500 tokens                    ║
║  └─ Total estimado sem DL: 20,150 tokens                ║
║                                                          ║
║  ⭐ DISTRIBUIÇÃO                                         ║
║  ├─ 1★ Simples:   15 (60%)                              ║
║  ├─ 2★ Médio:      7 (28%)                              ║
║  └─ 3★ Complexo:   3 (12%)                              ║
║                                                          ║
║  🏆 AVALIAÇÃO DA IA POTENTE                              ║
║  ├─ Precisão das análises: 85%                           ║
║  ├─ Sugestões pendentes: 3                               ║
║  └─ Última revisão: 2026-05-04 18:30                     ║
║                                                          ║
║  📚 KNOWLEDGE BASE                                       ║
║  ├─ Artigos no wiki: 42                                  ║
║  ├─ Knowledge Score: 65% ████████████░░░░░░              ║
║  ├─ KB Hits (wiki evitou análise): 18                    ║
║  ├─ Wiki Health: ✅ 2 issues (lint)                       ║
║  └─ Último lint: 2026-05-04 20:00                         ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

## Passos Técnicos

### Passo 1: Token Tracker
```python
# src/metrics/token_tracker.py
from dataclasses import dataclass, field
from datetime import datetime
import json

@dataclass
class TokenMetrics:
    tokens_base_input: int = 0
    tokens_base_output: int = 0
    tokens_premium_input: int = 0
    tokens_premium_output: int = 0
    estimated_raw_tokens: int = 0  # quanto gastaria sem DL
    problems_by_star: dict = field(default_factory=lambda: {1: 0, 2: 0, 3: 0})
    
    @property
    def total_base(self) -> int:
        return self.tokens_base_input + self.tokens_base_output
    
    @property
    def total_premium(self) -> int:
        return self.tokens_premium_input + self.tokens_premium_output
    
    @property
    def tokens_saved(self) -> int:
        return self.estimated_raw_tokens - self.total_premium
    
    @property
    def savings_percentage(self) -> float:
        if self.estimated_raw_tokens == 0:
            return 0.0
        return (self.tokens_saved / self.estimated_raw_tokens) * 100

class TokenTracker:
    def __init__(self, persist_path: str):
        self.metrics = TokenMetrics()
        self.persist_path = persist_path
        self._load()
    
    def record_base_usage(self, input_tokens: int, output_tokens: int):
        self.metrics.tokens_base_input += input_tokens
        self.metrics.tokens_base_output += output_tokens
        self._save()
    
    def record_premium_usage(self, input_tokens: int, output_tokens: int):
        self.metrics.tokens_premium_input += input_tokens
        self.metrics.tokens_premium_output += output_tokens
        self._save()
    
    def record_estimated_raw(self, tokens: int):
        self.metrics.estimated_raw_tokens += tokens
        self._save()
    
    def record_classification(self, stars: int):
        self.metrics.problems_by_star[stars] += 1
        self._save()
```

### Passo 2: Dashboard com Rich
```python
# src/cli/dashboard.py
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, BarColumn
from rich.layout import Layout

class Dashboard:
    def __init__(self, tracker: TokenTracker):
        self.console = Console()
        self.tracker = tracker
    
    def render(self):
        m = self.tracker.metrics
        
        # Barra de economia
        savings = f"Economizados: {m.tokens_saved:,} tokens ({m.savings_percentage:.0f}%)"
        
        # Tabela de consumo
        table = Table(title="💰 Consumo")
        table.add_column("Provider", style="cyan")
        table.add_column("Tokens", justify="right", style="green")
        table.add_row("IA Base (Groq)", f"{m.total_base:,}")
        table.add_row("IA Potente", f"{m.total_premium:,}")
        table.add_row("Estimado sem DL", f"{m.estimated_raw_tokens:,}", style="dim")
        
        self.console.print(Panel(
            f"📊 {savings}\n\n" + str(table),
            title="🔴 DANGER LINE — PAINEL",
            border_style="red"
        ))
```

### Passo 3: Estimativa de Tokens Raw
```python
# Estimar quanto custaria sem o Danger Line
def estimate_raw_tokens(code: str, problem: str) -> int:
    """Estima tokens que seriam gastos enviando tudo cru para IA potente."""
    # ~4 chars por token (estimativa conservadora)
    total_chars = len(code) + len(problem)
    return total_chars // 4
```

### Passo 4: Feedback da IA Potente sobre Análises
```python
# Via MCP tool ou batch review
@mcp.tool()
def submit_quality_feedback(accuracy_score: float, suggestions: list[str]) -> str:
    """Submit quality feedback from the premium AI about base AI analyses.
    
    Args:
        accuracy_score: 0.0-1.0 accuracy rating
        suggestions: List of improvement suggestions
    """
    tracker.record_feedback(accuracy_score, suggestions)
    return "Feedback recorded"
```

### Passo 5: Persistência em JSON
Métricas salvas em `.danger_line/metrics.json` no workspace, atualizadas a cada operação.

---

## Métricas Expostas via MCP

A tool `get_metrics` retorna tudo isso formatado, permitindo que o Antigravity mostre métricas sob demanda.

---

## Métricas do Knowledge Base (NOVO)

| Métrica | Descrição | Fonte |
|---------|-----------|-------|
| `wiki_articles` | Total de artigos no wiki | Contagem de .md em wiki/ |
| `wiki_words` | Total de palavras no wiki | Soma de words em artigos |
| `knowledge_score` | % do projeto documentado | Módulos com artigo / total módulos |
| `kb_hits` | Vezes que o wiki evitou análise completa | Contador de cache hits via wiki |
| `wiki_health` | Issues encontradas pelo Linter | Último resultado do `lint_wiki` |
| `last_lint` | Data do último lint | Timestamp |
| `stale_articles` | Artigos desatualizados | Linter detecta |
| `backlinks_count` | Total de [[wikilinks]] | Contagem de links internos |
