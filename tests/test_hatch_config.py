import os
import pytest

# Fallback for older python versions
try:
    import tomllib
except ImportError:
    try:
        import pip._vendor.tomli as tomllib
    except ImportError:
        # If everything fails, we can't run this test easily without tomli installed
        pass

def test_hatch_docs_serve_script():
    """Verifica se o script docs-serve está configurado no pyproject.toml."""
    pyproject_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pyproject.toml"))
    
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)
    
    scripts = data.get("tool", {}).get("hatch", {}).get("envs", {}).get("default", {}).get("scripts", {})
    
    assert "docs-serve" in scripts, "Script docs-serve não encontrado no pyproject.toml"
    assert "npm run dev --prefix docs-site" in scripts["docs-serve"], "Comando do script docs-serve incorreto"

def test_hatch_build_scripts():
    """Verifica se os novos scripts de build estão configurados."""
    pyproject_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pyproject.toml"))
    
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)
    
    scripts = data.get("tool", {}).get("hatch", {}).get("envs", {}).get("default", {}).get("scripts", {})
    
    assert "build-local" in scripts, "Script build-local não encontrado"
    assert "clean" in scripts, "Script clean não encontrado"

def test_project_urls():
    """Verifica se as URLs do projeto estão configuradas."""
    pyproject_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pyproject.toml"))
    
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)
    
    urls = data.get("project", {}).get("urls", {})
    
    assert "Repository" in urls
    assert "Documentation" in urls
    assert "Bug Tracker" in urls
    assert urls["Repository"] == "https://github.com/mtpontes/docker-clean-pro"

def test_project_name_and_command():
    """Verifica se o nome do projeto e o comando CLI estão corretos."""
    pyproject_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pyproject.toml"))
    
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)
    
    assert data.get("project", {}).get("name") == "docker-clean-pro"
    assert "docker-clean" in data.get("project", {}).get("scripts", {})
