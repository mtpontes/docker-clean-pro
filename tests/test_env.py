import sys

def test_python_version():
    assert sys.version_info >= (3, 8)

def test_imports():
    import typer
    import rich
    import docker
    import psutil
    assert True
