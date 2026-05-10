import os
import pytest
from pathlib import Path
import sys

# Add project root to sys.path to import the script if needed
# But since it's a standalone script, we might just call it via subprocess or import its function
# Let's assume it has an update_version(file_path, new_version) function for easier testing

# Import the script logic (we'll define it in a way that's importable)
# For now, let's just use subprocess to test it as a CLI tool as intended

import subprocess

def test_version_update_basic(tmp_path):
    """Testa atualização básica de versão."""
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('version = "1.0.0"\nname = "test"')
    
    script_path = Path(__file__).parent.parent.parent / "scripts" / "update_version.py"
    
    # Run script: python scripts/update_version.py 1.1.0 --file tmp_path/pyproject.toml
    result = subprocess.run(
        [sys.executable, str(script_path), "1.1.0", "--file", str(pyproject)],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0
    assert 'version = "1.1.0"' in pyproject.read_text()

def test_version_update_with_v_prefix(tmp_path):
    """Testa se remove o prefixo 'v'."""
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('version = "1.0.0"\n')
    
    script_path = Path(__file__).parent.parent.parent / "scripts" / "update_version.py"
    
    subprocess.run(
        [sys.executable, str(script_path), "v1.2.3", "--file", str(pyproject)],
        check=True
    )
    
    assert 'version = "1.2.3"' in pyproject.read_text()

def test_version_update_preserves_other_content(tmp_path):
    """Testa se preserva o resto do arquivo."""
    content = """[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "docker-clean-pro"
version = "1.0.0"
description = "test"
"""
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(content)
    
    script_path = Path(__file__).parent.parent.parent / "scripts" / "update_version.py"
    
    subprocess.run(
        [sys.executable, str(script_path), "2.0.0", "--file", str(pyproject)],
        check=True
    )
    
    new_content = pyproject.read_text()
    assert 'version = "2.0.0"' in new_content
    assert 'name = "docker-clean-pro"' in new_content
    assert 'build-backend = "hatchling.build"' in new_content

def test_version_not_found(tmp_path):
    """Testa comportamento quando a chave version não é encontrada."""
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('name = "test"')
    
    script_path = Path(__file__).parent.parent.parent / "scripts" / "update_version.py"
    
    result = subprocess.run(
        [sys.executable, str(script_path), "1.1.0", "--file", str(pyproject)],
        capture_output=True,
        text=True
    )
    
    assert result.returncode != 0
    assert "Nenhuma chave de versão encontrada" in result.stderr

def test_version_update_main_py_banner(tmp_path):
    """Testa se o script consegue atualizar a versão no banner do main.py."""
    main_py = tmp_path / "main.py"
    main_py.write_text('console.print("           DOCKER CLEAN PRO v1.1 (PY)", style="bold cyan")')
    
    script_path = Path(__file__).parent.parent.parent / "scripts" / "update_version.py"
    
    # Tentamos atualizar a versão para 2.0.0
    subprocess.run(
        [sys.executable, str(script_path), "2.0.0", "--file", str(main_py)],
        check=True
    )
    
    content = main_py.read_text()
    assert 'DOCKER CLEAN PRO v2.0.0 (PY)' in content
