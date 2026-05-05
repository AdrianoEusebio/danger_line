"""
MarkdownStore — Armazenamento em 3 camadas: cache, raw/, wiki/.

Camada 1 — cache/  : JSON para evitar re-análise (AnalysisCache)
Camada 2 — raw/    : Markdown append-only, alimenta o KB Compiler
Camada 3 — wiki/   : Compilado pelo KB Compiler (nunca escrito diretamente aqui)

TDD: TDD-06-STORAGE-CACHE.MD
"""
from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

from .models import AnalysisResult, SolutionResult


class MarkdownStore:
    """Gerencia escrita nas camadas raw/ e wiki/."""

    RAW_FRONTMATTER = """\
---
title: "{title}"
type: "{doc_type}"
date: "{date}"
language: "{language}"
difficulty: {difficulty}
provider: "{provider}"
tags: [danger-line, {doc_type}, {language}]
---

"""

    def __init__(self, project_danger_line_path: Path):
        """
        Args:
            project_danger_line_path: Path para a pasta danger_line/ do projeto.
                Ex: C:/MeuProjeto/danger_line/
        """
        self.base = project_danger_line_path
        self.raw_analyses = self.base / "raw" / "analyses"
        self.raw_solutions = self.base / "raw" / "solutions"
        self.raw_classifications = self.base / "raw" / "classifications"
        self.raw_reviews = self.base / "raw" / "reviews"

        # Criar estrutura se não existir
        for folder in [
            self.raw_analyses,
            self.raw_solutions,
            self.raw_classifications,
            self.raw_reviews,
        ]:
            folder.mkdir(parents=True, exist_ok=True)

    def save_analysis(self, result: AnalysisResult) -> Path:
        """
        Append em raw/analyses/ — nunca sobrescreve.
        Retorna o path do arquivo criado.
        """
        filename = f"{date.today().isoformat()}_{result.filename.replace('.', '_')}.md"
        filepath = self.raw_analyses / filename

        # Garantir unicidade (append-only — nunca sobrescreve)
        counter = 1
        while filepath.exists():
            stem = f"{date.today().isoformat()}_{result.filename.replace('.', '_')}_{counter}"
            filepath = self.raw_analyses / f"{stem}.md"
            counter += 1

        frontmatter = self.RAW_FRONTMATTER.format(
            title=f"Analysis: {result.filepath}",
            doc_type="analysis",
            date=result.analyzed_at,
            language=result.language,
            difficulty=result.difficulty,
            provider=result.provider_used,
        )

        content = frontmatter + f"# Analysis: {result.filepath}\n\n"
        content += f"## For AI\n\n{result.summary_for_ai}\n\n"
        content += f"## For Human\n\n{result.summary_for_human}\n"

        if result.issues:
            content += "\n## Issues Detected\n\n"
            for issue in result.issues:
                content += f"- {issue}\n"

        filepath.write_text(content, encoding="utf-8")
        return filepath

    def save_solution(self, solution: SolutionResult) -> Path:
        """
        Filed Back: salva solução aprovada em raw/solutions/.
        Retorna o path do arquivo criado.
        """
        filename = f"{date.today().isoformat()}_{solution.filename.replace('.', '_')}.md"
        filepath = self.raw_solutions / filename

        counter = 1
        while filepath.exists():
            stem = f"{date.today().isoformat()}_{solution.filename.replace('.', '_')}_{counter}"
            filepath = self.raw_solutions / f"{stem}.md"
            counter += 1

        content = f"---\ntype: solution\ndate: {solution.filed_at}\n"
        content += f"source: {solution.source}\ndifficulty: {solution.difficulty}\n"
        if solution.wiki_match:
            content += f"wiki_match: \"{solution.wiki_match}\"\n"
        content += "---\n\n"
        content += f"# Solution: {solution.filename}\n\n"
        content += f"## Problem\n\n{solution.problem}\n\n"
        content += f"## Solution\n\n{solution.solution}\n"

        filepath.write_text(content, encoding="utf-8")
        return filepath

    def save_review(self, batch_items: list[dict], batch_number: int) -> Path:
        """Salva batch review (alvará) da IA premium em raw/reviews/."""
        filename = f"{date.today().isoformat()}_batch_{batch_number:03d}.md"
        filepath = self.raw_reviews / filename

        content = f"---\ntype: review\ndate: {datetime.now().isoformat()}\n"
        content += f"items: {len(batch_items)}\n---\n\n"
        content += f"# Batch Review #{batch_number:03d}\n\n"

        for i, item in enumerate(batch_items, 1):
            content += f"## Item {i}: {item.get('filename', 'unknown')}\n\n"
            content += f"**Status**: {item.get('status', 'unknown')}\n"
            content += f"**Notes**: {item.get('notes', '')}\n\n"

        filepath.write_text(content, encoding="utf-8")
        return filepath
