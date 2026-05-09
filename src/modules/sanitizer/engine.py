from .shield import StaticShield
from .scrubber import AIScrubber
from src.shared.logger import logger

class SanitizerEngine:
    """The central orchestrator for data sanitization."""
    
    def __init__(self):
        self.static_shield = StaticShield()
        self.ai_scrubber = AIScrubber()

    async def clean(self, text: str, use_ai: bool = True) -> str:
        """Runs text through all sanitization layers."""
        if not text:
            return ""
            
        logger.debug("Starting sanitization process...")
        
        # Layer 1: Static Regex Shield (Fast and Mandatory)
        clean_text = self.static_shield.scrub(text)
        
        # Layer 2: AI Dynamic Scrubber (Smart but slower)
        if use_ai and self.ai_scrubber.enabled:
            logger.debug("Applying AI Scrubber...")
            clean_text = await self.ai_scrubber.scrub_dynamic(clean_text)
            
        logger.debug("Sanitization complete.")
        return clean_text

# Singleton instance
sanitizer = SanitizerEngine()
