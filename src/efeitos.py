 #!/usr/bin/env python3
import os
import subprocess
import sys
import math
import argparse
import time
from collections import deque


def main(frase :str, intervalo :float):

    while True:

        clear_screen()
        exibir_menu()

        opcao = input("Opção > ")
        print()

        match opcao.upper():
            case '1':
                clear_screen()
                efeito_1(frase)
            case '2':  
                clear_screen()
                efeito_2(frase)
            case '3':
                clear_screen()
                efeito_3(frase)
            case '4':
                clear_screen()
                efeito_4(frase)
            case '5':
                clear_screen()
                efeito_5(frase)
            case '6':
                clear_screen()
                efeito_6(frase, intervalo)
            case 'T':
                clear_screen()
                efeito_1(frase)
                pause()
                clear_screen()
                efeito_2(frase)
                pause()
                clear_screen()
                efeito_3(frase)
                pause()
                clear_screen()
                efeito_4(frase)
                pause()
                clear_screen()
                efeito_5(frase)
                pause()
                clear_screen()
                efeito_6(frase, intervalo)
                pause()
            case 'E':
                print("O programa vai encerrar")
                sys.exit()
            case _:
                print(f"ERRO: Opção <{opcao}> inválida!")

        print()
        pause()


def exibir_menu():
    sep = 50 * '*'
    print(sep)
    print(f"{"*":2}1 - Diagonal Esquerda{"*":>27}")
    print(f"{"*":2}2 - Diagonal Direita, Texto Invertido {"*":>10}")
    print(f"{"*":2}3 - Diagonais Cruzadas {"*":>25}")
    print(f"{"*":2}4 - Diagonal Direita, Palavras Ordem Inversa{"*":>4}")
    print(f"{"*":2}5 - Em V {"*":>39}")
    print(f"{"*":2}6 - Deslizante {"*":>33}")
    print(f"{"*":2}T - Todos {"*":>38}")
    print(f"{"*":2}E - Encerrar{"*":>36}")
    print(sep)

def clear_screen():
    if os.name == 'posix':
        subprocess.run(['clear'])
    elif os.name == 'nt':
        subprocess.run(['cls'], shell = True)

def efeito_1(txt: str):
    for i in range(len(txt)):
        print(" " * i + txt[i])

def efeito_2(txt: str):
    for i in reversed(range(len(txt))):
        print(" " * i + txt[i])

def efeito_3(txt: str):
    counter = 0
    meio = math.floor(len(txt) / 2)

    for i in range(0,meio):
        print(" " * i + txt[i] + " " * (len(txt) - i * 2) + txt[i])
        counter += 1
    
    print(" "*(meio+1)+txt[meio])
    counter += 1

    for i in range(meio,0,-1):
        print(" " * i + txt[counter] + " " * (len(txt) - i * 2) + txt[counter])
        counter += 1

def efeito_4(txt: str):
    txt_split = txt.split(" ")[::-1]
    counter = 0
    for i in range(len(txt),0,-1):
        print(" "*i + ' '.join(txt_split)[counter])
        counter += 1

def efeito_5(txt: str):
    tamanho = len(txt)
    txt_reversed = txt[::-1]
    for i in range(len(txt)):
        print(" " * i + txt[i] + " " * ((tamanho - (i+1))*2)  + txt_reversed[i])

def efeito_6(txt: str, timer: float):
    spaces = 40 - len(txt)

    txtlist = deque(list(txt))

    for i in range(40):
        txtlist.append(" ")

    while True:
        print("".join(txtlist))
        time.sleep(timer)
        txtlist.rotate(1)
        subprocess.run(['clear']) 



def pause():
    input("Pressione ENTER para continuar...")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Script that adds 3 numbers from CMD"
    )
    parser.add_argument("-i", required=False, type=float, default=0.5, help='Intervalo em segundos.')
    parser.add_argument('strings', nargs='+', help='Lista de srtings')
    args = parser.parse_args()

    frase = " ".join(args.strings).upper()
    
    main(frase, args.i)




