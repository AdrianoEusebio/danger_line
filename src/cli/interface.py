import re
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from core.agente import AgenteLibrarian
from core.ferramentas import ler_arquivo_e_dependencias

console = Console()

class InterfaceCLI:
    def __init__(self):
        self.agente = AgenteLibrarian()

    def scan_mentions(self, texto):
        """Busca por @arquivo no texto e carrega o conteúdo."""
        mentions = re.findall(r"@([\w./\\]+)", texto)
        contexto_extra = ""
        
        for m in mentions:
            console.print(f"[yellow]🔍 Detectada menção automática: {m}[/yellow]")
            # Tenta ler o arquivo. Como é local, pode ser caminho relativo ou absoluto.
            # Aqui assumimos que se não houver projeto selecionado, tentamos o path literal.
            try:
                # Divide em projeto/arquivo se houver uma barra, ou tenta o path direto
                partes = m.split('/', 1)
                projeto = partes[0] if len(partes) > 1 else "."
                arquivo = partes[1] if len(partes) > 1 else partes[0]
                
                res = ler_arquivo_e_dependencias(projeto, arquivo)
                contexto_extra += f"\n--- CONTEÚDO DE {m} ---\n{res['conteudo']}\nDeps: {res['dependencias']}\n"
            except Exception as e:
                console.print(f"[red]⚠ Não consegui ler {m} automaticamente: {e}[/red]")
        
        return contexto_extra

    def menu_principal(self):
        console.print(Panel(
            "[bold green]Librarian-AI: Agente Local + IA de Performance[/bold green]\n"
            "Modo Local Ativado. Acesso total ao seu PC.\n"
            "Dica: Use [bold cyan]@arquivo[/bold cyan] para injetar contexto automaticamente."
        ))
        
        while True:
            pergunta = Prompt.ask("\n[bold cyan]Você[/bold cyan]").strip()
            
            if pergunta.lower() in ["sair", "exit", "quit"]:
                console.print("[yellow]Desligando o Agente...[/yellow]")
                break
            
            if not pergunta:
                continue

            # Scanner de @mensões
            contexto_extra = self.scan_mentions(pergunta)
            prompt_final = pergunta
            if contexto_extra:
                prompt_final = f"{contexto_extra}\n\nPERGUNTA DO USUÁRIO: {pergunta}"
                
            try:
                self.agente.executar(prompt_final)
            except Exception as e:
                console.print(f"[red]Erro no Agente: {e}[/red]")
