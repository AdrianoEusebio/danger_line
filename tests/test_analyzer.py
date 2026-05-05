"""
TDD-01: Análise de Arquivo
Referência: documents/TDD/TDD-01-ANALISE-ARQUIVO.MD
"""
import pytest
from pathlib import Path
from core.analyzer import CodeAnalyzer
from storage.cache import AnalysisCache
from storage.markdown_store import MarkdownStore

class TestAnalyzeFile:
    """T-01.x — Análise de arquivo individual."""

    async def test_01_1_analyze_python_file(self, tmp_workspace, mock_chain):
        """T-01.1: Analisar arquivo Python válido."""
        dl_path = tmp_workspace / "danger_line"
        cache = AnalysisCache(dl_path / "cache")
        store = MarkdownStore(dl_path)
        
        analyzer = CodeAnalyzer(mock_chain, cache, store)
        file_to_analyze = tmp_workspace / "src" / "auth.py"
        
        result = await analyzer.analyze(file_to_analyze)
        
        assert result.language == "python"
        assert "Technical Summary" in result.summary_for_ai
        assert "Human Summary" in result.summary_for_human
        assert result.file_hash is not None
        
        # Verificar se salvou no cache
        assert (dl_path / "cache" / f"{result.file_hash}.json").exists()
        
        # Verificar se salvou no raw/
        raw_files = list((dl_path / "raw" / "analyses").glob("*.md"))
        assert len(raw_files) == 1

    async def test_01_2_analyze_nonexistent_file(self, tmp_workspace, mock_chain):
        """T-01.2: Arquivo inexistente deve retornar erro."""
        analyzer = CodeAnalyzer(mock_chain)
        with pytest.raises(FileNotFoundError):
            await analyzer.analyze(tmp_workspace / "nonexistent.py")
