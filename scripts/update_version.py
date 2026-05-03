#!/usr/bin/env python3
import re
import sys
import argparse
from pathlib import Path

def update_version(file_path: Path, new_version: str):
    if not file_path.exists():
        print(f"Erro: Arquivo {file_path} não encontrado.", file=sys.stderr)
        sys.exit(1)

    # Normalize version: remove 'v' prefix
    if new_version.startswith('v'):
        new_version = new_version[1:]

    content = file_path.read_text()
    
    # Regex to find version = "..."
    # We use a non-greedy match to ensure we only catch the version string
    version_pattern = r'(version\s*=\s*")([^"]+)(")'
    
    if not re.search(version_pattern, content):
        print(f"Erro: Chave 'version' não encontrada em {file_path}", file=sys.stderr)
        sys.exit(1)

    new_content = re.sub(version_pattern, fr'\g<1>{new_version}\g<3>', content)
    
    file_path.write_text(new_content)
    print(f"Sucesso: Versão atualizada para {new_version} em {file_path}")

def main():
    parser = argparse.ArgumentParser(description="Atualiza a versão no pyproject.toml")
    parser.add_argument("version", help="Nova versão (ex: 1.1.0 ou v1.1.0)")
    parser.add_argument("--file", default="pyproject.toml", help="Caminho para o arquivo (padrão: pyproject.toml)")
    
    args = parser.parse_args()
    
    file_path = Path(args.file)
    update_version(file_path, args.version)

if __name__ == "__main__":
    main()
