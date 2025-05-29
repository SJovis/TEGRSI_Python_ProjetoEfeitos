#!/usr/bin/env python3

"""
treep.py — Listagem em formato de árvore de uma diretoria

Descrição:
    Este script percorre recursivamente uma diretoria e apresenta
    a sua estrutura hierárquica em formato de árvore, com suporte a
    profundidade limitada (-L), exibição de caminhos completos (-f),
    listagem apenas de diretórios (-d) e exportação do output para
    um ficheiro .html (-H). O script exibe primeiro as pastas e depois
    os ficheiros.
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
    # Exporta para um ficheiro html
    exportar_para_html(diretoria) if args.html else None

def mostrar_arvore(diretoria: str):
    # Snapshot dos ficheiros presentes na diretoria root
    rootpath, _, rootfiles = next(os.walk(diretoria))
    print(f'├── {Color.BOLD + Color.GREEN}{rootpath}{Color.END}')

    # os.walk() retorna um gerador(comporta-se como um iterador) que percorre de forma recursiva
    # todos as pastas e ficheiros a partir da diretoria fornecida.
    for dirpath, dirnames, _ in os.walk(diretoria):
        # Conta a quantidade de separadores '/' para defenir a profundidade da diretoria atual em relação à root
        depth = dirpath[len(diretoria):].count(os.sep)
        is_root = rootpath == dirpath # Verifica se a diretoria corrente é a root
        # Se o -L introduzido for 0 mostra apenas as diretorias sem ficheiros
        if args.level == 0:
            print_diretoria(depth=depth-1,
                        dirpath=dirpath,
                        sub_dir=os.path.basename(dirpath), 
                        root=is_root,
                        nofiles=True)
            break
        # Se o nível de recursividade for maior que o args.level a lista diretorias fica vazia impedindo
        # o os.walk() de continuar a descer de níveis.
        if depth > args.level:
            dirnames[:] = [] 
            continue # Passa para a próxima iteração
        
        # Se o dirpath a ser avaliado for o mesmo que a root, salta para a próxima iteração
        if dirpath == diretoria:
            continue
        # Exibe todas as diretorias e os seus ficheiross
        print_diretoria(depth=depth-1,
                        dirpath=dirpath,
                        sub_dir=os.path.basename(dirpath), 
                        root=is_root,
                        nofiles=False)
        
    # Exibe os ficheiros da diretoria root
    if not args.d:
        exibir_ficheiros(ficheiros=rootfiles,depth=0, dirpath=dirpath)
    print()
    # Mostrar número de diretorias e ficheiros encontrados
    print(f"{total_diretorias} diretorias, {total_ficheiros} ficheiros")

# Todos os prints estão formatados com a indentação ser proporcional ao nível de profundidade
def exibir_ficheiros(ficheiros : list[str], depth : int, dirpath : str):
    global total_ficheiros
    for f in ficheiros:
        total_ficheiros += 1
        file_indent = '│   ' * (depth) # Indentação da linha
        # Junta o caminho actual com o nome do ficheiro para obter o caminho do ficheiro
        file_path = os.path.join(dirpath, f)
        # Verifica se é o ultimo ficheiro
        line = f"{file_indent}└── {f}" if f == ficheiros[-1] else f"{file_indent}├── {f}"
        if args.f:
            line += f"{Color.CYAN} {file_path}{Color.END}"
        print(line)

# As diretorias têm o texto a verde e bold e todos os paths/caminhos a ciano 
def print_diretoria(depth : int, dirpath : str, sub_dir : str, root : bool, nofiles: bool):
    global total_diretorias
    # Se a diretoria NÃO for a diretoria root, exibe primeiro o nome da diretoria 
    #if not args.diretoria == dirpath:
    #    indent = '│   ' * depth 
    #    line = f"{indent}├── {Color.BOLD + Color.GREEN}{sub_dir}{Color.END}" 
    #    if args.f:
    #        line += f"{Color.CYAN} {dirpath}{Color.END}"
    #    total_diretorias += 1
    #    print(line)
    #print(dirpath)
    # Se a diretoria tiver sub pastas, exibe primeiro as pastas.
    path, sub_folders, _ = next(os.walk(dirpath))
    print(next(os.walk(dirpath)))
    if sub_folders:
        for subf in sub_folders:
            indent = '│   ' * (depth)
            line = f"{indent}├── {Color.BOLD + Color.GREEN}{os.path.basename(subf)}{Color.END}"
            if args.f:
                line += f"{Color.CYAN} {os.path.join(dirpath, subf)}{Color.END}"
            total_diretorias += 1
            print(line)
    
    # Por fim exibe os ficheiros se não tiver opção -d ou {nofiles}
    # {nofiles} é usado para quando queremos exibir só as diretorias sem os ficheiros respetivos
    if not args.d or nofiles:
        ficheiros = []
        for f in os.listdir(dirpath):
            # Se o f for avaliado como ficheiro adiciona à lista.
            if os.path.isfile(os.path.join(dirpath, os.path.basename(f))):
                ficheiros.append(f)
        # Se a diretoria a ser avaliada for root não exibe ficheiros
        if not root:
            exibir_ficheiros(ficheiros=ficheiros, depth=depth+1, dirpath=dirpath)

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
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])') # Regex para ANSI TAGS
    return ansi_escape.sub('', html)


def exportar_para_html(diretoria: str):
    nome_ficheiro = ''.join([diretoria.split('/')[-1], '_export.html'])
    # Inicializar ficheiro HTML
    html_file = io.StringIO()
    # A tag <pre> de html permite manter o formato do texto
    html_file.write("<html><head><meta charset='utf-8'><title>TREEP.py</title></head><body>")
    html_file.write(f"<h1>Estrutura de {diretoria}</h1><pre><br>")

    # Redireciona a saída padrão temporariamente para capturar o output da funcção {mostrar_arvore}
    with redirect_stdout(html_file):
        mostrar_arvore(diretoria)

    html_file.write("</pre></body></html>")
    
    # Cria um ficheiro 
    with open(f'{nome_ficheiro}', "w", encoding="utf-8") as f:
        # Remove código ANSII e grava o ficheiro
        f.write(remove_ansi_code(html_file.getvalue()))

    print(f"\nEstrutura exportada com sucesso para {diretoria}/{nome_ficheiro}")

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

    # Normaliza a entrada de diretoria para tornar consistente a quantidade de '/' como separadores.
    args.diretoria = os.path.abspath(args.diretoria).rstrip(os.sep)

    # VALIDAçÕES
    validations(args, unknown)

    main(args.diretoria)
