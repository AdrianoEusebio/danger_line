import subprocess
import os
from rich.console import Console

console = Console()

class IAExterna:
    def __init__(self):
        # Comando base configurado no .env (ex: gemini ou claude)
        self.comando_base = os.getenv("EXTERNAL_IA_CMD", "gemini")

    def executar(self, prompt):
        """Dispara o comando do CLI externo com o prompt fornecido."""
        console.print(f"\n[bold green]>>> Handoff: Disparando {self.comando_base}...[/bold green]")
        
        try:
            # Executa o comando e captura a saída
            # Nota: Usamos shell=True no Windows para comandos globais
            resultado = subprocess.run(
                f'{self.comando_base} "{prompt}"', 
                shell=True, 
                capture_output=True, 
                text=True, 
                encoding='utf-8',
                errors='ignore'
            )
            
            if resultado.returncode == 0:
                return resultado.stdout
            else:
                return f"Erro no CLI Externo: {resultado.stderr}"
                
        except Exception as e:
            return f"Falha ao executar {self.comando_base}: {e}"
