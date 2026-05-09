import google.generativeai as genai
from typing import Optional
from .base import AIProvider
from src.shared.config import Config
from src.shared.logger import logger

class GeminiProvider(AIProvider):
    """Implementation of AIProvider for Google Gemini."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.GEMINI_API_KEY
        self.model = None
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                logger.info("Gemini AI Provider initialized.")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini Provider: {e}")

    async def generate(self, prompt: str, system_instruction: Optional[str] = None) -> Optional[str]:
        if not self.model:
            logger.warning("Gemini Provider not configured.")
            return None
            
        try:
            # Note: system_instruction can be passed to the model constructor or in the prompt
            # For simplicity here, we append it to the prompt
            full_prompt = f"{system_instruction}\n\nUSER REQUEST:\n{prompt}" if system_instruction else prompt
            response = await self.model.generate_content_async(full_prompt)
            if response and response.text:
                return response.text.strip()
            return None
        except Exception as e:
            logger.error(f"Gemini generation error: {e}")
            return None
