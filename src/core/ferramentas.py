from filesystem.leitor import LeitorDeProjeto
from filesystem.obsidian import GerenciadorObsidian
from core.ia_externa import IAExterna
import json

leitor = LeitorDeProjeto()
obsidian = GerenciadorObsidian()
ia_ext = IAExterna()

def listar_projetos():
    """Retorna uma lista de nomes dos projetos disponíveis na pasta PROJETOS."""
    itens = leitor.listar_diretorio()
    return [i["nome"] for i in itens if i["tipo"] == "diretory"]

def listar_arquivos(projeto: str, pasta: str = ""):
    """Lista os arquivos dentro de um projeto específico. Pode receber uma subpasta."""
    caminho = f"{projeto}/{pasta}".strip("/")
    return leitor.listar_diretorio(caminho)

def mapear_projeto(projeto: str):
    """Retorna a árvore de diretórios do projeto (ignora pastas inúteis). Use para visão geral."""
    return leitor.mapear_projeto(projeto)

def ler_arquivo_e_dependencias(projeto: str, caminho_arquivo: str):
    """Lê o conteúdo de um arquivo de código e extrai suas dependências automáticas."""
    caminho_total = f"{projeto}/{caminho_arquivo}"
    conteudo = leitor.ler_arquivo(caminho_total)
    deps = leitor.extrair_dependencias(caminho_total)
    return {
        "conteudo": conteudo,
        "dependencias": deps
    }

def salvar_no_obsidian(projeto: str, titulo: str, conteudo_markdown: str):
    """Salva uma análise ou super-prompt no cofre do Obsidian."""
    metadados = {"tags": ["librarian-agent", projeto], "projeto": projeto}
    sucesso = obsidian.salvar_nota(titulo, conteudo_markdown, metadados, sub_pasta=f"Agente/{projeto}")
    return "Sucesso ao salvar no Obsidian" if sucesso else "Erro ao salvar no Obsidian"

def executar_ia_performance(prompt_final: str):
    """Dispara a IA de alta performance (Gemini/Claude) com o contexto refinado."""
    resultado = ia_ext.executar(prompt_final)
    return f"Resultado da IA de Performance:\n{resultado}"

# Mapa de funções para o Agente
FERRAMENTAS_MAP = {
    "listar_projetos": listar_projetos,
    "listar_arquivos": listar_arquivos,
    "mapear_projeto": mapear_projeto,
    "ler_arquivo_e_dependencias": ler_arquivo_e_dependencias,
    "salvar_no_obsidian": salvar_no_obsidian,
    "executar_ia_performance": executar_ia_performance
}
