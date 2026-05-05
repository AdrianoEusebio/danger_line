import ollama
import json
import os
import re
from core.ferramentas import FERRAMENTAS_MAP
from rich.console import Console

console = Console()

class AgenteLibrarian:
    def __init__(self):
        # Local: Usa localhost em vez de host.docker.internal
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.modelo = os.getenv("OLLAMA_MODEL", "gemma4:e4b")
        self.cliente = ollama.Client(host=self.host)
        self.historico = []
        self.sistema = """Você é o Librarian-AI, um Arquiteto de Contexto Autônomo.
Seu objetivo é ajudar o usuário a analisar códigos e preparar Super-Prompts para IAs de performance.

Você tem acesso às seguintes ferramentas:
- listar_projetos(): Retorna lista de projetos disponíveis.
- mapear_projeto(projeto): Retorna a árvore de diretórios COMPLETA do projeto (ignora pastas inúteis como venv/node_modules). Use esta ferramenta PRIMEIRO para ter uma visão geral.
- listar_arquivos(projeto, pasta=""): Lista arquivos em uma pasta específica.
- ler_arquivo_e_dependencias(projeto, caminho_arquivo): Lê o código e extrai dependências.
- salvar_no_obsidian(projeto, titulo, conteudo_markdown): Salva o resultado no cofre.
- executar_ia_performance(prompt_final): Dispara o CLI externo com o contexto refinado.

DIRETRIZES DE PERFORMANCE:
1. NÃO repita a mesma ação com os mesmos argumentos.
2. Use 'mapear_projeto' para entender a estrutura antes de ler arquivos individuais.
3. Ignore pastas de sistema ou dependências (venv, node_modules, etc) que já são filtradas automaticamente.
4. Pense passo-a-passo. Se o objetivo for um "resumo", leia os arquivos principais (main, README, config) em vez de todos os arquivos.

Para usar uma ferramenta, você DEVE escrever no formato exatamente assim:
AÇÃO: nome_da_ferramenta(argumentos_em_json)

Quando terminar, escreva RESPOSTA FINAL: [sua mensagem].
"""

    def executar(self, prompt_usuario):
        self.historico.append({"role": "user", "content": prompt_usuario})
        
        # Máximo de 10 passos por interação para evitar loops infinitos
        for _ in range(10):
            console.print("[blue]IA está pensando...[/blue]")
            
            resposta = self.cliente.chat(
                model=self.modelo,
                messages=[{"role": "system", "content": self.sistema}] + self.historico
            )
            
            conteudo = resposta['message']['content']
            console.print(f"\n[bold green]Librarian:[/bold green]\n{conteudo}")
            
            # Procura por uma chamada de ação
            match = re.search(r"AÇÃO:\s+(\w+)\((.*)\)", conteudo)
            
            if match:
                nome_func = match.group(1)
                args_str = match.group(2)
                
                try:
                    args = json.loads(args_str)
                    if nome_func in FERRAMENTAS_MAP:
                        console.print(f"[yellow]⚙ Executando ferramenta: {nome_func}...[/yellow]")
                        resultado = FERRAMENTAS_MAP[nome_func](**args)
                        
                        observacao = f"\nOBSERVAÇÃO: {json.dumps(resultado, indent=2, ensure_ascii=False)}"
                        self.historico.append({"role": "assistant", "content": conteudo})
                        self.historico.append({"role": "user", "content": observacao})
                    else:
                        error_msg = f"\nOBSERVAÇÃO: Erro - Ferramenta '{nome_func}' não existe."
                        self.historico.append({"role": "user", "content": error_msg})
                except Exception as e:
                    error_msg = f"\nOBSERVAÇÃO: Erro ao processar argumentos ou executar: {e}"
                    self.historico.append({"role": "user", "content": error_msg})
            
            elif "RESPOSTA FINAL:" in conteudo:
                self.historico.append({"role": "assistant", "content": conteudo})
                break
            else:
                # Se não houver ação nem resposta final, o modelo apenas conversou
                self.historico.append({"role": "assistant", "content": conteudo})
                break
