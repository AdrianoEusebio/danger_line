from src.modules.obsidian.markdown_parser import MarkdownBuilder

def test_markdown_builder_build_rascunho():
    meta = {"title": "Test Note", "tags": ["tag1", "tag2"]}
    content = "# Hello World\nBody content here."
    result = MarkdownBuilder.build(meta, content)
    
    assert "title: Test Note" in result
    assert "tags: [tag1, tag2, contexto/rascunho]" in result
    assert "date: " in result
    assert "# Hello World" in result

def test_markdown_builder_build_medio():
    meta = {"title": "Test Note Medium"}
    content = "A" * 600
    result = MarkdownBuilder.build(meta, content)
    assert "contexto/medio" in result

def test_markdown_builder_build_profundo():
    meta = {"title": "Test Note Deep"}
    content = "B" * 2100
    result = MarkdownBuilder.build(meta, content)
    assert "contexto/profundo" in result

def test_markdown_builder_build_project_link():
    meta = {"title": "Test Note Link", "project": "MyProj"}
    content = "Some short text."
    result = MarkdownBuilder.build(meta, content)
    assert "[[MyProj]]" in result

def test_markdown_builder_build_project_link_legacy():
    meta = {"title": "Test Note Legacy", "project": "MyProj"}
    content = "Legacy reference: [[Project Master Card: MyProj]]"
    result = MarkdownBuilder.build(meta, content)
    assert "[[MyProj]]" in result
    assert "[[Project Master Card: MyProj]]" not in result

def test_markdown_builder_parse():
    raw_md = """---
title: Parse Note
tags: ["t1", "t2"]
date: 2026-05-25
---
# Body
Hello from body."""
    meta, body = MarkdownBuilder.parse(raw_md)
    assert meta["title"] == "Parse Note"
    assert meta["tags"] == ["t1", "t2"]
    assert meta["date"] == "2026-05-25"
    assert body == "# Body\nHello from body."
