#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Fri Jul  11 04:57:55 2014

@author: T. Wissenklaus (Francisco Lucas da Silva)

"""

#===============================================================

import gzip
import random
import string
from datetime import datetime
import base64

#===============================================================

def lerArquivo(path_arquivo):
    with open(path_arquivo, mode='rb') as arq:
        conteudo = arq.read()
    return conteudo

#===============================================================

def compactarString(txt):
    return gzip.compress(bytes(txt,'utf-8'))

#===============================================================

def descompactarString(txt):
    stringDescompactada = gzip.decompress(txt)
    return stringDescompactada

#===============================================================

def gerarStringsAleatorias():
    letters = string.ascii_lowercase
    letrasMinusculas = ''.join(random.choice(letters) for i in range(26))
    letters = string.ascii_uppercase
    letrasMaiusculas = ''.join(random.choice(letters) for i in range(26))
    letters = string.ascii_letters
    letras = ''.join(random.choice(letters) for i in range(26))
    letters = string.digits
    numeros = ''.join(random.choice(letters) for i in range(26))
    letters = string.punctuation
    pontos = ''.join(random.choice(letters) for i in range(26))
    timestamp = str(datetime.timestamp(datetime.now()))

    return letrasMinusculas + letrasMaiusculas + letras + numeros + pontos + timestamp

#===============================================================
