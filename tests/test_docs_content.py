import os
import pytest

def test_docs_index_exists():
    """Verifica se a página inicial da documentação existe (index.md ou index.mdx)."""
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs-site", "src", "content", "docs"))
    
    index_md = os.path.join(base_path, "index.md")
    index_mdx = os.path.join(base_path, "index.mdx")
    
    assert os.path.isfile(index_md) or os.path.isfile(index_mdx), "Página inicial index.md ou index.mdx não encontrada"

def test_docs_index_content():
    """Verifica se o conteúdo da página inicial possui o frontmatter esperado."""
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs-site", "src", "content", "docs"))
    
    index_path = os.path.join(base_path, "index.mdx")
    if not os.path.isfile(index_path):
        index_path = os.path.join(base_path, "index.md")
        
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    assert "title:" in content, "Frontmatter 'title' ausente"
    assert "description:" in content, "Frontmatter 'description' ausente"
    assert "Docker Cleanup Pro" in content, "O título do projeto deve estar no conteúdo"
