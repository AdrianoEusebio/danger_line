import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import sys
from pathlib import Path
import re
import os
from fastmcp import FastMCP
from src.shared.logger import logger
from src.shared.config import Config
from src.core.engine import knowledge_engine
from src.modules.obsidian.markdown_parser import MarkdownBuilder

# Initialize FastMCP Server
mcp = FastMCP("Danger Line")

@mcp.tool()
async def ping() -> str:
    """Verifies that the Danger Line MCP server is alive."""
    return "pong - Danger Line is active"

@mcp.tool()
async def query_kb(query: str = "", tags: list = None) -> str:
    """
    Searches the Knowledge Base (Obsidian) for relevant patterns, specs, or solutions.
    Can search by filename keywords, filter by semantic tags, or combine both.
    """
    logger.info(f"Querying KB with query='{query}' and tags={tags}")
    
    results = []
    results.append(f"### 🔍 Search Results")
    if query:
        results.append(f"- Keyword: '{query}'")
    if tags:
        results.append(f"- Tags: {', '.join(tags)}")
    results.append("")

    found_any = False

    if tags:
        # Perform semantic tag search across all folders
        matched_notes = knowledge_engine.vault.find_notes_by_tags(tags)
        
        # If query is also provided, filter by keyword (case-insensitive in filename or body)
        if query:
            matched_notes = [
                n for n in matched_notes 
                if query.lower() in n["filename"].lower() or query.lower() in n["content"].lower()
            ]
            
        for note in matched_notes:
            found_any = True
            results.append("---")
            results.append(f"📄 **Note: {note['filename']}** (Folder: {note['folder']})")
            content = note["content"]
            snippet = content[:500].strip() + "..." if len(content) > 500 else content
            results.append(snippet)
    else:
        # Keyword-only search in filenames across all folders
        for folder in knowledge_engine.vault.get_all_folders():
            notes = knowledge_engine.vault.list_notes(folder)
            matches = [n for n in notes if query.lower() in n.lower()]
            
            for match in matches:
                content = knowledge_engine.vault.read_note(folder, match)
                if content:
                    found_any = True
                    results.append("---")
                    results.append(f"📄 **Note: {match}** (Folder: {folder})")
                    snippet = content[:500].strip() + "..." if len(content) > 500 else content
                    results.append(snippet)

    if not found_any:
        results.append("⚠️ No matching notes found in the Knowledge Base.")

    return "\n".join(results)

@mcp.resource("obsidian://overview")
def get_vault_overview() -> str:
    """Returns a general overview of the folders and available notes in the Obsidian Vault."""
    summary = [
        "=== Danger Line Vault Overview ===",
        "Below is a list of available directories in your Knowledge Base and the notes inside them:",
        ""
    ]
    
    for folder in knowledge_engine.vault.get_all_folders():
        notes = knowledge_engine.vault.list_notes(folder)
        if notes:
            summary.append(f"📁 {folder} ({len(notes)} notes):")
            summary.append("  " + ", ".join(notes[:10]))
        else:
            summary.append(f"📁 {folder}: (empty)")
            
    return "\n".join(summary)

@mcp.resource("obsidian://project-rules")
def get_project_rules() -> str:
    """
    Exposes project-specific rules (from Obsidian Vault) based on the active IDE project directory.
    Detects the current workspace path and matches it with a registered Project Master Card.
    """
    current_cwd = os.getcwd()
    logger.info(f"Loading rules resource. CWD: {current_cwd}")
    
    # 1. Search for a Project Master Card in '🗂️ Projects'
    project_cards = knowledge_engine.vault.list_notes("🗂️ Projects")
    matched_project = None
    
    for card_name in project_cards:
        content = knowledge_engine.vault.read_note("🗂️ Projects", card_name)
        if content:
            metadata, _ = MarkdownBuilder.parse(content)
            card_path = metadata.get("path")
            if card_path:
                # Normalize paths for comparison (e.g. resolve Windows backslashes)
                normalized_card_path = os.path.normpath(str(card_path)).lower()
                normalized_cwd = os.path.normpath(current_cwd).lower()
                
                # Check if CWD starts with or equals the registered project path
                if normalized_cwd.startswith(normalized_card_path) or normalized_card_path.startswith(normalized_cwd):
                    matched_project = metadata.get("project")
                    break
                    
    if not matched_project:
        return f"=== 📋 Project Rules ===\nNo registered project card matches the current directory: '{current_cwd}'\nRegister a project card to link rules."
        
    # 2. Look for rules note. Expected name: 'Regras - {matched_project}.md'
    rules_note_name = f"Regras - {matched_project}"
    resolved_rules = knowledge_engine.vault.find_note_path(rules_note_name)
    
    if not resolved_rules:
        return f"=== 📋 Rules for: {matched_project} ===\nNo rules note found at 'Regras - {matched_project}.md'.\nCreate this note to override or inject custom coding standards for this workspace."
        
    folder, filename = resolved_rules
    rules_content = knowledge_engine.vault.read_note(folder, filename)
    if not rules_content:
        return f"=== 📋 Rules for: {matched_project} ===\nFailed to read rules file."
        
    _, rules_body = MarkdownBuilder.parse(rules_content)
    
    return f"""=== 📋 Project Rules: {matched_project} ===
Source: {folder}/{filename}
Workspace: {current_cwd}

{rules_body}
"""

@mcp.prompt()
def init_assistant() -> str:
    """Standard instructions to force the assistant to check the KB first and save new discoveries."""
    return """
You are an expert developer integrated with Danger Line (Obsidian Knowledge Base MCP).
Your mission is to maintain a perfect, updated and redundancy-free technical "brain" (Obsidian Vault).

Operational Protocol (Strict Loop):

1. CHECK FIRST (Search):
   - At the beginning of EVERY request (e.g., implementing a feature, refactoring, fixing a bug), you MUST call `query_kb` with relevant keywords or tags to see if a similar pattern or playbook already exists in the Obsidian brain.
   
2. COMPILE DIFFERENCES:
   - If a pattern exists, use it as your base logic and tell the user you are following the registered pattern.
   - If the pattern exists but is outdated or slightly different, adapt it and plan to update the note.
   
3. SAVE NEW DISCOVERIES (Proactive Commit):
   - If NO similar note or solution is found in the brain, you MUST implement the solution first.
   - Once the user confirms the solution works, you MUST proactively offer to save it by invoking:
     - `commit_bugfix` (if it was an error or bug).
     - `commit_knowledge` (if it was a new pattern, playbook, architecture rule, or feature spec).
   - Do not wait for the user to ask you to save it. Suggest saving it immediately after validation!

4. EXCLUDE DUPLICATES:
   - If the knowledge already exists in the vault and has not changed, do NOT create a duplicate note.
"""

@mcp.tool()
async def register_project(name: str, path: str, stack: list, description: str) -> str:
    """
    Registers a new project or updates an existing Project Master Card in Obsidian.
    Use this when analyzing a project for the first time or identifying stack changes.
    """
    logger.info(f"MCP Request: Register project {name}")
    success = await knowledge_engine.register_project(
        name=name,
        path=path,
        stack=stack,
        description=description
    )
    
    if success:
        return f"Project Master Card for '{name}' successfully created/updated in Obsidian."
    return f"Failed to register project '{name}'. Check server logs."

@mcp.tool()
async def commit_knowledge(name: str, content: str, tags: list = None, folder: str = "🧩 Padrões", project: str = "Global") -> str:
    """
    Saves new knowledge (specs, playbooks, architectural patterns) directly to the Obsidian KB.
    Use this to persist technical learnings, patterns, or manuals.
    It will be saved inside the project's folder.
    """
    logger.info(f"Committing new knowledge: {name} under project {project} with tags={tags}")
    success = await knowledge_engine.capture_pattern(
        name=name,
        content=content,
        tags=tags,
        project=project
    )
    
    if success:
        return f"Knowledge successfully committed to project '{project}' as '{name}'."
    return "Failed to commit knowledge. Check logs for details."

@mcp.tool()
async def commit_bugfix(error_log: str, solution: str, project: str = "Global") -> str:
    """
    Saves a bugfix playbook directly to the project's folder in the Obsidian KB.
    Use this after resolving a bug to persist the solution.
    """
    logger.info(f"Committing bugfix for project: {project}")
    success = await knowledge_engine.capture_bugfix(
        error_log=error_log,
        solution=solution,
        project=project
    )
    
    if success:
        return f"Bugfix successfully committed for project '{project}'."
    return "Failed to commit bugfix. Check logs for details."

@mcp.tool()
async def explore_graph(note_name: str) -> str:
    """
    Explores the Obsidian Knowledge Base graph starting from a root note name.
    Identifies all wikilinks [[Note Name]] within the note and provides a summary of connected notes.
    """
    logger.info(f"Exploring graph from note: {note_name}")
    
    resolved = knowledge_engine.vault.find_note_path(note_name)
    if not resolved:
        return f"⚠️ Note '{note_name}' could not be located in the vault."
        
    folder, filename = resolved
    content = knowledge_engine.vault.read_note(folder, filename)
    if not content:
        return f"⚠️ Failed to read content of note '{note_name}'."
        
    metadata, body = MarkdownBuilder.parse(content)
    
    # Match [[Note Name]] or [[Note Name|Alias]]
    wikilinks = re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", body)
    
    results = []
    results.append(f"=== 🕸️ Graph Exploration from: '{note_name}' ===")
    results.append(f"Folder: {folder}")
    if metadata.get("tags"):
        results.append(f"Tags: {', '.join(metadata.get('tags'))}")
    results.append("")
    results.append("## Description/Context:")
    snippet = body[:300].strip() + "..." if len(body) > 300 else body
    results.append(snippet)
    results.append("")
    
    results.append("## Connected Notes (Wikilinks found):")
    if not wikilinks:
        results.append("- (No connections found in this note)")
        return "\n".join(results)
        
    for link in wikilinks:
        link = link.strip()
        link_resolved = knowledge_engine.vault.find_note_path(link)
        if link_resolved:
            l_folder, l_filename = link_resolved
            l_content = knowledge_engine.vault.read_note(l_folder, l_filename)
            if l_content:
                l_metadata, l_body = MarkdownBuilder.parse(l_content)
                l_type = l_metadata.get("type", "Unknown")
                l_tags = l_metadata.get("tags", [])
                results.append(f"🔗 **[[{link}]]** (Folder: {l_folder} | Type: {l_type})")
                if l_tags:
                    results.append(f"   Tags: {', '.join(l_tags)}")
                l_snippet = l_body[:150].strip() + "..." if len(l_body) > 150 else l_body
                results.append(f"   Excerpt: {l_snippet}")
            else:
                results.append(f"🔗 **[[{link}]]** (Folder: {l_folder} | ⚠️ Unreadable)")
        else:
            results.append(f"🔗 **[[{link}]]** (⚠️ Broken Link - Note does not exist in vault)")
            
    return "\n".join(results)

def start_server():
    """Starts the MCP server."""
    logger.info("Starting Danger Line MCP Server...")
    Config.validate()
    mcp.run()

if __name__ == "__main__":
    start_server()
