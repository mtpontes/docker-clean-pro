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
