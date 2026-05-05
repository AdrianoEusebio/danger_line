"""
Cache — Evita re-análise de arquivos não modificados.

TDD: TDD-06-STORAGE-CACHE.MD
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from .models import AnalysisResult


class AnalysisCache:
    """
    Cache de análises baseado em hash do conteúdo do arquivo.
    Um cache miss ocorre quando: arquivo não existe no cache, ou foi modificado.
    """

    INDEX_FILE = "cache_index.json"

    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._index: dict = self._load_index()

    def _load_index(self) -> dict:
        index_path = self.cache_dir / self.INDEX_FILE
        if index_path.exists():
            return json.loads(index_path.read_text(encoding="utf-8"))
        return {}

    def _save_index(self) -> None:
        index_path = self.cache_dir / self.INDEX_FILE
        index_path.write_text(json.dumps(self._index, indent=2), encoding="utf-8")

    @staticmethod
    def compute_hash(file_path: Path) -> str:
        """Computa hash SHA256 do conteúdo do arquivo."""
        content = file_path.read_bytes()
        return hashlib.sha256(content).hexdigest()[:16]

    def get(self, file_path: Path) -> Optional[dict]:
        """
        Retorna dados do cache se o arquivo não foi modificado.
        Retorna None em caso de cache miss.
        """
        current_hash = self.compute_hash(file_path)
        cached = self._index.get(str(file_path))

        if cached and cached.get("file_hash") == current_hash:
            cache_file = self.cache_dir / f"{current_hash}.json"
            if cache_file.exists():
                return json.loads(cache_file.read_text(encoding="utf-8"))

        return None  # Cache miss

    def set(self, file_path: Path, result: AnalysisResult) -> None:
        """Salva resultado no cache."""
        cache_file = self.cache_dir / f"{result.file_hash}.json"
        cache_file.write_text(
            json.dumps(result.to_cache_dict(), indent=2), encoding="utf-8"
        )
        self._index[str(file_path)] = {
            "file_hash": result.file_hash,
            "cached_at": datetime.now().isoformat(),
        }
        self._save_index()

    def invalidate(self, file_path: Path) -> None:
        """Remove entrada do cache para um arquivo."""
        self._index.pop(str(file_path), None)
        self._save_index()
