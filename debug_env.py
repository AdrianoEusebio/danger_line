import os
import sys
from pathlib import Path
from dotenv import load_dotenv

print("--- DIAGNÓSTICO DANGER LINE ---")
src_path = str(Path("src").resolve())
sys.path.insert(0, src_path)
print(f"PYTHONPATH: {src_path}")

env_path = Path(".env").resolve()
print(f"Procurando .env em: {env_path}")
load_dotenv(dotenv_path=env_path)

vault = os.getenv("OBSIDIAN_VAULT_PATH")
print(f"OBSIDIAN_VAULT_PATH: {vault}")

try:
    from providers.base import ProviderChain
    print("✅ Imports de Providers: OK")
    from core.agent import AgentOrchestrator
    print("✅ Imports de Core: OK")
    from storage.obsidian import ObsidianIntegration
    print("✅ Imports de Storage: OK")
    
    if vault:
        obsidian = ObsidianIntegration(vault)
        print("✅ Inicialização do Obsidian: OK")
except Exception as e:
    print(f"❌ ERRO: {e}")
