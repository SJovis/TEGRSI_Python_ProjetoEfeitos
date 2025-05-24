#!/usr/bin/env python3

import os
import sys
import argparse
from colors import color


def main(diretoria: str):
    while True:
        print(diretoria)
        print(f"Conteúdo: ", os.listdir(diretoria))

        # Mostrar o conteúdo da diretoria em formato de árvore
        mostrar_arvore(diretoria)
        print(input("Pressione Enter para continuar ou 'q' para sair: "))
        if input().strip().lower() == 'q':
            print("Saindo...")
            break

def mostrar_arvore(diretoria: str):
    diretorias, ficheiros = listar_conteudo(diretoria)

    for dir in diretorias:
        if dir == diretorias[-1]:
            print(f"{color.bold}└── {dir}{color.end}")
        else:
            print(f"{color.bold}├── {dir}{color.end}")

    for file in ficheiros:
        if file == ficheiros[-1]:
            print(f"└── {file}")
        else:
            print(f"├── {file}")


def listar_conteudo(diretoria: str):
    ficheiros = []
    diretorias = []

    for item in os.listdir(diretoria):
        caminho_completo = os.path.join(diretoria, item)

        if os.path.isdir(caminho_completo):
            diretorias.append(item)
        else:
            ficheiros.append(item)

    return diretorias, ficheiros

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

    # Se não for introduzido nenhuma diretoria
    if not args.diretoria:
        print("Caminho de diretoria não providenciado.")
        input("Pressione Enter para sair...")
        sys.exit(1)

    # Se for introduzido algum argumento não reconhecido pelo script
    if unknown:
        print(f"Argumentos não reconhecidos: {''.join(unknown)}")

    # Se o caminho introduzido não for identificado como uma diretoria
    if not os.path.isdir(args.diretoria):
        print(f"O caminho '{args.diretoria}' não é uma diretoria.")
        input("Pressione Enter para sair...")
        sys.exit(1)

    # Se não tiver permissões para aceder à diretoria
    try:
        os.listdir(args.diretoria)
    except PermissionError:
        print("Sem permissão para aceder a diretoria.")
        input("Pressione Enter para sair...")
        sys.exit(1)

    main(args.diretoria)
