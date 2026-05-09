import os
from pathlib import Path
from .manager import BrainContext

class ContextDetector:
    """Automatically detects the appropriate brain context based on file paths/extensions."""
    
    EXTENSION_MAP = {
        # Backend
        ".py": BrainContext.BACKEND,
        ".go": BrainContext.BACKEND,
        ".java": BrainContext.BACKEND,
        ".sql": BrainContext.BACKEND,
        ".php": BrainContext.BACKEND,
        ".rb": BrainContext.BACKEND,
        # Frontend
        ".ts": BrainContext.FRONTEND,
        ".tsx": BrainContext.FRONTEND,
        ".js": BrainContext.FRONTEND,
        ".jsx": BrainContext.FRONTEND,
        ".css": BrainContext.FRONTEND,
        ".scss": BrainContext.FRONTEND,
        ".html": BrainContext.FRONTEND,
        ".vue": BrainContext.FRONTEND,
        # Infra
        ".yml": BrainContext.INFRA,
        ".yaml": BrainContext.INFRA,
        ".sh": BrainContext.INFRA,
        "Dockerfile": BrainContext.INFRA,
        "docker-compose": BrainContext.INFRA,
    }

    @classmethod
    def detect(cls, file_path: str) -> BrainContext:
        """Suggests a brain context based on the file name or extension."""
        filename = os.path.basename(file_path)
        ext = os.path.splitext(filename)[1].lower()
        
        # Check by extension first
        if ext in cls.EXTENSION_MAP:
            return cls.EXTENSION_MAP[ext]
            
        # Check by full filename (for Dockerfile, etc.)
        if filename in cls.EXTENSION_MAP:
            return cls.EXTENSION_MAP[filename]
            
        return BrainContext.GENERAL

if __name__ == "__main__":
    # Test Detector
    print(f"main.py -> {ContextDetector.detect('main.py')}")
    print(f"App.tsx -> {ContextDetector.detect('App.tsx')}")
    print(f"docker-compose.yml -> {ContextDetector.detect('docker-compose.yml')}")
    print(f"README.md -> {ContextDetector.detect('README.md')}")
