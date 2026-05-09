import os
from typing import Optional
from src.shared.logger import logger
from src.shared.config import Config

class AIScrubber:
    """Dynamic security layer using AI to identify and remove sensitive context or production data."""
    
    def __init__(self):
        self.enabled = False
        self.model = None
        
        # Initialize Gemini if key is present
        if Config.GEMINI_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.enabled = True
                logger.info("AI Scrubber initialized with Gemini Flash.")
            except Exception as e:
                logger.error(f"Failed to initialize AI Scrubber: {e}")

    async def scrub_dynamic(self, text: str) -> str:
        """Asks AI to rewrite/sanitize text while preserving technical logic."""
        if not self.enabled or not self.model:
            return text
            
        prompt = f"""
        Act as a Security Data Sanitizer. 
        Your task is to identify and remove any REAL production data, specific client names, 
        internal IPs, or secret strings from the technical text below.
        Replace them with generic placeholders (e.g., <PRODUCTION_DB>, <CLIENT_NAME>, <INTERNAL_IP>).
        Maintain the technical logic, code snippets, and architecture details intact.
        
        TEXT TO SANITIZE:
        {text}
        
        OUTPUT ONLY THE SANITIZED TEXT:
        """
        
        try:
            # Note: This is a simplified call. Real implementation might need better error handling.
            response = await self.model.generate_content_async(prompt)
            if response and response.text:
                return response.text.strip()
            return text
        except Exception as e:
            logger.warning(f"AI Scrubbing failed, falling back to original text: {e}")
            return text

if __name__ == "__main__":
    import asyncio
    
    async def test():
        scrubber = AIScrubber()
        if scrubber.enabled:
            result = await scrubber.scrub_dynamic("The client 'Banco do Brasil' reported an error in IP 10.0.0.5.")
            print(f"Sanitized: {result}")
        else:
            print("AI Scrubber not enabled.")
            
    asyncio.run(test())
