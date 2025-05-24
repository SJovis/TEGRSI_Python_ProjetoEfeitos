#!/usr/bin/env python3

import os
import sys
import argparse
from colors import color


def main(diretoria: str):
    while True:
        print(diretoria)

        # Mostrar o conteúdo da diretoria em formato de árvore
        mostrar_arvore(diretoria)
        print("Pressione 'q' para sair: ")
        user_input = input("> ")
        if user_input.lower() == 'q':
            print("Saindo...")
            break

def mostrar_arvore(diretoria: str):
    diretorias = listar_diretorias(diretoria)


    for dir in diretorias:
        if dir == diretorias[-1]:
            line = []
            line += f"{color.BOLD + color.GREEN}└── {dir}{color.END}"
            if args.f:
                line += f" {diretoria+dir}"
            print(''.join(line))
        else:
            line = []
            line += f"{color.BOLD + color.GREEN}└── {dir}{color.END}"
            if args.f:
                line += f" {diretoria+dir}"
            print(''.join(line))

    if not args.d:
        ficheiros = listar_ficheiros(diretoria)
        for file in ficheiros:
            line = []
            line += file
            if args.f:
                line += f" {diretoria+file}"
            print(''.join(line))

def listar_diretorias(diretoria: str):
    diretorias = []

    for item in os.listdir(diretoria):
        caminho_completo = os.path.join(diretoria, item)

        if os.path.isdir(caminho_completo):
            diretorias.append(item)

    return diretorias

def listar_ficheiros(diretoria: str):
    ficheiros = []

    for item in os.listdir(diretoria):
        caminho_completo = os.path.join(diretoria, item)

        if os.path.isfile(caminho_completo):
            ficheiros.append(item)

    return ficheiros

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

    parser.add_argument(
        '-d',
        help='Exibir apenas diretorias',
        action='store_true',
    )

    parser.add_argument(
        '-f',
        help='Exibir caminho completo de diretorias e ficheiros',
        action='store_true',
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
