import httpx
from typing import Optional, Dict, Any, List
from src.shared.logger import logger
from src.shared.config import Config

class ObsidianAPIClient:
    """Client for the Obsidian Local REST API plugin."""
    
    def __init__(self):
        self.base_url = Config.OBSIDIAN_API_URL
        self.api_key = Config.OBSIDIAN_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Optional[Dict]:
        """Generic request handler."""
        if not self.api_key:
            logger.warning("Obsidian API Key missing. API calls will fail.")
            return None
            
        url = f"{self.base_url}{endpoint}"
        try:
            async with httpx.AsyncClient(verify=False) as client:
                response = await client.request(method, url, headers=self.headers, json=data, timeout=5.0)
                if response.status_code in [200, 201, 204]:
                    return response.json() if response.status_code != 204 else {"status": "success"}
                else:
                    logger.error(f"Obsidian API Error ({response.status_code}): {response.text}")
                    return None
        except Exception as e:
            logger.error(f"Obsidian API Connection Failed: {e}")
            return None

    async def get_active_file(self) -> Optional[Dict]:
        """Returns the content and metadata of the active file in Obsidian."""
        return await self._request("GET", "/active")

    async def search(self, query: str) -> List[Dict]:
        """Performs a search using the Obsidian engine."""
        result = await self._request("POST", "/search/", data={"query": query})
        return result if result else []

    async def open_note(self, path: str) -> bool:
        """Opens a specific note in the Obsidian UI."""
        # path is relative to vault root
        result = await self._request("POST", f"/open/{path}", data={})
        return result is not None

    async def get_all_files(self) -> List[str]:
        """Lists all files in the vault via API."""
        result = await self._request("GET", "/files/")
        if result and "files" in result:
            return result["files"]
        return []

if __name__ == "__main__":
    import asyncio
    
    async def test():
        client = ObsidianAPIClient()
        print("Testing connection...")
        files = await client.get_all_files()
        if files:
            print(f"Connected! Found {len(files)} files.")
        else:
            print("Failed to connect or vault is empty.")
            
    asyncio.run(test())
