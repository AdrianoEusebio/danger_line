"""
TokenTracker — Rastreamento de tokens consumidos e economizados.

TDD: TDD-07-TOKEN-TRACKER.MD
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SessionMetrics:
    """Métricas da sessão atual."""
    tokens_base_ai: int = 0        # Tokens gastos na IA base (Groq/Gemini/Ollama)
    tokens_premium_ai: int = 0     # Tokens gastos na IA premium
    tokens_estimated_raw: int = 0  # Tokens estimados sem o Danger Line
    problems_1star: int = 0
    problems_2star: int = 0
    problems_3star: int = 0
    cache_hits: int = 0
    kb_hits: int = 0               # Vezes que o wiki evitou análise completa
    wiki_articles: int = 0
    knowledge_score: float = 0.0   # % do projeto documentado
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())

    @property
    def tokens_saved(self) -> int:
        return max(0, self.tokens_estimated_raw - self.tokens_base_ai - self.tokens_premium_ai)

    @property
    def savings_percentage(self) -> float:
        if self.tokens_estimated_raw == 0:
            return 0.0
        return round((self.tokens_saved / self.tokens_estimated_raw) * 100, 1)

    @property
    def total_problems(self) -> int:
        return self.problems_1star + self.problems_2star + self.problems_3star


class TokenTracker:
    """Rastreia tokens e gera métricas da sessão."""

    def __init__(self):
        self.session = SessionMetrics()

    def record_base_ai_usage(self, input_tokens: int, output_tokens: int) -> None:
        self.session.tokens_base_ai += input_tokens + output_tokens

    def record_premium_ai_usage(self, input_tokens: int, output_tokens: int) -> None:
        self.session.tokens_premium_ai += input_tokens + output_tokens

    def record_raw_estimate(self, estimated_tokens: int) -> None:
        """Registra estimativa de tokens que seriam usados sem o Danger Line."""
        self.session.tokens_estimated_raw += estimated_tokens

    def record_problem(self, difficulty: int) -> None:
        if difficulty == 1:
            self.session.problems_1star += 1
        elif difficulty == 2:
            self.session.problems_2star += 1
        elif difficulty == 3:
            self.session.problems_3star += 1

    def record_cache_hit(self) -> None:
        self.session.cache_hits += 1

    def record_kb_hit(self) -> None:
        self.session.kb_hits += 1

    def update_wiki_stats(self, articles: int, knowledge_score: float) -> None:
        self.session.wiki_articles = articles
        self.session.knowledge_score = knowledge_score

    def get_metrics(self) -> SessionMetrics:
        return self.session

    def format_dashboard(self) -> str:
        """Retorna texto formatado para o dashboard."""
        m = self.session
        lines = [
            "╔══════════════════════════════════════════════════════════╗",
            "║              🔴 DANGER LINE — PAINEL DE CONTROLE        ║",
            "╠══════════════════════════════════════════════════════════╣",
            "║                                                          ║",
            f"║  📊 TOKENS ECONOMIZADOS: {m.tokens_saved:>8,} ({m.savings_percentage:.0f}%)".ljust(59) + "║",
            "║                                                          ║",
            "║  💰 CONSUMO                                              ║",
            f"║  ├─ IA Base (Groq):    {m.tokens_base_ai:>10,} tokens".ljust(59) + "║",
            f"║  ├─ IA Premium:        {m.tokens_premium_ai:>10,} tokens".ljust(59) + "║",
            f"║  └─ Estimado sem DL:   {m.tokens_estimated_raw:>10,} tokens".ljust(59) + "║",
            "║                                                          ║",
            "║  ⭐ DISTRIBUIÇÃO                                         ║",
            f"║  ├─ 1★ Simples:  {m.problems_1star:>4} problemas".ljust(59) + "║",
            f"║  ├─ 2★ Médio:    {m.problems_2star:>4} problemas".ljust(59) + "║",
            f"║  └─ 3★ Complexo: {m.problems_3star:>4} problemas".ljust(59) + "║",
            "║                                                          ║",
            "║  📚 KNOWLEDGE BASE                                       ║",
            f"║  ├─ Artigos:    {m.wiki_articles:>4}  | KB Hits: {m.kb_hits:>4}".ljust(59) + "║",
            f"║  └─ Coverage:   {m.knowledge_score:.0%}".ljust(59) + "║",
            "║                                                          ║",
            "╚══════════════════════════════════════════════════════════╝",
        ]
        return "\n".join(lines)
