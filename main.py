#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Fri Jul  11 03:27:55 2014

@author: T. Wissenklaus (Francisco Lucas da Silva)

"""

#===============================================================

import os
import frontend

#===============================================================

def autenticacao(PATH_PEM):
    #arquivo com a ego existe?
    if os.path.isfile(PATH_PEM):
        #carregar chaves salvas
        conteudo = frontend.obterChaveEAmigos(PATH_PEM)
        return conteudo["chave"], conteudo["amigos"]
    #se não existir, então criar a chave
    criar, chave = frontend.desejaCriarChave(PATH_PEM)
    if criar:
        #criptografar arquivo com a chave
        conteudo = frontend.senhaParaDescriptografarChaves(PATH_PEM, chave)
        return conteudo["chave"], conteudo["amigos"]
    else:
        return {}, []

##===============================================================

#[{nome, hash, cpu, id hash em comum, servidor}]

PATH_PEM = "usuario/ego.pem"

chave, amigos = autenticacao(PATH_PEM)

if chave:
    while True:
        opcao = frontend.menuAmigos(amigos)
        if opcao[0] == "comando":
            if opcao[1] == "sair":
                break
            if opcao[1] == "add":
                adicionou, amigo = frontend.addAmigo(amigos)
                if adicionou:
                    amigoSalvo, amigos = frontend.salvarAmigo(PATH_PEM, 
                                                            chave['privada'], 
                                                            amigos,
                                                             amigo)
            if opcao[1] == "rem":
                amigoSelecionado, objAmigoSelecionado = frontend.listaEditRemoveAmigos(amigos, "remove")
                if not amigoSelecionado == "sair":
                    amigoSalvo, amigos = frontend.salvarAmigo(PATH_PEM, 
                                                            chave['privada'], 
                                                            amigos,
                                                            objAmigoSelecionado,
                                                            remover = True)
            if opcao[1] == "edit":
                amigoSelecionado, objAmigoSelecionado = frontend.listaEditRemoveAmigos(amigos, "edit")
                if not amigoSelecionado == "sair":
                    editado, amigo = frontend.editAmigo(amigos, objAmigoSelecionado)
                    if editado:
                        amigoSalvo, amigos = frontend.salvarAmigo(PATH_PEM, 
                                                        chave['privada'], 
                                                        amigos,
                                                        amigo)
            if opcao[1] == "mc":
                frontend.mc(chave["publica"])
        if opcao[0] == "amigo":
            frontend.chat(opcao[3], chave)

                    

        
    
