import pytest
import tempfile
from pathlib import Path
from src.core.engine import KnowledgeEngine
from src.modules.obsidian.vault_manager import VaultManager
from src.modules.obsidian.markdown_parser import MarkdownBuilder

@pytest.mark.asyncio
async def test_knowledge_engine_capture():
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = KnowledgeEngine()
        engine.vault = VaultManager(vault_path=tmpdir)
        
        # Test capture pattern
        res = await engine.capture_pattern(
            name="MyPattern",
            content="Pattern content",
            tags=["pytest"],
            project="E2EProj"
        )
        assert res
        # Check that note is created in E2EProj folder
        note_content = engine.vault.read_note("E2EProj", "MyPattern")
        assert note_content is not None
        assert "Pattern content" in note_content
        
        # Test capture bugfix
        res_bug = await engine.capture_bugfix(
            error_log="Error logging details",
            solution="Fixed by adding error check",
            project="E2EProj"
        )
        assert res_bug
        # Check note is in E2EProj folder
        bug_content = engine.vault.read_note("E2EProj", "fix-E2EProj")
        assert bug_content is not None
        assert "Error logging details" in bug_content

@pytest.mark.asyncio
async def test_project_stack_affinity():
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = KnowledgeEngine()
        engine.vault = VaultManager(vault_path=tmpdir)
        
        # Register first project (python, rust)
        res1 = await engine.register_project(
            name="ProjA",
            path="/path/a",
            stack=["python", "rust"],
            description="First project"
        )
        assert res1
        
        # Register second project (python, js) - matches python!
        res2 = await engine.register_project(
            name="ProjB",
            path="/path/b",
            stack=["JS", "Python"],
            description="Second project"
        )
        assert res2
        
        # Check ProjA card has link to ProjB
        content_a = engine.vault.read_note("🗂️ Projects", "ProjA")
        assert "[[ProjB]]" in content_a
        
        # Check ProjB card has link to ProjA
        content_b = engine.vault.read_note("🗂️ Projects", "ProjB")
        assert "[[ProjA]]" in content_b
