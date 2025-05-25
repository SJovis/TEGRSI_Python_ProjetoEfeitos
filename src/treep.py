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

def main(diretoria: str):

    # Mostrar o conteúdo da diretoria em formato de árvore
    print(f"{Color.CYAN}┌── {diretoria}{Color.END}")
    mostrar_arvore(diretoria)

def mostrar_arvore(diretoria: str):
    dirs_raiz = []
    ficheiros_raiz = []
    total_ficheiros = 0
    total_diretorias = 0
    # os.walk() retorna um gerador(comporta-se como um iterador) que percorre de forma recursiva
    # todos as pastas e ficheiros a partir da diretoria fornecida.
    for dircaminho, dirnomes, ficheiros in os.walk(diretoria):
        # Conta a quantidade de separadores '/' a contar do fim da diretoria raiz até ao final
        depth = dircaminho[len(diretoria):].count(os.sep)
        # Se o nível de recursividade for maior que o args.level a lista diretorias fica vazia impedindo
        # o os.walk() de continuar a descer de níveis.
        if depth >= args.level:
            dirnomes[:] = [] 
            continue # Passa para a próxima iteração
        
        indent = '│   ' * depth # Indentação correspondente ao nível
        dir_nome = os.path.basename(dircaminho) # Nome da diretoria
        dir_caminho = os.path.join(dircaminho) # Caminho da diretoria

        # Exibe as diretorias presentes na raiz
        if depth == 0:
            dirs_raiz = dirnomes.copy()
            ficheiros_raiz  = ficheiros.copy()
            # Exibir as diretorias da raiz
            for sub_dir in dirs_raiz:
                total_diretorias += 1
                line = f"{indent}├── {Color.BOLD + Color.GREEN}{sub_dir}{Color.END}"
                if args.f:
                    line += f" {os.path.join(dircaminho, sub_dir)}"
                print(line)
            continue

        # Exibe as diretorias dentro da diretoria currente
        line = f"{indent}├── {Color.BOLD + Color.GREEN}{dir_nome}{Color.END}"
        if args.f:
            diretoria_path = os.path.join(dircaminho, dir_nome)
            line += f" {diretoria_path}"
        print(line)
        total_diretorias += 1

        # Mostra todos os ficheiros dentro da diretoria currente
        if not args.d:
            for f in ficheiros:
                total_ficheiros += 1
                file_indent = '│   ' * (depth + 1) # Indentação da linha
                file_path = os.path.join(dircaminho, f) # Junta o caminho actual com o nome do ficheiro para obter o caminho do ficheiro
                line = f"{file_indent}└── {f}"
                if args.f:
                    line += f" {file_path}"
                print(line)

    # Após percorrer todas as sub-diretorias exibe os ficheiros da diretoria raiz
    if not args.d:
        for f in ficheiros_raiz:
            total_ficheiros += 1
            line = f"└── {f}"
            if args.f:
                line += f" {os.path.join(diretoria, f)}"
            print(line)
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
