#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Fri Jul  11 08:43:38 2014

@author: T. Wissenklaus (Francisco Lucas da Silva)

"""

#===============================================================

import rsa
from rsa import PublicKey
import base64
import hashlib
##pip install pycryptodome
from Crypto import Random
from Crypto.Cipher import AES

#===============================================================
#Hash

def resumoHash(chave):
    return hashlib.sha256(str(chave).encode()).hexdigest()#tem o sha512

#===============================================================
#AES

def decriptarAES(conteudo, senha):
    bs = AES.block_size
    senha = hashlib.sha256(senha.encode()).digest()
    conteudo = base64.b64decode(conteudo)
    
    cifra = AES.new(senha, AES.MODE_CBC, conteudo[:bs])
    cifra = cifra.decrypt(conteudo[bs:])
    cifra = cifra[:-ord(cifra[len(cifra)-1:])]
    
    return cifra.decode('utf-8')

#===============================================================

def encriptarAES(conteudo, senha):
    senha = hashlib.sha256(senha.encode()).digest()
    bs = AES.block_size
    conteudo = conteudo + (bs - len(conteudo) % bs) * chr(bs - len(conteudo) % bs)
    vi = Random.new().read(bs)
    cifra = AES.new(senha, AES.MODE_CBC, vi)
    return base64.b64encode(vi + cifra.encrypt(conteudo.encode()))

#===============================================================
#RSA

def carregarChaveRSA(chave):
    return rsa.PrivateKey.load_pkcs1(chave.encode())

#===============================================================

def gerarChaveRSA():
    chavePublica, chavePrivada = rsa.newkeys(2048) #2048 para 245 bytes, 4096 para 501
    return chavePrivada #chavePrivada.save_pkcs1()

#===============================================================

def criptografarRSA(txt, chavePublica): 
    chavePublica = rsa.PublicKey(chavePublica, 65537)
    return base64.b64encode(rsa.encrypt(txt.encode(), chavePublica)).decode()

#===============================================================

def decriptografarRSA(txt, chavePrivada):
    return rsa.decrypt(base64.b64decode(txt.encode()), chavePrivada).decode()

#===============================================================

def assinarRSA(msg, chavePrivada):
    hashMSG = resumoHash(msg)
    assinar = rsa.sign(hashMSG.encode(), chavePrivada, 'SHA-512')
    return base64.b64encode(assinar)

#===============================================================

def verificarRSA(msg, assinatura, chavePublicaAmigo):
    try:        
        hashMSG = resumoHash(msg)
        rsa.verify(hashMSG.encode(),
                   base64.b64decode(assinatura), 
                   PublicKey(chavePublicaAmigo, 65537)
                   )
        return True
    except:
        return False
