import asyncio
import os
import sys
from pathlib import Path

# Force UTF-8 encoding for standard streams
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from src.modules.obsidian.vault_manager import VaultManager
from src.modules.obsidian.markdown_parser import MarkdownBuilder
from src.core.engine import knowledge_engine
from src.shared.logger import logger
from src.modules.mcp.server import query_kb, explore_graph, get_project_rules, register_project, commit_knowledge, commit_bugfix

async def validate_pipeline():
    """Performs an End-to-End validation of the knowledge pipeline for Danger Line 5.0."""
    print(">>> Starting Danger Line 5.0 E2E Validation...")
    
    # Setup VaultManager
    vm = VaultManager()
    print("OK: Vault structure ensured.")
    
    project_name = "E2E_Test_Project"
    
    # 1. Test MarkdownBuilder & Tags Density
    print("\n[1/4] Testing MarkdownBuilder & Density Tags...")
    meta = {"type": "Test", "project": project_name, "tags": ["test", "validation", "phase5"]}
    body = "# Test Note\nThis is a short test note for E2E."
    built = MarkdownBuilder.build(meta, body)
    
    # Save inside project-specific folder
    test_note = "e2e_test_note_tags"
    save_ok = vm.save_note(project_name, test_note, built)
    assert save_ok
    print(f"OK: Note saved in dynamic folder: {project_name}.")
    
    # Read and assert density tag (rascunho)
    saved_content = vm.read_note(project_name, test_note)
    assert "contexto/rascunho" in saved_content
    # Assert project wikilink back-reference
    assert f"[[{project_name}]]" in saved_content
    print("OK: Note contains correct density tag and project master card wikilink.")
    
    # Verify semantic tag search through MCP tool query_kb
    search_res = await query_kb(tags=["phase5"])
    assert "e2e_test_note_tags" in search_res
    print("OK: query_kb successfully fetched note by tag.")
    
    # 2. Test Graph Explore (Wikilinks)
    print("\n[2/4] Testing Graph Explore...")
    child_note_name = "linked_child_note"
    child_content = MarkdownBuilder.build(
        {"type": "Pattern", "project": project_name, "tags": ["child"]}, 
        "# Child Note\nThis note is linked from the parent."
    )
    vm.save_note(project_name, child_note_name, child_content)
    
    parent_note_name = "linked_parent_note"
    parent_content = MarkdownBuilder.build(
        {"type": "Pattern", "project": project_name, "tags": ["parent"]},
        f"# Parent Note\nCheck this linked note: [[{child_note_name}]]"
    )
    vm.save_note(project_name, parent_note_name, parent_content)
    
    # Explore graph from parent
    graph_res = await explore_graph(parent_note_name)
    assert child_note_name in graph_res
    assert "linked_child_note" in graph_res
    print("OK: explore_graph successfully navigated wikilinks.")
    
    # 3. Test Project Registration & Stack Affinity
    print("\n[3/4] Testing Project Registration & Stack Affinity...")
    project_path = os.getcwd()
    
    # Register similar project A
    proj_a_name = "ProjE2E_A"
    await register_project(
        name=proj_a_name,
        path=project_path,
        stack=["python", "rust"],
        description="E2E test project A"
    )
    
    # Register similar project B (matches python stack!)
    proj_b_name = "ProjE2E_B"
    await register_project(
        name=proj_b_name,
        path=project_path,
        stack=["python", "go"],
        description="E2E test project B"
    )
    
    # Check if ProjE2E_A contains link to ProjE2E_B and vice-versa
    content_a = vm.read_note("🗂️ Projects", proj_a_name)
    content_b = vm.read_note("🗂️ Projects", proj_b_name)
    assert f"[[{proj_b_name}]]" in content_a
    assert f"[[{proj_a_name}]]" in content_b
    print("OK: Stack Affinity successfully cross-linked similar projects.")
    
    # Create project rules file: Regras - ProjE2E_A
    rules_body = "# Rules\n1. Use double quotes for strings.\n2. Add docstrings."
    rules_content = MarkdownBuilder.build(
        {"type": "Rules", "project": proj_a_name},
        rules_body
    )
    vm.save_note(proj_a_name, f"Regras - {proj_a_name}", rules_content)
    
    # Test reading rules resource (temporarily mock/check get_project_rules)
    # We will simulate CWD check by changing CWD or mocking, but get_project_rules matches registered path.
    # Since proj_a_name is registered with CWD, it will match.
    rules_res = get_project_rules()
    assert proj_a_name in rules_res
    print("OK: get_project_rules successfully resolved regras note.")
    
    # 4. Clean up E2E Notes
    print("\n[4/4] Cleaning up E2E Notes...")
    try:
        os.remove(vm.vault_path / project_name / f"{test_note}.md")
        os.remove(vm.vault_path / project_name / f"{child_note_name}.md")
        os.remove(vm.vault_path / project_name / f"{parent_note_name}.md")
        os.remove(vm.vault_path / proj_a_name / f"Regras - {proj_a_name}.md")
        os.remove(vm.vault_path / "🗂️ Projects" / f"{proj_a_name}.md")
        os.remove(vm.vault_path / "🗂️ Projects" / f"{proj_b_name}.md")
        
        # Remove empty test directories
        for d in [project_name, proj_a_name, proj_b_name]:
            dir_path = vm.vault_path / d
            if dir_path.exists():
                dir_path.rmdir()
        print("OK: Cleaned up all test notes and directories.")
    except Exception as e:
        print(f"Warning: Failed to clean up some test notes: {e}")
        
    print("\nDONE: All Danger Line 5.0 E2E validations passed successfully!")

if __name__ == "__main__":
    asyncio.run(validate_pipeline())
