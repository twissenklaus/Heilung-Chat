#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Fri Jul  11 04:30:19 2014

@author: T. Wissenklaus (Francisco Lucas da Silva)

"""

#===============================================================

import json
import utils
import base64
import criptografia as cr
from Google import Create_Service
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from math import ceil
import mimetypes
import os
from email.mime.base import MIMEBase
from email import encoders

#===============================================================

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

#===============================================================

def gerarChavePrivada():
    try:
        chavePrivada = cr.gerarChaveRSA()
        return True, chavePrivada
    except:
        return False, ""

#===============================================================

def descriptografarUsuario(path, senha):
    try:
        conteudo = utils.lerArquivo(path)
        conteudo = utils.descompactarString(conteudo)
        conteudo = cr.decriptarAES(conteudo, senha)      
        conteudo = json.loads(conteudo)
        amigos = conteudo['amigos']
        
        chave = cr.carregarChaveRSA(conteudo['chave'])
   
        chave = {"publica": chave.n, 
                 "privada": chave, 
                 "hash": cr.resumoHash(chave.n)
                 }
        return True, {"chave":chave, "amigos":amigos}
    except:
        return False, {"chave":None, "amigos":[]}

##===============================================================

def criptografarUsuario(PATH_PEM, chavePrivada, senha, amigos = []):
    
    conteudo = json.dumps({"chave": chavePrivada.save_pkcs1().decode(),
                           "amigos": amigos})
    conteudo = cr.encriptarAES(conteudo, senha).decode()
    conteudo = utils.compactarString(conteudo)
    
    with open(PATH_PEM, mode='wb') as privatefile:
        privatefile.write(conteudo)

    objFinal = {
        "publica": chavePrivada.n, 
        "privada": chavePrivada, 
        "hash": cr.resumoHash(chavePrivada.n)
    }

    return objFinal

#===============================================================

def gerarId():
    stringsAleatorias = utils.gerarStringsAleatorias()
    return cr.resumoHash(stringsAleatorias)

#===============================================================

def parse_msg(msg):
    if msg.get("payload").get("body").get("data"):
        return base64.urlsafe_b64decode(msg.get("payload").get("body").get("data").encode("ASCII")).decode("utf-8")
    return msg.get("snippet") 

#===============================================================

def listaDeEmails(hashChaveAmigo):
    CLIENT_SECRET_FILE = 'credentials.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    conteudo = ""
    assunto = ""
    listaMSG = []

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    result = service.users().messages().list(userId='me').execute()
    messages = result.get('messages')

    for m in messages:
        responseMSG = service.users().messages().get(userId="me", id=m['id'], format="full").execute()
        if "INBOX" in responseMSG["labelIds"]:
            conteudo = parse_msg(responseMSG)

            for rm in responseMSG["payload"]["headers"]:
                if rm['name'] == "Subject":
                    assunto = rm["value"]
            
            if assunto == hashChaveAmigo:
                conteudoFinal = ""
                conteudo = conteudo.replace("\n", " ")
                conteudoAscii2list = conteudo.split(" ")
                
                for c in conteudoAscii2list:
                    if c == "" or c == " ":
                        pass
                    else:
                        conteudoFinal += chr(int(c))
                objMSGEmail = {
                    "de_hash":assunto,
                    "conteudo":conteudoFinal,
                    "timestamp": responseMSG["internalDate"]
                }
                listaMSG.append(objMSGEmail)
                service.users().messages().delete(userId="me", id=m['id']).execute()
    return listaMSG

#===============================================================

def filtrarPeloAmigo(emailsAmigoChave, objEmail):
    listaMGSThread = []
    temAmigoNaThread = False

    for oe in objEmail:
        try:
            conteudo = oe["conteudo"].split("} ")[0] + "}" 
            conteudo = conteudo.replace("&#39;", '"')
            conteudo = conteudo.strip()
            if conteudo[-3:] == r'"}}':
                conteudo = conteudo[0:len(conteudo)-1]
            conteudo = json.loads(conteudo)
            if conteudo["de"] == emailsAmigoChave:
                listaMGSThread.append(conteudo)
                temAmigoNaThread = True
        except:
            pass
    return temAmigoNaThread, listaMGSThread

#===============================================================

def enviarEmail(emailReceptor, subject, conteudoEmail, chvM, chvMP, chvA):
    de = str(chvMP)
    para = str(chvA)
    msg = cr.criptografarRSA(conteudoEmail, chvA)
    assinatura = cr.assinarRSA(conteudoEmail, chvM).decode()
    
    conteudoEmail = "{"
    conteudoEmail += "'de':"+de+","
    conteudoEmail += "'para':"+para+","
    conteudoEmail += "'msg':"+"'"+msg+"',"
    conteudoEmail += "'assinatura':"+"'"+assinatura+"'"
    conteudoEmail += "}"

    corpoEmail = ""

    for c in conteudoEmail:
        corpoEmail += str(ord(c))+" "
        
    corpoEmail = corpoEmail.strip()

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = emailReceptor
    mimeMessage['subject'] = subject
    emailMsg = corpoEmail
    mimeMessage.attach(MIMEText(emailMsg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
    retorno = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
    return retorno

#===============================================================

def amigoID2obj(idAmigo, amigos):
    objAmigo = {}
    for a in amigos:
        if a["id"] == idAmigo:
            objAmigo = a
            break
    return objAmigo

#===============================================================

def gerarHash(txt):
    return cr.resumoHash(txt)

#===============================================================

def msgsTraduzidas(listEmails, chvM, chvA):
    
    novaListaEmail = []
    for le in listEmails:
        try:
            conteudo = le["conteudo"]
            conteudo = json.loads(conteudo.replace("'", '"'))           
            msgD = cr.decriptografarRSA(conteudo["msg"], chvM)
            if cr.verificarRSA(msgD, conteudo["assinatura"].encode(), chvA):
                novaListaEmail.append({"msg":msgD, "ts": le["timestamp"]})
        except:
            pass
    return novaListaEmail

#===============================================================
