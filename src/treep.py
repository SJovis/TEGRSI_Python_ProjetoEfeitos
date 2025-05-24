#!/usr/bin/env python3

import os
import sys
import argparse

def main(diretoria: str):
    print(diretoria)
    

if __name__ == "__main__":
    # Configuração de argparse para defenir e ler os argumentos na chamada do script
    parser = argparse.ArgumentParser(
        description="Este script exibe o conteúdo de uma directoria em formato de árvore",
        epilog="Exemplo: ./treep.py ~/Desktop/"
    )
    parser.add_argument(
        'diretoria',
        help='Caminho para a diretoria',
        type=str,
    )

    args, unknown = parser.parse_known_args()

    if unknown:
        print(f"Argumentos não reconhecidos: {''.join(unknown)}")

    if not os.path.isdir(args.diretoria):
        parser.error(f"O caminho '{args.directory}' não é uma diretoria.")

    main(args.diretoria)