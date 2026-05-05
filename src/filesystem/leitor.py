import os
import re
import json
from pathlib import Path
from rich.console import Console

console = Console()

class LeitorDeProjeto:
    def __init__(self):
        # Local: Usa o caminho real do Windows configurado no .env
        self.raiz_projetos = os.getenv("PROJECTS_PATH", os.getcwd())
        self.pastas_ignoradas = {
            "node_modules", "venv", ".git", "__pycache__", 
            ".pytest_cache", ".vscode", ".idea", "dist", "build"
        }

    def listar_diretorio(self, sub_pasta=""):
        """Lista arquivos e pastas, ignorando itens irrelevantes."""
        caminho_alvo = Path(self.raiz_projetos) / sub_pasta
        
        if not caminho_alvo.exists():
            return []
            
        itens = []
        try:
            for item in caminho_alvo.iterdir():
                if item.name in self.pastas_ignoradas:
                    continue
                    
                itens.append({
                    "nome": item.name,
                    "tipo": "diretory" if item.is_dir() else "arquivo",
                    "caminho_relativo": str(item.relative_to(self.raiz_projetos))
                })
        except Exception as e:
            return [{"erro": str(e)}]
        return itens

    def mapear_projeto(self, pasta_projeto, profundidade=2):
        """Cria uma visualização em árvore do projeto para dar visão geral à IA."""
        raiz = Path(self.raiz_projetos) / pasta_projeto
        
        def build_tree(path, current_depth):
            if current_depth > profundidade:
                return "..."
            
            tree = {}
            try:
                for item in path.iterdir():
                    if item.name in self.pastas_ignoradas:
                        continue
                    if item.is_dir():
                        tree[f"📁 {item.name}"] = build_tree(item, current_depth + 1)
                    else:
                        tree[item.name] = "📄"
            except:
                pass
            return tree

        return {pasta_projeto: build_tree(raiz, 1)}

    def ler_arquivo(self, caminho_relativo):
        """Lê o conteúdo de um arquivo específico."""
        caminho_completo = Path(self.raiz_projetos) / caminho_relativo
        
        try:
            with open(caminho_completo, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Erro ao ler arquivo: {e}"

    def extrair_dependencias(self, caminho_relativo):
        """Identifica dependências com base na extensão do arquivo e conteúdo."""
        conteudo = self.ler_arquivo(caminho_relativo)
        extensao = Path(caminho_relativo).suffix.lower()
        
        dependencias = set()
        
        # Regex para Python (import e from)
        if extensao == ".py":
            dependencias.update(re.findall(r'^import\s+([\w, ]+)', conteudo, re.MULTILINE))
            dependencias.update(re.findall(r'^from\s+([\w.]+)\s+import', conteudo, re.MULTILINE))
            
        # Regex para JS/TS/Vue (import e require)
        elif extensao in [".js", ".ts", ".vue"]:
            dependencias.update(re.findall(r"import\s+.*from\s+['\"](.*)['\"]", conteudo))
            dependencias.update(re.findall(r"require\(['\"](.*)['\"]\)", conteudo))
            
        # Regex para PHP (use e require)
        elif extensao == ".php":
            dependencias.update(re.findall(r'^use\s+([\w\\]+);', conteudo, re.MULTILINE))
            dependencias.update(re.findall(r"require(?:_once)?\s+['\"](.*)['\"]", conteudo))

        # Limpeza simples dos nomes capturados
        resultado_limpo = []
        for d in dependencias:
            # Pega apenas o primeiro módulo (antes da vírgula ou ponto)
            limpo = d.split(',')[0].split('.')[0].strip()
            if limpo:
                resultado_limpo.append(limpo)

        return sorted(list(set(resultado_limpo)))

    def analisar_configuracoes(self, pasta_projeto):
        """Busca arquivos de manifesto como package.json ou requirements.txt."""
        caminho_projeto = Path(self.raiz_projetos) / pasta_projeto
        manifestos = {}

        # Requirements.txt (Python)
        req_file = caminho_projeto / "requirements.txt"
        if req_file.exists():
            with open(req_file, 'r') as f:
                manifestos["python"] = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        # Package.json (JS)
        pkg_file = caminho_projeto / "package.json"
        if pkg_file.exists():
            with open(pkg_file, 'r') as f:
                try:
                    data = json.load(f)
                    manifestos["javascript"] = list(data.get("dependencies", {}).keys())
                except:
                    pass

        # Composer.json (PHP)
        comp_file = caminho_projeto / "composer.json"
        if comp_file.exists():
            with open(comp_file, 'r') as f:
                try:
                    data = json.load(f)
                    manifestos["php"] = list(data.get("require", {}).keys())
                except:
                    pass

        return manifestos
