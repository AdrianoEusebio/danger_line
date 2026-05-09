from enum import Enum
from typing import List, Dict
from src.shared.logger import logger

class BrainContext(Enum):
    CORE = "00_Core_Library"
    BACKEND = "01_Backend"
    FRONTEND = "02_Frontend"
    INFRA = "03_Infrastructure"
    GENERAL = "General"

class ContextManager:
    """Manages the active 'Brain' context of the system."""
    
    def __init__(self):
        self._active_brain = BrainContext.GENERAL
        logger.info(f"ContextManager initialized. Default brain: {self._active_brain.name}")

    def set_context(self, brain_name: str) -> bool:
        """Sets the active brain context by name."""
        try:
            # Normalize and try to find the enum member
            normalized_name = brain_name.upper().strip()
            self._active_brain = BrainContext[normalized_name]
            logger.info(f"Context switched to: {self._active_brain.name}")
            return True
        except KeyError:
            logger.warning(f"Invalid brain context name: {brain_name}")
            return False

    def get_active_context(self) -> BrainContext:
        """Returns the currently active BrainContext."""
        return self._active_brain

    def get_relevant_folders(self) -> List[str]:
        """Returns the list of Obsidian folders relevant to the current context."""
        folders = [BrainContext.CORE.value]
        if self._active_brain != BrainContext.GENERAL and self._active_brain != BrainContext.CORE:
            folders.append(self._active_brain.value)
        return folders

# Singleton instance
context_manager = ContextManager()

if __name__ == "__main__":
    # Test Manager
    cm = ContextManager()
    print(f"Initial: {cm.get_active_context()}")
    cm.set_context("backend")
    print(f"Switched: {cm.get_active_context()}")
    print(f"Relevant Folders: {cm.get_relevant_folders()}")
