import os
import pytest

def test_banner_content():
    """Verifica se o banner no main.py exibe o novo nome do projeto."""
    main_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "main.py"))
    
    with open(main_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    assert "DOCKER CLEAN PRO" in content
    assert "v1.1 (PY)" in content # Manter a versão atual por enquanto
