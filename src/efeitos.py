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
        # Limpa o ecrã, exibe o menu de opções e regista o input do utilizador.

        clear_screen()
        exibir_menu()

        opcao = input("Opção > ")
        print()

        # Dependendo da escolha do utilizador, corre a respetiva função ao efeito escolhido.

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
                # Corre todos os efeitos de texto. Com Pause entre efeitos.
                clear_screen()
                todos()
            case 'E':
                # Encerra o script.
                print("O programa vai encerrar")
                sys.exit()
            case _:
                # Qualquer outro caso exibe mensagem de erro.
                print(f"ERRO: Opção <{opcao}> inválida!")

        print()
        pause()

# Menu de opções de escolha formatado.
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

# Função de limpeza de ecrã em diferentes OS's.
def clear_screen():
    if os.name == 'posix':
        subprocess.run(['clear'])
    elif os.name == 'nt':
        subprocess.run(['cls'], shell = True)

# Efeito Diagonal Esquerda: Exibe cada caracter da string com espaçamento crescente.
def efeito_1(txt: str):
    for i in range(len(txt)):
        print(" " * i + txt[i])

# Efeito Diagonal Direita, Texto Invertido:
# Exibe cada caracter da string invertida com espaçamendo
# decrescente da direita para a esquerda.
def efeito_2(txt: str):
    for i in reversed(range(len(txt))):
        print(" " * i + txt[i])

# Efeito Diagonais Cruzadas: 
# Exibe a string em duplicada na diagonal e invertida.
# As strings cruzam-se no centro.
def efeito_3(txt: str):
    size = len(txt)

    for i, caracter in enumerate(txt):
        linha = [' '] * size  # Cria uma lista com o tamanho da string
        linha[i] = caracter  # Introduz o caracter na posição da diagonal da esquerda
        linha[size - 1 - i] = caracter # Introduz o caracter da diagonal da direita
        print(''.join(linha)) # Transforma a lista em string

# Efeito Diagonal Direita, Palavras Ordem Inversa: 
# Exibe a string na diagonal direita em que a posição
# das palavras é invertida mas não a ordem dos caracteres
def efeito_4(txt: str):
    txt_split = txt.split(" ")[::-1]  # Transfoma a string numa lista e inverte a ordem das palavras
    counter = 0 # Contador de index dos caracteres
    for i in range(len(txt),0,-1): # Contagem inversa do número de caracteres para defenir espaçamento
        print(" "*i + ' '.join(txt_split)[counter])
        counter += 1

# Efeito em V:
# Exibe a string em duplicado numa diagonal invertida mas em formato de V em vez de X.
def efeito_5(txt: str):
    tamanho = len(txt)
    txt_reversed = txt[::-1] # Inverte a ordem dos caracteres da string
    for i in range(len(txt)):
        # Exibe os dois valores da string normal e a invertida com espaçamento entre elas proporcional à posição do caracter.
        print(" " * i + txt[i] + " " * ((tamanho - (i+1))*2)  + txt_reversed[i])

# Efeito Deslizante:
# Exibe a string num ciclo onde a string desliza ao longo da linha e retorna ao início.
# Usa a data structure Deque para alterar a posição da string.
def efeito_6(txt: str, timer: float):

    spaces = 40 - len(txt) # Estabelece o tamanho necessário de espaços para completar 40 caracteres em conjunto com a string
    txtDeque = deque(list(txt)) # convert a string em lista que depois converte para deque

    for i in range(spaces): # Por cada espaço adiciona ao deque para completar os 40 caracteres
        txtDeque.append(" ")

    while True: 
        print("".join(txtDeque)) # Exibe o deque em string
        time.sleep(timer) # Pausa de 0.5s default ou o valor atribuido pelo utilizador
        txtDeque.rotate(1) # Transpõe o deque para uma posição á direita
        subprocess.run(['clear']) # limpa o ecrã

        """
        # SEM DEQUE

        txtlist = list(txt)

        for i in range(spaces): 
            txtlist.append(" ")

        while True:
            print("".join(txtlist))
            time.sleep(timer) # Pausa de 0.5s default ou o valor atribuido pelo utilizador
            ultimo = txtlist.pop() # Guarda o ultimo elemento da lista
            txtlist.insert(0, ultimo) # Adiciona o elemento ao início da lista
            subprocess.run(['clear']) # limpa o ecrã 
        """

def todos(): # Corre todos os efeitos com pause e limpeza de tela entre efeitos
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
    efeito_6(frase, args.i)

def pause(): # Pausa, aguarda input do utilizador para continuar
    input("Pressione ENTER para continuar...")

if __name__ == '__main__':

    # Configuração de argparse para defenir e ler os argumentos na chamada do script
    parser = argparse.ArgumentParser(
        description="Script de efeitos de texto.",
        epilog="Exemplo: ./efeitos.py -i 0.1 hello world"
    )
    # Argumento -i opcional, corresponde ao intervalo de segundos para o efeito_6(deslizante)
    parser.add_argument("-i", "--intervalo", required=False, type=float, default=0.5, help='Opcional, Intervalo em segundos. Default 0.5')
    # Argumentos extras
    parser.add_argument('strings', nargs='+', help='Texto a ser exibido')
    args = parser.parse_args() 
    frase = " ".join(args.strings).upper() # Transforma os argumentos numa string
    main(frase, args.intervalo) # É chamada a função main com os valores dos argumentos
