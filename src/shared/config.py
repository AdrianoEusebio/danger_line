import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Centralized configuration for Danger Line."""
    
    # Project Paths
    BASE_DIR = Path(__file__).parent.parent.parent
    SRC_DIR = BASE_DIR / "src"
    
    # Obsidian Configuration
    # Default to a local path if not provided in .env
    OBSIDIAN_VAULT_PATH = Path(os.getenv("OBSIDIAN_VAULT_PATH", str(BASE_DIR / "storage" / "vault")))
    
    # System Settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate(cls):
        """Validates that essential configuration is present."""
        if not cls.OBSIDIAN_VAULT_PATH.exists():
            # Create the vault path if it doesn't exist (safety)
            cls.OBSIDIAN_VAULT_PATH.mkdir(parents=True, exist_ok=True)
        return True

if __name__ == "__main__":
    # Test config loading
    print(f"Base Dir: {Config.BASE_DIR}")
    print(f"Vault Path: {Config.OBSIDIAN_VAULT_PATH}")
    if Config.validate():
        print("✅ Configuration is valid.")
    else:
        print("❌ Configuration is invalid.")
