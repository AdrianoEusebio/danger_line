import asyncio
import os
import sys

# Force UTF-8 encoding for standard streams
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from src.modules.obsidian.vault_manager import VaultManager
from src.modules.obsidian.markdown_parser import MarkdownBuilder
from src.core.engine import knowledge_engine
from src.shared.logger import logger
from src.modules.mcp.server import query_kb, explore_graph, get_project_rules

async def validate_pipeline():
    """Performs an End-to-End validation of the knowledge pipeline for Danger Line 4.0."""
    print(">>> Starting Danger Line E2E Validation...")
    
    # Setup VaultManager
    vm = VaultManager()
    print("OK: Vault structure ensured.")
    
    # 1. Test MarkdownBuilder & Tags
    print("\n[1/4] Testing MarkdownBuilder & Semantic Tags...")
    meta = {"type": "Test", "tags": ["test", "validation", "phase3"]}
    body = "# Test Note\nThis is a test note."
    built = MarkdownBuilder.build(meta, body)
    
    test_note = "e2e_test_note_tags"
    save_ok = vm.save_note("🧩 Padrões", test_note, built)
    assert save_ok
    print("OK: Note saved in vault.")
    
    # Verify semantic tag search through MCP tool query_kb
    search_res = await query_kb(tags=["phase3"])
    assert "e2e_test_note_tags" in search_res
    print("OK: query_kb successfully fetched note by tag.")
    
    # 2. Test Graph Explore (Wikilinks)
    print("\n[2/4] Testing Graph Explore...")
    child_note_name = "linked_child_note"
    child_content = MarkdownBuilder.build(
        {"type": "Pattern", "tags": ["child"]}, 
        "# Child Note\nThis note is linked from the parent."
    )
    vm.save_note("🧩 Padrões", child_note_name, child_content)
    
    parent_note_name = "linked_parent_note"
    parent_content = MarkdownBuilder.build(
        {"type": "Pattern", "tags": ["parent"]},
        f"# Parent Note\nCheck this linked note: [[{child_note_name}]]"
    )
    vm.save_note("🧩 Padrões", parent_note_name, parent_content)
    
    # Explore graph from parent
    graph_res = await explore_graph(parent_note_name)
    assert child_note_name in graph_res
    assert "linked_child_note" in graph_res
    print("OK: explore_graph successfully navigated wikilinks.")
    
    # 3. Test Project Rules (Resources)
    print("\n[3/4] Testing Project Rules (Resources)...")
    project_name = "E2E_Test_Project"
    project_path = os.getcwd()
    
    # Register project master card
    await knowledge_engine.register_project(
        name=project_name,
        path=project_path,
        stack=["python"],
        description="E2E test project rules injection."
    )
    
    # Create project rules file: Regras - E2E_Test_Project
    rules_body = "# Rules\n1. Use double quotes for strings.\n2. Add docstrings."
    rules_content = MarkdownBuilder.build(
        {"type": "Rules", "project": project_name},
        rules_body
    )
    vm.save_note("📚 Playbooks", f"Regras - {project_name}", rules_content)
    
    # Test reading the project rules resource
    rules_res = get_project_rules()
    assert project_name in rules_res
    assert "Use double quotes for strings." in rules_res
    print("OK: get_project_rules resource successfully resolved rules based on CWD.")
    
    # 4. Clean up E2E Notes
    print("\n[4/4] Cleaning up E2E Notes...")
    try:
        os.remove(vm.vault_path / "🧩 Padrões" / f"{test_note}.md")
        os.remove(vm.vault_path / "🧩 Padrões" / f"{child_note_name}.md")
        os.remove(vm.vault_path / "🧩 Padrões" / f"{parent_note_name}.md")
        os.remove(vm.vault_path / "🗂️ Projects" / f"{project_name}.md")
        os.remove(vm.vault_path / "📚 Playbooks" / f"Regras - {project_name}.md")
        print("OK: Cleaned up all test notes.")
    except Exception as e:
        print(f"Warning: Failed to clean up some test notes: {e}")
        
    print("\nDONE: All Phase 3 E2E validations passed successfully!")

if __name__ == "__main__":
    asyncio.run(validate_pipeline())
