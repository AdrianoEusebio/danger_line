import hashlib
from pathlib import Path

class StorageManager:
    """
    Gerencia o local de armazenamento centralizado para cada projeto.
    Evita criar pastas dentro dos projetos dos usuários (Zero Footprint).
    """
    
    def __init__(self, storage_root: Path | None = None):
        if storage_root is None:
            # Padrão: pasta 'storage' na raiz do Danger Line
            storage_root = Path(__file__).parent.parent.parent / "storage"
        
        self.root = storage_root
        self.root.mkdir(exist_ok=True)

    def get_project_storage_path(self, project_path: Path) -> Path:
        """
        Retorna o path da pasta de dados de um projeto específico.
        Usa o nome do projeto + hash do path absoluto para evitar colisões.
        """
        abs_path = str(project_path.resolve())
        path_hash = hashlib.md5(abs_path.encode()).hexdigest()[:8]
        folder_name = f"{project_path.name}_{path_hash}"
        
        project_storage = self.root / folder_name
        project_storage.mkdir(exist_ok=True)
        
        return project_storage

    def get_all_projects(self) -> list[dict]:
        """Lista todos os projetos que possuem dados no storage."""
        projects = []
        for p in self.root.iterdir():
            if p.is_dir():
                projects.append({
                    "id": p.name,
                    "path": p
                })
        return projects
