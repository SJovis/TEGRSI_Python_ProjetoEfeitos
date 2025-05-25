#!/usr/bin/env python3

"""
treep.py — Listagem em formato de árvore de uma diretoria

Descrição:
    Este script percorre recursivamente uma diretoria e apresenta
    a sua estrutura hierárquica em formato de árvore, com suporte a
    profundidade limitada (-L), exibição de caminhos completos (-f),
    e listagem apenas de diretórios (-d).
"""

import os
import sys
import argparse

# Códigos ANSI para colorir o output das diretorias
class Color:
    GREEN = '\033[92m'
    BOLD = '\033[1m'
    CYAN = '\033[96m'
    END = '\033[0m'

total_ficheiros = 0
total_diretorias = 0

def main(diretoria: str):
    # Mostrar o conteúdo da diretoria em formato de árvore
    mostrar_arvore(diretoria)


def exibir_ficheiros(ficheiros : list[str], depth : int, dirpath : str):
    for f in ficheiros:
        global total_ficheiros
        total_ficheiros += 1
        file_indent = '│   ' * (depth) # Indentação da linha
        file_path = os.path.join(dirpath, f) # Junta o caminho actual com o nome do ficheiro para obter o caminho do ficheiro
        line = f"{file_indent}└── {f}"
        if args.f:
            line += f"{Color.CYAN} {file_path}{Color.END}"
        print(line)

def exibir_diretorias(diretorias : list[str], depth : int, dirpath : str):
    global total_diretorias
    if depth == 0:
        for sub_dir in diretorias:
            print_diretoria(depth=depth, dirpath=dirpath, sub_dir=sub_dir)
    else:
        for sub_dir in diretorias:
                    total_diretorias += 1
                    print_diretoria(depth=depth, dirpath=dirpath, sub_dir=sub_dir)
                    if not args.d:
                        files_path = os.path.join(dirpath,sub_dir)
                        sub_files = [f for f in os.listdir(files_path) if os.path.isfile(os.path.join(files_path,f))]
                        exibir_ficheiros(ficheiros=sub_files, depth=depth+1, dirpath=dirpath)
                    
def print_diretoria(depth : int, dirpath : str, sub_dir : str):
    indent = '│   ' * depth 
    line = f"{indent}├── {Color.BOLD + Color.GREEN}{sub_dir}{Color.END}"
    if args.f:
        line += f"{Color.CYAN} {os.path.join(dirpath, sub_dir)}{Color.END}"
    print(line)


def mostrar_arvore(diretoria: str):

    _, _, ficheiros_raiz = next(os.walk(diretoria))
    # os.walk() retorna um gerador(comporta-se como um iterador) que percorre de forma recursiva
    # todos as pastas e ficheiros a partir da diretoria fornecida.
    for dirpath, dirnames, _ in os.walk(diretoria):
        # Conta a quantidade de separadores '/' a contar do fim da diretoria raiz até ao final
        depth = dirpath[len(diretoria):].count(os.sep)
        # Se o nível de recursividade for maior que o args.level a lista diretorias fica vazia impedindo
        # o os.walk() de continuar a descer de níveis.
        if depth > args.level:
            dirnames[:] = [] 
            continue # Passa para a próxima iteração

        exibir_diretorias(diretorias=dirnames, depth=depth, dirpath=dirpath)

    if not args.d:
        exibir_ficheiros(ficheiros=ficheiros_raiz,depth=0, dirpath=dirpath)
    print()
    # Mostrar número de diretorias e ficheiros encontrados
    print(f"{total_diretorias} diretorias, {total_ficheiros} ficheiros")


def validations(args,unknown):

    # Se for introduzido algum argumento não reconhecido pelo script
    if unknown:
        print(f"Argumentos não reconhecidos: {''.join(unknown)}")

    # Se o caminho introduzido não for identificado como uma diretoria
    if not os.path.isdir(args.diretoria):
        print(f"O caminho '{args.diretoria}' não é uma diretoria.")
        sys.exit(1)

    # Se não tiver permissões para aceder à diretoria
    try:
        os.listdir(args.diretoria)
    except PermissionError:
        print(f"Sem permissão para aceder à diretoria {args.diretoria}")
        sys.exit(1)


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

    parser.add_argument(
        '-L', '--level',
        help='Número de níveis de diretorias a exibir',
        type=int,
        default=1,
    )

    # Atribuição dos argumentos introduzidos.
    args, unknown = parser.parse_known_args()

    # VALIDAçÕES
    validations(args, unknown)

    main(args.diretoria)
