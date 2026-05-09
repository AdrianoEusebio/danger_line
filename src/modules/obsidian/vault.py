import os
from pathlib import Path
from typing import Optional, Dict, Any
from src.shared.logger import logger
from src.shared.config import Config

class VaultManager:
    """Manages direct file system interactions with the Obsidian Vault."""
    
    def __init__(self, vault_path: Optional[str] = None):
        self.vault_path = Path(vault_path) if vault_path else Config.OBSIDIAN_VAULT_PATH
        self._ensure_structure()

    def _ensure_structure(self):
        """Ensures the basic multi-brain directory structure exists."""
        directories = [
            "00_Core_Library",
            "01_Backend",
            "02_Frontend",
            "03_Infrastructure",
            "🗂️ Projects",
            "🐞 BugTracker",
            "⚙️ System"
        ]
        for folder in directories:
            path = self.vault_path / folder
            if not path.exists():
                logger.info(f"Creating vault directory: {folder}")
                path.mkdir(parents=True, exist_ok=True)

    def save_note(self, folder: str, filename: str, content: str) -> bool:
        """Saves a markdown note to the specified vault folder."""
        try:
            if not filename.endswith(".md"):
                filename += ".md"
            
            # Sanitize filename (basic)
            filename = filename.replace("/", "-").replace("\\", "-")
            
            target_path = self.vault_path / folder / filename
            
            # Ensure parent folder exists (if it's a subfolder)
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

    def list_notes(self, folder: str) -> list[str]:
        """Lists all notes in a specific folder."""
        try:
            path = self.vault_path / folder
            if path.exists():
                return [f.name for f in path.glob("*.md")]
            return []
        except Exception as e:
            logger.error(f"Failed to list notes in {folder}: {e}")
            return []

if __name__ == "__main__":
    # Test VaultManager
    vm = VaultManager()
    print(f"Vault Path: {vm.vault_path}")
    print("Folders created successfully.")
