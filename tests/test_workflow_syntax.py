import os
import yaml
import pytest

def test_workflow_exists():
    """Verifica se o arquivo do workflow existe."""
    workflow_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".github", "workflows", "deploy-docs.yml"))
    assert os.path.isfile(workflow_path), "deploy-docs.yml não encontrado"

def test_workflow_content():
    """Verifica se o workflow possui os passos necessários."""
    workflow_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".github", "workflows", "deploy-docs.yml"))
    
    with open(workflow_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    assert data["name"] == "Deploy Starlight Documentation"
    
    # Verifica permissões
    permissions = data.get("permissions", {})
    assert permissions.get("pages") == "write"
    assert permissions.get("id-token") == "write"
    
    # Verifica jobs
    jobs = data.get("jobs", {})
    assert "build" in jobs
    assert "deploy" in jobs
    
    # Verifica passos do build
    steps = jobs["build"]["steps"]
    step_names = [step.get("name") for step in steps]
    assert "Checkout" in step_names
    assert "Setup Node" in step_names
    assert "Install dependencies" in step_names
    assert "Build with Astro" in step_names
    assert "Upload artifact" in step_names
