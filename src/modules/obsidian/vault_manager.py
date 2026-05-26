import os
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from src.shared.logger import logger
from src.shared.config import Config

class VaultManager:
    """A reusable class to safely manage folder structures and file I/O inside the Obsidian Vault."""

    def __init__(self, vault_path: Optional[str] = None):
        self.vault_path = Path(vault_path) if vault_path else Config.OBSIDIAN_VAULT_PATH
        self.folders = [
            "🗂️ Projects",
            "⚙️ System"
        ]
        self.ensure_structure()

    # Note: We keep the old name _ensure_structure as fallback, but also expose ensure_structure for standard API.
    def _ensure_structure(self):
        self.ensure_structure()

    def ensure_structure(self):
        """Ensures the basic directory structure exists."""
        for folder in self.folders:
            path = self.vault_path / folder
            if not path.exists():
                logger.info(f"Creating vault directory: {folder}")
                path.mkdir(parents=True, exist_ok=True)

    def get_all_folders(self) -> List[str]:
        """Returns all folders in the vault, including dynamically created project folders."""
        try:
            if not self.vault_path.exists():
                return self.folders
            folders = []
            for p in self.vault_path.iterdir():
                if p.is_dir() and not p.name.startswith("."):
                    folders.append(p.name)
            # Ensure folders contains at least the base folders
            for folder in self.folders:
                if folder not in folders:
                    folders.append(folder)
            return folders
        except Exception as e:
            logger.error(f"Failed to scan folders: {e}")
            return self.folders

    def save_note(self, folder: str, filename: str, content: str) -> bool:
        """Saves a markdown note to the specified vault folder."""
        try:
            if not filename.endswith(".md"):
                filename += ".md"
            
            # Sanitize filename (basic)
            filename = filename.replace("/", "-").replace("\\", "-")
            
            target_path = self.vault_path / folder / filename
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            logger.info(f"Note saved: {folder}/{filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to save note {filename}: {e}")
            return False

    def read_note(self, folder: str, filename: str) -> Optional[str]:
        """Reads a note from the vault."""
        try:
            if not filename.endswith(".md"):
                filename += ".md"
            target_path = self.vault_path / folder / filename
            if target_path.exists():
                return target_path.read_text(encoding="utf-8")
            return None
        except Exception as e:
            logger.error(f"Failed to read note {filename}: {e}")
            return None

    def list_notes(self, folder: str) -> List[str]:
        """Lists all notes in a specific folder."""
        try:
            path = self.vault_path / folder
            if path.exists():
                return [f.name for f in path.glob("*.md")]
            return []
        except Exception as e:
            logger.error(f"Failed to list notes in {folder}: {e}")
            return []

    def find_note_path(self, note_name: str) -> Optional[Tuple[str, str]]:
        """Finds the folder and exact filename of a note by its name (without folder) across all vault folders."""
        # Normalize target filename
        filename = note_name if note_name.endswith(".md") else f"{note_name}.md"
        for folder in self.get_all_folders():
            for n in self.list_notes(folder):
                if n.lower() == filename.lower():
                    return folder, n
        return None

    def find_notes_by_tags(self, tags: List[str]) -> List[Dict[str, Any]]:
        """Searches notes across all folders matching the specified tags in metadata."""
        from src.modules.obsidian.markdown_parser import MarkdownBuilder
        results = []
        for folder in self.get_all_folders():
            for note_name in self.list_notes(folder):
                content = self.read_note(folder, note_name)
                if content:
                    metadata, body = MarkdownBuilder.parse(content)
                    note_tags = metadata.get("tags", [])
                    if isinstance(note_tags, list):
                        # Case-insensitive checks for matching all tags
                        normalized_note_tags = [t.lower() for t in note_tags]
                        normalized_search_tags = [t.lower() for t in tags]
                        if all(t in normalized_note_tags for t in normalized_search_tags):
                            results.append({
                                "filename": note_name,
                                "folder": folder,
                                "metadata": metadata,
                                "content": content
                            })
        return results
