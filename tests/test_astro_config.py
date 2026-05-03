import os
import re
import pytest

def test_astro_config_exists():
    """Verifica se o arquivo astro.config.mjs existe."""
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs-site", "astro.config.mjs"))
    assert os.path.isfile(config_path), "astro.config.mjs não encontrado"

def test_astro_config_content():
    """Verifica o conteúdo do astro.config.mjs para site, base e starlight."""
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs-site", "astro.config.mjs"))
    
    with open(config_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Verifica site e base
    assert "site: 'https://mtpontes.github.io/docker-cleanup-pro/'" in content or 'site: "https://mtpontes.github.io/docker-cleanup-pro/"' in content, "Configuração 'site' incorreta"
    assert "base: '/docker-cleanup-pro'" in content or "base: \"/docker-cleanup-pro\"" in content, "Configuração 'base' incorreta"
    
    # Verifica se starlight está presente
    assert "starlight(" in content or "starlight {" in content, "Integração Starlight ausente"
    assert "title: 'Docker Cleanup Pro'" in content or 'title: "Docker Cleanup Pro"' in content, "Título do projeto incorreto no Starlight"
