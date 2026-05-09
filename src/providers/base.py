from abc import ABC, abstractmethod
from typing import Optional

class AIProvider(ABC):
    """Abstract base class for AI providers (Gemini, Groq, etc.)."""
    
    @abstractmethod
    async def generate(self, prompt: str, system_instruction: Optional[str] = None) -> Optional[str]:
        pass
