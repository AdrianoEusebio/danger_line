"""
Danger Line v2 — Test Configuration
Fixtures compartilhadas entre todos os testes.
"""
import pytest
import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock


# =============================================================================
# FIXTURES — Paths e estrutura de arquivos temporários
# =============================================================================

@pytest.fixture
def tmp_workspace(tmp_path: Path) -> Path:
    """Cria um workspace temporário com estrutura danger_line/."""
    workspace = tmp_path / "test_project"
    workspace.mkdir()

    # Criar estrutura danger_line/
    dl = workspace / "danger_line"
    (dl / "raw" / "analyses").mkdir(parents=True)
    (dl / "raw" / "solutions").mkdir(parents=True)
    (dl / "raw" / "classifications").mkdir(parents=True)
    (dl / "raw" / "reviews").mkdir(parents=True)
    (dl / "cache").mkdir()

    # Criar arquivo de código de exemplo
    (workspace / "src").mkdir()
    (workspace / "src" / "auth.py").write_text(
        "def login(user, password):\n    return user == 'admin'\n"
    )

    return workspace


@pytest.fixture
def tmp_vault(tmp_path: Path) -> Path:
    """Cria um vault Obsidian temporário."""
    vault = tmp_path / "obsidian_vault"
    (vault / "projects").mkdir(parents=True)
    (vault / "global" / "patterns").mkdir(parents=True)
    (vault / "global" / "lessons").mkdir(parents=True)
    return vault


@pytest.fixture
def sample_config(tmp_workspace: Path) -> dict:
    """Configuração de projeto de exemplo."""
    return {
        "project": {
            "name": "test_project",
            "path": str(tmp_workspace),
            "language": ["python"],
            "framework": "none",
        },
        "knowledge_base": {
            "lint_interval": 10,
            "initial_scan_depth": "quick",
            "stale_threshold_days": 30,
        },
        "providers": {
            "primary": "auto",
        },
        "compilation": {
            "ignore": ["__pycache__/", "*.pyc"],
            "priority_files": [],
        },
        "metrics": {
            "compile_count": 0,
            "total_analyses": 0,
            "total_kb_hits": 0,
            "last_lint": "",
        },
    }


# =============================================================================
# FIXTURES — Providers mockados
# =============================================================================

@pytest.fixture
def mock_groq_provider():
    """Provider Groq mockado para testes sem chamadas de API reais."""
    from providers.base import CompletionResponse, ProviderName
    provider = AsyncMock()
    provider.name = ProviderName.GROQ
    provider.is_available = AsyncMock(return_value=True)
    
    # Retorno real do CompletionResponse
    response = CompletionResponse(
        content="===AI_START===\nTechnical Summary\n===AI_END===\n===HUMAN_START===\nHuman Summary\n===HUMAN_END===",
        provider=ProviderName.GROQ,
        input_tokens=10,
        output_tokens=20
    )
    provider.complete = AsyncMock(return_value=response)
    return provider

@pytest.fixture
def mock_chain(mock_groq_provider):
    """Cria uma ProviderChain com o Groq mockado."""
    from providers.base import ProviderChain
    return ProviderChain([mock_groq_provider])


@pytest.fixture
def mock_gemini_provider():
    """Provider Gemini mockado."""
    from providers.base import CompletionResponse, ProviderName
    provider = AsyncMock()
    provider.name = ProviderName.GEMINI
    provider.is_available = AsyncMock(return_value=True)
    
    response = CompletionResponse(
        content="Mock Gemini response",
        provider=ProviderName.GEMINI
    )
    provider.complete = AsyncMock(return_value=response)
    return provider


@pytest.fixture
def mock_unavailable_provider():
    """Provider que simula falha total."""
    provider = AsyncMock()
    provider.name = "broken"
    provider.is_available = AsyncMock(return_value=False)
    provider.complete = AsyncMock(side_effect=ConnectionError("Provider unavailable"))
    return provider


# =============================================================================
# FIXTURES — Dados de exemplo
# =============================================================================

@pytest.fixture
def sample_analysis_result():
    """AnalysisResult de exemplo."""
    from storage.models import AnalysisResult
    return AnalysisResult(
        file_hash="abc123",
        filename="auth.py",
        filepath="src/auth.py",
        language="python",
        summary_for_ai="AUTH MODULE: Simple login function. No hashing. Security risk.",
        summary_for_human="# Análise: auth.py\n\nFunção de login simples sem hash de senha.",
        difficulty=2,
        dependencies=[],
        issues=["Senha não hasheada"],
    )


@pytest.fixture
def sample_wiki_articles():
    """Artigos de wiki de exemplo para testes de Q&A e Linter."""
    return {
        "auth_system": """---
title: Authentication System
compiled_from: raw/analyses/2026-05-04_auth_py.md
last_compiled: 2026-05-04T18:00:00
tags: [auth, security, python]
related: ["Error Handling", "User Model"]
confidence: 0.9
---

# Authentication System

The auth module handles user login using bcrypt password hashing.

## Key Functions
- `login(user, password)` — validates credentials
- `hash_password(raw)` — bcrypt hashing

## Known Issues
- [[Race Condition - Token Refresh]] (resolved 2026-05-01)
""",
        "error_handling": """---
title: Error Handling
compiled_from: raw/analyses/2026-05-04_errors_py.md
last_compiled: 2026-05-04T18:00:00
tags: [errors, patterns, python]
related: ["Authentication System"]
confidence: 0.85
---

# Error Handling

All errors extend `CustomError` with code and context.
""",
    }
