import requests
import os
import json
from rich.console import Console

console = Console()

class ClienteOllama:
    def __init__(self):
        # Local: Usa localhost em vez de host.docker.internal
        self.url_base = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.modelo = os.getenv("OLLAMA_MODEL", "gemma4:e4b")
        
    def verificar_conexao(self):
        """Verifica se o serviço Ollama está acessível."""
        try:
            resposta = requests.get(f"{self.url_base}/api/tags", timeout=5)
            return resposta.status_code == 200
        except Exception as e:
            console.print(f"[red]Erro ao conectar ao Ollama: {e}[/red]")
            return False

    def gerar_resposta(self, prompt, sistema="Você é o Librarian-AI, um Arquiteto de Contexto."):
        """Envia um prompt para o Ollama e retorna a resposta completa."""
        url = f"{self.url_base}/api/generate"
        
        payload = {
            "model": self.modelo,
            "prompt": prompt,
            "system": sistema,
            "stream": False
        }
        
        try:
            resposta = requests.post(url, json=payload, timeout=60)
            resposta.raise_for_status()
            return resposta.json().get("response", "")
        except Exception as e:
            return f"Erro na geração da IA: {e}"

    def gerar_resposta_streaming(self, prompt, sistema="Você é o Librarian-AI, um Arquiteto de Contexto."):
        """Envia um prompt para o Ollama e gera a resposta via streaming."""
        url = f"{self.url_base}/api/generate"
        
        payload = {
            "model": self.modelo,
            "prompt": prompt,
            "system": sistema,
            "stream": True
        }
        
        try:
            with requests.post(url, json=payload, stream=True, timeout=60) as resposta:
                resposta.raise_for_status()
                for linha in resposta.iter_lines():
                    if linha:
                        json_linha = json.loads(linha)
                        chunk = json_linha.get("response", "")
                        yield chunk
                        if json_linha.get("done", False):
                            break
        except Exception as e:
            yield f"\n[red]Erro no streaming: {e}[/red]"
