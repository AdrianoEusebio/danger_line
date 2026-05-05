"""
MCP Server — Danger Line exposto via FastMCP.

Tools disponíveis: analyze_file, classify_problem, get_optimized_context,
get_metrics, compile_knowledge, query_knowledge, lint_wiki,
get_project_card, get_known_patterns, get_known_bugs, set_workspace.

TDD: TDD-04-MCP-SERVER.MD
"""
from __future__ import annotations
import os
import sys
import io
from pathlib import Path
from dotenv import load_dotenv

# Forçar encoding UTF-8 para evitar erros no Windows e não sujar o stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from mcp.server.fastmcp import FastMCP # type: ignore

# Adicionar a pasta 'src' ao sys.path dinamicamente
src_path = str(Path(__file__).parent.parent.resolve())
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Carregar .env
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

from providers.base import ProviderChain, CompletionRequest
from providers.groq_provider import GroqProvider
from providers.gemini_provider import GeminiProvider
from providers.ollama_provider import OllamaProvider
from storage.obsidian import ObsidianIntegration
from storage.cache import AnalysisCache
from storage.markdown_store import MarkdownStore
from storage.wiki_store import WikiStore
from core.agent import AgentOrchestrator
from core.knowledge.qa_engine import WikiQA
from core.knowledge.bootstrap import ProjectBootstrap
from core.knowledge.compiler import KBCompiler
from core.knowledge.feedback import FeedbackLoop
from metrics.token_tracker import TokenTracker

# Inicializar servidor
mcp = FastMCP("danger-line")

# --- ESTADO GLOBAL (Singletons) ---
_providers = ProviderChain([
    GroqProvider(),
    GeminiProvider(),
    OllamaProvider()
])

_obsidian: ObsidianIntegration | None = None
_tracker = TokenTracker()
_workspace: Path | None = None

def _get_workspace() -> Path:
    global _workspace
    if _workspace is None:
        default = os.getenv("DEFAULT_WORKSPACE_PATH", "")
        if default:
            _workspace = Path(default)
        else:
            raise RuntimeError(
                "ERROR: No workspace configured. "
                "Use set_workspace tool or set DEFAULT_WORKSPACE_PATH in .env"
            )
    return _workspace

def _get_obsidian() -> ObsidianIntegration:
    global _obsidian
    if _obsidian is None:
        path = os.getenv("OBSIDIAN_VAULT_PATH")
        if not path:
            raise RuntimeError("ERROR: OBSIDIAN_VAULT_PATH not set in .env")
        _obsidian = ObsidianIntegration(path)
    return _obsidian

def _get_orchestrator() -> AgentOrchestrator:
    workspace = _get_workspace()
    
    from storage.manager import StorageManager
    storage_mgr = StorageManager()
    dl_path = storage_mgr.get_project_storage_path(workspace)
    
    cache = AnalysisCache(dl_path / "cache")
    store = MarkdownStore(dl_path)
    wiki_store = WikiStore(dl_path / "wiki")
    wiki_qa = WikiQA(_providers, wiki_store)
    
    return AgentOrchestrator(_providers, cache, store, wiki_qa, _tracker)


def _validate_path(path: str) -> Path:
    """Valida que o path está dentro do workspace (segurança)."""
    workspace = _get_workspace()
    resolved = (workspace / path).resolve()
    if not str(resolved).startswith(str(workspace.resolve())):
        raise PermissionError(f"ERROR: PATH_OUTSIDE_WORKSPACE — '{path}'")
    return resolved


# =============================================================================
# TOOLS — Análise
# =============================================================================

@mcp.tool()
async def analyze_file(path: str) -> str:
    """
    Analisa um arquivo de código e retorna resumo otimizado para IA.
    """
    try:
        file_path = _validate_path(path)
        orchestrator = _get_orchestrator()
        result = await orchestrator.analyzer.analyze(file_path)
        
        return f"### ANALYSIS: {path}\n\n{result.summary_for_human}\n\n**Difficulty**: {result.difficulty}★\n**Tokens**: {result.tokens_used}"
    except Exception as e:
        return f"ERROR: {str(e)}"

@mcp.tool()
async def register_project(path: str) -> str:
    """
    Registra um projeto novo e executa o scan inicial (Option C Hybrid).
    """
    try:
        project_path = Path(path)
        if not project_path.exists():
            return f"ERROR: PATH_NOT_FOUND — '{path}'"
            
        bootstrap = ProjectBootstrap(_providers, _get_obsidian())
        result = await bootstrap.register(project_path)
        
        return (
            f"✅ Project '{result['project']}' registered successfully!\n"
            f"Structure analyzed: {result['tree'][:500]}...\n"
            f"Key files analyzed: {result['files_analyzed']}\n"
            f"Project Card created in Obsidian."
        )
    except Exception as e:
        return f"ERROR: {str(e)}"


@mcp.tool()
async def analyze_project(path: str = "", depth: int = 2, full: bool = False) -> str:
    """
    Mapeia e analisa a estrutura de um projeto completo.

    Args:
        path: Path do projeto (default: workspace atual)
        depth: Profundidade do scan (default: 2)
        full: Se True, faz scan profundo com Project Card (~3000 tokens)
    """
    # TODO: Implementar ProjectAnalyzer
    workspace = _get_workspace() if not path else Path(path)
    return f"[STUB] analyze_project('{workspace}', depth={depth}, full={full})\n⚠ Pending."


# =============================================================================
# TOOLS — Classificação
# =============================================================================

@mcp.tool()
async def classify_problem(description: str, files: list[str] | None = None) -> str:
    """
    Classifica a dificuldade de um problema (1-3★).
    Consulta o KB antes de classificar para possível reclassificação.

    Args:
        description: Descrição do problema
        files: Arquivos relevantes (opcional)
    """
    # TODO: Integrar com DifficultyClassifier + Q&A Engine
    return (
        f"[STUB] classify_problem('{description[:50]}...')\n"
        "⚠ Pending implementation."
    )


@mcp.tool()
async def get_optimized_context(problem: str, path: str) -> str:
    """
    Gera super-prompt otimizado para envio à IA premium.
    
    Args:
        problem: Problema ou pergunta do usuário
        path: Path do arquivo principal relacionado ao problema
    """
    try:
        file_path = _validate_path(path)
        orchestrator = _get_orchestrator()
        result = await orchestrator.process_task(problem, file_path)
        
        return result["super_prompt"]
    except Exception as e:
        return f"ERROR: {str(e)}"


# =============================================================================
# TOOLS — Knowledge Base
# =============================================================================

@mcp.tool()
async def compile_knowledge() -> str:
    """
    Compila o Knowledge Base do projeto atual (transforma raw/ em wiki/).
    """
    try:
        workspace = _get_workspace()
        from storage.manager import StorageManager
        storage_mgr = StorageManager()
        dl_path = storage_mgr.get_project_storage_path(workspace)
        
        wiki_store = WikiStore(dl_path / "wiki")
        compiler = KBCompiler(_providers, wiki_store, dl_path)
        
        result = await compiler.compile_incremental()
        
        if "error" in result:
            return f"ERROR: {result['error']}"
            
        return (
            f"✅ Compilation finished!\n"
            f"Articles created: {result['articles_created']}\n"
            f"Knowledge Base is now updated for queries."
        )
    except Exception as e:
        return f"ERROR: {str(e)}"


@mcp.tool()
async def query_knowledge(query: str) -> str:
    """
    Faz uma pergunta ao Knowledge Base do projeto atual.
    """
    try:
        orchestrator = _get_orchestrator()
        result = await orchestrator.wiki_qa.query(query)
        
        if result.not_found:
            return "❌ NOT_FOUND: Não encontrei informações sobre isso no wiki."
            
        sources = ", ".join([f"[[{s}]]" for s in result.sources])
        return f"### ANSWER\n{result.answer}\n\n**Sources**: {sources}"
    except Exception as e:
        return f"ERROR: {str(e)}"


@mcp.tool()
async def lint_wiki(project: str = "") -> str:
    """
    Executa health check completo do wiki (hot-update manual).
    Roda todos os checks: INCONSISTENCY, MISSING, STALE, CONNECTION.
    NÃO modifica nenhum arquivo.
    """
    # TODO: Implementar WikiLinter
    return "[STUB] lint_wiki()\n⚠ Pending."


@mcp.tool()
async def get_project_card(project: str = "") -> str:
    """
    Retorna o Project Card do projeto.
    Se não existir, gera um novo (deep scan).
    """
    try:
        obsidian = _get_obsidian()
        if not project:
            project = _get_workspace().name
            
        content = obsidian.get_project_card(project)
        if not content:
            return f"❌ NOT_FOUND: Project Card para '{project}' não encontrado no Obsidian."
            
        return content
    except Exception as e:
        return f"ERROR: {str(e)}"


@mcp.tool()
async def get_known_patterns(project: str = "", category: str = "") -> str:
    """Lista patterns de código detectados no wiki."""
    return f"[STUB] get_known_patterns(project='{project}', category='{category}')\n⚠ Pending."


@mcp.tool()
async def get_known_bugs(project: str = "", status: str = "all") -> str:
    """Lista bugs conhecidos e soluções do wiki."""
    return f"[STUB] get_known_bugs(project='{project}', status='{status}')\n⚠ Pending."


# =============================================================================
# TOOLS — Métricas e Configuração
# =============================================================================

@mcp.tool()
async def get_metrics() -> str:
    """
    Retorna o dashboard de economia de tokens e uso do sistema.
    """
    return _tracker.format_dashboard()


@mcp.tool()
async def set_workspace(path: str) -> str:
    """
    Define ou troca o workspace ativo.

    Args:
        path: Path absoluto do projeto
    """
    global _workspace
    workspace_path = Path(path)

    if not workspace_path.exists():
        return f"ERROR: PATH_NOT_FOUND — '{path}'"
    if not workspace_path.is_dir():
        return f"ERROR: NOT_A_DIRECTORY — '{path}'"

    _workspace = workspace_path
    project_name = workspace_path.name

    return (
        f"✅ Workspace set to: {path}\n"
        f"Project: {project_name}\n"
        f"KB Status: Pending first scan."
    )


# =============================================================================
# Entry point
# =============================================================================

if __name__ == "__main__":
    mcp.run()
