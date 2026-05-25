from src.modules.obsidian.markdown_parser import MarkdownBuilder

def test_markdown_builder_build():
    meta = {"title": "Test Note", "tags": ["tag1", "tag2"]}
    content = "# Hello World\nBody content here."
    result = MarkdownBuilder.build(meta, content)
    
    assert "title: Test Note" in result
    assert "tags: [tag1, tag2]" in result
    assert "date: " in result
    assert "# Hello World" in result

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
