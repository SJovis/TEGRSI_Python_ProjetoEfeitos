#!/usr/bin/env python3

import os
import sys
import argparse

def main(diretoria: str):
    print(diretoria)
    print(f"Conteúdo: ", os.listdir(diretoria))
    

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

    # Atribuição dos argumentos introduzidos.
    args, unknown = parser.parse_known_args()

    # Se for introduzido algum argumento não reconhecido pelo script
    if unknown:
        print(f"Argumentos não reconhecidos: {''.join(unknown)}")

    # Se o caminho introduzido não for identificado como uma diretoria
    if not os.path.isdir(args.diretoria):
        parser.error(f"O caminho '{args.diretoria}' não é uma diretoria.")

    main(args.diretoria)