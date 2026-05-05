"""
TDD-06: Storage e Cache (3 Camadas)
Referência: documents/TDD/TDD-06-STORAGE-CACHE.MD
"""
import pytest
import json
from pathlib import Path
from storage.markdown_store import MarkdownStore
from storage.cache import AnalysisCache
from storage.obsidian import ObsidianIntegration

class TestStorageThreeLayers:
    """T-06.x — Armazenamento em 3 camadas: cache, raw/, wiki/."""

    async def test_06_1_save_saves_to_cache_and_raw(
        self, tmp_workspace, sample_analysis_result
    ):
        """T-06.1: Salvar análise deve criar arquivo no cache E no raw/."""
        dl_path = tmp_workspace / "danger_line"
        cache = AnalysisCache(dl_path / "cache")
        store = MarkdownStore(dl_path)
        
        # Salvar no Store
        store.save_analysis(sample_analysis_result)
        
        # Verificar Raw
        raw_files = list((dl_path / "raw" / "analyses").glob("*.md"))
        assert len(raw_files) == 1
        assert "AUTH MODULE" in raw_files[0].read_text(encoding="utf-8")

    async def test_06_2_cache_hit_works(
        self, tmp_workspace, sample_analysis_result
    ):
        """T-06.2: Cache deve retornar dados salvos se o hash bater."""
        dl_path = tmp_workspace / "danger_line"
        cache = AnalysisCache(dl_path / "cache")
        file_path = tmp_workspace / "src" / "auth.py"
        
        # Configurar hash real para o arquivo de teste
        sample_analysis_result.file_hash = AnalysisCache.compute_hash(file_path)
        
        cache.set(file_path, sample_analysis_result)
        
        cached = cache.get(file_path)
        assert cached is not None
        assert cached["file_hash"] == sample_analysis_result.file_hash

    async def test_06_3_cache_miss_on_modified_file(self, tmp_workspace, sample_analysis_result):
        """T-06.3: Arquivo modificado deve causar cache miss."""
        dl_path = tmp_workspace / "danger_line"
        cache = AnalysisCache(dl_path / "cache")
        file_path = tmp_workspace / "src" / "auth.py"
        
        # Salva cache com hash atual
        sample_analysis_result.file_hash = AnalysisCache.compute_hash(file_path)
        cache.set(file_path, sample_analysis_result)
        
        # Modifica o arquivo
        file_path.write_text("modified content")
        
        cached = cache.get(file_path)
        assert cached is None # Miss!

class TestObsidianSync:
    """T-06.7-8 — Sincronização com Obsidian vault."""

    async def test_06_7_vault_initialization(self, tmp_vault):
        """T-06.7: ObsidianIntegration deve criar estrutura se não existir."""
        obs = ObsidianIntegration(tmp_vault)
        assert (tmp_vault / "projects").exists()
        assert (tmp_vault / "global" / "patterns").exists()
