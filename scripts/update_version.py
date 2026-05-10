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
    
    # List of (pattern, replacement_template)
    patterns = [
        (r'(version\s*=\s*")([^"]+)(")', fr'\g<1>{new_version}\g<3>'),
        (r'(DOCKER CLEAN PRO v)([0-9.]+)', fr'\g<1>{new_version}')
    ]
    
    found = False
    new_content = content
    for pattern, replacement in patterns:
        if re.search(pattern, new_content):
            new_content = re.sub(pattern, replacement, new_content)
            found = True
    
    if not found:
        print(f"Erro: Nenhuma chave de versão encontrada em {file_path}", file=sys.stderr)
        sys.exit(1)
    
    file_path.write_text(new_content)
    print(f"Sucesso: Versão atualizada para {new_version} em {file_path}")

def main():
    parser = argparse.ArgumentParser(description="Atualiza a versão no pyproject.toml ou main.py banner")
    parser.add_argument("version", help="Nova versão (ex: 1.1.0 ou v1.1.0)")
    parser.add_argument("--file", default="pyproject.toml", help="Caminho para o arquivo (padrão: pyproject.toml)")
    
    args = parser.parse_args()
    
    file_path = Path(args.file)
    update_version(file_path, args.version)

if __name__ == "__main__":
    main()
