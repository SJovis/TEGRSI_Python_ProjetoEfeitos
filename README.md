# Efeitos

## 📜 Sobre o Script

Este script exibe efeitos visuais com texto no terminal, como diagonais, cruzamentos, e animações deslizantes.

## Como usar:

```bash
./efeitos.py [-i INTERVALO] texto a ser exibido
```

* -i (opcional): intervalo de tempo (em segundos) usado no efeito deslizante. Padrão: 0.5.

* texto: frase a ser exibida nos efeitos. Coloca entre aspas se tiver espaços.

**Exemplo:**

```bash
chmod +x efeitos.py
./efeitos.py -i 0.2 Hello world
```