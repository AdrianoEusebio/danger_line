"""
Storage — Models e tipos compartilhados.

TDD: TDD-06-STORAGE-CACHE.MD
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class AnalysisResult:
    """Resultado de uma análise de arquivo."""
    file_hash: str
    filename: str
    filepath: str
    language: str
    summary_for_ai: str
    summary_for_human: str
    difficulty: int  # 1, 2 ou 3
    dependencies: list[str] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)
    analyzed_at: str = field(default_factory=lambda: datetime.now().isoformat())
    provider_used: str = ""
    tokens_used: int = 0

    def to_cache_dict(self) -> dict:
        return {
            "file_hash": self.file_hash,
            "filename": self.filename,
            "filepath": self.filepath,
            "language": self.language,
            "difficulty": self.difficulty,
            "analyzed_at": self.analyzed_at,
            "provider_used": self.provider_used,
            "tokens_used": self.tokens_used,
        }


@dataclass
class SolutionResult:
    """Solução aprovada pela IA premium — alimenta o Filed Back loop."""
    filename: str
    problem: str
    solution: str
    source: str  # "base" | "premium"
    difficulty: int
    wiki_match: Optional[str] = None
    filed_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Classification:
    """Resultado da classificação de dificuldade."""
    difficulty: int  # 1, 2 ou 3
    confidence: float
    reasoning: str
    category: str  # syntax | logic | architecture | performance | security | config
    wiki_match: Optional[str] = None
    recommended_action: str = "resolve_locally"  # resolve_locally | ask_user | escalate


@dataclass
class LintReport:
    """Resultado do Wiki Linter."""
    health_score: float  # 0.0 a 1.0
    issues: list[dict] = field(default_factory=list)
    suggestions: list[dict] = field(default_factory=list)
    linted_at: str = field(default_factory=lambda: datetime.now().isoformat())

    @property
    def is_healthy(self) -> bool:
        return self.health_score >= 0.8 and len(self.issues) == 0


@dataclass
class QAResult:
    """Resultado de uma query ao wiki."""
    answer: str
    sources: list[str] = field(default_factory=list)
    not_found: bool = False
