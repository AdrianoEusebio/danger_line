import pytest
import tempfile
from src.core.engine import KnowledgeEngine
from src.modules.obsidian.vault_manager import VaultManager

@pytest.mark.asyncio
async def test_knowledge_engine_capture():
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = KnowledgeEngine()
        # Override vault with temporary vault manager
        engine.vault = VaultManager(vault_path=tmpdir)
        
        # Test capture pattern
        res = await engine.capture_pattern(
            name="MyPattern",
            content="Pattern content",
            tags=["pytest"],
            project="E2EProj"
        )
        assert res
        
        # Test register project
        res_proj = await engine.register_project(
            name="E2EProj",
            path="/path/to/proj",
            stack=["python"],
            description="Desc"
        )
        assert res_proj
        
        # Test capture bugfix
        res_bug = await engine.capture_bugfix(
            error_log="Error logging details",
            solution="Fixed by adding error check",
            project="E2EProj"
        )
        assert res_bug
