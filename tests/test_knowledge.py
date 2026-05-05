"""
TDD-11-13: Knowledge Base (QA, Compiler, Feedback)
"""
import pytest
from core.knowledge.qa_engine import WikiQA
from core.knowledge.compiler import KBCompiler
from core.knowledge.feedback import FeedbackLoop
from storage.wiki_store import WikiStore
from storage.markdown_store import MarkdownStore
from storage.models import SolutionResult

class TestKBQA:
    """T-13.x — Q&A Engine."""

    async def test_13_1_query_finds_exact_match(self, mock_chain, sample_wiki_articles, tmp_path):
        """T-13.1: Busca deve encontrar conteúdo no wiki."""
        wiki_path = tmp_path / "wiki"
        store = WikiStore(wiki_path)
        
        # Popular wiki
        for slug, content in sample_wiki_articles.items():
            store.write_article(slug, content)
            
        qa = WikiQA(mock_chain, store)
        
        # Mockando a resposta da IA para o Q&A
        from providers.base import CompletionResponse, ProviderName
        from unittest.mock import AsyncMock
        mock_chain._providers[0].complete = AsyncMock(return_value=CompletionResponse(
            content="Use bcrypt for hashing. See [[auth_system]].",
            provider=ProviderName.GROQ
        ))

        result = await qa.query("How to handle login?")
        
        assert not result.not_found
        assert "bcrypt" in result.answer
        assert "auth_system" in result.sources

class TestFeedbackLoop:
    """T-13.6: Filed Back Loop."""

    def test_13_6_filed_back_saves_solution(self, tmp_workspace):
        """T-13.6: Feedback deve salvar a solução na camada raw/."""
        store = MarkdownStore(tmp_workspace / "danger_line")
        feedback = FeedbackLoop(store)
        
        sol = SolutionResult(
            filename="auth.py",
            problem="Insecure login",
            solution="Add bcrypt hashing",
            source="premium",
            difficulty=3
        )
        
        path = feedback.file_back_solution(sol)
        assert path.exists()
        assert "bcrypt" in path.read_text()
        assert (tmp_workspace / "danger_line" / "raw" / "solutions").exists()
