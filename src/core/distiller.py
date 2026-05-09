from typing import Optional
from src.providers.gemini import GeminiProvider
from src.shared.logger import logger

class Distiller:
    """The Engine that transforms raw data into AI-optimized KB notes."""
    
    def __init__(self, provider=None):
        self.provider = provider or GeminiProvider()
        
    SYSTEM_PROMPT = """
    Act as a Senior Software Architect and Knowledge Engineer.
    Your goal is to DISTILL raw technical data into high-density Markdown notes for an AI Knowledge Base.
    
    RULES:
    1. Language: Always output technical content in ENGLISH.
    2. Format: Use clean Markdown headers (## Context, ## Logic, ## Snippet).
    3. Density: Remove generic filler text. Focus on "The Why" and "The How".
    4. Code: Provide only the essential logic in code blocks.
    5. Placeholders: If you see sensitive data, replace it with <HIDDEN_DATA>.
    
    You will receive raw data (logs, code, or conversations).
    Distill it into a note that an AI developer can use as a "Playbook" or "Spec".
    """

    async def distill(self, raw_data: str, note_type: str = "Pattern") -> Optional[str]:
        """Runs the distillation process via the AI Provider."""
        if not raw_data:
            return None
            
        logger.info(f"Distilling raw data into {note_type}...")
        
        prompt = f"TYPE: {note_type}\nRAW DATA:\n{raw_data}"
        
        result = await self.provider.generate(prompt, system_instruction=self.SYSTEM_PROMPT)
        
        if result:
            logger.info("Distillation complete.")
            return result
        return None
