from src.modules.sanitizer.engine import sanitizer
from src.modules.obsidian.vault import VaultManager
from src.modules.obsidian.templates import KBTemplate
from src.core.distiller import Distiller
from src.shared.logger import logger

class KnowledgeEngine:
    """The central orchestrator that manages the KB pipeline."""
    
    def __init__(self):
        self.vault = VaultManager()
        self.distiller = Distiller()

    async def capture_pattern(self, raw_data: str, name: str, project: str, brain: str) -> bool:
        """Full pipeline: Sanitize -> Distill -> Save as Pattern."""
        try:
            logger.info(f"Capturing new pattern: {name}")
            
            # 1. Sanitize raw data
            clean_raw = await sanitizer.clean(raw_data)
            
            # 2. Distill into AI-optimized content
            distilled_content = await self.distiller.distill(clean_raw, note_type="Pattern")
            if not distilled_content:
                return False
                
            # 3. Create the final note using templates
            final_note = KBTemplate.atomic_pattern(
                name=name,
                project=project,
                brain=brain,
                context="Automatically captured logic.",
                content=distilled_content
            )
            
            # 4. Save to vault (using the correct brain folder)
            folder = brain # In real use, this would map to 01_Backend, etc.
            return self.vault.save_note(folder, name, final_note)
            
        except Exception as e:
            logger.error(f"Error in capture pipeline: {e}")
            return False

    async def register_project(self, name: str, path: str, stack: list, description: str) -> bool:
        """Creates or updates a Project Master Card in the vault."""
        try:
            logger.info(f"Registering project master card: {name}")
            
            # Create the note using the project template
            final_note = KBTemplate.project_master_card(
                name=name,
                path=path,
                stack=stack,
                description=description
            )
            
            # Save to the special "🗂️ Projects" folder
            return self.vault.save_note("🗂️ Projects", name, final_note)
            
        except Exception as e:
            logger.error(f"Error registering project: {e}")
            return False

    async def capture_bugfix(self, error_log: str, project: str, brain: str) -> bool:
        """Full pipeline: Sanitize -> Distill -> Save as Bugfix."""
        try:
            logger.info(f"Capturing bugfix for project: {project}")
            
            clean_log = await sanitizer.clean(error_log)
            distilled_solution = await self.distiller.distill(clean_log, note_type="Bugfix")
            if not distilled_solution:
                return False
                
            final_note = KBTemplate.bugfix_playbook(
                error=error_log[:50] + "...", # Simplified error name
                project=project,
                brain=brain,
                solution=distilled_solution
            )
            
            return self.vault.save_note("🐞 BugTracker", f"fix-{project}-{brain}", final_note)
            
        except Exception as e:
            logger.error(f"Error in bugfix pipeline: {e}")
            return False

# Singleton
knowledge_engine = KnowledgeEngine()
