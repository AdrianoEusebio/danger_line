import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar .env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

import click
from rich.console import Console

from providers.base import ProviderChain
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
from metrics.token_tracker import TokenTracker

console = Console()

# --- Helpers de Inicialização ---

def get_shared_state(project_path: Path):
    """Inicializa os serviços para um projeto específico usando storage centralizado."""
    providers = ProviderChain([GroqProvider(), GeminiProvider(), OllamaProvider()])
    
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH")
    if not vault_path:
        raise click.UsageError("OBSIDIAN_VAULT_PATH não configurado no .env")
        
    obsidian = ObsidianIntegration(vault_path)
    
    from storage.manager import StorageManager
    storage_mgr = StorageManager()
    dl_path = storage_mgr.get_project_storage_path(project_path)
    
    cache = AnalysisCache(dl_path / "cache")
    store = MarkdownStore(dl_path)
    wiki_store = WikiStore(dl_path / "wiki")
    wiki_qa = WikiQA(providers, wiki_store)
    tracker = TokenTracker()
    
    return providers, obsidian, cache, store, wiki_qa, tracker

# --- Comandos CLI ---

@click.group()
@click.version_option(version="2.0.0", prog_name="Danger Line")
def app():
    """🔴 Danger Line v2 — Otimizador de contexto para IAs premium."""
    pass

@app.command()
@click.argument("path", type=click.Path(exists=True))
def analyze(path: str):
    """Analisa um arquivo de código."""
    file_path = Path(path).resolve()
    project_path = file_path.parent
    # Tenta subir até achar a raiz (onde tem danger_line/) ou usa o parent
    while project_path.parent != project_path and not (project_path / "danger_line").exists():
        project_path = project_path.parent

    async def _run():
        providers, _, cache, store, _, _ = get_shared_state(project_path)
        from core.analyzer import CodeAnalyzer
        analyzer = CodeAnalyzer(providers, cache, store)
        
        with console.status(f"[bold yellow]Analisando {file_path.name}..."):
            result = await analyzer.analyze(file_path)
            console.print(f"\n[bold green]✅ Análise concluída![/bold green]")
            console.print(result.summary_for_human)

    asyncio.run(_run())

@app.command()
@click.argument("project_path", type=click.Path(exists=True))
def compile(project_path: str):
    """Compila o Knowledge Base (raw/ → wiki/)."""
    path = Path(project_path).resolve()
    
    async def _run():
        providers, _, _, _, _, _ = get_shared_state(path)
        
        from storage.manager import StorageManager
        storage_mgr = StorageManager()
        dl_path = storage_mgr.get_project_storage_path(path)
        
        wiki_store = WikiStore(dl_path / "wiki")
        compiler = KBCompiler(providers, wiki_store, dl_path)
        
        with console.status("[bold blue]Compilando Knowledge Base..."):
            result = await compiler.compile_incremental()
            console.print(f"\n[bold green]✅ Compilação finalizada![/bold green]")
            console.print(f"Artigos criados: {result['articles_created']}")

    asyncio.run(_run())

@app.command()
@click.argument("path", type=click.Path(exists=True))
def register(path: str):
    """Registra um projeto novo e faz o scan inicial."""
    project_path = Path(path).resolve()

    async def _run():
        providers, obsidian, _, _, _, _ = get_shared_state(project_path)
        bootstrap = ProjectBootstrap(providers, obsidian)
        
        with console.status(f"[bold cyan]Registrando projeto em {project_path.name}..."):
            result = await bootstrap.register(project_path)
            console.print(f"\n[bold green]Projeto registrado com sucesso![/bold green]")
            console.print(f"Arquivos analisados: {result['files_analyzed']}")
            console.print(f"Project Card gerado no Obsidian.")

    asyncio.run(_run())

@app.command()
@click.option("--project", type=click.Path(exists=True), help="Path do projeto")
def dashboard(project: str):
    """Exibe o painel de métricas (mockado se sem projeto ativo)."""
    # Para o dashboard real, precisaríamos persistir o TokenTracker em disco
    console.print("[bold blue]🔴 DANGER LINE — PAINEL DE CONTROLE[/bold blue]")
    console.print("[yellow]Métricas persistidas em desenvolvimento.[/yellow]")

if __name__ == "__main__":
    app()
