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
import io
import re
from contextlib import redirect_stdout

# Códigos ANSI para diferenciar melhor as diretorias dos ficheiros com cores diferentes
class Color:
    GREEN = '\033[92m'
    BOLD = '\033[1m'
    CYAN = '\033[96m'
    END = '\033[0m'
    RED = '\x1b[31m'

# Contadores globais, track de quantas diretorias e ficheiros foram percorridos.
total_ficheiros = 0
total_diretorias = 0

def main(diretoria: str):
    # Exibe em modo árvore todas as diretorias e ficheiros recursivamente
    mostrar_arvore(diretoria)
    exportar_para_html(diretoria) if args.html else None

def mostrar_arvore(diretoria: str):
    # Snapshot dos ficheiros presentes na diretoria root
    _, _, ficheiros_raiz = next(os.walk(diretoria))

    # os.walk() retorna um gerador(comporta-se como um iterador) que percorre de forma recursiva
    # todos as pastas e ficheiros a partir da diretoria fornecida.
    for dirpath, dirnames, _ in os.walk(diretoria):
        # Conta a quantidade de separadores '/' para defenir a profundidade da diretoria atual em relação à root
        depth = dirpath[len(diretoria):].count(os.sep)
        # Se o nível de recursividade for maior que o args.level a lista diretorias fica vazia impedindo
        # o os.walk() de continuar a descer de níveis.
        if depth > args.level:
            dirnames[:] = [] 
            continue # Passa para a próxima iteração

        # Exibe todas as diretorias e os seus ficheiross
        exibir_diretorias(diretorias=dirnames, depth=depth, dirpath=dirpath)

    if not args.d:
        exibir_ficheiros(ficheiros=ficheiros_raiz,depth=0, dirpath=dirpath)
    print()
    # Mostrar número de diretorias e ficheiros encontrados
    print(f"{total_diretorias} diretorias, {total_ficheiros} ficheiros")

# Todos os prints estão formatados com a indentação ser proporcional ao nível de profundidade
def exibir_ficheiros(ficheiros : list[str], depth : int, dirpath : str):
    for f in ficheiros:
        global total_ficheiros
        total_ficheiros += 1
        file_indent = '│   ' * (depth) # Indentação da linha
        file_path = os.path.join(dirpath, f) # Junta o caminho actual com o nome do ficheiro para obter o caminho do ficheiro
        #hasPermission = os.access(file_path, os.R_OK) # permissões não estão a funcionar para ficheiros
        #if hasPermission:
        line = f"{file_indent}└── {f}"
        # else:
         #   line = f"{file_indent}└──{Color.RED} {f}{Color.END}"
        if args.f:
            line += f"{Color.CYAN} {file_path}{Color.END}"
        print(line)


def exibir_diretorias(diretorias : list[str], depth : int, dirpath : str):
    global total_diretorias
    if depth == 0:
        # Se o nível de profundidade for 0, exibe apenas as diretorias sem ficheiros, 
        # Não exibe ficheiros para garantir que os ficheiros da root aparecem sempre em último.
        for sub_dir in diretorias:
            total_diretorias += 1
            print_diretoria(depth=depth, dirpath=dirpath, sub_dir=sub_dir)
    else:
        # Exibe pastas e ficheiros
        for sub_dir in diretorias:
                    total_diretorias += 1
                    print_diretoria(depth=depth, dirpath=dirpath, sub_dir=sub_dir)
                    if not args.d:
                        # Path dos ficheiros da sub-diretoria 
                        files_path = os.path.join(dirpath,sub_dir)
                        sub_files = []
                        # [sub_files.append(f) for f in os.listdir(files_path) if os.path.isfile(os.path.join(files_path,file))]
                        for file in os.listdir(files_path):
                            # Todos os ficheiros validados são guardados
                            if os.path.isfile(os.path.join(files_path,file)):
                                sub_files.append(file) 
                        # São exibidos todos os ficheiros das sub-diretorias
                        exibir_ficheiros(ficheiros=sub_files, depth=depth+1, dirpath=dirpath)

# As diretorias têm o texto a verde e bold e todos os paths/caminhos a ciano 
def print_diretoria(depth : int, dirpath : str, sub_dir : str):
    indent = '│   ' * depth 
    hasPermission = os.access(os.path.join(dirpath, sub_dir), os.R_OK)
    # Vermelho se não tiver permissões
    if hasPermission:
        line = f"{indent}├── {Color.BOLD + Color.GREEN}{sub_dir}{Color.END}"
    else:
        line = f"{indent}├── {Color.BOLD + Color.RED}{sub_dir}{Color.END}"
    if args.f:
        line += f"{Color.CYAN} {os.path.join(dirpath, sub_dir)}{Color.END}"
    print(line)

# Validação de input e argumentos
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

def remove_ansi_code(html : str):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])') # Regex ANSI TAGS
    return ansi_escape.sub('', html)


def exportar_para_html(diretoria: str):
    nome_ficheiro = ''.join([diretoria, '_export.html'])
    # Inicializar ficheiro HTML
    html_file = io.StringIO()
    html_file.write("<html><head><meta charset='utf-8'><title>TREEP.py</title></head><body>")
    html_file.write(f"<h1>Estrutura de {diretoria}</h1><pre><br>")

    # Redireciona a saída padrão temporariamente para capturar o output da árvore
    with redirect_stdout(html_file):
        mostrar_arvore(diretoria)
    html_file.write("</pre></body></html>")
    
    with open(nome_ficheiro, "w", encoding="utf-8") as f:
        # Remove código ANSII e grava o ficheiro
        f.write(remove_ansi_code(html_file.getvalue()))

    print(f"\nEstrutura exportada com sucesso para {nome_ficheiro}")

# Exporta a estrutura para HTML automaticamente após exibir no terminal

if __name__ == "__main__":
    # Configuração de argparse e argumentos opcionais.
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

    parser.add_argument(
        '-H', '--html',
        help='Exportar o output para ficheiro .html',
        action='store_true'
    )

    # Atribuição dos argumentos introduzidos.
    args, unknown = parser.parse_known_args()

    # VALIDAçÕES
    validations(args, unknown)

    main(args.diretoria)
