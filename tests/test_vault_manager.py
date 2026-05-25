import tempfile
from pathlib import Path
from src.modules.obsidian.vault_manager import VaultManager
from src.modules.obsidian.markdown_parser import MarkdownBuilder

def test_vault_manager_lifecycle():
    with tempfile.TemporaryDirectory() as tmpdir:
        vm = VaultManager(vault_path=tmpdir)
        
        # Verify structure
        for folder in vm.folders:
            assert (Path(tmpdir) / folder).exists()
            
        # Test save and read note
        content = "Test content"
        save_ok = vm.save_note("🧩 Padrões", "test_note", content)
        assert save_ok
        
        read_content = vm.read_note("🧩 Padrões", "test_note")
        assert read_content == content
        
        # Test list
        notes = vm.list_notes("🧩 Padrões")
        assert "test_note.md" in notes
        
        # Test find note path
        resolved = vm.find_note_path("test_note")
        assert resolved is not None
        assert resolved[0] == "🧩 Padrões"
        assert resolved[1] == "test_note.md"

        # Test tag search
        note_with_tags = MarkdownBuilder.build({"tags": ["searchable", "tag2"]}, "Body here")
        vm.save_note("🧩 Padrões", "note_tags", note_with_tags)
        
        search_res = vm.find_notes_by_tags(["searchable"])
        assert len(search_res) == 1
        assert search_res[0]["filename"] == "note_tags.md"
