#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Fri Jul  11 04:11:35 2014

@author: T. Wissenklaus (Francisco Lucas da Silva)

"""

#===============================================================

import time
import backend
import PySimpleGUI as sg
from threading import Thread

#===============================================================

sg.theme("DarkBrown4")

#===============================================================

def obterChaveEAmigos(PATH_PEM):
    conteudo = {"chave":None, "amigos":[]}
    tela = [
        [sg.Text('Senha para decriptar as chaves', 
                 text_color='white',
                 font=('bold', 10), 
                 justification='center',
                 key='texto')],
        [sg.Input('',key='senha', password_char='*')],
        [sg.Button('Avançar')]
    ]
    
    window = sg.Window('Matterhorn', tela)      

    while True:
        event, values = window.read() 
        if event == sg.WIN_CLOSED:
            break
        
        window.find_element("Avançar").Update(disabled=True)
        window.find_element("Avançar").Update(button_color=('white', 'grey'))
        window.find_element("senha").Update('')
        window.find_element("texto").Update('Verificando...')
        window.find_element("texto").Update(text_color='yellow')
        window.find_element("texto").Update(font=('bold', 15))
        
        decriptou, conteudo = backend.descriptografarUsuario(PATH_PEM, values["senha"])
        
        if decriptou:
            break
        else:
            window.find_element("Avançar").Update(disabled=False)
            window.find_element("Avançar").Update(button_color=('white', 'black'))
            window.find_element("senha").Update('')
            window.find_element("texto").Update('Não foi possível decriptar a chave')
            window.find_element("texto").Update(text_color='red')
            
    window.close()
    return conteudo

#===============================================================

def desejaCriarChave(PATH_PEM):
    tela = [
        [sg.Text('Deseja criar a chave?', 
                 text_color='white',
                 font=('bold', 10), 
                 justification='center',
                 key='texto')],
        [sg.Button('Sim',button_color=('white', '#18B303')),
         sg.Button('Não',button_color=('white', '#B30803'))]
    ]
    
    window = sg.Window('Matterhorn', tela)
    
    foi = False
    chave = None
    
    while True:
        event, values = window.read() 
        if event == sg.WIN_CLOSED:
            break
        
        if event == 'Sim':
            window.find_element("Sim").Update(disabled=True)
            window.find_element("Não").Update(disabled=True)
            window.find_element("Sim").Update(button_color=('white', 'grey'))
            window.find_element("Não").Update(button_color=('white', 'grey'))
            gerou, chave = backend.gerarChavePrivada()
            if gerou:
                foi = True
                break
            break
        if event == 'Não':
            foi = False
            break
    
    window.close()
    
    return foi, chave

#===============================================================

def senhaParaDescriptografarChaves(PATH_PEM, chavePrivada):
    tela = [
        [sg.Text('Criar senha para decriptar as chaves', 
                 text_color='white',
                 font=('bold', 10), 
                 justification='center',
                 key='texto')],
        [sg.Input('',key='senha1', password_char='*')],
        [sg.Input('',key='senha2', password_char='*')],
        [sg.Button('Avançar')]
    ]
    
    window = sg.Window('Matterhorn', tela)      
    conteudo = {"chave":{}, "amigos": []}
    chaves = {}
    
    while True:
        event, values = window.read() 
        if event == sg.WIN_CLOSED:
            break
        
        window.find_element("Avançar").Update(disabled=True)
        window.find_element("Avançar").Update(button_color=('white', 'grey'))
        window.find_element("senha1").Update('')
        window.find_element("senha2").Update('')
        window.find_element("texto").Update('Criptografando chaves...')
        window.find_element("texto").Update(text_color='yellow')
        window.find_element("texto").Update(font=('bold', 10))
        
        if values['senha1'] == values['senha2']:
            chaves = backend.criptografarUsuario(PATH_PEM, chavePrivada, values["senha1"])
            break
        else:
            window.find_element("Avançar").Update(disabled=False)
            window.find_element("Avançar").Update(button_color=('white', 'black'))
            window.find_element("senha1").Update('')
            window.find_element("senha2").Update('')
            window.find_element("texto").Update('As senhas não batem, digite novamente')
            window.find_element("texto").Update(text_color='red')
            
    window.close()
    conteudo["chave"] = chaves
    return conteudo

#===============================================================

def menuAmigos(amigos):
    listaAmigos = []
    linha = 0
    if len(amigos):
        for amigo in amigos:
            if len(listaAmigos) == 0:
                listaAmigos.append([sg.Button(
                    amigo['nome'], key="amigo<>"+amigo['nome']+"<>"+amigo['id'])])
            else:
                if len(listaAmigos[linha]) == 3:
                    listaAmigos.append([])
                    linha += 1
                listaAmigos[linha].append(sg.Button(amigo['nome'], key="amigo<>"+amigo['nome']+"<>"+amigo['id']))
                
    layout = [
        [sg.Button('Minha chave pública', 
            button_color=('white', '#0080ff'), 
            size=(45, 1),
            key="comando<>mc<>x")],
        [sg.Button('Adicionar',
            button_color=('white', '#18AF05'),
            key="comando<>add<>x"), 
         sg.Button('Remover', 
            button_color=('white', '#AF2005'),
            key="comando<>rem<>x"), 
         sg.Button('Editar', 
            button_color=('white', '#FAA806'),
            key="comando<>edit<>x")],
        
        [sg.Column(listaAmigos, scrollable=True,  vertical_scroll_only=True, size=(500, 400))]
    ]
    
    window = sg.Window('Amigos', layout, default_button_element_size=(12,4), auto_size_buttons=False, size=(420, 500))
    
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        event = "comando<>sair<>x"

    acao = event.split("<>")
    
    if acao[0] == "amigo":
        acao.append(backend.amigoID2obj(acao[2], amigos))
    
    window.close()
    
    return acao

#===============================================================

def addAmigo(amigos):
    
    tela = [
        [sg.Text('Apelido', 
                 text_color='white',
                 font=('bold', 10), 
                 justification='center',
                 key='texto0')],
        [sg.Input('',key='apelido')],
        
        [sg.Text('Chave pública', 
                 text_color='white',
                 font=('bold', 10), 
                 justification='center',
                 key='texto1')],
        [sg.Input('',key='chave')],
        
        [sg.Text('Email', 
                 text_color='white',
                 font=('bold', 10), 
                 justification='center',
                 key='texto2')],
        [sg.Input('',key='email')],
        
        [sg.Text('', 
                 text_color='white',
                 font=('bold', 10),
                 justification='center',
                 key='texto3')],
        [sg.Button('Salvar')]
    ]
    
    window = sg.Window('Matterhorn', tela)
    
    ok = False
    salvou = False
    obj = {"id": "", "nome": "", "chave": 0, "email": ""}
    blackListNames = ["adicionar", "remover", "editar", "sair", "minha chave pública"]
    
    while not ok:
        event, values = window.read() 
        if event == sg.WIN_CLOSED:
            break
        
        window.find_element("Salvar").Update(disabled=True)
        window.find_element("Salvar").Update(button_color=('white', 'grey'))
        window.find_element("texto3").Update('Salvando amigo...')
        window.find_element("texto3").Update(text_color='yellow')
        window.find_element("texto3").Update(font=('bold', 10))
        
        for amigo in amigos:
            if values['apelido'] == amigo['nome']:
                window.find_element("Salvar").Update(disabled=False)
                window.find_element("Salvar").Update(button_color=('white', 'grey'))
                window.find_element("texto3").Update('Apelido duplicado.')
                window.find_element("texto3").Update(text_color='red')
                window.find_element("texto3").Update(font=('bold', 10))
                salvou = False
                break
            elif values['apelido'].lower() in blackListNames or len(values['apelido'].lower().strip()) <= 0:
                window.find_element("Salvar").Update(disabled=False)
                window.find_element("Salvar").Update(button_color=('white', 'grey'))
                window.find_element("texto3").Update('Nome inválido.')
                window.find_element("texto3").Update(text_color='red')
                window.find_element("texto3").Update(font=('bold', 10))
                salvou = False
                break
            elif values['chave'] == str(amigo['chave']):
                window.find_element("Salvar").Update(disabled=False)
                window.find_element("Salvar").Update(button_color=('white', 'grey'))
                window.find_element("texto3").Update('Chave duplicada.')
                window.find_element("texto3").Update(text_color='red')
                window.find_element("texto3").Update(font=('bold', 10))
                salvou = False
                break
            elif not values['chave'].isdigit():
                window.find_element("Salvar").Update(disabled=False)
                window.find_element("Salvar").Update(button_color=('white', 'grey'))
                window.find_element("texto3").Update('Chave deve ser numérica.')
                window.find_element("texto3").Update(text_color='red')
                window.find_element("texto3").Update(font=('bold', 10))
                salvou = False
                break
            
            else:
                salvou = True
        
        if not values['chave'].isdigit():
            window.find_element("Salvar").Update(disabled=False)
            window.find_element("Salvar").Update(button_color=('white', 'grey'))
            window.find_element("texto3").Update('Chave deve ser numérica.')
            window.find_element("texto3").Update(text_color='red')
            window.find_element("texto3").Update(font=('bold', 10))
            salvou = False
            
        elif len(amigos) == 0:
            salvou = True
            
        if salvou:
            obj["id"] = backend.gerarId()
            obj["nome"] = values['apelido']
            obj['email'] = values['email']
            obj['chave'] = int(values['chave'])
            break
        
    window.close()
    return salvou, obj

#===============================================================

def listaEditRemoveAmigos(amigos, opc):
    listaAmigos = []
    linha = 0
    objsAmigos = {"sair": None}
    corBtn = ('black', '#FAA806') if opc == "edit" else ('white', '#AF2005')
    
    if len(amigos):
        for amigo in amigos:
            if len(listaAmigos) == 0:
                listaAmigos.append([sg.Button(amigo['nome'], button_color=corBtn)])
            else:
                if len(listaAmigos[linha]) == 3:
                    listaAmigos.append([])
                    linha += 1
                listaAmigos[linha].append(sg.Button(amigo['nome'],
                                    button_color=corBtn))
            objsAmigos[amigo['nome']] = amigo
                
    layout = [
        [sg.Column(listaAmigos, scrollable=True,  vertical_scroll_only=True, size=(500, 400))]
    ]
    
    window = sg.Window('Amigos', layout, default_button_element_size=(12,4), auto_size_buttons=False, size=(420, 500))
    
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        event = "sair"
    
    window.close()
    
    return event, objsAmigos[event]

#===============================================================

def editAmigo(amigos, amigoSelecionado):
    
    tela = [
        [sg.Text('Apelido', 
                 text_color='white',
                 font=('bold', 10), 
                 justification='center',
                 key='texto0')],
        [sg.Input(amigoSelecionado["nome"],key='apelido')],
        
        [sg.Text('Chave pública', 
                 text_color='white',
                 font=('bold', 10), 
                 justification='center',
                 key='texto1')],
        [sg.Input(str(amigoSelecionado["chave"]),key='chave')],
        
        [sg.Text('Email', 
                 text_color='white',
                 font=('bold', 10), 
                 justification='center',
                 key='texto2')],
        [sg.Input(amigoSelecionado["email"],key='email')],
        
        [sg.Text('', 
                 text_color='white',
                 font=('bold', 10),
                 justification='center',
                 key='texto3')],
        [sg.Button('Salvar')]
    ]
    
    window = sg.Window('Matterhorn', tela)
    
    ok = False
    salvou = False
    obj = {"nome": "", "chave": 0, "email": ""}
    blackListNames = ["adicionar", "remover", "editar", "sair", "minha chave pública"]
    
    while not ok:
        event, values = window.read() 
        if event == sg.WIN_CLOSED:
            break
        
        window.find_element("Salvar").Update(disabled=True)
        window.find_element("Salvar").Update(button_color=('white', 'grey'))
        window.find_element("texto3").Update('Salvando amigo...')
        window.find_element("texto3").Update(text_color='yellow')
        window.find_element("texto3").Update(font=('bold', 10))
        
        for amigo in amigos:
            if values['apelido'] == amigo['nome'] and not amigoSelecionado['id'] == amigo['id']:
                window.find_element("Salvar").Update(disabled=False)
                window.find_element("Salvar").Update(button_color=('white', 'grey'))
                window.find_element("texto3").Update('Apelido duplicado.')
                window.find_element("texto3").Update(text_color='red')
                window.find_element("texto3").Update(font=('bold', 10))
                salvou = False
                break
            elif values['apelido'].lower() in blackListNames or len(values['apelido'].lower().strip()) <= 0:
                window.find_element("Salvar").Update(disabled=False)
                window.find_element("Salvar").Update(button_color=('white', 'grey'))
                window.find_element("texto3").Update('Nome inválido.')
                window.find_element("texto3").Update(text_color='red')
                window.find_element("texto3").Update(font=('bold', 10))
                salvou = False
                break
            elif values['chave'] == str(amigo['chave']) and not amigoSelecionado['id'] == amigo['id']:
                window.find_element("Salvar").Update(disabled=False)
                window.find_element("Salvar").Update(button_color=('white', 'grey'))
                window.find_element("texto3").Update('Chave duplicada.')
                window.find_element("texto3").Update(text_color='red')
                window.find_element("texto3").Update(font=('bold', 10))
                salvou = False
                break
            elif not values['chave'].isdigit():
                window.find_element("Salvar").Update(disabled=False)
                window.find_element("Salvar").Update(button_color=('white', 'grey'))
                window.find_element("texto3").Update('Chave deve ser numérica.')
                window.find_element("texto3").Update(text_color='red')
                window.find_element("texto3").Update(font=('bold', 10))
                salvou = False
                break
            
            else:
                salvou = True
        
        if not values['chave'].isdigit():
            window.find_element("Salvar").Update(disabled=False)
            window.find_element("Salvar").Update(button_color=('white', 'grey'))
            window.find_element("texto3").Update('Chave deve ser numérica.')
            window.find_element("texto3").Update(text_color='red')
            window.find_element("texto3").Update(font=('bold', 10))
            salvou = False
            
        elif len(amigos) == 0:
            salvou = True
            
        if salvou:
            obj["id"] = amigoSelecionado['id']
            obj["nome"] = values['apelido']
            obj['email'] = values['email']
            obj['chave'] = int(values['chave'])
            break
        
    window.close()
    return salvou, obj

#===============================================================

def salvarAmigo(PATH_PEM, chave, amigos, amigo, remover=False):
    
    tela = [
        [sg.Text('Senha', 
                 text_color='white',
                 font=('bold', 10), 
                 justification='center',
                 key='texto')],
        [sg.Input('',key='senha', password_char='*')],
        [sg.Button('Avançar')]
    ]
    
    window = sg.Window('Matterhorn', tela)      

    while True:
        event, values = window.read() 
        if event == sg.WIN_CLOSED:
            salvo = False
            break
        
        window.find_element("Avançar").Update(disabled=True)
        window.find_element("Avançar").Update(button_color=('white', 'grey'))
        window.find_element("senha").Update('')
        window.find_element("texto").Update('Salvando...')
        window.find_element("texto").Update(text_color='yellow')
        window.find_element("texto").Update(font=('bold', 15))
        
        decriptou, conteudo = backend.descriptografarUsuario(PATH_PEM, values["senha"])
        
        if decriptou:
            novaListaAmigos = []
            for amigoListaOld in amigos:
                if not amigoListaOld["id"] == amigo["id"]:
                    novaListaAmigos.append(amigoListaOld)
            if not remover:
                novaListaAmigos.append(amigo)
            backend.criptografarUsuario(PATH_PEM, chave, values["senha"], novaListaAmigos)
            salvo = True
            break
        else:
            window.find_element("Avançar").Update(disabled=False)
            window.find_element("Avançar").Update(button_color=('white', 'black'))
            window.find_element("senha").Update('')
            window.find_element("texto").Update('Não foi possível salvar o amigo.')
            window.find_element("texto").Update(text_color='red')
            
    window.close()
    return salvo, novaListaAmigos

#===============================================================

def chat(amigo, minhaChave):
    ativo = True
    chaveHashAmigo = backend.gerarHash(amigo["chave"])
    
    lm = backend.listaDeEmails(chaveHashAmigo)
    lm = backend.msgsTraduzidas(lm, minhaChave["privada"], amigo["chave"])

    msgIDs = []
    for l in lm:
        msgIDs.append(l["ts"])

    layout = [
        [
            sg.Text(
                'Chat com ' + amigo["nome"], 
                size=(40, 1)
            )
        ],
        [
            sg.Output(
                size=(110, 20), 
                font=('Helvetica 10')
            )
        ],
        [
            sg.Multiline(
                size=(70, 5), 
                enter_submits=False, 
                key='-QUERY-', 
                do_not_clear=True,
                enable_events=True
            ),
            
            sg.Button(
                'SEND', 
                button_color=(
                    sg.YELLOWS[0],
                    sg.BLUES[0]
                ), 
                bind_return_key=True
            ),
            sg.Button(
                'EXIT', 
                button_color=(sg.YELLOWS[0], 
                sg.GREENS[0])
            )
        ],
        [
            sg.Input(key='-sourcefile-', size=(45, 1)),
            sg.FileBrowse("Arquivos",button_color=('white', '#0080ff'),file_types=(("Qualquer", "*"), ),key='-aaaaa-'),
            sg.Button('Enviar',key="env-arquivo",button_color=('white', '#18AF05'))
        ],]
    window = sg.Window('Chat window', layout, font=('Helvetica', ' 13'), default_button_element_size=(8,2), use_default_focus=False)

    def aaa():
        time.sleep(3)
        lm.reverse()
        for m in lm:
            print("<"+amigo["nome"]+">", m["msg"],flush=True)
            print("_"*50,flush=True)

    def recebendoMSGs():
        time.sleep(5)
        while ativo:
            time.sleep(1)
            rmsg = backend.listaDeEmails(chaveHashAmigo)
            rmsg = backend.msgsTraduzidas(rmsg, minhaChave["privada"], amigo["chave"])
            rmsg.reverse()
            for rms in rmsg:
                if not rms["ts"] in msgIDs:
                    msgIDs.append(rms["ts"])
                    print("<"+amigo["nome"]+">",rms["msg"],flush=True)
                    print("_"*50,flush=True)

    t = Thread(target=aaa)
    t.start()

    t2 = Thread(target=recebendoMSGs)
    t2.start()

    while True:     # The Event Loop
        event, value = window.read()
        if event in (sg.WIN_CLOSED, 'EXIT'):
            ativo = False
            break
        if len(value['-QUERY-']) > 245:
            window.Element('-QUERY-').Update(value['-QUERY-'][:-1])
        if event == 'SEND':
            query = value['-QUERY-'].rstrip()
            window.find_element("-QUERY-").Update('')
            retorno = backend.enviarEmail(amigo["email"], minhaChave["hash"], query,  minhaChave["privada"], minhaChave["publica"], amigo["chave"])
            print("<Eu>", query, flush=True)
            print("_"*50,flush=True)

    window.close()

#===============================================================

def recebidos(lemailsrecebidos = []):
    espacos = "_"*50
    listaAmigos = [[sg.Text(espacos, text_color="white")]]
    
    if len(lemailsrecebidos):
        for amigo in lemailsrecebidos:
            listaAmigos.append(
                [sg.Text(amigo["msg"]+"\n"+espacos, text_color="white")]
            )
    layout = [
        [sg.Button('Responder', button_color=('white', '#18AF05')),],
        [sg.Column(listaAmigos, scrollable=True,  vertical_scroll_only=True, size=(500, 400))]
    ]
    
    window = sg.Window('Amigos', layout, default_button_element_size=(12,4), auto_size_buttons=False, size=(420, 500))
    
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        event = "sair"
    
    window.close()
    
    return event

#===============================================================

def mc(chaveP):

    layout = [  
            [sg.InputText(str(chaveP), 
            use_readonly_for_disable=True, 
            disabled=True, 
            key='-IN-')]]
            
    window = sg.Window('Window Title', layout, finalize=True)
    window['-IN-'].Widget.config(readonlybackground=sg.theme_background_color())
    window['-IN-'].Widget.config(borderwidth=0) 

    while True:
        event, values = window.read() 
        if event == sg.WIN_CLOSED:
            break
        
       
    window.close()
