import os
from pathlib import Path
from datetime import datetime
from rich.console import Console

console = Console()

class GerenciadorObsidian:
    def __init__(self):
        # Local: Recarrega o caminho do cofre para garantir que o .env foi lido
        self.caminho_vault = os.getenv("OBSIDIAN_VAULT_PATH")
        
        if not self.caminho_vault:
            self.caminho_vault = os.getcwd()
            console.print(f"[yellow]⚠ Aviso: OBSIDIAN_VAULT_PATH não encontrado no .env. Usando pasta local: {self.caminho_vault}[/yellow]")
        else:
            console.print(f"[blue]📂 Contexto Obsidian: {self.caminho_vault}[/blue]")

    def salvar_nota(self, titulo, conteudo, metadados=None, sub_pasta=""):
        """Salva uma nota no Obsidian com Frontmatter opcional."""
        if metadados is None:
            metadados = {}
            
        # Garante que a data está nos metadados
        if "data" not in metadados:
            metadados["data"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Cria o diretório se não existir
        caminho_dir = Path(self.caminho_vault) / sub_pasta
        caminho_dir.mkdir(parents=True, exist_ok=True)

        # Prepara o nome do arquivo (limpando caracteres especiais do título)
        nome_arquivo = "".join(c for c in titulo if c.isalnum() or c in (' ', '-', '_')).strip()
        caminho_completo = caminho_dir / f"{nome_arquivo}.md"

        # Formata o Frontmatter (YAML)
        frontmatter = "---\n"
        for chave, valor in metadados.items():
            if isinstance(valor, list):
                frontmatter += f"{chave}: [{', '.join(valor)}]\n"
            else:
                frontmatter += f"{chave}: {valor}\n"
        frontmatter += "---\n\n"

        # Grava o arquivo
        try:
            with open(caminho_completo, "w", encoding="utf-8") as f:
                f.write(frontmatter)
                f.write(conteudo)
            console.print(f"[green]✔ Nota salva com sucesso: {caminho_completo.relative_to(self.caminho_vault)}[/green]")
            return True
        except Exception as e:
            console.print(f"[red]✘ Erro ao salvar nota no Obsidian: {e}[/red]")
            return False

    def formatar_super_prompt(self, contexto, prompt_otimizado):
        """Helper para criar o corpo da nota do Super-Prompt."""
        corpo = f"# Super-Prompt Gerado\n\n"
        corpo += f"## Contexto Analisado\n"
        corpo += f"```text\n{contexto}\n```\n\n"
        corpo += f"## Prompt Otimizado\n"
        corpo += f"> [!TIP]\n"
        corpo += f"> Copie e cole o texto abaixo na sua IA de preferência.\n\n"
        corpo += f"--- \n\n"
        corpo += f"{prompt_otimizado}\n"
        return corpo
