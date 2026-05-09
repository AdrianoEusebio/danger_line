import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from fastmcp import FastMCP
from src.shared.logger import logger
from src.shared.config import Config
from src.core.engine import knowledge_engine
from src.modules.context.manager import context_manager
from src.modules.context.detector import ContextDetector

# Initialize FastMCP Server
mcp = FastMCP("Danger Line")

@mcp.tool()
async def ping() -> str:
    """Verifies that the Danger Line MCP server is alive."""
    return "pong - Danger Line is active"

@mcp.tool()
async def get_active_brain() -> str:
    """Returns the currently active brain context."""
    return f"Active Brain: {context_manager.get_active_context().name}"

@mcp.tool()
async def switch_brain(context_name: str) -> str:
    """Manually switches the active brain context (CORE, BACKEND, FRONTEND, INFRA)."""
    if context_manager.set_context(context_name):
        return f"Successfully switched to {context_name} context."
    return f"Failed to switch context. Invalid name: {context_name}"

@mcp.tool()
async def query_kb(query: str) -> str:
    """
    Searches the Knowledge Base (Obsidian) for relevant patterns, specs, or solutions.
    Always prioritizes the active brain context using DFS (Direct File System).
    """
    logger.info(f"Querying KB for: {query}")
    relevant_folders = context_manager.get_relevant_folders()
    
    results = []
    results.append(f"### 🔍 Search Results for: '{query}'")
    results.append(f"Context: {context_manager.get_active_context().name}")
    results.append(f"Searching in: {', '.join(relevant_folders)}\n")

    found_any = False
    for folder in relevant_folders:
        notes = knowledge_engine.vault.list_notes(folder)
        # Simple keyword match for the query in filenames
        matches = [n for n in notes if query.lower() in n.lower()]
        
        for match in matches:
            content = knowledge_engine.vault.read_note(folder, match)
            if content:
                found_any = True
                results.append(f"---")
                results.append(f"📄 **Note: {match}** (Folder: {folder})")
                # Show first 300 chars of content as a snippet
                snippet = content[:300].strip() + "..." if len(content) > 300 else content
                results.append(snippet)

    if not found_any:
        results.append("⚠️ No matching notes found in the current context.")
        results.append("Tip: Try switching brain context using 'switch_brain' if searching for another area.")

    return "\n".join(results)

@mcp.tool()
async def commit_knowledge(raw_data: str, name: str, note_type: str = "Pattern") -> str:
    """
    Sanitizes, distills, and saves new knowledge to the Obsidian KB.
    Use this to save bugfixes, technical specs, or new architectural patterns.
    """
    logger.info(f"Committing new knowledge: {name} ({note_type})")
    
    # Detect brain from name or content if possible
    suggested_brain = context_manager.get_active_context().name
    
    success = await knowledge_engine.capture_pattern(
        raw_data=raw_data,
        name=name,
        project="Global",
        brain=suggested_brain
    )
    
    if success:
        return f"Knowledge successfully committed to {suggested_brain} as {name}."
    return "Failed to commit knowledge. Check logs for details."

def start_server():
    """Starts the MCP server."""
    logger.info("Starting Danger Line MCP Server...")
    Config.validate()
    mcp.run()

if __name__ == "__main__":
    start_server()
