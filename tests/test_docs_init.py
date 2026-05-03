import os
import json
import pytest

def test_docs_site_structure_exists():
    """Verifica se a pasta docs-site e os arquivos base existem."""
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs-site"))
    
    assert os.path.isdir(base_path), "Pasta docs-site não encontrada"
    assert os.path.isfile(os.path.join(base_path, "package.json")), "package.json não encontrado"
    assert os.path.isfile(os.path.join(base_path, "package-lock.json")), "package-lock.json não encontrado"

def test_package_json_dependencies():
    """Verifica se o package.json contém as dependências do Astro e Starlight."""
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs-site"))
    package_json_path = os.path.join(base_path, "package.json")
    
    with open(package_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    dependencies = data.get("dependencies", {})
    assert "astro" in dependencies, "Astro não está nas dependências"
    assert "@astrojs/starlight" in dependencies, "Starlight não está nas dependências"
